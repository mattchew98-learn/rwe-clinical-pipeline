from pipeline.utils import clean_gender, is_active_medication


def test_clean_gender_normalizes():
    assert clean_gender("m") == "M"
    assert clean_gender(" F ") == "F"


def test_clean_gender_rejects_unknown():
    assert clean_gender("X") is None
    assert clean_gender("") is None
    assert clean_gender(None) is None


def test_is_active_medication():
    assert is_active_medication(None) is True
    assert is_active_medication("") is True
    assert is_active_medication("2024-01-01") is False
