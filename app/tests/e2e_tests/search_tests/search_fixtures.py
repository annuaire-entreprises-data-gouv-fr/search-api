"""
Entités de références utilisées par les tests e2e de recherche.
Les regrouper ici évite de disséminer les SIREN dans les tests.
"""

# Dénomination exacte + très grand nombre d'établissements ouverts
LA_POSTE = "356000000"
LA_POSTE_SABLE_SIRET = "35600000024221"
LA_POSTE_SABLE_ADRESSE = "1 AVENUE JOEL LE THEULE 72300 SABLE-SUR-SARTHE"
LA_POSTE_SABLE_CODE_POSTAL = "72300"
# Ancien SIREN de la poste
# A aussi un établissement (fermé) à Sable-sur-Sarthe
LA_POSTE_ANCIEN_SIREN = "356000521"

# Sigle EDF distinct de la raison sociale ELECTRICITE DE FRANCE
# Volume d'établissements très important
EDF = "552081317"
# Homonyme dont le nom complet est aussi ELECTRICITE DE FRANCE
# mais qui ne possède qu'une poignée d'établissements
EDF_HOMONYME = "776222275"

# Sigle CNRS utilisé par plusieurs SIREN
CNRS = "180089013"

# Enseigne « PFG - SERVICES FUNERAIRES » portée par des établissements dont la
# dénomination de l'unité légale est tout autre.
OGF_SERVICES_FUNERAIRES = "828160069"
OGF_ENSEIGNE = "pfg services funeraires"
OGF_ADRESSE_DROUOT = "rue drouot"

# Nom commercial distinct de la dénomination.
GANYMEDE_NOM_COMMERCIAL = "981195464"
NOM_COMMERCIAL_FRIANDISES = "une poignee de friandises"

# Association dotée d'un numéro RNA.
SECOURS_POPULAIRE_RNA = "312160534"
RNA_SECOURS_POPULAIRE = "W751004625"

# Personne physique : le nom complet est « PRENOM NOM ».
PERSONNE_PHYSIQUE_ALLIETTA = "529842163"
PERSONNE_PHYSIQUE_ALLIETTA_NOM_COMPLET = "JEAN-LOUIS ALLIETTA"
# Unité légale dont la dénomination est exactement « ALLIETTA ».
DENOMINATION_ALLIETTA = "479104838"

# Deux unités légales partageant le même dirigeant
ARCTURUS = "104049424"
GANYMEDE = "880878145"
DIRIGEANT_NOM = "jouppe"
DIRIGEANT_PRENOM_EXACT = "xavier"
DIRIGEANT_PRENOMS_PARTIELS = "xavier erwan"
DIRIGEANT_ANNEE_NAISSANCE = "1990"

# Collectivité territoriale et une de ses élues.
COMMUNE_DE_LAMBESC = "211300504"
ELU_NOM = "allietta"

# Homonymes « GANYMEDE » distingués uniquement par leur commune.
GANYMEDE_LAMBESC = "940221229"
GANYMEDE_NARBONNE = "423208180"

# Unité légale non diffusible, personne physique : accessible par siren
# uniquement, jamais par la recherche textuelle.
NON_DIFFUSIBLE_PERSONNE_PHYSIQUE = "929693232"
MASQUE_NON_DIFFUSIBLE = "[NON-DIFFUSIBLE]"

# Requête qui ne doit rien renvoyer.
TERMES_INEXISTANTS = "azertyuiop zzzzqqqxxxyyy"

# Point de recherche géographique : Langeac (Haute-Loire). Assez dense pour
# remonter des réseaux nationaux (LA POSTE, EDF) sans dépasser 10 000 résultats.
POINT_LANGEAC_LAT = "45.123"
POINT_LANGEAC_LON = "3.456"
