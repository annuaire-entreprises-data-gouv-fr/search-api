from app.models.unite_legale import Admin


def format_admin(result_unite_legale):
    def get_field(field, default=None):
        return result_unite_legale.get(field, default)

    slug = get_field("slug")
    a_acces_espace_agent = get_field("a_acces_espace_agent")

    return Admin(slug=slug, a_acces_espace_agent=a_acces_espace_agent)
