import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from docscout.engine import DocumentIndex, extract_text

st.set_page_config(page_title='DocScout AI', page_icon='📚', layout='wide')
st.title('📚 DocScout AI — Local Document Q&A')
st.caption('TF-IDF-powered retrieval with extractive answers. No paid APIs or cloud upload required.')
files = st.file_uploader('Upload documents (TXT, MD, PDF, DOCX)', type=['txt','md','pdf','docx'], accept_multiple_files=True)
query = st.text_input('Ask a question about the documents', placeholder='What are the deployment steps?')
top_k = st.slider('Source passages', 1, 10, 3)
if files:
    documents = []
    for f in files:
        try:
            text = extract_text(f.name, f.getvalue())
            if text.strip():
                documents.append((f.name, text))
            else:
                st.warning(f'{f.name}: no selectable text found. Scanned PDFs require OCR.')
        except Exception as exc:
            st.error(f'{f.name}: {exc}')
    index = DocumentIndex()
    count = index.build(documents)
    st.success(f'Indexed {count} passages across {len(documents)} documents') if count else st.warning('No searchable text was found.')
    if query and count:
        result = index.answer(query, top_k)
        st.subheader('Extractive answer')
        st.write(result['answer'])
        st.subheader('Supporting passages')
        for hit in result['sources']:
            with st.expander(f"{hit['source']} · passage {hit['chunk']} · similarity {hit['score']:.3f}"):
                st.write(hit['text'])
else:
    st.info('Upload one or more documents to start. You can try samples/ files in the repository.')
st.caption('Educational retrieval tool: TF-IDF lexical similarity is not semantic understanding. Verify the original source before relying on an answer.')
