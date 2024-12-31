from app.features.athlete.utils import (
    convert_birht_number_to_date,
    validate_birth_number,
)


def test_validate_birth_number():
    assert validate_birth_number("0409090033") == True
    assert validate_birth_number("0409090034") == False


def test_convert_birht_number_to_date():
    assert convert_birht_number_to_date("0409090033") == "2004-09-09"
    assert convert_birht_number_to_date("6459290034") == "1964-09-29"
