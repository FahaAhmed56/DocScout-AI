# DocScout AI 📚

A privacy-minded, local **document search and extractive question-answering app** built using **Python, TF-IDF, Scikit-learn, and Streamlit**. Upload TXT, MD, DOCX, or text-based PDF files, ask questions, and inspect the supporting document passages.

> Not an LLM: this app retrieves overlapping words and extracts candidate sentences from the best-matching passage. It may return irrelevant text; verify original sources. No OCR support for scanned PDFs.

## Features
- Multi-file upload and local processing
- TF-IDF unigram/bigram indexing and cosine-similarity ranking
- Short extractive answer with document references and similarity scores
- Sample policy documents and command-line interface
- Automated pytest suite and GitHub Actions
- No credentials or external inference API needed

## Windows / VS Code setup
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app/dashboard.py
```
Open http://localhost:8501 and upload files from `samples/`.

## Command line
```powershell
.venv\Scripts\python.exe -m docscout.cli "What should we do before deployment?" samples/deployment_guide.md
```

## Test
```powershell
.venv\Scripts\python.exe -m pytest -q
```

## How it works
1. Extracts text from files using native parsers (no OCR).
2. Splits text into 130-word passages with 25-word overlap.
3. Builds a TF-IDF matrix (unigrams and bigrams).
4. Ranks passages by cosine similarity to the query.
5. Selects up to two sentences with greatest query-word overlap as an **extractive** answer and shows supporting passages.

**Limitations:** Keyword similarity may miss paraphrases; no true semantic reasoning or grounded generative answering. Documents stay within the Streamlit process on your machine, but normal application behavior depends on your hosting setup. Avoid uploading sensitive documents to public deployments.

## GitHub repository details
- **Name:** `DocScout-AI`
- **Description:** Local AI-inspired document search and extractive Q&A with Python, TF-IDF, Scikit-learn, Streamlit, and source references.
- **Topics:** `python`, `nlp`, `document-search`, `information-retrieval`, `streamlit`, `scikit-learn`

## Structure
```text
docscout-ai/
├── app/dashboard.py
├── docscout/{__init__.py,engine.py,cli.py}
├── samples/{deployment_guide.md,security_policy.txt}
├── tests/test_engine.py
├── .github/workflows/tests.yml
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## License
MIT.
