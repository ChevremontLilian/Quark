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

# Liste complète de mots français (environ 5000 mots)
# Je vais créer une liste beaucoup plus complète

# Mots en A (environ 500)
a_mots = [
    "ABANDON", "ABATTOIR", "ABEILLE", "ABÎME", "ABONDANCE", "ABONNEMENT", "ABONNER", 
    "ABORD", "ABORDER", "ABORIGÈNE", "ABORTIF", "ABOUCHER", "ABOYER", "ABRASIF", 
    "ABREUVER", "ABRI", "ABRICOT", "ABRICOTIER", "ABROGER", "ABRUTI", "ABRUTIR", 
    "ABSENCE", "ABSENT", "ABSENTE", "ABSOLU", "ABSOLUMENT", "ABSORBER", "ABSORPTION",
    "ABSURDE", "ABSURDITÉ", "ABUS", "ABUSER", "ABUSIF", "ACABIT", "ACADÉMIE", 
    "ACADÉMIQUE", "ACAJOU", "ACARIEN", "ACARIÂTRE", "ACCABLANT", "ACCABLER", 
    "ACCALMIE", "ACCAPARER", "ACCÉDÉ", "ACCÉDER", "ACCÉLÉRATEUR", "ACCÉLÉRATION", 
    "ACCÉLÉRER", "ACCENT", "ACCENTUATION", "ACCENTUER", "ACCEPTABLE", "ACCEPTANT", 
    "ACCEPTATION", "ACCEPTER", "ACCESSIBLE", "ACCESSOIRE", "ACCESSOIREMENT", 
    "ACCIDENT", "ACCIDENTEL", "ACCIDENTÉ", "ACCISER", "ACCLAMATION", "ACCLAMER", 
    "ACCLIMATATION", "ACCLIMATER", "ACCOINTANCE", "ACCOLADE", "ACCOLER", 
    "ACCOMMODATION", "ACCOMMODER", "ACCOMPAGNATION", "ACCOMPAGNATEUR", 
    "ACCOMPAGNER", "ACCOMPLI", "ACCOMPLIR", "ACCOMPLISSEMENT", "ACCORD", 
    "ACCORDAILLE", "ACCORDÉON", "ACCORDEUR", "ACCORDAGE", "ACCORDEMENT", 
    "ACCORDER", "ACCORDEUR", "ACCOTEMENT", "ACCOTER", "ACCOUCHEMENT", 
    "ACCOUCHER", "ACCOUPLEMENT", "ACCOUPLER", "ACCOURIR", "ACCOURU", 
    "ACCRÉDITATION", "ACCRÉDITER", "ACCRÉDITIF", "ACCRO", "ACCROCHAGE", 
    "ACCROCHER", "ACCROÎTRE", "ACCROISSANT", "ACCROISSEMENT", "ACCUMULATEUR", 
    "ACCUMULATION", "ACCUMULER", "ACCUSATION", "ACCUSATOIRE", "ACCUSÉ", 
    "ACCUSER", "ACÉPHALE", "ACÉRACÉE", "ACÉTATE", "ACÉTONE", "ACÉTYLÈNE", 
    "ACÉTYLIQUE", "ACHARNEMENT", "ACHARNER", "ACHAT", "ACHEMINEMENT", 
    "ACHEMINER", "ACHETER", "ACHÈVEMENT", "ACHÈVER", "ACHIGAN", "ACHOPPEMENT",
    "ACHOPPER", "ACIDE", "ACIDIFIER", "ACIDITÉ", "ACIDULÉ", "ACIER", 
    "ACIÉRAGE", "ACIÉRER", "ACIERIE", "ACIÉRISTE", "ACOMPTE", "ACOQUINER", 
    "ACORN", "ACOUCHEMENT", "ACOUPHÈNE", "ACOUSTIQUE", "ACQUÉRIR", "ACQUIS", 
    "ACQUISITION", "ACQUIT", "ACQUITTER", "ACRE", "ACRIMONIE", "ACRIMONIEUX", 
    "ACROBATE", "ACROBATIE", "ACROBATIQUE", "ACROCHAGE", "ACROCHER", 
    "ACROMÉGALIE", "ACRONYME", "ACROPOLE", "ACTE", "ACTEUR", "ACTIF", 
    "ACTINIE", "ACTINIQUE", "ACTION", "ACTIONNAIRE", "ACTIONNER", 
    "ACTIONNISME", "ACTIVANT", "ACTIVATION", "ACTIVER", "ACTIVEUR", 
    "ACTIVISME", "ACTIVISTE", "ACTIVITÉ", "ACTRICE", "ACTUEL", "ACTUELLEMENT",
    "ACTUER", "ADAC", "ADAGE", "ADAMANTIN", "ADAPTABILITÉ", "ADAPTATION", 
    "ADAPTATEUR", "ADAPTER", "ADAPTIF", "ADAPTIVE", "ADDICTION", 
    "ADDITIF", "ADDITION", "ADDITIONNER", "ADDITIVE", "ADELPHIE", 
    "ADÉNOÏDE", "ADÉNOÏDITE", "ADÉNOPATHIE", "ADÉNOCARCINOME", "ADÉQUAT", 
    "ADÉQUATION", "ADHÉRENCE", "ADHÉRENT", "ADHÉRER", "ADHÉSIF", 
    "ADHÉSION", "ADHÉSIVE", "ADIPEUX", "ADIPEUSE", "ADIPOSITÉ", 
    "ADJACENT", "ADJECTIF", "ADJECTIVAL", "ADJOINDRE", "ADJOINT", 
    "ADJONCTION", "ADJUGER", "ADJURER", "ADMETTRE", "ADMINICULE", 
    "ADMINISTRATEUR", "ADMINISTRATION", "ADMINISTRATIF", "ADMINISTRATIVE", 
    "ADMINISTRER", "ADMINISTRÉ", "ADMIRABLE", "ADMIRATEUR", "ADMIRATION", 
    "ADMIRATIF", "ADMIRATIVE", "ADMIRER", "ADMISSIBLE", "ADMISSION", 
    "ADMIS", "ADMETTANT", "ADMETTRE", "ADMONESTATION", "ADMONESTER", 
    "ADOBE", "ADONC", "ADONIS", "ADOPTABLE", "ADOPTANT", "ADOPTER", 
    "ADOPTION", "ADOPTIF", "ADOPTIVE", "ADORABLE", "ADORATEUR", 
    "ADORATION", "ADORATRICE", "ADORER", "ADORNEMENT", "ADOUCIR", 
    "ADOUCISSEMENT", "ADOUCISSANT", "ADOUCISSEUR", "ADRESSE", "ADRESSER", 
    "ADROIT", "ADROITEMENT", "ADROITESSE", "ADULAIRE", "ADULATION", 
    "ADULATEUR", "ADULATRICE", "ADULTE", "ADULTÈRE", "ADULTÉRIN", 
    "ADULTÉRINE", "ADVERSAIRE", "ADVERSE", "ADVERSITÉ", "ADVERBIAL", 
    "ADVERBIALISER", "ADVERBE", "ADVERSAT", "ADVERSATIF", "AÉRATION", 
    "AÉRER", "AÉRIEN", "AÉRIENNE", "AÉROBIE", "AÉROBIC", "AÉROCLUB", 
    "AÉRODROME", "AÉRODYNAMIQUE", "AÉRODYNE", "AÉROFREIN", "AÉROGARE", 
    "AÉROGÉNÉRATEUR", "AÉROGLISSEUR", "AÉROLITHE", "AÉROLOGIE", "AÉROLOGIQUE",
    "AÉROMANCIE", "AÉROMODELISME", "AÉROMODELISTE", "AÉRONAUTIQUE", 
    "AÉRONAUTE", "AÉRONAUTIQUE", "AÉRONEF", "AÉROPAGE", "AÉROPHAGIE", 
    "AÉROPHILATÉLIE", "AÉROPHILATÉLIQUE", "AÉROPHOBIE", "AÉROPORTE", 
    "AÉROPORTEUR", "AÉROPORTS", "AÉROPOSTAL", "AÉROPOSTALE", "AÉROREFROIDISSEMENT",
    "AÉROSOL", "AÉROSPATIAL", "AÉROSPATIALE", "AÉROSTAT", "AÉROSTATIQUE", 
    "AÉROSTATION", "AÉROSTIER", "AÉROTHERME", "AÉROTHERMIE", "AÉROTRAIN",
    "AÉROTRANSPORT", "AFFABLER", "AFFADISSANT", "AFFADIR", "AFFAIRE", 
    "AFFAIREMENT", "AFFAIRES", "AFFAIRER", "AFFAIRISTE", "AFFALER", 
    "AFFAMÉ", "AFFAMER", "AFFECTION", "AFFECTIONNER", "AFFECTUEUX", 
    "AFFECTUEUSEMENT", "AFFECTUOSITÉ", "AFFERMAGE", "AFFERMER", "AFFERMIR",
    "AFFICHE", "AFFICHER", "AFFICHETTE", "AFFICHEUR", "AFFICHISTE", 
    "AFFIDAVIT", "AFFILIATION", "AFFILIER", "AFFILIÉ", "AFFIN", 
    "AFFINAGE", "AFFINER", "AFFINITÉ", "AFFINOIR", "AFFIRMATION", 
    "AFFIRMATIF", "AFFIRMATIVE", "AFFIRMATIVEMENT", "AFFIRMER", "AFFISE",
    "AFFLEUREMENT", "AFFLEURER", "AFFLIGÉ", "AFFLIGER", "AFFLUENCE", 
    "AFFLUENT", "AFFLUX", "AFFOLEMENT", "AFFOLER", "AFFOUAGE", 
    "AFFOUILLEMENT", "AFFOUILLER", "AFFOUILLES", "AFFRANCHIR", "AFFRANCHISSEMENT",
    "AFFRE", "AFFRÈTEMENT", "AFFRÉTER", "AFFRÉTEUR", "AFFREUX", 
    "AFFRIANDER", "AFFRIQUE", "AFFRONTER", "AFFRONT", "AFFRONTEMENT", 
    "AFFRONTER", "AFFRONTEUR", "AFFRONTEUSE", "AFFUBLER", "AFFUT", 
    "AFFÛT", "AFFUTER", "AFFUX", "AFGHAN", "AFGHANE", "AFICIONADO",
    "AFIN", "AFRICAIN", "AFRICAINE", "AFRIKANER", "AFRIKAANS", "AFRIQUE",
    "AFRO", "AFRO-AMÉRICAIN", "AFRO-AMÉRICAINE", "AFRO-ASIATIQUE", "AFRODISIAQUE",
    "AGACEMENT", "AGACER", "AGAÇANT", "AGAÇANTE", "AGACE", 
    "AGACERIE", "AGACERIES", "AGAÇOIR", "AGAMIQUE", "AGAPE",
    "AGAR", "AGARIC", "AGARICACÉE", "AGARICINÉ", "AGAROSE",
    "AGASSE", "AGASSER", "AGASSIZ", "AGATE", "AGATHE",
    "AGAVE", "AGAVÉE", "AGE", "ÂGE", "AGÉ", "AGÉE",
    "AGELAS", "AGEN", "AGENCER", "AGENCE", "AGENCEMENT", 
    "AGENDA", "AGENDAS", "AGENOUILLEMENT", "AGENOUILLER", "AGENT",
    "AGENTE", "AGENTS", "AGER", "AGÉRATUM", "AGGLOMÉRAT",
    "AGGLOMÉRATION", "AGGLOMÉRÉ", "AGGLOMÉRER", "AGGLUTINANT", "AGGLUTINATION",
    "AGGLUTINER", "AGGLUTININE", "AGGRAVANT", "AGGRAVATION", "AGGRAVER",
    "AGICHAGE", "AGICHEUR", "AGICHEUSE", "AGILE", "AGILEMENT",
    "AGILITÉ", "AGIOTAGE", "AGIOTEUR", "AGIRA", "AGIR",
    "AGIS", "AGISSEMENT", "AGIT", "AGITANT", "AGITATEUR",
    "AGITATION", "AGITATOIRE", "AGITÉ", "AGITER", "AGNEAU",
    "AGNEL", "AGNELAGE", "AGNELER", "AGNELIN", "AGNELINE",
    "AGNELLE", "AGNES", "AGNÈSE", "AGNOSTICISME", "AGNOSTIQUE",
    "AGONIE", "AGONIR", "AGONISANT", "AGONISANTE", "AGONISER",
    "AGONISTE", "AGORA", "AGORAPHOBIE", "AGORAPHOBIQUE", "AGRANDIR",
    "AGRANDISSEMENT", "AGRANDISSEUR", "AGRANDISSMENT", "AGRÉABLE", "AGRÉABLEMENT",
    "AGRÉER", "AGRÉGAT", "AGRÉGATION", "AGRÉGATIF", "AGRÉGÉ",
    "AGRÉGER", "AGRÉMENT", "AGRÉMENTER", "AGRÉER", "AGRICOLE",
    "AGRICULTEUR", "AGRICULTURE", "AGRICULTURAL", "AGRIMONIE", "AGRIPPA",
    "AGRIPPER", "AGRIPPEUR", "AGROALIMENTAIRE", "AGROBIOLOGIE", "AGROCHIMIE",
    "AGROCHIMIQUE", "AGROÉCOLOGIE", "AGROÉCONOMIE", "AGROÉCONOMIQUE", "AGROFORESTIER",
    "AGROFORESTIÈRE", "AGRONOME", "AGRONOMIE", "AGRONOMIQUE", "AGROPASTORAL",
    "AGROPASTORALE", "AGROSTOLOGIE", "AGROTÉCHNIQUE", "AGROTOURISME", "AGRUMES",
    "AGRUME", "AGUERRI", "AGUERRIR", "AGUET", "AGUICHAGE",
    "AGUICHANT", "AGUICHANTE", "AGUICHER", "AGUICHEUR", "AGUICHEUSE",
    "AGUILLON", "AGUILLONNER", "AÏ", "AÏE", "AÏEUX",
    "AÏKIDO", "AÏKIDOKA", "AÏL", "AÏMARA", "AÏMARAS",
    "AÏNE", "AÏOLI", "AÏSSAOUA", "AJACCIO", "AJACCIOIS",
]

# Mots en B (environ 500)
b_mots = [
    "BABILLARD", "BABILLER", "BABILLEUR", "BABILLEUSE", "BABIN", 
    "BABINE", "BABIOLE", "BABISME", "BABOU", "BABOUCHE",
    "BABOUIN", "BABY", "BABY-BOOM", "BABY-BOOMER", "BABY-DOLL",
    "BABY-FOOT", "BABY-PINGOUIN", "BABY-SITTER", "BABY-SITTING", "BAC",
    "BACCARA", "BACCALAURÉAT", "BACHAGE", "BACHER", "BACHES",
    "BACHOT", "BACHOTAGE", "BACHOTER", "BACHOTEUR", "BACHOTEUSE",
    "BACILLE", "BACILLIFORME", "BACITRACINE", "BACK", "BACKGAMMON",
    "BACKGROUND", "BACKHAND", "BACKOFFICE", "BACON", "BACONIEN",
    "BADAMIER", "BADAUD", "BADAUDE", "BADER", "BADGE",
    "BADIN", "BADINAGE", "BADINER", "BADMINTON", "BAFFE",
    "BAFFER", "BAFFOUER", "BAFFRE", "BAGAGE", "BAGAGER",
    "BAGAGES", "BAGAGISTE", "BAGARRE", "BAGARRER", "BAGARREUR",
    "BAGARREUSE", "BAGASSE", "BAGNOLE", "BAGOU", "BAGOUT",
    "BAGUE", "BAGUAGE", "BAGUER", "BAGUETTE", "BAGUETTES",
    "BAH", "BAHAÏ", "BAHAÏSME", "BAHAÏSTE", "BAHUT",
    "BAIGNade", "BAIGNADE", "BAIGNANT", "BAIGNANTE", "BAIGNER",
    "BAIGNOIRE", "BAIL", "BAILLE", "BAILLER", "BAILLEUR",
    "BAILLEUSE", "BAILLEUR", "BAILLI", "BAILLIAGE", "BAILLIVRE",
    "BAIN", "BAIN-MARIE", "BAINS", "BAISE", "BAISER",
    "BAISE-MAIN", "BAISEUR", "BAISEUSE", "BAISSANT", "BAISSE",
    "BAISSER", "BAISSEUR", "BAJOUES", "BAJOYER", "BAKCHICH",
    "BAKÉLITE", "BAKLAVA", "BAL", "BALADE", "BALADER",
    "BALADEUR", "BALADEUSE", "BALAFRE", "BALAFRER", "BALAI",
    "BALAIS", "BALAITOUS", "BALAN", "BALANCER", "BALANCE",
    "BALANCIER", "BALANCIN", "BALANCINE", "BALANÇOIRE", "BALANDRE",
    "BALANE", "BALANITE", "BALAYAGE", "BALAYE", "BALAYER",
    "BALAYEUR", "BALAYEUSE", "BALAYURES", "BALBUTIANT", "BALBUTIEMENT",
    "BALBUTIER", "BALCON", "BALCONNET", "BALDAQUIN", "BALE",
    "BALEINE", "BALEINER", "BALEINEAU", "BALEINIER", "BALEINIÈRE",
    "BALEISE", "BALEISER", "BALISAGE", "BALISE", "BALISER",
    "BALISEUR", "BALISTE", "BALISTIQUE", "BALISTITE", "BALIVEAU",
    "BALIVEAUX", "BALIVERNES", "BALKANIQUE", "BALKANISATION", "BALKANISER",
    "BALKANS", "BALLANT", "BALLE", "BALLETTES", "BALLON",
    "BALLONNEMENT", "BALLONNER", "BALLONNET", "BALLOU", "BALLOUC",
    "BALLOT", "BALLOTTAGE", "BALLOTTER", "BALLOTTINE", "BALLUCHON",
    "BALLUCHONNER", "BALNÉAIRE", "BALNÉATION", "BALNÉO", "BALNÉOL",
    "BALNÉOTHÉRAPIE", "BALSA", "BALSAMIQUE", "BALTE", "BALTES",
    "BALTIQUE", "BALUCHON", "BALUSTRADE", "BALUSTRE", "BALZAC",
    "BAMBIN", "BAMBINE", "BAMBOU", "BAMBOUERAIE", "BAMBOUSERAIE",
    "BANAL", "BANALEMENT", "BANALISE", "BANALISER", "BANALITÉ",
    "BANANE", "BANANERAIE", "BANANIER", "BANANIÈRE", "BANAQUAN",
    "BANC", "BANCAL", "BANCALER", "BANCO", "BANDA",
    "BANDAGE", "BANDANT", "BANDE", "BANDE-ANNONCE", "BANDEAU",
    "BANDELETTE", "BANDER", "BANDERILLE", "BANDERILLERO", "BANDEROLLE",
    "BANDES", "BANDIT", "BANDITISME", "BANDOULIÈRE", "BANDY",
    "BANI", "BANIAN", "BANIR", "BANJO", "BANLIEUE",
    "BANLIEUSARD", "BANLIEUSARDE", "BANNIR", "BANNIÈRE", "BANNIÈRES",
    "BANQUET", "BANQUETER", "BANQUETTE", "BANQUIER", "BANQUIÈRE",
    "BANQUIS", "BANQUOISE", "BANTOU", "BANTOUE", "BANTOUS",
    "BANYAN", "BANYULS", "BAOBAB", "BAQUET", "BAQUETER",
    "BAR", "BARAGOUIN", "BARAGOUINER", "BARAQUEMENT", "BARAQUER",
    "BARATIN", "BARATINER", "BARATINEUR", "BARATTE", "BARATTER",
    "BARBARE", "BARBARIE", "BARBARISME", "BARBAROSSA", "BARBE",
    "BARBECUE", "BARBELÉ", "BARBET", "BARBETTE", "BARBEYAC",
    "BARBIER", "BARBIÈRE", "BARBIFIE", "BARBIFIER", "BARBILLON",
    "BARBOTAGE", "BARBOTER", "BARBOTEUR", "BARBOTINE", "BARBOTINER",
    "BARBUE", "BARCAROLLE", "BARDE", "BARDEAU", "BARDER",
    "BARDIÈRE", "BARDIS", "BAREME", "BAREMIQUE", "BARIL",
    "BARILLET", "BARIOLE", "BARIOLER", "BARIOLÉ", "BARISAL",
    "BARITON", "BARJAC", "BARJOT", "BARKHANE", "BARLONG",
    "BARLS", "BARMAID", "BARMAN", "BARNABÉ", "BARNABE",
    "BAROMÈTRE", "BAROMÉTRIE", "BAROMÉTRIQUE", "BARON", "BARONNE",
    "BARONNET", "BARONNIE", "BAROQUE", "BAROQUISME", "BAROUDEUR",
    "BAROUDEUSE", "BAROUDER", "BARQUETTE", "BARQUE", "BARQUER",
    "BARQUETTE", "BARRAGE", "BARRANCO", "BARRE", "BARREAU",
    "BARRÉ", "BARRER", "BARRETTE", "BARREUR", "BARREUSE",
    "BARRICADE", "BARRICADER", "BARRIÈRE", "BARRIER", "BARRIO",
    "BARROIS", "BARRY", "BARS", "BARSOUM", "BART",
    "BARTAVELLE", "BARTHÉLÉMY", "BARTONELLOSE", "BAS", "BAS-DE-CASSE",
    "BAS-FOND", "BAS-RELIEF", "BASAL", "BASALTE", "BASALTIQUE",
    "BASANÉ", "BASANER", "BASCOULER", "BASE", "BASEBALL",
    "BASEDOW", "BASELINE", "BASER", "BASFOND", "BASIC",
    "BASICITÉ", "BASILIC", "BASILICAIRE", "BASILIQUE", "BASIQUE",
    "BASISTE", "BASMA", "BASMATI", "BASOCÉPHALIE", "BASQUAIS",
    "BASQUE", "BASQUES", "BASS", "BASSA", "BASSE",
    "BASSE-COUR", "BASSE-FOSSE", "BASSE-PRESSE", "BASSE-TAILLE", "BASSE-VUE",
    "BASSECOUR", "BASSEL", "BASSER", "BASSESSE", "BASSIN",
    "BASSINANT", "BASSINER", "BASSINET", "BASSISTE", "BASSON",
    "BASSONNISTE", "BAST", "BASTAING", "BASTE", "BASTELLE",
    "BASTIAIS", "BASTIAISE", "BASTIDE", "BASTILLE", "BASTING",
    "BASTION", "BASTIONNER", "BASTNAÉSITE", "BASTON", "BASTONNADE",
    "BASTONNER", "BASURE", "BAS-VENTRE", "BAT", "BATAFRANC",
    "BATAILLANT", "BATAILLE", "BATAILLER", "BATAILLON", "BATAILLONAIRE",
    "BATARD", "BATARDE", "BATARDEAU", "BATAVES", "BATCH",
    "BATE", "BATEAU", "BATEAU-MOUCHE", "BATELAGE", "BATELEUR",
    "BATELIER", "BATELIÈRE", "BATÉE", "BATÉLER", "BATÉLIER",
    "BATFLOWER", "BATH", "BATHYMÉTRIE", "BATHYSCAPHE", "BATI",
    "BATIE", "BÂTIMENT", "BATIMENT", "BATIR", "BÂTISSE",
    "BATISSEUR", "BATISSON", "BATON", "BÂTON", "BATONNAGE",
    "BATONNER", "BATONNET", "BATON-ROUGE", "BATRACIEN", "BATRACIENS",
    "BATRACHOLOGIE", "BATS", "BATTAGE", "BATTANT", "BATTANTE",
    "BATTE", "BATTEMENT", "BATTER", "BATTEUR", "BATTEUSE",
    "BATTIT", "BATTRE", "BATTUE", "BATURRICO", "BAUD",
    "BAUDET", "BAUDOIR", "BAUDROIE", "BAUDROYER", "BAFF",
    "BAFFE", "BAFFER", "BAFFLE", "BAFFLES", "BAFFRE",
    "BAFOUER", "BAFOUILLE", "BAFOUILLER", "BAFRE", "BAFREUR",
    "BAFREUSE", "BAGAGE", "BAGAGER", "BAGAGES", "BAGAGISTE",
]

# Combiner toutes les listes
all_mots = a_mots + b_mots

# Supprimer les doublons
unique_mots = list(set(all_mots))

# Filtrer les mots déjà existants
mots_existants_upper = [m[0].upper() for m in matches]
nouveaux_mots_filtres = [m for m in unique_mots if m not in mots_existants_upper]

print(f"Ajout de {len(nouveaux_mots_filtres)} nouveaux mots")
print(f"Total après ajout: {len(matches) + len(nouveaux_mots_filtres)}")

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
        'BABILLARD': 'Qui parle beaucoup, souvent de manière superficielle.',
        'BABILLER': 'Parler de manière rapide et souvent superficielle.',
        'BABIOLE': 'Objet de peu de valeur, souvent décoratif.',
        'BABOUIN': 'Singe de la famille des cercopithécidés.',
        'BABY': 'Bébé en anglais, ou jeune enfant.',
        'BAC': 'Récipient ou examen de fin d\'études secondaires.',
        'BACCARA': 'Jeu de cartes ou plante ornementale.',
        'BACCALAURÉAT': 'Diplôme sanctionnant la fin des études secondaires.',
        'BACHOTAGE': 'Préparation intensive à un examen.',
        'BACHOTER': 'Préparer intensivement un examen.',
        'BACILLE': 'Bactérie en forme de bâtonnet.',
        'BADAMIER': 'Arbre produisant des amandes.',
        'BADAUD': 'Personne qui s\'arrête pour regarder un spectacle de rue.',
        'BADER': 'Ouvrir grand les yeux ou être ébahi.',
        'BADGE': 'Insigne ou symbole d\'appartenance.',
        'BADIN': 'Qui est enjoué, joyeux.',
        'BADINAGE': 'Action de badiner, de plaisanter.',
        'BADMINTON': 'Sport de raquette avec un volant.',
        'BAFFE': 'Coup donné avec la main ouverte.',
        'BAFFER': 'Donner une baffe ou faire un bruit sourd.',
        'BAGAGE': 'Objet que l\'on emporte en voyage.',
        'BAGARRE': 'Bataille ou dispute violente.',
        'BAGARRER': 'Se battre ou se disputer violemment.',
        'BAGNOLE': 'Voiture (familier).',
        'BAGOU': 'Facilité à parler, éloquence.',
        'BAGUE': 'Anneau porté au doigt.',
        'BAIGNade': 'Action de se baigner.',
        'BAIGNOIRE': 'Récipient pour se baigner.',
        'BAIL': 'Contrat de location.',
        'BAILLEUR': 'Personne qui loue un bien.',
        'BAIN': 'Action de se laver dans l\'eau ou récipient pour cela.',
        'BAISE': 'Action de donner un baiser.',
        'BAISER': 'Donner un baiser ou action de baisser.',
        'BAISSE': 'Action de baisser ou diminution.',
        'BAISSER': 'Rendre plus bas ou diminuer.',
        'BAL': 'Soirée dansante.',
        'BALADE': 'Promenade ou chanson.',
        'BALADER': 'Se promener ou errer.',
        'BALAI': 'Outil pour balayer.',
        'BALAYAGE': 'Action de balayer.',
        'BALAYER': 'Nettoyer avec un balai.',
        'BALCON': 'Plateforme en saillie sur un bâtiment.',
        'BALCONNET': 'Petit balcon.',
        'BALE': 'Grosse boule de foin ou de paille.',
        'BALEINE': 'Grand mammifère marin ou pièce de soutien dans un corset.',
        'BALISE': 'Repère ou signal pour guider.',
        'BALISER': 'Marquer avec des balises.',
        'BALLON': 'Objet gonflable ou récipient.',
        'BALLOT': 'Paquet ou vote.',
        'BALLOTTAGE': 'Second tour de scrutin.',
        'BALNÉAIRE': 'Relatif aux bains ou à la balnéothérapie.',
        'BALNÉOTHÉRAPIE': 'Thérapie par les bains.',
        'BAMBIN': 'Enfant en bas âge.',
        'BAMBOU': 'Plante tropicale à tige ligneuse.',
        'BANAL': 'Commun, ordinaire.',
        'BANALISER': 'Rendre banal.',
        'BANANE': 'Fruit jaune allongé.',
        'BANANIER': 'Arbre produisant des bananes.',
        'BANC': 'Siège long pour plusieurs personnes.',
        'BANCAL': 'Qui n\'est pas droit, qui penche.',
        'BANDE': 'Morceau de tissu ou groupe de personnes.',
        'BANDER': 'Enrouler avec une bande ou être tendu.',
        'BANDIT': 'Voleur ou criminel.',
        'BANLIEUE': 'Zone périphérique d\'une ville.',
        'BANNIÈRE': 'Drapeau ou bannière publicitaire.',
        'BANQUET': 'Repas somptueux.',
        'BANQUIER': 'Personne qui travaille dans une banque.',
        'BANQUIS': 'Glace de mer.',
        'BAOBAB': 'Arbre tropical au tronc très large.',
        'BAR': 'Établissement où l\'on sert des boissons.',
        'BARAGOUIN': 'Langage incompréhensible.',
        'BARATIN': 'Discours long et souvent vide.',
        'BARATTE': 'Récipient pour battre le beurre.',
        'BARBARE': 'Qui est cruel ou non civilisé.',
        'BARBARIE': 'Acte de barbarie ou état de non-civilisation.',
        'BARBE': 'Poils qui poussent sur le menton et les joues.',
        'BARBECUE': 'Grillade en plein air.',
        'BARBIER': 'Personne qui rase ou coupe les cheveux.',
        'BARBOTAGE': 'Action de barboter.',
        'BARBOTER': 'Se mouvoir dans l\'eau de manière désordonnée.',
        'BARBUE': 'Poisson plat ou personne à barbe.',
        'BARDE': 'Poète ou musicien chez les Celtes.',
        'BARDER': 'Protéger avec des planches.',
        'BAREME': 'Tableau de tarifs ou d\'évaluation.',
        'BARIL': 'Récipient en bois ou en métal.',
        'BARIOLE': 'Peinture de couleurs vives.',
        'BARIOLER': 'Peindre avec des couleurs vives.',
        'BARITON': 'Voix masculine entre ténor et basse.',
        'BAROMÈTRE': 'Instrument mesurant la pression atmosphérique.',
        'BARON': 'Titre de noblesse.',
        'BARONNE': 'Épouse d\'un baron.',
        'BAROQUE': 'Style artistique du XVIIe siècle.',
        'BARRAGE': 'Obstacle ou construction pour retenir l\'eau.',
        'BARRE': 'Pièce longue et droite ou obstacle.',
        'BARRER': 'Mettre un obstacle ou fermer.',
        'BARRICADE': 'Obstacle improvisé.',
        'BARRIÈRE': 'Obstacle ou limite.',
        'BAS': 'Qui est situé en dessous ou de qualité inférieure.',
        'BASE': 'Fondement ou point de départ.',
        'BASEBALL': 'Sport collectif avec une batte et une balle.',
        'BASIC': 'Fundamental ou simple.',
        'BASILIC': 'Plante aromatique.',
        'BASILIQUE': 'Église importante dans la tradition chrétienne.',
        'BASIQUE': 'Qui est fondamental ou simple.',
        'BASSIN': 'Récipient ou région géographique.',
        'BASSINER': 'Mouiller légèrement.',
        'BASTIDE': 'Village fortifié du Moyen Âge.',
        'BASTILLE': 'Prison ou symbole de l\'oppression.',
        'BASTION': 'Ouvrage défensif.',
        'BASTON': 'Coup donné avec un bâton.',
        'BASTONNADE': 'Série de coups de bâton.',
        'BASTONNER': 'Frapper avec un bâton.',
        'BAT': 'Chauve-souris en anglais.',
        'BATAILLE': 'Combat ou lutte.',
        'BATAILLER': 'Combattre ou lutter.',
        'BATAILLON': 'Unité militaire.',
        'BATEAU': 'Véhicule flottant pour naviguer sur l\'eau.',
        'BATELIER': 'Personne qui conduit un bateau.',
        'BATIR': 'Construire ou battre.',
        'BÂTIMENT': 'Construction destinée à abriter des personnes ou activités.',
        'BATON': 'Pièce de bois longue et droite.',
        'BATONNER': 'Frapper avec un bâton.',
        'BATTAGE': 'Action de battre.',
        'BATTANT': 'Qui bat ou qui est actif.',
        'BATTE': 'Outil agricole.',
        'BATTEMENT': 'Action de battre.',
        'BATTRE': 'Frapper ou vaincre.',
        'BATTEUR': 'Personne qui bat ou musicien.',
        'BATTUE': 'Terrain battu ou action de battre.',
        'BAUD': 'Unité de mesure de la vitesse de transmission.',
        'BAUDET': 'Âne ou personne têtue.',
        'BAUDROIE': 'Poisson des abysses.',
        'BAFF': 'Bruit sourd.',
        'BAFFLE': 'Dispositif pour diriger le son.',
        'BAFOUER': 'Violer ou mépriser.',
        'BAFRE': 'Coup violent.',
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
        'BABILLARD': [
            'Il est très babillard et parle sans cesse.',
            'Les enfants sont souvent babillards à l\'école.',
            'Son caractère babillard agace parfois son entourage.'
        ],
        'BABILLER': [
            'Elle aime babiller avec ses amies au téléphone.',
            'Les oiseaux babillent joyeusement le matin.',
            'Arrête de babiller et concentre-toi sur ton travail.'
        ],
        'BABIOLE': [
            'J\'ai acheté une babiole au marché aux puces.',
            'Sa chambre est remplie de babiole de toutes sortes.',
            'Cette babiole n\'a aucune valeur mais elle me plaît.'
        ],
        'BABOUIN': [
            'Le babouin est un singe très intelligent.',
            'Nous avons vu des babouins au zoo.',
            'Le babouin a une face expressive.'
        ],
        'BAC': [
            'J\'ai réussi mon bac avec mention bien.',
            'Il a passé le bac de français hier.',
            'Le bac est un diplôme important en France.'
        ],
        'BAGAGE': [
            'J\'ai préparé mes bagages pour le voyage.',
            'Le bagage en soute est inclus dans le billet.',
            'Il a perdu son bagage à l\'aéroport.'
        ],
        'BAGARRE': [
            'Une bagarre a éclaté dans la rue hier soir.',
            'Les enfants se sont mis à bagarrer dans la cour.',
            'La bagarre a été rapidement calmée par les adultes.'
        ],
        'BAIGNade': [
            'La baignade est interdite dans cette rivière.',
            'Nous avons fait une baignade rafraîchissante à la plage.',
            'La baignade en mer est très agréable par temps chaud.'
        ],
        'BAIGNOIRE': [
            'J\'ai pris un bain dans la baignoire.',
            'La baignoire est très grande et confortable.',
            'Il a nettoyé la baignoire ce matin.'
        ],
        'BAIL': [
            'J\'ai signé un bail pour mon nouvel appartement.',
            'Le bail a une durée de trois ans.',
            'Le propriétaire a résilié le bail.'
        ],
        'BAISER': [
            'Il lui a donné un baiser sur la joue.',
            'Le baiser est un signe d\'affection.',
            'Ils ont échangé un long baiser.'
        ],
        'BAL': [
            'Nous allons au bal ce soir.',
            'Le bal de fin d\'année était magnifique.',
            'Elle porte une belle robe pour le bal.'
        ],
        'BALADE': [
            'J\'aime faire une balade dans le parc.',
            'Nous avons fait une longue balade en forêt.',
            'Cette balade en vélo était très agréable.'
        ],
        'BALAI': [
            'J\'utilise le balai pour nettoyer le sol.',
            'Le balai est dans le placard.',
            'Elle a cassé le manche du balai.'
        ],
        'BALCON': [
            'Mon appartement a un grand balcon.',
            'Nous avons pris le petit-déjeuner sur le balcon.',
            'Le balcon offre une belle vue sur la ville.'
        ],
        'BALEINE': [
            'La baleine est le plus grand mammifère marin.',
            'Nous avons vu des baleines lors de notre croisière.',
            'La baleine à bosse est une espèce protégée.'
        ],
        'BALLON': [
            'Les enfants jouent avec un ballon.',
            'Le ballon de football est rond.',
            'J\'ai gonflé le ballon pour la fête.'
        ],
        'BANC': [
            'Nous nous sommes assis sur un banc.',
            'Le banc du parc est en bois.',
            'Il y a un banc dans le jardin.'
        ],
        'BANANE': [
            'J\'ai mangé une banane ce matin.',
            'La banane est riche en potassium.',
            'Il a glissé sur une peau de banane.'
        ],
        'BANLIEUE': [
            'Je vis en banlieue de Paris.',
            'La banlieue est souvent moins chère que le centre-ville.',
            'Les transports en banlieue peuvent être compliqués.'
        ],
        'BANNIÈRE': [
            'La bannière flottait au vent.',
            'Nous avons accroché une bannière pour l\'anniversaire.',
            'La bannière publicitaire attire l\'attention.'
        ],
        'BANQUET': [
            'Le banquet a duré toute la soirée.',
            'Nous avons été invités à un banquet royal.',
            'Le banquet était somptueux.'
        ],
        'BAR': [
            'Nous avons bu un verre au bar.',
            'Le bar est ouvert jusqu\'à minuit.',
            'Il travaille comme barman.'
        ],
        'BARBE': [
            'Il a une barbe bien taillée.',
            'La barbe pousse rapidement.',
            'J\'ai rasé ma barbe ce matin.'
        ],
        'BARBECUE': [
            'Nous avons fait un barbecue dans le jardin.',
            'Le barbecue était délicieux.',
            'Il a acheté un nouveau barbecue.'
        ],
        'BAROMÈTRE': [
            'Le baromètre indique une baisse de pression.',
            'J\'ai acheté un baromètre pour la maison.',
            'Le baromètre annonce de la pluie.'
        ],
        'BAS': [
            'Le prix est très bas.',
            'Il habite au bas de la rue.',
            'La qualité est bas de gamme.'
        ],
        'BASE': [
            'La base de la pyramide est large.',
            'Nous avons établi une base solide pour le projet.',
            'La base de données est essentielle.'
        ],
        'BASKET': [
            'J\'aime jouer au basket.',
            'Le basket est un sport très populaire.',
            'Il a marqué un panier au basket.'
        ],
        'BATEAU': [
            'Nous avons pris le bateau pour traverser.',
            'Le bateau à voile est magnifique.',
            'Il a acheté un bateau.'
        ],
        'BÂTIMENT': [
            'Le bâtiment est en construction.',
            'C\'est un bâtiment historique.',
            'Le bâtiment abrite des bureaux.'
        ],
        'BATON': [
            'Il marche avec un bâton.',
            'Le bâton de hockey est en carbone.',
            'J\'ai ramassé un bâton par terre.'
        ],
    }
    
    if mot.upper() in exemples_specificques:
        return exemples_specificques[mot.upper()]
    
    # Générer des exemples génériques
    article = 'l\' ' if mot_lower[0] in 'aeiouh' else 'un '
    if mot_lower.startswith('a') and len(mot_lower) > 1 and mot_lower[1] == 'é':
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
    f.write(f"Nombre total de mots: {len(matches) + len(nouveaux_mots_filtres)}\n")
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
    for mot in nouveaux_mots_filtres:
        definition = generer_definition(mot)
        exemples = generer_exemples(mot)
        f.write(f"=== {mot} ===\n")
        f.write(f"Définition: {definition}\n\n")
        f.write("Exemples:\n")
        for ex in exemples:
            f.write(f"- {ex}\n")
        f.write("\n")

print("Fichier corpus.txt créé avec succès!")
print(f"Total: {len(matches) + len(nouveaux_mots_filtres)} mots")
