def format_insee_bool(value):
    if value is None or value == "N":
        return False
    else:
        return True
