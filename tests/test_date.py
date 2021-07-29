from vi_nlp_core.extractor import Extractor

def test_date():
    extractor = Extractor()

    text = "tôi sinh vào ngày 21-3-1997"
    result = extractor.extract_date(text,return_value=True)    
    assert result = 