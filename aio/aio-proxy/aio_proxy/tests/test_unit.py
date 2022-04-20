from typing import Tuple, Any

import requests
import pytest
import parameters
import index


@pytest.mark.parametrize("code_postal, expected", [("45 000", "45000"), (None, None)])
def test_parse_and_validate_code_postal(code_postal, expected):
    assert parameters.parse_and_validate_code_postal(code_postal) == expected


@pytest.mark.parametrize("activite_principale, expected", [("45 000", "45000"), (None, None)])
def test_parse_and_validate_activite_principale(activite_principale, expected):
    assert parameters.parse_and_validate_activite_principale(activite_principale) == expected

