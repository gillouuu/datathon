# Modèle de lettre de motivation
TEMPLATE_LETTER = """
Madame, Monsieur,

Je me permets de vous adresser ma candidature pour intégrer la formation {formation}, qui correspond parfaitement à mon projet professionnel.

Titulaire d'un diplome de niveau {diplome}, je souhaite approfondir mes compétences en {formation} afin de m'orienter vers le métier de {metier}.

Rigoureux(se) et motivé(e), je suis prêt(e) à m'investir pleinement dans cette formation pour acquérir les compétences nécessaires.

Dans l’attente de votre retour, je vous prie d’agréer, Madame, Monsieur, mes salutations distinguées.

Signature
"""

def generate_motivation_letter(metier, formation, diplome):
    return TEMPLATE_LETTER.format(metier=metier, formation=formation, diplome=diplome)