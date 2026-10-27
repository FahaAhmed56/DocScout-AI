import argparse
from pathlib import Path
from .engine import DocumentIndex, extract_text

def main():
    parser = argparse.ArgumentParser(description='Search local documents with TF-IDF')
    parser.add_argument('question')
    parser.add_argument('files', nargs='+', help='TXT, MD, PDF, or DOCX files')
    args = parser.parse_args()
    docs = [(Path(f).name, extract_text(f, Path(f).read_bytes())) for f in args.files]
    index = DocumentIndex()
    index.build(docs)
    result = index.answer(args.question)
    print('Answer:', result['answer'])
    for hit in result['sources']:
        print(f"[{hit['source']} chunk {hit['chunk']}, score {hit['score']}]")

if __name__ == '__main__':
    main()
