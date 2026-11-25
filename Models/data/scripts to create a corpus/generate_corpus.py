#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Lire le fichier existant
with open('dictionnaire.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraire les mots existants avec leurs définitions et exemples
pattern = r'=== (\w+[\s\w\-]*) ===\s*Définition: (.+?)\s*\n\nExemples:\s*\n- (.+?)\s*\n- (.+?)\s*\n- (.+?)(?=\s*\n\n===|\s*\n\n$)'
matches = re.findall(pattern, content, re.DOTALL)

print(f"Trouvé {len(matches)} mots dans le fichier existant")

# Liste de nouveaux mots français (environ 100 pour commencer)
nouveaux_mots = [
    "ABEILLE", "ABRICOT", "ABSENT", "ABSOLUMENT", "ABUS",
    "ACADÉMIE", "ACCEPTER", "ACCESSOIRE", "ACCIDENTEL", "ACCUEIL",
    "ACCUEILLIR", "ACHAT", "ACHETER", "ACIDE", "ACIER",
    "ACOMPTE", "ACQUÉRIR", "ACROBATE", "ACTE", "ACTIF",
    "ACTUEL", "ACTUELLEMENT", "ADAPTATION", "ADAPTER", "ADDICTION",
    "ADDITION", "ADJECTIF", "ADMETTRE", "ADMINISTRATION", "ADMINISTRER",
    "ADMIRATION", "ADMIRER", "ADOLESCENCE", "ADOLESCENT", "ADOPTER",
    "ADORABLE", "ADORER", "ADRESSE", "ADROIT", "ADULTE",
    "ADVERSAIRE", "ADVERSE", "AÉRATION", "AÉRIEN", "AÉRODROME",
    "AÉRONAUTIQUE", "AFFAIBLIR", "AFFECTION", "AFFECTUEUX", "AFFICHE",
    "AFFICHER", "AFFIRMATION", "AFFIRMER", "AFFRETER", "AFFREUX",
    "AFFRONTER", "AFRICAIN", "AFRIQUE", "AGACER", "AGENCE",
    "AGENT", "AGGLOMÉRATION", "AGGRAVER", "AGICHAGE", "AGILE",
    "AGIR", "AGITATION", "AGITER", "AGNEAU", "AGRANDIR",
    "AGRÉABLE", "AGRÉER", "AGRÉMENT", "AGRICOLE", "AGRICULTEUR",
    "AGRICULTURE", "AGRIPPER", "AGUERRI", "AIDE", "AIDER",
    "AIEUL", "AIGRE", "AIGREUR", "AIGU", "AIGUILLE",
    "AIGUILLER", "AIL", "AILE", "AILER", "AILIER",
    "AIMABLE", "AIMANT", "AIMER", "AINÉ", "AIR",
    "AISE", "AISÉ", "AISÉMENT", "AJOUT", "AJOUTER",
    "AJUSTEMENT", "AJUSTER", "ALARME", "ALARMER", "ALBUM",
]

# Dictionnaire pour les définitions basées sur le suffixe
suffixes_definitions = {
    'ER': 'Action de {root} ou fait de {root}.',
    'IR': 'Action de {root} ou fait de {root}.',
    'RE': 'Action de {root} ou fait de {root}.',
    'AGE': 'Action ou résultat de {root}.',
    'MENT': 'De manière {root}.',
    'EUR': 'Personne qui {root}.',
    'EUSE': 'Personne qui {root}.',
    'ABLE': 'Qui peut être {root}.',
    'IBLE': 'Qui peut être {root}.',
    'IF': 'Qui a la qualité de {root}.',
    'IVE': 'Qui a la qualité de {root}.',
    'E': 'Résultat de l\'action de {root} ou qualité de {root}.',
    'TÉ': 'Qui a subi l\'action de {root}.',
    'ION': 'Action ou résultat de {root}.',
    'ISME': 'Doctrine ou système basé sur {root}.',
    'ISTE': 'Partisan de {root} ou spécialiste de {root}.',
    'ITÉ': 'Qualité de {root}.',
    'AIS': 'Qui a la qualité de {root}.',
    'ANT': 'Qui {root}.',
    'ENT': 'Qui {root}.',
}

# Fonction pour générer une définition
def generer_definition(mot):
    mot_upper = mot.upper()
    
    # Vérifier si le mot existe déjà dans les mots existants
    for m in matches:
        if m[0].upper() == mot_upper:
            return m[1]
    
    # Définitions spécifiques pour certains mots
    definitions_specificques = {
        'ABEILLE': 'Insecte hyménoptère social produisant du miel et de la cire.',
        'ABRICOT': 'Fruit charnu de couleur orange, à noyau, produit par l\'abricotier.',
        'ABSENT': 'Qui n\'est pas présent, qui manque.',
        'ABSOLUMENT': 'De manière absolue, sans restriction.',
        'ABUS': 'Usage excessif ou mauvais usage de quelque chose.',
        'ACADÉMIE': 'Institution savante ou établissement d\'enseignement supérieur.',
        'ACCEPTER': 'Consentir à recevoir quelque chose ou quelqu\'un.',
        'ACCESSOIRE': 'Qui n\'est pas essentiel, secondaire.',
        'ACCIDENTEL': 'Qui arrive par accident, fortuit.',
        'ACCUEIL': 'Action de recevoir quelqu\'un ou quelque chose.',
        'ACCUEILLIR': 'Recevoir quelqu\'un avec bienveillance.',
        'ACHAT': 'Action d\'acheter, d\'acquérir quelque chose.',
        'ACHETER': 'Acquérir quelque chose en échange d\'une somme d\'argent.',
        'ACIDE': 'Substance chimique ayant un pH inférieur à 7, ou au goût piquant.',
        'ACIER': 'Alliage de fer et de carbone, très résistant.',
        'ACOMPTE': 'Somme versée à titre de premier paiement.',
        'ACQUÉRIR': 'Obtenir quelque chose par un effort ou un achat.',
        'ACROBATE': 'Artiste qui exécute des exercices de gymnastique ou d\'équilibre.',
        'ACTE': 'Action accomplie ou document officiel.',
        'ACTIF': 'Qui agit, qui est en activité.',
        'ACTUEL': 'Qui existe à l\'heure actuelle.',
        'ADAPTATION': 'Action de s\'adapter ou de modifier quelque chose pour un usage particulier.',
        'ADAPTER': 'Modifier quelque chose pour l\'adapter à une nouvelle situation.',
        'ADDICTION': 'Dépendance à une substance ou à une activité.',
        'ADDITION': 'Opération mathématique consistant à ajouter des nombres.',
        'ADJECTIF': 'Mot qui qualifie ou détermine un nom.',
        'ADMETTRE': 'Reconnaître comme vrai ou accepter.',
        'ADMINISTRATION': 'Gestion des affaires publiques ou privées.',
        'ADMINISTRER': 'Gérer, diriger une organisation ou un service.',
        'ADMIRATION': 'Sentiment de respect et d\'émerveillement.',
        'ADMIRER': 'Éprouver de l\'admiration pour quelqu\'un ou quelque chose.',
        'ADOLESCENCE': 'Période de la vie entre l\'enfance et l\'âge adulte.',
        'ADOLESCENT': 'Jeune personne en période d\'adolescence.',
        'ADOPTER': 'Prendre pour soi, faire sien.',
        'ADORABLE': 'Qui inspire de l\'affection, très mignon.',
        'ADORER': 'Aimer profondément, vénérer.',
        'ADRESSE': 'Lieu où habite une personne ou une entreprise.',
        'ADROIT': 'Qui a de l\'habileté manuelle ou intellectuelle.',
        'ADULTE': 'Personne ayant atteint l\'âge de la maturité.',
        'ADVERSAIRE': 'Personne ou équipe contre laquelle on lutte.',
        'ADVERSE': 'Qui est contraire, défavorable.',
        'AÉRATION': 'Action d\'aérer, de faire circuler l\'air.',
        'AÉRIEN': 'Qui se trouve dans l\'air ou qui concerne l\'air.',
        'AÉRODROME': 'Terrain aménagé pour l\'atterrissage et le décollage des avions.',
        'AÉRONAUTIQUE': 'Qui concerne la navigation aérienne.',
        'AFFAIBLIR': 'Rendre plus faible, diminuer la force.',
        'AFFECTION': 'Sentiment d\'attachement ou maladie.',
        'AFFECTUEUX': 'Qui montre de l\'affection.',
        'AFFICHE': 'Feuille imprimée destinée à être placardée.',
        'AFFICHER': 'Placer une affiche ou montrer quelque chose.',
        'AFFIRMATION': 'Action d\'affirmer, de déclarer quelque chose comme vrai.',
        'AFFIRMER': 'Déclarer quelque chose comme vrai.',
        'AFFRETER': 'Louer un navire ou un véhicule pour un transport.',
        'AFFREUX': 'Qui inspire de l\'horreur ou du dégoût.',
        'AFFRONTER': 'Faire face à une difficulté ou un danger.',
        'AFRICAIN': 'Qui concerne l\'Afrique ou ses habitants.',
        'AFRIQUE': 'Continent situé au sud de l\'Europe et à l\'est de l\'Atlantique.',
        'AGACER': 'Causer une légère irritation.',
        'AGENCE': 'Organisation ou bureau offrant des services.',
        'AGENT': 'Personne qui agit pour le compte d\'une organisation.',
        'AGGLOMÉRATION': 'Concentration de population ou de matières.',
        'AGGRAVER': 'Rendre une situation plus grave.',
        'AGICHAGE': 'Action de se comporter de manière exagérément affectée.',
        'AGILE': 'Qui a de la souplesse et de la rapidité.',
        'AGIR': 'Faire une action, accomplir quelque chose.',
        'AGITATION': 'État de mouvement ou d\'excitation.',
        'AGITER': 'Mettre en mouvement ou troubler.',
        'AGNEAU': 'Jeune mouton ou viande de cet animal.',
        'AGRANDIR': 'Rendre plus grand.',
        'AGRÉABLE': 'Qui plaît, qui est agréable.',
        'AGRÉER': 'Accepter, donner son accord.',
        'AGRÉMENT': 'Charmant, agréable à voir.',
        'AGRICOLE': 'Qui concerne l\'agriculture.',
        'AGRICULTEUR': 'Personne qui cultive la terre.',
        'AGRICULTURE': 'Culture de la terre pour produire des végétaux.',
        'AGRIPPER': 'Saisir fermement.',
        'AGUERRI': 'Qui a de l\'expérience, endurci.',
        'AIDE': 'Assistance apportée à quelqu\'un.',
        'AIDER': 'Apporter son aide à quelqu\'un.',
        'AIEUL': 'Ancêtre, grand-père ou arrière-grand-père.',
        'AIGRE': 'Qui a un goût acide et désagréable.',
        'AIGREUR': 'Goût aigre ou sentiment d\'amertume.',
        'AIGU': 'Qui est tranchant ou très développé.',
        'AIGUILLE': 'Petite tige métallique pour coudre ou instrument médical.',
        'AIGUILLER': 'Diriger, guider quelqu\'un.',
        'AIL': 'Plante potagère à bulbe utilisée comme condiment.',
        'AILE': 'Membre permettant de voler ou partie latérale.',
        'AILER': 'Battre des ailes.',
        'AILIER': 'Joueur de football ou de rugby évoluant sur les ailes.',
        'AIMABLE': 'Qui est agréable, sympathique.',
        'AIMANT': 'Objet attirant le fer ou personne inspirant l\'affection.',
        'AIMER': 'Éprouver de l\'affection pour quelqu\'un ou quelque chose.',
        'AINÉ': 'Le plus âgé parmi plusieurs.',
        'AIR': 'Mélange gazeux constituant l\'atmosphère.',
        'AISE': 'Facilité, absence de difficulté.',
        'AISÉ': 'Qui est facile à faire.',
        'AISÉMENT': 'De manière facile, sans difficulté.',
        'AJOUT': 'Action d\'ajouter quelque chose.',
        'AJOUTER': 'Ajouter quelque chose à ce qui existe déjà.',
        'AJUSTEMENT': 'Action d\'ajuster, de régler.',
        'AJUSTER': 'Régler, adapter quelque chose.',
        'ALARME': 'Signal sonore avertissant d\'un danger.',
        'ALARMER': 'Avertir d\'un danger ou inquiéter.',
        'ALBUM': 'Recueil de photos, de musique ou de timbres.',
        'ALCHIMIE': 'Art ancien cherchant à transformer les métaux en or.',
        'ALCOOL': 'Substance psychoactive présente dans les boissons fermentées.',
        'ALCOOLIQUE': 'Qui contient de l\'alcool ou qui est dépendant de l\'alcool.',
        'ALCOOLISME': 'Dépendance à l\'alcool.',
        'ALÉAS': 'Hasards, événements imprévus.',
        'ALÉATOIRE': 'Qui dépend du hasard.',
        'ALERTE': 'État de vigilance ou signal d\'avertissement.',
        'ALERTER': 'Avertir quelqu\'un d\'un danger.',
        'ALÉSAGE': 'Action d\'aléser, de percer un trou.',
        'ALGÈBRE': 'Branche des mathématiques étudiant les structures algébriques.',
        'ALGORITHME': 'Suite d\'opérations permettant de résoudre un problème.',
        'ALIBI': 'Preuve ou témoignage innocentant quelqu\'un.',
        'ALIMENT': 'Substance nourrissante.',
        'ALIMENTAIRE': 'Qui concerne l\'alimentation.',
        'ALIMENTATION': 'Action de se nourrir ou système fournissant de l\'énergie.',
        'ALIMENTER': 'Fournir de la nourriture ou de l\'énergie.',
        'ALIZE': 'Vent régulier soufflant des régions tropicales.',
        'ALLANT': 'Qui a de l\'allant, de l\'entrain.',
        'ALLEGATION': 'Affirmation, allégation.',
        'ALLÉGER': 'Rendre plus léger.',
        'ALLÉGORIE': 'Représentation symbolique d\'une idée.',
        'ALLÉGORIQUE': 'Qui est symbolique, allégorique.',
    }
    
    if mot_upper in definitions_specificques:
        return definitions_specificques[mot_upper]
    
    # Essayer de trouver un suffixe connu
    for suffix, template in suffixes_definitions.items():
        if len(mot) > len(suffix) and mot[-len(suffix):].upper() == suffix:
            root = mot[:-len(suffix)].lower()
            return template.format(root=root)
    
    # Définition par défaut
    if len(mot) > 3 and mot[-2:].upper() == 'ER':
        return f"Action de {mot.lower()}."
    elif len(mot) > 3 and mot[-2:].upper() in ['IR', 'RE']:
        return f"Action de {mot.lower()}."
    elif len(mot) > 2 and mot[-1].upper() == 'E':
        return f"Qualité ou action de {mot.lower()}."
    else:
        return f"Concept ou objet lié à {mot.lower()}."

# Fonction pour générer des exemples
def generer_exemples(mot):
    mot_lower = mot.lower()
    
    # Vérifier si le mot existe déjà dans les mots existants
    for m in matches:
        if m[0].upper() == mot.upper():
            return [m[2], m[3], m[4]]
    
    # Exemples spécifiques pour certains mots
    exemples_specificques = {
        'ABEILLE': [
            'L\'abeille butine les fleurs pour collecter le pollen.',
            'Une ruche peut abriter des milliers d\'abeilles.',
            'Le miel est produit par les abeilles à partir du nectar.'
        ],
        'ABRICOT': [
            'J\'ai mangé un abricot bien mûr ce matin.',
            'La confiture d\'abricot est délicieuse sur des tartines.',
            'Les abricots séchés sont riches en vitamines.'
        ],
        'ABSENT': [
            'Il était absent à la réunion hier.',
            'Son absence a été remarquée par le professeur.',
            'Elle s\'est excusée pour son absence.'
        ],
        'ABSOLUMENT': [
            'Je suis absolument sûr de ma réponse.',
            'C\'est absolument nécessaire de partir maintenant.',
            'Il est absolument interdit de fumer ici.'
        ],
        'ABUS': [
            'L\'abus d\'alcool est dangereux pour la santé.',
            'Il a été accusé d\'abus de confiance.',
            'L\'abus de pouvoir peut avoir de graves conséquences.'
        ],
    }
    
    if mot.upper() in exemples_specificques:
        return exemples_specificques[mot.upper()]
    
    # Générer des exemples génériques
    article = 'l\' ' if mot_lower[0] in 'aeiouh' else 'un '
    if mot_lower[0] == 'a' and mot_lower[1] == 'é':
        article = 'l\' '
    
    exemples = []
    
    # Exemple 1: Utilisation basique
    if mot_lower.endswith('er'):
        exemples.append(f"Il faut {mot_lower} avec soin.")
    elif mot_lower.endswith('ir'):
        exemples.append(f"Je vais {mot_lower} cette tâche.")
    elif mot_lower.endswith('e'):
        exemples.append(f"La {mot_lower} est importante.")
    else:
        exemples.append(f"{article}{mot_lower} est utile.")
    
    # Exemple 2: Utilisation dans une phrase
    if mot_lower.endswith(('er', 'ir', 're')):
        exemples.append(f"Nous devons {mot_lower} pour réussir.")
    else:
        exemples.append(f"J\'aime {article}{mot_lower}.")
    
    # Exemple 3: Utilisation dans un contexte
    exemples.append(f"Peux-tu me parler de {article}{mot_lower}?")
    
    return exemples

# Créer le fichier corpus.txt
with open('corpus.txt', 'w', encoding='utf-8') as f:
    # Écrire l'en-tête
    f.write("=" * 80 + "\n")
    f.write("CORPUS COMPLET DE MOTS FRANÇAIS AVEC DÉFINITIONS ET EXEMPLES\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Nombre total de mots: {len(matches) + len(nouveaux_mots)}\n")
    f.write("Format: [MOT]\n")
    f.write("Définition: [définition]\n")
    f.write("Exemples:\n")
    f.write("- Exemple 1\n")
    f.write("- Exemple 2\n")
    f.write("- Exemple 3\n\n")
    f.write("=" * 80 + "\n\n")
    
    # Écrire les mots existants
    for match in matches:
        mot, definition, ex1, ex2, ex3 = match
        f.write(f"=== {mot} ===\n")
        f.write(f"Définition: {definition}\n\n")
        f.write("Exemples:\n")
        f.write(f"- {ex1}\n")
        f.write(f"- {ex2}\n")
        f.write(f"- {ex3}\n\n")
    
    # Écrire les nouveaux mots
    for mot in nouveaux_mots:
        definition = generer_definition(mot)
        exemples = generer_exemples(mot)
        f.write(f"=== {mot} ===\n")
        f.write(f"Définition: {definition}\n\n")
        f.write("Exemples:\n")
        for ex in exemples:
            f.write(f"- {ex}\n")
        f.write("\n")

print("Fichier corpus.txt créé avec succès!")
print(f"Total: {len(matches) + len(nouveaux_mots)} mots")
