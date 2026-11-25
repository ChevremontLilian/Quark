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
# Je vais créer une liste beaucoup plus complète en ajoutant des mots de C à Z

# Mots en C (environ 800)
c_mots = [
    "CABANE", "CABANON", "CABAS", "CABESTAN", "CABIAI", "CABILLOT", "CABINET", 
    "CABLE", "CABLER", "CABLAGE", "CABLÉ", "CABLÉE", "CABLERIE", "CABLÉS",
    "CABLOT", "CABOCHARD", "CABOCHON", "CABOSSE", "CABOSSER", "CABOT",
    "CABOTAGE", "CABOTER", "CABOTIN", "CABOTINAGE", "CABOULOT", "CABRE",
    "CABRER", "CABRI", "CABRIER", "CABRIOLE", "CABRIOLER", "CABRIOLET",
    "CABUS", "CAC", "CACA", "CACAO", "CACAOTIER", "CACAOU", "CACARDER",
    "CACHALOT", "CACHE", "CACHER", "CACHET", "CACHETTER", "CACHETTE",
    "CACHOT", "CACHOTTE", "CACHOTTIER", "CACHOU", "CADAVRE", "CADAVRÉIQUE",
    "CADENAS", "CADENCE", "CADENCER", "CADENCIER", "CADET", "CADETTE",
    "CADI", "CADMIUM", "CADRAN", "CADRE", "CADRER", "CADUC",
    "CADUCEE", "CADUCÉE", "CADUCITÉ", "CAFARD", "CAFARDE", "CAFARDER",
    "CAFÉ", "CAFÉIER", "CAFÉINE", "CAFÉINÉ", "CAFÉINER", "CAFÉTÉRIA",
    "CAFÉTIÈRE", "CAFOUILLAGE", "CAFOUILLER", "CAFOUILLIS", "CAFRE",
    "CAFTER", "CAGE", "CAGEOT", "CAGETTE", "CAGIBI", "CAGNA",
    "CAGNARD", "CAGNE", "CAGNER", "CAGOU", "CAGOULE", "CAGOUS",
    "CAHIER", "CAHIN-CAHA", "CAHOT", "CAHOTANT", "CAHOTER", "CAHOTEUX",
    "CAHUTE", "CAHUTER", "CAILLASSE", "CAILLE", "CAILLEBOTTER",
    "CAILLET", "CAILLETE", "CAILLETER", "CAILLEUX", "CAILLOU",
    "CAILLOUX", "CAILLOUTAGE", "CAILLOUTER", "CAILLOUTEUX", "CAIMAN",
    "CAISSIER", "CAISSIÈRE", "CAISSE", "CAISSES", "CAISSON",
    "CAJOLER", "CAJOLERIE", "CAJOU", "CAJUN", "CAL", "CALAGE",
    "CALAMAR", "CALAMARS", "CALAMINAGE", "CALAMINER", "CALAMISTRER",
    "CALAMITÉ", "CALAMITEUX", "CALANQUE", "CALAO", "CALBRAS",
    "CALC", "CALCAIRE", "CALCEDOINE", "CALCEOLAIRE", "CALCICOLE",
    "CALCIF", "CALCIFICATION", "CALCIFIER", "CALCIN", "CALCINATION",
    "CALCINER", "CALCINOSIS", "CALCIQUE", "CALCIUM", "CALCUL",
    "CALCULABLE", "CALCULATEUR", "CALCULATRICE", "CALCULER", "CALCULETTES",
    "CALDEIRA", "CALE", "CALEBASSE", "CALECHE", "CALECON",
    "CALEDONIEN", "CALEFACTION", "CALEFACTIONNER", "CALENDOS", "CALENDRIER",
    "CALEPIN", "CALEPIAGE", "CALEPIER", "CALER", "CALERIE",
    "CALETTE", "CALEUR", "CALEUSE", "CALFEUTRAGE", "CALFEUTRER",
    "CALIBRAGE", "CALIBRE", "CALIBRER", "CALIBREUR", "CALICHE",
    "CALICOT", "CALICUL", "CALIF", "CALIFAT", "CALIFORNIUM",
    "CALIN", "CALINER", "CALINERIE", "CALINERIES", "CALINOT",
    "CALISAYA", "CALIX", "CALLEUX", "CALLGIRL", "CALLOSITÉ",
    "CALMANT", "CALMANTE", "CALME", "CALMER", "CALMES",
    "CALMIE", "CALOMNIE", "CALOMNIER", "CALOMNIES", "CALOMNIEUX",
    "CALORIE", "CALORIFÈRE", "CALORIFUGE", "CALORIFUGER", "CALORIQUE",
    "CALORISATION", "CALORISER", "CALORISTAT", "CALOT", "CALOTIN",
    "CALOTTE", "CALOTTES", "CALOYER", "CALQUAGE", "CALQUE",
    "CALQUER", "CALQUIN", "CALS", "CALTAVUTURO", "CALUMET",
    "CALVA", "CALVADOS", "CALVAIRE", "CALVATIA", "CALVINISME",
    "CALVINISTE", "CALVITIE", "CALYCE", "CALYPSO", "CAMAÏEU",
    "CAMARADE", "CAMARADERIE", "CAMARDE", "CAMARD", "CAMARDEUR",
    "CAMARGUE", "CAMBALA", "CAMBALER", "CAMBIS", "CAMBOUIS",
    "CAMBRIOLAGE", "CAMBRIOLE", "CAMBRIOLER", "CAMBRIOLEUR", "CAMBRIOLEUSE",
    "CAMBROUSSE", "CAMBROUSSIER", "CAME", "CAMÉ", "CAMELIA",
    "CAMELIDÉ", "CAMELIN", "CAMELLE", "CAMELOT", "CAMELOTE",
    "CAMÉLÉON", "CAMÉRA", "CAMÉRAMAN", "CAMÉRAS", "CAMÉRAVION",
    "CAMÉRISTE", "CAMION", "CAMIONNAGE", "CAMIONNER", "CAMIONNETTE",
    "CAMIONNEUR", "CAMIONNEUSE", "CAMIONS", "CAMISARD", "CAMISE",
    "CAMISOLE", "CAMOMILLE", "CAMP", "CAMPAGNE", "CAMPAGNOL",
    "CAMPAGNOLE", "CAMPAILLER", "CAMPANAIRE", "CAMPANILE", "CAMPANULE",
    "CAMPANULACÉE", "CAMPCHE", "CAMPE", "CAMPÉ", "CAMPEMENT",
    "CAMPER", "CAMPHRE", "CAMPHRIER", "CAMPING", "CAMPING-CAR",
    "CAMPUS", "CANA", "CANACAN", "CANADIA", "CANADIEN",
    "CANADIENNE", "CANAILLE", "CANAL", "CANALAIRE", "CANALISATION",
    "CANALISER", "CANALS", "CANAPE", "CANAPÉ", "CANAPÉS",
    "CANARD", "CANARDE", "CANARDEAU", "CANARI", "CANARIA",
    "CANARIS", "CANAUX", "CANCAN", "CANCANER", "CANCANIER",
    "CANCANIÈRE", "CANDÉLABRE", "CANDÉRISATION", "CANDÉRISER", "CANDI",
    "CANDID", "CANDIDAT", "CANDIDATE", "CANDIDATURE", "CANDIDE",
    "CANDIDEMENT", "CANDIR", "CANDIS", "CANDISSAGE", "CANDOS",
    "CANE", "CANEBAS", "CANEBIÈRE", "CANECAN", "CANELLE",
    "CANELON", "CANELONS", "CANER", "CANETON", "CANETTE",
    "CANEZOU", "CANICHE", "CANICULAIRE", "CANICULE", "CANIF",
    "CANIN", "CANINE", "CANINES", "CANISSON", "CANIVEAU",
    "CANIVET", "CANNABINACÉE", "CANNABINOL", "CANNABIS", "CANNAGE",
    "CANNAIE", "CANNE", "CANNÉ", "CANNELÉ", "CANNELER",
    "CANNELIER", "CANNELURE", "CANNE À PÊCHE", "CANNE À SUCRE",
    "CANNEAU", "CANNELLE", "CANNER", "CANNETTE", "CANNETILLE",
    "CANNEUR", "CANNEUSE", "CANOË", "CANOE", "CANOÉISTE",
    "CANON", "CANONIQUE", "CANONISATION", "CANONISER", "CANONNADE",
    "CANONNE", "CANONNER", "CANONNIÈRE", "CANOT", "CANOTAGE",
    "CANOTER", "CANOTIER", "CANOTIÈRE", "CANOUE", "CANS",
    "CANTALE", "CANTALOU", "CANTALOUP", "CANTARIDE", "CANTATE",
    "CANTATRICE", "CANTE", "CANTÉ", "CANTER", "CANTHARIDE",
    "CANTIEN", "CANTILENE", "CANTILÈNE", "CANTINA", "CANTINE",
    "CANTINIÈRE", "CANTON", "CANTONADE", "CANTONAL", "CANTONALE",
    "CANTONALES", "CANTONNER", "CANTONNIÈRE", "CANULAIRE", "CANULAR",
    "CANULARD", "CANULE", "CANULER", "CANUT", "CANUTE",
    "CANYON", "CANYONING", "CANZONI", "CAOUA", "CAOUANE",
    "CAOUM", "CAOUTCHOU", "CAOUTCHOUTAGE", "CAOUTCHOUTER", "CAOUTCHOUTEUX",
    "CAP", "CAPABLE", "CAPABILITÉ", "CAPACITÉ", "CAPACITIF",
    "CAPARACON", "CAPARACONNER", "CAPARAÇON", "CAPE", "CAPÉ",
    "CAPELET", "CAPELLE", "CAPER", "CAPES", "CAPET",
    "CAPETIEN", "CAPETIENNE", "CAPHARNAÜM", "CAPILLAIRE", "CAPILLARITÉ",
    "CAPILLOTADE", "CAPITAL", "CAPITALE", "CAPITALISATION", "CAPITALISER",
    "CAPITALISME", "CAPITALISTE", "CAPITALISTIQUE", "CAPITAN", "CAPITANERIE",
    "CAPITANNE", "CAPITATION", "CAPITE", "CAPITEL", "CAPITELLE",
    "CAPITON", "CAPITONNAGE", "CAPITONNER", "CAPITOUL", "CAPITOULAT",
    "CAPITULARD", "CAPITULARDE", "CAPITULATION", "CAPITULER", "CAPOEIRA",
    "CAPON", "CAPONNER", "CAPORAL", "CAPORALISME", "CAPOT",
    "CAPOTAGE", "CAPOTER", "CAPOTEUR", "CAPOTINE", "CAPRICE",
    "CAPRICIEUX", "CAPRICIEUSE", "CAPRICORNE", "CAPRIER", "CAPRIN",
    "CAPRINE", "CAPRINS", "CAPS", "CAPSULAGE", "CAPSULE",
    "CAPSULER", "CAPSULEUR", "CAPTAGE", "CAPTE", "CAPTER",
    "CAPTEUR", "CAPTIF", "CAPTIVE", "CAPTIVANT", "CAPTIVANTE",
    "CAPTIVER", "CAPTIVITÉ", "CAPTURE", "CAPTURER", "CAPUCHON",
    "CAPUCHONNER", "CAPUCIN", "CAPUCINE", "CAPUE", "CAPULA",
    "CAQUET", "CAQUETER", "CAQUETTE", "CAQUETTER", "CAR",
    "CARABASSE", "CARABIN", "CARABINE", "CARABINER", "CARABINIER",
    "CARACAL", "CARACOL", "CARACOLER", "CARACOLE", "CARACOLEE",
]

# Mots en D (environ 500)
d_mots = [
    "DAB", "DABE", "DACQUOIS", "DACQUOISE", "DACTYLO",
    "DACTYLOGIE", "DACTYLOGRAPHE", "DACTYLOGRAPHIER", "DACTYLOGRAPHIE", "DACTYLOGRAPHIQUE",
    "DADA", "DADAÏSME", "DADAÏSTE", "DAGUE", "DAGUER",
    "DAGUERRÉOTYPE", "DAGUET", "DAHLIA", "DAHOMÉEN", "DAHOMÉENNE",
    "DAÏKON", "DAIM", "DAIMIO", "DAINE", "DAINS",
    "DAIS", "DAKAR", "DAKOTA", "DAL", "DALAÏ-LAMA",
    "DALHIA", "DALLAGE", "DALLER", "DALLE", "DALLES",
    "DALMATE", "DALMATIEN", "DALMATIENNE", "DALOT", "DALTON",
    "DALTONIEN", "DALTONIENNE", "DALTONISME", "DAM", "DAMA",
    "DAMAN", "DAMAS", "DAMASQUINAGE", "DAMASQUINER", "DAMASQUINE",
    "DAMASQUINURE", "DAME", "DAME-JEANNE", "DAMES", "DAMIER",
    "DAMIERS", "DAMNANT", "DAMNATION", "DAMNER", "DAMNÉ",
    "DAMNÉE", "DAMOISEAU", "DAMOISELLE", "DAN", "DANAÏDE",
    "DANDIN", "DANDINER", "DANDY", "DANDYSME", "DANE",
    "DANES", "DANGER", "DANGEREUX", "DANGEREUSE", "DANGEREUSEMENT",
    "DANOIS", "DANOISE", "DANS", "DANSE", "DANSANT",
    "DANSANTE", "DANSER", "DANSEUR", "DANSEUSE", "DANSEUSES",
    "DANTE", "DANTESQUE", "DANUBE", "DANUBIEN", "DANUBIENNE",
    "DAO", "DAUBE", "DAUBER", "DAUBEUR", "DAUBEUSE",
    "DAVANTAGE", "DAVID", "DAVIS", "DAX", "DAYAK",
    "DAYAKS", "DAZIBAO", "DE", "DÉ", "DÉBACLE",
    "DÉBACLER", "DÉBAGOULER", "DÉBALLAGE", "DÉBALLER", "DÉBALLEUR",
    "DÉBANDER", "DÉBARBOUILLER", "DÉBARCADÈRE", "DÉBARDEUR", "DÉBARDER",
    "DÉBARQUER", "DÉBARRAS", "DÉBARRASSER", "DÉBAT", "DÉBATS",
    "DÉBATTRE", "DÉBATU", "DÉBAUCHE", "DÉBAUCHER", "DÉBAUCHÉ",
    "DÉBAUCHÉE", "DÉBAUCHERIE", "DÉBILE", "DÉBILITANT", "DÉBILITANTE",
    "DÉBILITÉ", "DÉBINER", "DÉBIT", "DÉBITER", "DÉBITEUR",
    "DÉBITEUSE", "DÉBLATÉRATION", "DÉBLATÉRER", "DÉBLAYAGE", "DÉBLAYER",
    "DÉBLOQUER", "DÉBOBINER", "DÉBOGAGE", "DÉBOGUER", "DÉBOIRE",
    "DÉBOIRES", "DÉBOÎTER", "DÉBONDER", "DÉBORDANT", "DÉBORDANTE",
    "DÉBORDER", "DÉBORDEMENT", "DÉBOSSELER", "DÉBOUCHER", "DÉBOUCHÉ",
    "DÉBOUCHÉE", "DÉBOUCHES", "DÉBOUCHERIE", "DÉBOUCHOIR", "DÉBOUCLER",
    "DÉBOULONNER", "DÉBOURBER", "DÉBOURRER", "DÉBOURS", "DÉBOURSER",
    "DÉBOUT", "DÉBOUTER", "DÉBOUTONNER", "DÉBRANCHER", "DÉBRAYAGE",
    "DÉBRAYER", "DÉBREDAILLER", "DÉBRIEFING", "DÉBRIS", "DÉBROUILLARD",
    "DÉBROUILLARDE", "DÉBROUILLER", "DÉBROUSSAILLAGE", "DÉBROUSSAILLER", "DÉBROUSSAILLEUSE",
    "DÉBRUMER", "DÉBUT", "DÉBUTANT", "DÉBUTANTE", "DÉBUTER",
    "DÉBUTS", "DÉCACHETER", "DÉCADENCE", "DÉCADENT", "DÉCADENTE",
    "DÉCADRER", "DÉCAFÉINÉ", "DÉCAFÉINER", "DÉCAGER", "DÉCALAGE",
    "DÉCALAMINER", "DÉCALCARISER", "DÉCALCOMANIE", "DÉCALER", "DÉCALITRE",
    "DÉCALOGUE", "DÉCALOTTER", "DÉCALQUER", "DÉCAMER", "DÉCAMÉTER",
    "DÉCAMPEMENT", "DÉCAMPER", "DÉCANAILLER", "DÉCANAT", "DÉCAPANT",
    "DÉCAPER", "DÉCAPITALISER", "DÉCAPITER", "DÉCAPODE", "DÉCAPOTABLE",
    "DÉCAPSULER", "DÉCARBONATER", "DÉCARBONATATION", "DÉCARBONER", "DÉCARBONISATION",
    "DÉCARBONISER", "DÉCARBURANT", "DÉCARBURATION", "DÉCARBURER", "DÉCARDER",
    "DÉCARELER", "DÉCARNAGE", "DÉCARNER", "DÉCASER", "DÉCASSER",
    "DÉCATIR", "DÉCATISSAGE", "DÉCATISSER", "DÉCAUSER", "DÉCAVÉ",
    "DÉCELER", "DÉCELLEMENT", "DÉCELER", "DÉCEMBRE", "DÉCENIE",
    "DÉCENNALE", "DÉCENNIES", "DÉCENNIAL", "DÉCENT", "DÉCENTE",
    "DÉCENTEMENT", "DÉCENTRALISATION", "DÉCENTRALISER", "DÉCENTRALISÉ", "DÉCENTRALISÉE",
    "DÉCENTREMENT", "DÉCENTRER", "DÉCEPTION", "DÉCEVOIR", "DÉCHAINEMENT",
    "DÉCHAINER", "DÉCHANT", "DÉCHANTER", "DÉCHAPER", "DÉCHARGE",
    "DÉCHARGER", "DÉCHARGEUR", "DÉCHARNE", "DÉCHARNER", "DÉCHAUMAGE",
    "DÉCHAUMER", "DÉCHAÎNER", "DÉCHET", "DÉCHETS", "DÉCHEU",
    "DÉCHIFFONNER", "DÉCHIFFRABLE", "DÉCHIFFRAGE", "DÉCHIFFREMENT", "DÉCHIFFRER",
    "DÉCHIFFREUR", "DÉCHIFFREUSE", "DÉCHIRANT", "DÉCHIRANTE", "DÉCHIREMENT",
    "DÉCHIRER", "DÉCHIREUR", "DÉCHIREUSE", "DÉCHIRURE", "DÉCHOIR",
    "DÉCHOUQUER", "DÉCHU", "DÉCHUE", "DÉCIDABILITÉ", "DÉCIDABLE",
    "DÉCIDÉ", "DÉCIDÉE", "DÉCIDÉMENT", "DÉCIDER", "DÉCIDEUR",
    "DÉCIDEUSE", "DÉCIDU", "DÉCIDUE", "DÉCIEUR", "DÉCIGRAMME",
    "DÉCILITRE", "DÉCIMAL", "DÉCIMALE", "DÉCIMALISATION", "DÉCIMALISER",
    "DÉCIMATION", "DÉCIMER", "DÉCIMÈTRE", "DÉCINTRESSER", "DÉCIRER",
    "DÉCISIF", "DÉCISIVE", "DÉCISIVEMENT", "DÉCISIVE", "DÉCIVILISER",
    "DÉCLAMATION", "DÉCLAMATOIRE", "DÉCLAMER", "DÉCLARATION", "DÉCLARATIF",
    "DÉCLARATIVE", "DÉCLARATIVEMENT", "DÉCLARER", "DÉCLASSEMENT", "DÉCLASSER",
    "DÉCLENCHEMENT", "DÉCLENCHER", "DÉCLIC", "DÉCLIN", "DÉCLINAISON",
    "DÉCLINANT", "DÉCLINANTE", "DÉCLINER", "DÉCLIVE", "DÉCLIVITÉ",
    "DÉCOCHER", "DÉCODAGE", "DÉCODER", "DÉCODEUR", "DÉCODEUSE",
    "DÉCOIFFER", "DÉCOINCER", "DÉCOLLAGE", "DÉCOLLER", "DÉCOLLETE",
    "DÉCOLLETÉ", "DÉCOLLETÉE", "DÉCOLONISATION", "DÉCOLONISER", "DÉCOLORANT",
    "DÉCOLORATION", "DÉCOLORER", "DÉCOLORISATION", "DÉCOLORISER", "DÉCOMBRE",
    "DÉCOMBRER", "DÉCOMMISSIONNER", "DÉCOMPENSATION", "DÉCOMPENSER", "DÉCOMPOSABLE",
    "DÉCOMPOSANT", "DÉCOMPOSANTE", "DÉCOMPOSER", "DÉCOMPOSITION", "DÉCOMPTE",
    "DÉCOMPTER", "DÉCONCERTANT", "DÉCONCERTANTE", "DÉCONCERTER", "DÉCONCERTION",
    "DÉCONCERTONNER", "DÉCONFIT", "DÉCONFITE", "DÉCONFITURE", "DÉCONGELATION",
    "DÉCONGELER", "DÉCONGESTIONNANT", "DÉCONGESTIONNER", "DÉCONNEXION", "DÉCONNECTER",
    "DÉCONNEXION", "DÉCONSIDÉRATION", "DÉCONSIDÉRER", "DÉCONTAMINATION", "DÉCONTAMINER",
    "DÉCONTENANCER", "DÉCONTENANCÉ", "DÉCONTENANCÉE", "DÉCONTRACTION", "DÉCONTRACTER",
    "DÉCONVERSER", "DÉCONVERTIR", "DÉCOR", "DÉCORATIF", "DÉCORATIVE",
    "DÉCORATION", "DÉCORATRICE", "DÉCORCEUR", "DÉCORCER", "DÉCORER",
    "DÉCORNE", "DÉCORNER", "DÉCORUM", "DÉCOUCHER", "DÉCOUENNER",
    "DÉCOULER", "DÉCOUPAGE", "DÉCOUPER", "DÉCOUPEUR", "DÉCOUPEUSE",
    "DÉCOUPLE", "DÉCOUPLER", "DÉCOURAGER", "DÉCOURAGEMENT", "DÉCOURAGÉ",
]

# Combiner toutes les listes
all_mots = c_mots + d_mots

# Supprimer les doublons
unique_mots = list(set(all_mots))

# Filtrer les mots déjà existants
mots_existants_upper = [m[0].upper() for m in matches]

# Lire les mots déjà dans corpus.txt pour éviter les doublons
try:
    with open('corpus.txt', 'r', encoding='utf-8') as f:
        corpus_content = f.read()
    corpus_pattern = r'=== (\w+[\s\w\-]*) ==='
    corpus_matches = re.findall(corpus_pattern, corpus_content)
    mots_existants_upper += [m.upper() for m in corpus_matches]
except:
    pass

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
        'CABANE': 'Petite construction en bois ou en pierre servant d\'abri.',
        'CABANON': 'Petite cabane, souvent dans un jardin.',
        'CABLE': 'Fil métallique ou électrique.',
        'CABLER': 'Équiper de câbles.',
        'CABLAGE': 'Ensemble des câbles ou action de câbler.',
        'CABOCHARD': 'Qui est têtu, entêté.',
        'CABOCHON': 'Pierre taillée en forme de dôme.',
        'CABRI': 'Jeune chèvre.',
        'CABRIOLE': 'Saut ou mouvement acrobatique.',
        'CABRIOLET': 'Voiture décapotable.',
        'CACAO': 'Poudre obtenue à partir des fèves de cacao.',
        'CACAOTIER': 'Arbre produisant le cacao.',
        'CACHE': 'Endroit secret ou action de cacher.',
        'CACHER': 'Mettre à l\'abri des regards.',
        'CACHET': 'Sceau ou cachet.',
        'CADAVRE': 'Corps d\'une personne ou d\'un animal mort.',
        'CADENAS': 'Serrure portable.',
        'CADENCE': 'Rythme ou vitesse.',
        'CADRAN': 'Partie d\'une horloge ou d\'une montre.',
        'CADRE': 'Structure ou personne encadrant.',
        'CAFARD': 'Insecte ou sentiment de déprime.',
        'CAFÉ': 'Boisson stimulante ou établissement où on la sert.',
        'CAFÉIER': 'Arbre produisant le café.',
        'CAFÉINE': 'Substance stimulante présente dans le café.',
        'CAGE': 'Enclos pour animaux ou structure métallique.',
        'CAGEOT': 'Caisse en bois pour transporter des fruits.',
        'CAHIER': 'Recueil de feuilles pour écrire.',
        'CAHOT': 'Mouvement brusque ou irrégulier.',
        'CAILLASSE': 'Pierre cassée ou chemin de pierres.',
        'CAILLE': 'Oiseau gallinacé.',
        'CAILLOU': 'Petite pierre.',
        'CAILLOUX': 'Petites pierres.',
        'CAIMAN': 'Reptile ressemblant au crocodile.',
        'CAISSE': 'Récipient ou boîte.',
        'CAISSIER': 'Personne qui gère une caisse.',
        'CAJOLER': 'Flatter ou caresser avec affection.',
        'CAJOU': 'Noix comestible.',
        'CALANQUE': 'Vallée étroite et escarpée.',
        'CALCUL': 'Opération mathématique.',
        'CALCULATEUR': 'Appareil ou personne qui calcule.',
        'CALCULER': 'Effectuer un calcul.',
        'CALE': 'Outil pour mesurer ou tracer.',
        'CALEBASSE': 'Fruit ou récipient fait avec sa coque.',
        'CALECHE': 'Voiture à chevaux.',
        'CALER': 'Placer solidement ou bloquer.',
        'CALENDRIER': 'Tableau indiquant les jours, mois et années.',
        'CALIBRE': 'Diamètre ou taille.',
        'CALIBRER': 'Régler selon un calibre.',
        'CALME': 'Absence d\'agitation.',
        'CALMER': 'Rendre calme.',
        'CALOMNIE': 'Accusation mensongère.',
        'CALOMNIER': 'Diffamer quelqu\'un.',
        'CALORIE': 'Unité de mesure de l\'énergie.',
        'CALORIFÈRE': 'Appareil de chauffage.',
        'CALVITIE': 'Perte des cheveux.',
        'CAMARADE': 'Ami ou collègue.',
        'CAMARADERIE': 'Amitié entre camarades.',
        'CAMBRIOLAGE': 'Vol avec effraction.',
        'CAMBRIOLE': 'Vol avec effraction.',
        'CAMBRIOLER': 'Commettre un cambriolage.',
        'CAMBROUSSE': 'Terrain accidenté.',
        'CAME': 'Bosse sur le dos de certains animaux.',
        'CAMÉLÉON': 'Reptile capable de changer de couleur.',
        'CAMÉRA': 'Appareil pour filmer.',
        'CAMÉRAMAN': 'Personne qui manipule une caméra.',
        'CAMION': 'Véhicule de transport de marchandises.',
        'CAMIONNETTE': 'Petit camion.',
        'CAMIONNEUR': 'Conducteur de camion.',
        'CAMP': 'Lieu de camping ou camp militaire.',
        'CAMPAGNE': 'Région rurale ou période de promotion.',
        'CAMPAGNOL': 'Petit rongeur.',
        'CAMPING': 'Terrain aménagé pour camper.',
        'CAMPUS': 'Ensemble des bâtiments d\'une université.',
        'CANARD': 'Oiseau palmipède ou canular.',
        'CANARI': 'Petit oiseau chanteur.',
        'CANAL': 'Voie d\'eau artificielle.',
        'CANALISATION': 'Réseau de canaux.',
        'CANALISER': 'Diriger dans un canal.',
        'CANAPÉ': 'Siège confortable.',
        'CANCAN': 'Bruit ou commérage.',
        'CANCANER': 'Faire du bruit ou des commérages.',
        'CANDIDAT': 'Personne qui se présente à une élection.',
        'CANDIDATURE': 'Action de se présenter à une élection.',
        'CANDIDE': 'Naïf ou sincère.',
        'CANE': 'Bâton ou roseau.',
        'CANETON': 'Jeune canard.',
        'CANICHE': 'Race de chien.',
        'CANICULAIRE': 'Relatif à la canicule.',
        'CANICULE': 'Période de forte chaleur.',
        'CANIF': 'Petit couteau.',
        'CANIN': 'Relatif au chien.',
        'CANNE': 'Bâton ou tube.',
        'CANOË': 'Embarcation légère.',
        'CANON': 'Arme à feu ou tube.',
        'CANONIQUE': 'Conforme aux règles.',
        'CANOT': 'Petite embarcation.',
        'CANOTAGE': 'Action de canoter.',
        'CANOTIER': 'Personne qui canote.',
        'CANTATE': 'Composition musicale.',
        'CANTATRICE': 'Chanteuse.',
        'CANTINE': 'Lieu où l\'on mange collectivement.',
        'CANTON': 'Division administrative.',
        'CANTONNER': 'Limiter à un espace.',
        'CAP': 'Extrémité ou couverture.',
        'CAPABLE': 'Qui a la capacité de faire quelque chose.',
        'CAPACITÉ': 'Aptitude ou volume.',
        'CAPITAL': 'Ville principale ou argent investi.',
        'CAPITALE': 'Ville principale.',
        'CAPITALISME': 'Système économique basé sur le capital.',
        'CAPITALISTE': 'Partisan du capitalisme.',
        'CAPITULER': 'Se rendre, abandonner.',
        'CAPON': 'Coq castré.',
        'CAPORAL': 'Grade militaire.',
        'CAPOTE': 'Toit souple de voiture.',
        'CAPRICE': 'Désir soudain et passager.',
        'CAPRICIEUX': 'Qui a des caprices.',
        'CAPSULE': 'Petit récipient ou enveloppe.',
        'CAPTAGE': 'Action de capter.',
        'CAPTER': 'Attirer ou enregistrer.',
        'CAPTEUR': 'Appareil qui capte.',
        'CAPTIF': 'Qui est prisonnier.',
        'CAPTIVER': 'Attirer l\'attention.',
        'CAPTURE': 'Action de capturer.',
        'CAPTURER': 'Prendre prisonnier ou enregistrer.',
        'CAR': 'Voiture en anglais.',
        'CARABASSE': 'Calebasse.',
        'CARABIN': 'Étudiant en médecine.',
        'CARABINE': 'Arme à feu.',
        'CARABINIER': 'Militaire ou policier.',
        'CARACOL': 'Figure de manège.',
        'CARACOLER': 'Faire des caracoles.',
        'CARACTÈRE': 'Ensemble des traits de personnalité.',
        'CARACTÉRISER': 'Définir les caractéristiques.',
        'CARAFE': 'Récipient pour liquides.',
        'CARAPACE': 'Coquille protectrice.',
        'CARAVANE': 'Véhicule aménagé pour voyager.',
        'CARAVANSÉRAIL': 'Lieu de repos pour caravanes.',
        'CARBONATE': 'Sel de l\'acide carbonique.',
        'CARBONE': 'Élément chimique.',
        'CARBURANT': 'Substance permettant la combustion.',
        'CARCASSE': 'Structure ou reste d\'un animal.',
        'CARDAN': 'Mécanisme de transmission.',
        'CARDE': 'Outil pour carder la laine.',
        'CARDIAQUE': 'Relatif au cœur.',
        'CARDINAL': 'Dignitaire de l\'Église ou nombre cardinal.',
        'CARDON': 'Plante comestible.',
        'CARE': 'Manque ou souci.',
        'CARÉ': 'Qui a une forme carrée.',
        'CARÉNAGE': 'Lieu où l\'on répare les navires.',
        'CARÉNER': 'Nettoyer la coque d\'un navire.',
        'CARESSANT': 'Qui caresse.',
        'CARESSE': 'Action de caresser.',
        'CARESSER': 'Passer la main doucement.',
        'CARFER': 'Nettoyer avec une carfe.',
        'CARFOUR': 'Croisement de routes.',
        'CARGaison': 'Chargement d\'un navire.',
        'CARGO': 'Navire de transport.',
        'CARICATURE': 'Dessin humoristique.',
        'CARICATURER': 'Représenter de manière exagérée.',
        'CARIE': 'Maladie des dents.',
        'CARILLON': 'Ensemble de cloches.',
        'CARILLONNER': 'Faire sonner un carillon.',
        'CARIOCA': 'Danse brésilienne.',
        'CARME': 'Religieux carme.',
        'CARMEL': 'Ordre religieux.',
        'CARMIN': 'Couleur rouge.',
        'CARNAGE': 'Massacre.',
        'CARNASSIER': 'Qui se nourrit de viande.',
        'CARNAVAL': 'Fête avec défilés et déguisements.',
        'CARNE': 'Viande.',
        'CARNET': 'Petit livre pour noter.',
        'CARONCULE': 'Excroissance charnue.',
        'CAROTTE': 'Légume racine orange.',
        'CARPE': 'Poisson d\'eau douce.',
        'CARRÉ': 'Forme géométrique.',
        'CARREAU': 'Pièce de carrelage ou de vitrail.',
        'CARREFOUR': 'Intersection de routes.',
        'CARRELAGE': 'Revêtement de sol.',
        'CARRELER': 'Poser du carrelage.',
        'CARRIÈRE': 'Lieu d\'extraction ou parcours professionnel.',
        'CARRIER': 'Ouvrier des carrières.',
        'CARROI': 'Motif en forme de losange.',
        'CARROSSE': 'Voiture hippomobile.',
        'CARROSSER': 'Équiper d\'une carrosserie.',
        'CARROSSERIE': 'Structure extérieure d\'un véhicule.',
        'CARROUSSEL': 'Manège.',
        'CARTE': 'Représentation géographique ou jeu.',
        'CARTÉSIEN': 'Relatif à Descartes.',
        'CARTILAGE': 'Tissu conjonctif.',
        'CARTON': 'Matériau rigide.',
        'CARTONNAGE': 'Art de travailler le carton.',
        'CARTONNER': 'Fabriquer en carton.',
        'CARTON-PIERRE': 'Matériau de construction.',
        'CARTOUCHE': 'Boîte ou charge explosive.',
        'CAS': 'Situation ou événement.',
        'CASA': 'Maison en espagnol.',
        'CASANIER': 'Qui aime rester chez soi.',
        'CASATEUR': 'Qui aime séduire.',
        'CASCADANT': 'Qui tombe en cascade.',
        'CASCADE': 'Chute d\'eau.',
        'CASCADEUR': 'Personne qui exécute des cascades.',
        'CASE': 'Compartiment ou logement.',
        'CASEIN': 'Protéine du lait.',
        'CASEMATE': 'Pièce voûtée.',
        'CASER': 'Placer ou loger.',
        'CASERNE': 'Bâtiment militaire.',
        'CASERNEMENT': 'Action de caserner.',
        'CASIER': 'Meuble de rangement.',
        'CASINO': 'Établissement de jeux.',
        'CASQUE': 'Protection pour la tête.',
        'CASQUETTE': 'Coiffure.',
        'CASSABLE': 'Qui peut se casser.',
        'CASSANT': 'Qui se casse facilement.',
        'CASSATION': 'Annulation.',
        'CASSER': 'Rompre ou briser.',
        'CASSEROLE': 'Récipient de cuisine.',
        'CASSETTE': 'Boîtier pour bande magnétique.',
        'CASSIS': 'Fruit ou liqueur.',
        'CASSONADE': 'Sucre non raffiné.',
        'CASTAGNETTES': 'Instrument de musique.',
        'CASTE': 'Système social hiérarchisé.',
        'CASTING': 'Sélection de comédiens.',
        'CASTRAT': 'Chanteur castré.',
        'CASTRATION': 'Ablation des organes reproducteurs.',
        'CASTRER': 'Pratiquer la castration.',
        'CASUAL': 'Décontracté.',
        'CASUEL': 'Occasionnel.',
        'CATACLYSME': 'Événement violent et destructeur.',
        'CATACOMBE': 'Galerie souterraine.',
        'CATALAN': 'Relatif à la Catalogne.',
        'CATALOGUE': 'Liste organisée.',
        'CATALOGUER': 'Classer dans un catalogue.',
        'CATALYSE': 'Accélération d\'une réaction chimique.',
        'CATALYSEUR': 'Substance qui catalyse.',
        'CATALYTIQUE': 'Relatif à la catalyse.',
        'CATAMARAN': 'Bateau à deux coques.',
        'CATAPLASME': 'Préparation médicinale.',
        'CATAPULTE': 'Machine de guerre ancienne.',
        'CATARACTE': 'Opacification du cristallin.',
        'CATARRHAL': 'Relatif au catarrhe.',
        'CATARRHE': 'Inflammation des muqueuses.',
        'CATAS': 'Désastre.',
        'CATASTROPHE': 'Événement tragique.',
        'CATASTROPHIQUE': 'Qui cause une catastrophe.',
        'CATCH': 'Lutte spectaculaire.',
        'CATCHEUR': 'Pratiquant du catch.',
        'CATÉCHÈSE': 'Enseignement religieux.',
        'CATÉCHISME': 'Livre d\'enseignement religieux.',
        'CATÉCHUMÈNE': 'Personne en cours d\'initiation religieuse.',
        'CATÉGORIE': 'Classe ou groupe.',
        'CATÉGORIQUE': 'Absolu, sans réserve.',
        'CATÉGORISER': 'Classer par catégories.',
        'CATENE': 'Chaîne.',
        'CATGUT': 'Fil chirurgical.',
        'CATHARSE': 'Purification émotionnelle.',
        'CATHARTIQUE': 'Qui provoque la catharsis.',
        'CATHÉDRAL': 'Relatif à une cathédrale.',
        'CATHÉDRALE': 'Église principale d\'un diocèse.',
        'CATHÉDRATIQUE': 'Relatif à une chaire épiscopale.',
        'CATHÉTÈRE': 'Tube médical.',
        'CATHODE': 'Électrode négative.',
        'CATHOLICISME': 'Religion catholique.',
        'CATHOLIQUE': 'Relatif au catholicisme.',
        'CATION': 'Ion positif.',
        'CATIMINI': 'En cachette.',
        'CATIN': 'Femme de mauvaise vie.',
        'CAUCHEMAR': 'Rêve effrayant.',
        'CAUCHEMARDER': 'Faire des cauchemars.',
        'CAUCHOIS': 'Relatif au Cauchois.',
        'CAUDAL': 'Relatif à la queue.',
        'CAUDILLISME': 'Système politique.',
        'CAULDRON': 'Chaudron.',
        'CAUSALITÉ': 'Relation de cause à effet.',
        'CAUSANT': 'Qui cause.',
        'CAUSE': 'Raison ou motif.',
        'CAUSER': 'Provoquer ou discuter.',
        'CAUSERIE': 'Conversation.',
        'CAUSEUR': 'Qui aime causer.',
        'CAUSEUSE': 'Qui aime causer.',
        'CAUSTICITÉ': 'Qualité de ce qui est caustique.',
        'CAUSTIQUE': 'Qui brûle ou corrode.',
        'CAUTÉRISATION': 'Action de cautériser.',
        'CAUTÉRISER': 'Brûler pour désinfecter.',
        'CAUTION': 'Somme versée en garantie.',
        'CAUTIONNEMENT': 'Action de cautionner.',
        'CAUTIONNER': 'Garantir.',
        'CAVALCADER': 'Faire une cavalcade.',
        'CAVALER': 'Monter à cheval.',
        'CAVALERIE': 'Troupes à cheval.',
        'CAVALIÈRE': 'Femme qui monte à cheval.',
        'CAVALIER': 'Homme qui monte à cheval.',
        'CAVE': 'Lieu souterrain.',
        'CAVEAU': 'Pièce voûtée.',
        'CAVER': 'Creuser.',
        'CAVERNE': 'Grotte.',
        'CAVERNEUX': 'Plein de cavernes.',
        'CAVETTE': 'Petite cave.',
        'CAVIAR': 'Œufs de poisson salés.',
        'CAVITÉ': 'Trou ou creux.',
        'CÉANTHE': 'Fleur.',
        'CÉCIDIE': 'Tumeur végétale.',
        'CÉCITÉ': 'Cécité.',
        'DAB': 'Compétence ou talent.',
        'DACQUOIS': 'Relatif à Dacquois.',
        'DACTYLO': 'Dactylographe.',
        'DACTYLOGIE': 'Langage par signes.',
        'DACTYLOGRAPHE': 'Personne qui dactylographie.',
        'DACTYLOGRAPHIE': 'Action de dactylographier.',
        'DADA': 'Cheval ou mouvement artistique.',
        'DADAÏSME': 'Mouvement artistique.',
        'DADAÏSTE': 'Adepte du dadaïsme.',
        'DAGUE': 'Arme blanche.',
        'DAGUER': 'Orner de dagues.',
        'DAGUERRÉOTYPE': 'Procédé photographique.',
        'DAGUET': 'Jeune cerf.',
        'DAHLIA': 'Fleur ornementale.',
        'DAHOMÉEN': 'Relatif au Dahomey.',
        'DAÏKON': 'Radis japonais.',
        'DAIM': 'Animal ou cuir.',
        'DAIMIO': 'Seigneur féodal japonais.',
        'DAINE': 'Peau de daim.',
        'DAIS': 'Estrade ou plateforme.',
        'DAKAR': 'Capitale du Sénégal.',
        'DAKOTA': 'Tribu amérindienne.',
        'DAL': 'Lentille en hindi.',
        'DALAÏ-LAMA': 'Chef spirituel tibétain.',
        'DALLAGE': 'Revêtement de dalles.',
        'DALLER': 'Poser des dalles.',
        'DALLE': 'Pierre plate.',
        'DALMATE': 'Race de chien.',
        'DALMATIEN': 'Relatif à la Dalmatie.',
        'DALOT': 'Petit canal.',
        'DALTON': 'Physicien.',
        'DALTONIEN': 'Atteint de daltonisme.',
        'DALTONISME': 'Trouble de la vision des couleurs.',
        'DAM': 'Barrage.',
        'DAMA': 'Jeu de société.',
        'DAMAN': 'Mammifère rongeur.',
        'DAMAS': 'Tissu ou ville.',
        'DAMASQUINAGE': 'Art de damasquiner.',
        'DAMASQUINER': 'Orner de motifs.',
        'DAME': 'Femme noble ou jeu.',
        'DAME-JEANNE': 'Bouteille en verre.',
        'DAMIER': 'Jeu de dames.',
        'DAMNANT': 'Qui condamne.',
        'DAMNATION': 'Condamnation.',
        'DAMNER': 'Condamner.',
        'DAMOISEAU': 'Jeune noble.',
        'DAMOISELLE': 'Jeune fille noble.',
        'DAN': 'Unité monétaire.',
        'DANAÏDE': 'Personnage mythologique.',
        'DANDIN': 'Qui se balance.',
        'DANDINER': 'Se balancer.',
        'DANDY': 'Homme élégant.',
        'DANDYSME': 'Attitude de dandy.',
        'DANE': 'Habitant du Danemark.',
        'DANES': 'Habitants du Danemark.',
        'DANGER': 'Risque ou péril.',
        'DANGEREUX': 'Qui présente un danger.',
        'DANOIS': 'Relatif au Danemark.',
        'DANOISE': 'Relatif au Danemark.',
        'DANS': 'Préposition.',
        'DANSE': 'Art de danser.',
        'DANSANT': 'Qui danse.',
        'DANSANTE': 'Qui danse.',
        'DANSER': 'Exécuter une danse.',
        'DANSEUR': 'Homme qui danse.',
        'DANSEUSE': 'Femme qui danse.',
        'DANUBE': 'Fleuve européen.',
        'DANUBIEN': 'Relatif au Danube.',
        'DAO': 'Arme blanche.',
        'DAUBE': 'Morceau de viande.',
        'DAUBER': 'Recouvrir de plâtre.',
        'DAUBEUR': 'Ouvrier qui daube.',
        'DAVID': 'Prénom.',
        'DAVIS': 'Nom de famille.',
        'DAX': 'Ville française.',
        'DAYAK': 'Peuple de Bornéo.',
        'DAYAKS': 'Peuples de Bornéo.',
        'DAZIBAO': 'Journal mural chinois.',
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
        'CABANE': [
            'Nous avons passé la nuit dans une cabane en bois.',
            'La cabane du jardin est très confortable.',
            'Les enfants aiment jouer dans la cabane.'
        ],
        'CABLE': [
            'Le câble électrique est endommagé.',
            'J\'ai acheté un nouveau câble pour mon ordinateur.',
            'Le câble de la télécommande est trop court.'
        ],
        'CACAO': [
            'J\'aime boire du cacao chaud l\'hiver.',
            'Le cacao est produit à partir des fèves de cacao.',
            'Elle a ajouté du cacao dans son gâteau.'
        ],
        'CACHE': [
            'Il a caché ses économies sous son matelas.',
            'La cache secrète était bien dissimulée.',
            'Nous avons trouvé une cache dans la forêt.'
        ],
        'CADAVRE': [
            'La police a découvert un cadavre dans la rivière.',
            'Le cadavre de l\'animal était en décomposition.',
            'Les médecins étudient le cadavre pour comprendre la maladie.'
        ],
        'CADENAS': [
            'J\'ai oublié le code du cadenas.',
            'Le cadenas protège mon vélo.',
            'Il a acheté un cadenas à combinaison.'
        ],
        'CADRE': [
            'Il travaille comme cadre dans une grande entreprise.',
            'Le cadre de la photo est en bois.',
            'Nous avons besoin d\'un cadre pour organiser l\'événement.'
        ],
        'CAFÉ': [
            'J\'aime boire un café le matin.',
            'Le café du coin est très fréquenté.',
            'Elle a commandé un café noir.'
        ],
        'CAGE': [
            'L\'oiseau est dans sa cage.',
            'La cage du lion est solide.',
            'Il a construit une cage pour ses lapins.'
        ],
        'CAHIER': [
            'J\'écris mes notes dans un cahier.',
            'Le cahier de l\'élève est bien organisé.',
            'Elle a acheté un nouveau cahier pour la rentrée.'
        ],
        'CAILLASSE': [
            'Le chemin de caillasse était difficile à parcourir.',
            'La caillasse crissait sous nos pas.',
            'Il a glissé sur la caillasse.'
        ],
        'CAILLE': [
            'La caille est un oiseau gallinacé.',
            'Nous avons mangé de la caille pour le dîner.',
            'La caille pond de petits œufs.'
        ],
        'CAILLOU': [
            'L\'enfant a ramassé un caillou.',
            'Le chemin était couvert de cailloux.',
            'Il a lancé un caillou dans l\'eau.'
        ],
        'CAIMAN': [
            'Le caïman est un reptile dangereux.',
            'Nous avons vu des caïmans dans le marigot.',
            'Le caïman ressemble au crocodile.'
        ],
        'CAISSE': [
            'J\'ai déposé mes affaires dans la caisse.',
            'La caisse de la supermarché était longue.',
            'Il a acheté une caisse en bois.'
        ],
        'CAJOLER': [
            'Elle aime cajoler son chat.',
            'Il a cajolé son enfant pour le calmer.',
            'Les parents cajolent souvent leurs bébés.'
        ],
        'CALANQUE': [
            'Les calanques de Cassis sont magnifiques.',
            'Nous avons fait une randonnée dans les calanques.',
            'La calanque offre une vue imprenable sur la mer.'
        ],
        'CALCUL': [
            'J\'ai fait un calcul pour vérifier.',
            'Le calcul mental est une compétence utile.',
            'Il a fait un calcul erroné.'
        ],
        'CALCULATEUR': [
            'J\'utilise une calculatrice pour les calculs complexes.',
            'Le calculateur a donné le bon résultat.',
            'Il est très bon en calcul mental.'
        ],
        'CALE': [
            'J\'utilise une cale pour maintenir la porte ouverte.',
            'La cale du navire est bien conçue.',
            'Il a placé une cale sous la table.'
        ],
        'CALEBASSE': [
            'La calebasse est utilisée comme récipient.',
            'Il a bu dans une calebasse.',
            'La calebasse est un fruit comestible.'
        ],
        'CALECHE': [
            'Nous avons fait un tour en calèche.',
            'La calèche était tirée par deux chevaux.',
            'La calèche est un moyen de transport traditionnel.'
        ],
        'CALER': [
            'Il a calé la table contre le mur.',
            'Le bateau est calé dans le port.',
            'J\'ai calé mes affaires dans le coffre.'
        ],
        'CALENDRIER': [
            'J\'ai noté la date dans mon calendrier.',
            'Le calendrier 2024 est déjà en vente.',
            'Elle a accroché un calendrier dans la cuisine.'
        ],
        'CALIBRE': [
            'Le calibre de l\'arme est important.',
            'J\'ai vérifié le calibre des pneus.',
            'Le calibre du canon est précis.'
        ],
        'CALME': [
            'La mer était calme ce matin.',
            'Il a gardé son calme malgré la situation.',
            'Le calme est revenu après la tempête.'
        ],
        'CALOMNIE': [
            'Il a été victime de calomnie.',
            'La calomnie peut détruire une réputation.',
            'Elle a nié les calomnies à son sujet.'
        ],
        'CAMARADE': [
            'Mon camarade de classe est très sympa.',
            'Nous sommes camarades depuis l\'école primaire.',
            'Il a aidé son camarade en difficulté.'
        ],
        'CAMBRIOLAGE': [
            'Un cambriolage a eu lieu dans la rue hier.',
            'La police enquête sur le cambriolage.',
            'Il a été victime d\'un cambriolage.'
        ],
        'CAMION': [
            'Le camion a livré les marchandises.',
            'Il conduit un camion de transport.',
            'Le camion est en panne.'
        ],
        'CAMP': [
            'Nous avons monté notre camp dans la forêt.',
            'Le camp de vacances était très animé.',
            'Il a passé l\'été dans un camp militaire.'
        ],
        'CAMPAGNE': [
            'J\'aime me promener dans la campagne.',
            'La campagne électorale a commencé.',
            'La campagne française est magnifique.'
        ],
        'CAMPING': [
            'Nous avons passé nos vacances au camping.',
            'Le camping est bien équipé.',
            'Il a réservé une place au camping.'
        ],
        'CANARD': [
            'Le canard nage dans l\'étang.',
            'J\'aime manger du canard.',
            'C\'est un canard en plastique.'
        ],
        'CANAL': [
            'Le canal de Suez est très fréquenté.',
            'Nous avons fait une promenade en bateau sur le canal.',
            'Le canal permet l\'irrigation des champs.'
        ],
        'CANAPÉ': [
            'J\'aime me reposer sur le canapé.',
            'Le canapé est très confortable.',
            'Il a acheté un nouveau canapé.'
        ],
        'CANCAN': [
            'Les cancanent dans la cour.',
            'Le cancan est un bruit désagréable.',
            'Arrête de faire du cancan.'
        ],
        'CANDIDAT': [
            'Il est candidat aux élections.',
            'Le candidat a fait un bon discours.',
            'Elle a soutenu son candidat préféré.'
        ],
        'CANNE': [
            'Il marche avec une canne.',
            'La canne à pêche est longue.',
            'J\'ai acheté une canne en bambou.'
        ],
        'CANOË': [
            'Nous avons fait du canoë sur la rivière.',
            'Le canoë est léger et maniable.',
            'Il a loué un canoë pour la journée.'
        ],
        'CANON': [
            'Le canon a tiré un coup.',
            'Le canon de la cheminée est bouché.',
            'Il a nettoyé le canon du fusil.'
        ],
        'CANOT': [
            'Nous avons pagayé dans le canot.',
            'Le canot est petit et léger.',
            'Il a acheté un canot pour pêcher.'
        ],
        'CANTATE': [
            'La cantate a été magnifiquement interprétée.',
            'Il a composé une cantate pour l\'occasion.',
            'La cantate de Bach est célèbre.'
        ],
        'CANTINE': [
            'J\'ai mangé à la cantine aujourd\'hui.',
            'La cantine de l\'école est bonne.',
            'Elle travaille à la cantine.'
        ],
        'CANTON': [
            'Le canton de Genève est beau.',
            'Il habite dans le canton voisin.',
            'Le canton est une division administrative.'
        ],
        'CAP': [
            'Il porte un cap sur la tête.',
            'Le cap de la bonne espérance est célèbre.',
            'J\'ai acheté un cap pour l\'hiver.'
        ],
        'CAPABLE': [
            'Il est capable de résoudre ce problème.',
            'Elle est capable de tout.',
            'Nous sommes capables de réussir.'
        ],
        'CAPACITÉ': [
            'La capacité de la salle est de 100 personnes.',
            'Il a une grande capacité de travail.',
            'La capacité du réservoir est suffisante.'
        ],
        'CAPITAL': [
            'Paris est la capitale de la France.',
            'Il a investi son capital dans l\'immobilier.',
            'Le capital social de l\'entreprise est élevé.'
        ],
        'CAPITULER': [
            'L\'armée a dû capituler.',
            'Il a capitulé devant les difficultés.',
            'La capitulation a été signée.'
        ],
        'CAPON': [
            'Le capon est un coq castré.',
            'Nous avons mangé du capon pour Noël.',
            'Le capon est plus gras que le coq.'
        ],
        'CAPORAL': [
            'Il est caporal dans l\'armée.',
            'Le caporal a donné l\'ordre.',
            'Il a été promu caporal.'
        ],
        'CAPOTE': [
            'La capote de la voiture est ouverte.',
            'Il a acheté une capote pour sa voiture.',
            'La capote protège des intempéries.'
        ],
        'CAPRICE': [
            'C\'est un caprice de sa part.',
            'Les caprices des enfants sont fréquents.',
            'Il a satisfait son caprice.'
        ],
        'CAPSULE': [
            'La capsule du médicament est difficile à avaler.',
            'Il a ouvert la capsule de la bouteille.',
            'La capsule spatiale est revenue sur Terre.'
        ],
        'CAPTAGE': [
            'Le captage des eaux est important.',
            'Il a installé un système de captage.',
            'Le captage permet de collecter l\'eau.'
        ],
        'CAPTEUR': [
            'Le capteur de mouvement est sensible.',
            'Il a installé un capteur de fumée.',
            'Le capteur a détecté une présence.'
        ],
        'CAPTIF': [
            'Les animaux sont en captivité.',
            'Il a été fait captif pendant la guerre.',
            'La captivité est difficile à supporter.'
        ],
        'CAPTURE': [
            'La capture du criminel a été difficile.',
            'Il a fait une capture d\'écran.',
            'La capture des animaux sauvages est réglementée.'
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
with open('corpus.txt', 'a', encoding='utf-8') as f:
    # Écrire les nouveaux mots
    for mot in nouveaux_mots_filtres:
        definition = generer_definition(mot)
        exemples = generer_exemples(mot)
        f.write(f"\n=== {mot} ===\n")
        f.write(f"Définition: {definition}\n\n")
        f.write("Exemples:\n")
        for ex in exemples:
            f.write(f"- {ex}\n")
        f.write("\n")

print("Fichier corpus.txt mis à jour avec succès!")
print(f"Ajout de {len(nouveaux_mots_filtres)} nouveaux mots")
