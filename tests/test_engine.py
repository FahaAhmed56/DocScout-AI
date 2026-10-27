import pytest
from docscout.engine import DocumentIndex, chunk_text, extract_text

def test_chunk_empty(): assert chunk_text('') == []
def test_chunk_overlap(): assert chunk_text('a b c d e', 3, 1) == ['a b c', 'c d e']
def test_chunk_invalid():
    with pytest.raises(ValueError): chunk_text('words', 2, 2)
def test_text_extract(): assert extract_text('a.txt', b'hello') == 'hello'
def test_unsupported():
    with pytest.raises(ValueError): extract_text('a.exe', b'abc')
def test_search_relevant():
    d = DocumentIndex(); d.build([('a', 'MongoDB stores documents.'), ('b', 'React builds user interfaces.')])
    assert d.search('React interfaces')[0]['source'] == 'b'
def test_no_result():
    d = DocumentIndex(); d.build([('a', 'MongoDB stores documents.')])
    assert d.answer('volcanoes')['sources'] == []
def test_empty_index():
    d = DocumentIndex(); assert d.build([('a', '')]) == 0
    assert d.search('anything') == []
def test_return_source():
    d = DocumentIndex(); d.build([('handbook', 'Deployment requires testing before release.')])
    assert d.answer('deployment testing')['sources'][0]['source'] == 'handbook'
def test_top_k():
    d = DocumentIndex(); d.build([('a', 'Python code testing.'), ('b', 'Python testing framework.')])
    assert len(d.search('Python testing', 1)) == 1
