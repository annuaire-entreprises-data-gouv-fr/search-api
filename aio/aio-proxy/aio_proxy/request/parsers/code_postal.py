import re


def validate_code_postal(list_code_postal_clean: list[str]):
    """Check the validity of code_postal.

    Args:
        list_code_postal_clean(list(str), optional): list of codes postaux extracted
        and cleaned.

    Returns:
        None if list_code_postal_clean is None.
        list_code_postal_clean if valid.

    Raises:
        ValueError: if one the values in list_code_postal_clean is not valid.
    """
    if list_code_postal_clean is None:
        return None
    length_cod_postal = 5
    for code_postal in list_code_postal_clean:
        if len(code_postal) != length_cod_postal:
            raise ValueError("Chaque code postal doit contenir 5 caractères !")
        codes_valides = "^((0[1-9])|([1-8][0-9])|(9[0-8])|(2A)|(2B))[0-9]{3}$"
        if not re.search(codes_valides, code_postal):
            raise ValueError("Au moins un code postal est non valide.")
    return list_code_postal_clean
