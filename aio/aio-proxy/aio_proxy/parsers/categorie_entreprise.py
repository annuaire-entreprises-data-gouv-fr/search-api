def validate_categorie_entreprise(list_categorie_entreprise_clean: list[str]):
    """Check the validity of list_categorie_entreprise.

    Args:
        list_categorie_entreprise_clean(list(str), optional): categorie_entreprise
        extracted and cleaned.

    Returns:
        None if categorie_entreprise_clean is None.
        list_categorie_entreprise_clean if valid.

    Raises:
        ValueError: if one of the values in list_categorie_entreprise_clean is not valid
    """
    if list_categorie_entreprise_clean is None:
        return None
    for categorie_entreprise in list_categorie_entreprise_clean:
        if categorie_entreprise not in ["GE", "PME", "ETI"]:
            raise ValueError(
                "Chaque catégorie d'entreprise doit prendre une de ces "
                "valeurs 'GE', 'PME' ou 'ETI'."
            )
    return list_categorie_entreprise_clean
