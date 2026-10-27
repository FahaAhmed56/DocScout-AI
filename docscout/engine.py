import re
from dataclasses import dataclass
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Passage:
    source: str
    chunk: int
    text: str


def chunk_text(text: str, max_words: int = 130, overlap: int = 25) -> list[str]:
    if max_words <= 0 or overlap < 0 or overlap >= max_words:
        raise ValueError('max_words must be positive and overlap must be smaller')
    words = re.sub(r'\s+', ' ', text).strip().split()
    if not words:
        return []
    chunks = []
    for start in range(0, len(words), max_words - overlap):
        part = words[start:start + max_words]
        if not part:
            break
        chunks.append(' '.join(part))
        if start + max_words >= len(words):
            break
    return chunks


def extract_text(filename: str, content: bytes) -> str:
    from io import BytesIO
    suffix = Path(filename).suffix.lower()
    if suffix == '.txt' or suffix == '.md':
        return content.decode('utf-8-sig', errors='replace')
    if suffix == '.pdf':
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(content))
        return '\n'.join(page.extract_text() or '' for page in reader.pages)
    if suffix == '.docx':
        from docx import Document
        return '\n'.join(p.text for p in Document(BytesIO(content)).paragraphs)
    raise ValueError('Only TXT, MD, PDF and DOCX files are supported')

class DocumentIndex:
    def __init__(self):
        self.passages: list[Passage] = []
        self.vectorizer = None
        self.matrix = None

    def build(self, documents: list[tuple[str, str]]) -> int:
        self.passages = [Passage(name, i + 1, chunk) for name, text in documents
                         for i, chunk in enumerate(chunk_text(text))]
        if not self.passages:
            self.vectorizer = None
            self.matrix = None
            return 0
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), sublinear_tf=True)
        try:
            self.matrix = self.vectorizer.fit_transform([p.text for p in self.passages])
        except ValueError:
            self.vectorizer = None
            self.matrix = None
        return len(self.passages)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if not query.strip() or self.matrix is None or top_k < 1:
            return []
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix)[0]
        order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
        return [{'source': self.passages[i].source, 'chunk': self.passages[i].chunk,
                 'score': round(float(scores[i]), 4), 'text': self.passages[i].text}
                for i in order[:top_k] if scores[i] > 0]

    def answer(self, query: str, top_k: int = 3) -> dict:
        matches = self.search(query, top_k)
        if not matches:
            return {'answer': 'No relevant passage found in the uploaded documents.', 'sources': []}
        best = matches[0]
        # Extractive, not generative: never invent an answer outside of the document.
        sentences = re.split(r'(?<=[.!?])\s+', best['text'])
        query_terms = set(re.findall(r'\w+', query.lower()))
        ranked = sorted(enumerate(sentences), key=lambda item: (-len(query_terms & set(re.findall(r'\w+', item[1].lower()))), item[0]))
        answer = ' '.join(sentence for _, sentence in ranked[:2]).strip()
        return {'answer': answer or best['text'], 'sources': matches}
