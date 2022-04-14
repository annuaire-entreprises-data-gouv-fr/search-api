import os

from elasticsearch_dsl import (
    Date,
    Document,
    Float,
    Integer,
    Keyword,
    Text,
    analyzer,
    token_filter,
    tokenizer,
)

# Define filters
french_elision = token_filter(
    "french_elision",
    type="elision",
    articles_case=True,
    articles=[
        "l",
        "m",
        "t",
        "qu",
        "n",
        "s",
        "j",
        "d",
        "c",
        "jusqu",
        "quoiqu",
        "lorsqu",
        "puisqu",
    ],
)
french_stop = token_filter("french_stop", type="stop", stopwords="_french_")
french_stemmer = token_filter("french_stemmer", type="stemmer", language="light_french")
# ignore_case option deprecated, use lowercase filter before synonym filter
french_synonym = token_filter(
    "french_synonym", type="synonym", expand=True, synonyms=[]
)

# Define analyzer
annuaire_analyzer = analyzer(
    "annuaire_analyzer",
    tokenizer=tokenizer("icu_tokenizer"),
    filter=[
        "lowercase",
        french_elision,
        french_stop,
        "icu_folding",
        french_synonym,
        "asciifolding",
        french_stemmer,
    ],
)


class Siren(Document):
    """
    Class used to represent a company headquarters,
    one siren number and the corresponding sheadquarters siret number
    """

    activite_principale = Keyword()  # Add index_prefixes option
    activite_principale_entreprise = Keyword()
    activite_principale_registre_metier = Keyword()
    categorie_entreprise = Text()
    code_postal = Keyword()
    commune = Keyword()
    concat_enseigne_adresse = Text(analyzer=annuaire_analyzer)
    concat_nom_adr_siren = Text(
        analyzer=annuaire_analyzer, fields={"keyword": Keyword()}
    )
    date_creation = Date()
    date_creation_entreprise = Date()
    date_debut_activite = Date()
    date_mise_a_jour = Date()
    economie_sociale_solidaire_unite_legale = Keyword()
    enseigne = Text()
    etat_administratif_unite_legale = Keyword()
    etat_administratif_etablissement = Keyword()
    geo_adresse = Text(analyzer=annuaire_analyzer)
    identifiant_association_unite_legale = Keyword()
    indice_repetition = Text()
    is_siege = Text()
    latitude = Text()
    libelle_commune = Text()
    libelle_voie = Text()
    liste_adresse = Text(analyzer=annuaire_analyzer)
    liste_enseigne = Text(analyzer=annuaire_analyzer)
    longitude = Text()
    nature_juridique_entreprise = Integer()
    nom = Text()
    nom_complet = Text(analyzer=annuaire_analyzer, fields={"keyword": Keyword()})
    nom_raison_sociale = Text()
    nombre_etablissements = Float()  # NaN can't be stored in an integer array
    nombre_etablissements_ouvert = Float()
    numero_voie = Text()
    prenom = Keyword()
    sigle = Keyword()
    siren = Keyword(required=True)
    siret = Keyword(required=True)
    type_voie = Text()
    tranche_effectif_salarie = Keyword()
    tranche_effectif_salarie_entreprise = Keyword()

    class Index:
        name = "siren-{}".format(os.getenv("CURRENT_COLOR")
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
