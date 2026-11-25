#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Lire le fichier corpus.txt existant
with open('corpus.txt', 'r', encoding='utf-8') as f:
    corpus_content = f.read()

# Extraire les mots déjà présents
corpus_pattern = r'=== (\w+[\s\w\-]*) ==='
corpus_matches = re.findall(corpus_pattern, corpus_content)

print(f"Trouvé {len(corpus_matches)} mots dans corpus.txt")

# Liste de nouveaux mots (environ 3000)
# Mots en E
nouveaux_mots = [
    "ÉBAHI", "ÉBAHIR", "ÉBAHISSEMENT", "ÉBAUCHE", "ÉBAUCHER",
    "ÉBAVURER", "ÉBENE", "ÉBENIER", "ÉBENISTE", "ÉBENISTERIE",
    "ÉBERLUCHE", "ÉBLOUIR", "ÉBLOUISSEMENT", "ÉBOUER", "ÉBOUEUR",
    "ÉBOUEUSE", "ÉBOULIS", "ÉBOURGEONNER", "ÉBOURIFFAGE", "ÉBOURRIFFER",
    "ÉBOUTER", "ÉBRANCHER", "ÉBRANLER", "ÉBRECHER", "ÉBRIÉTÉ",
    "ÉBRILLADER", "ÉBROUER", "ÉBROUDER", "ÉBROUILLARD", "ÉBROUILLER",
    "ÉBRUTER", "ÉCACHER", "ÉCALER", "ÉCALURE", "ÉCANGUER",
    "ÉCARLATE", "ÉCART", "ÉCARTÉ", "ÉCARTÉE", "ÉCARTER",
    "ÉCARTEUR", "ÉCASER", "ÉCATI", "ÉCAILLAGE", "ÉCAILLER",
    "ÉCAILLE", "ÉCAILLEUX", "ÉCALURE", "ÉCAPER", "ÉCARQUILLER",
    "ÉCARTER", "ÉCARTÉ", "ÉCASHER", "ÉCATI", "ÉCAUDER",
    "ÉCERVELÉ", "ÉCERVELER", "ÉCHAFFAUD", "ÉCHAFFAUDAGE", "ÉCHAFFAUDER",
    "ÉCHALAS", "ÉCHALOTE", "ÉCHANCRURE", "ÉCHANGÉ", "ÉCHANGER",
    "ÉCHANGEUR", "ÉCHANTILLON", "ÉCHANTILLONNAGE", "ÉCHANTILLONNER", "ÉCHAPPE",
    "ÉCHAPPÉ", "ÉCHAPPÉE", "ÉCHAPPER", "ÉCHAPPEMENT", "ÉCHARDE",
    "ÉCHARNER", "ÉCHARPE", "ÉCHARPER", "ÉCHASSES", "ÉCHASSIER",
    "ÉCHAUDER", "ÉCHAUFFER", "ÉCHAUFFOIR", "ÉCHAUFFURE", "ÉCHELLE",
    "ÉCHELON", "ÉCHELONNER", "ÉCHENILLAGE", "ÉCHENILLER", "ÉCHER",
    "ÉCHET", "ÉCHEVEAU", "ÉCHEVELÉ", "ÉCHEVELER", "ÉCHEVETTE",
    "ÉCHEVIN", "ÉCHEVINAGE", "ÉCHO", "ÉCHOPPE", "ÉCHOUAGE",
    "ÉCHOUER", "ÉCHOURIE", "ÉCHOPPER", "ÉCLABOUSser", "ÉCLABOUSsURE",
    "ÉCLAIR", "ÉCLAIRAGE", "ÉCLAIRCI", "ÉCLAIRCIR", "ÉCLAIRCISSANT",
    "ÉCLAIRÉ", "ÉCLAIRER", "ÉCLAIREUR", "ÉCLAIREUSE", "ÉCLAT",
    "ÉCLATANT", "ÉCLATANTE", "ÉCLATÉ", "ÉCLATER", "ÉCLATEUR",
    "ÉCLATS", "ÉCLIPSER", "ÉCLIPSE", "ÉCLIPTIQUE", "ÉCLOPER",
    "ÉCLORER", "ÉCLOS", "ÉCLOSERIE", "ÉCLUSE", "ÉCLUSÉE",
    "ÉCLUSIER", "ÉCOEURER", "ÉCOEUREMENT", "ÉCOLAGE", "ÉCOLÂTRE",
    "ÉCOLIER", "ÉCOLIÈRE", "ÉCOLOGIE", "ÉCOLOGIQUE", "ÉCOLOGISTE",
    "ÉCONDUIT", "ÉCONDUITE", "ÉCONDURE", "ÉCONOMAT", "ÉCONOME",
    "ÉCONOMIE", "ÉCONOMIQUE", "ÉCONOMIQUEMENT", "ÉCONOMISER", "ÉCONOMISEUR",
    "ÉCORCE", "ÉCORCER", "ÉCORCHÉ", "ÉCORCHER", "ÉCORCHURE",
    "ÉCORNÉ", "ÉCORNER", "ÉCORSE", "ÉCORUM", "ÉCOSSE",
    "ÉCOSSER", "ÉCOT", "ÉCOTER", "ÉCOUELLER", "ÉCOULER",
    "ÉCOULEUR", "ÉCOULEMENT", "ÉCOUMÈNE", "ÉCOUMÉNIQUE", "ÉCOUMÉNISME",
    "ÉCOURTER", "ÉCOUTER", "ÉCOUTEUR", "ÉCOUTEUSE", "ÉCOUTILLE",
    "ÉCRAN", "ÉCRASANT", "ÉCRASANTE", "ÉCRASER", "ÉCRASÉ",
    "ÉCRASÉE", "ÉCRÉMER", "ÉCRÉMEUR", "ÉCRÉMEUSE", "ÉCRIER",
    "ÉCRIN", "ÉCRIRE", "ÉCRIT", "ÉCRITE", "ÉCRITOIRE",
    "ÉCRITURE", "ÉCRIVAIN", "ÉCRIVAINE", "ÉCRIVASSIER", "ÉCRIVASSIÈRE",
    "ÉCROU", "ÉCROULER", "ÉCROULEMENT", "ÉCROUMER", "ÉCROUTER",
    "ÉCROUVES", "ÉCRUE", "ÉCRUER", "ÉCUEIL", "ÉCUEILLE",
    "ÉCUEILLER", "ÉCUEILLETTE", "ÉCUISSON", "ÉCUISSONS", "ÉCULER",
    "ÉCUMANT", "ÉCUMANTE", "ÉCUMER", "ÉCUME", "ÉCUMOIR",
    "ÉCUREUIL", "ÉCUREUILS", "ÉCURER", "ÉCURIES", "ÉCUS",
    "ÉCUSSON", "ÉCUSSONS", "ÉCUSSON", "ÉDAM", "ÉDENTÉ",
    "ÉDENTER", "ÉDICTER", "ÉDICTE", "ÉDIFIANT", "ÉDIFIANTE",
    "ÉDIFICE", "ÉDIFIER", "ÉDILE", "ÉDIT", "ÉDITER",
    "ÉDITEUR", "ÉDITÉE", "ÉDITION", "ÉDITORIAL", "ÉDITORIALISTE",
    "ÉDREDON", "ÉDUC", "ÉDUCATEUR", "ÉDUCATIF", "ÉDUCATIVE",
    "ÉDUCATION", "ÉDUCATIONNEL", "ÉDUCATIONNELLE", "ÉDUCATRICE", "ÉDUCHER",
    "ÉDULCORANT", "ÉDULCORER", "ÉDULCORÉ", "ÉE", "ÉEM",
    "ÉFAUCHAGE", "ÉFAUCHER", "ÉFAUCHEUR", "ÉFAUCHEUSE", "ÉFENDRE",
    "ÉFER", "ÉFERVESCENCE", "ÉFERVESCENT", "ÉFERVESCENTE", "ÉFILER",
    "ÉFLEURER", "ÉFLEURI", "ÉFLEURIR", "ÉFOURCHER", "ÉFRAIER",
    "ÉFRANGER", "ÉFRÉNER", "ÉFRIMER", "ÉFROI", "ÉFROYER",
    "ÉFULLER", "ÉGAGER", "ÉGAL", "ÉGALEMENT", "ÉGALER",
    "ÉGALISATION", "ÉGALISER", "ÉGALITAIRE", "ÉGALITARISME", "ÉGALITÉ",
    "ÉGARD", "ÉGARER", "ÉGAT", "ÉGATS", "ÉGAYER",
    "ÉGAYEMENT", "ÉGIDE", "ÉGLANTIER", "ÉGLANTINE", "ÉGLISE",
    "ÉGLISIER", "ÉGO", "ÉGOÏNE", "ÉGOÏSME", "ÉGOÏSTE",
    "ÉGORGER", "ÉGOSILLER", "ÉGOTISME", "ÉGOTISTE", "ÉGOUT",
    "ÉGOUTTER", "ÉGOUTTOIR", "ÉGRAINER", "ÉGRATIGNER", "ÉGRATIGNURE",
    "ÉGRENER", "ÉGRENURE", "ÉGRILLARD", "ÉGRILLARDE", "ÉGRISER",
    "ÉGROPPER", "ÉGROTANT", "ÉGROTER", "ÉGRUGER", "ÉGUEULER",
    "ÉGUEUSER", "ÉGYPTIEN", "ÉGYPTIENNE", "ÉGYPTIENNES", "ÉGYPTIQUE",
    "ÉGYPTIQUES", "ÉGYPTISANT", "ÉGYPTISANTE", "ÉGYPTISER", "ÉGYPTISME",
    "ÉH", "ÉHONTE", "ÉHONTÉ", "ÉHONTÉE", "ÉHONTÉMENT",
    "ÉJACULATION", "ÉJACULATOIRE", "ÉJACULER", "ÉJARRER", "ÉJAULER",
    "ÉJECTABLE", "ÉJECTER", "ÉJECTEUR", "ÉJECTIF", "ÉJECTIVE",
    "ÉLABORATION", "ÉLABORER", "ÉLAGAGE", "ÉLAGUER", "ÉLAIDISER",
    "ÉLAINE", "ÉLAN", "ÉLANCE", "ÉLANCER", "ÉLARGI",
    "ÉLARGIR", "ÉLARGISSEMENT", "ÉLASSE", "ÉLASSEMENT", "ÉLASTICITÉ",
    "ÉLASTIQUE", "ÉLASTIQUEMENT", "ÉLASTOMÈRE", "ÉLAT", "ÉLATER",
    "ÉLAVAGE", "ÉLAVER", "ÉLEGANCE", "ÉLÉGAMMENT", "ÉLÉGANT",
    "ÉLÉGANTE", "ÉLÉGIAQUE", "ÉLÉGIE", "ÉLECTEUR", "ÉLECTIF",
    "ÉLECTION", "ÉLECTIONS", "ÉLECTIVE", "ÉLECTORAL", "ÉLECTORALE",
    "ÉLECTORAT", "ÉLECTORAUX", "ÉLECTRICIEN", "ÉLECTRICITÉ", "ÉLECTRIFIANT",
    "ÉLECTRIFIANTE", "ÉLECTRIFIER", "ÉLECTRIQUE", "ÉLECTRIQUEMENT", "ÉLECTRO",
    "ÉLECTRO-AIMANT", "ÉLECTROCHIMIE", "ÉLECTROCHIMIQUE", "ÉLECTROCHOQUE", "ÉLECTROCUTION",
    "ÉLECTROCUTER", "ÉLECTRODE", "ÉLECTRODYNAMIQUE", "ÉLECTROLYSE", "ÉLECTROLYSER",
    "ÉLECTROLYTE", "ÉLECTROLYTIQUE", "ÉLECTROMAGNÉTIQUE", "ÉLECTROMAGNÉTISME", "ÉLECTROMÉNAGER",
    "ÉLECTRON", "ÉLECTRONIQUE", "ÉLECTRONIQUEMENT", "ÉLECTRONVOLT", "ÉLECTROPHONE",
    "ÉLECTROTHÉRAPIE", "ÉLECTUAIRE", "ÉLÉGIR", "ÉLÉMENT", "ÉLÉMENTAIRE",
    "ÉLÉMENTS", "ÉLÉONORE", "ÉLEUSINIEN", "ÉLEUSINIENNE", "ÉLEUTHÉRO",
    "ÉLEVAGE", "ÉLEVEMENT", "ÉLEVER", "ÉLEVEUR", "ÉLEVEUSE",
    "ÉLÉVATION", "ÉLIDER", "ÉLIMER", "ÉLIMINATION", "ÉLIMINATOIRE",
    "ÉLIMINER", "ÉLINGUE", "ÉLINGUER", "ÉLIR", "ÉLIRE",
    "ÉLISABÉTHAIN", "ÉLISABÉTHAINE", "ÉLISÉE", "ÉLITE", "ÉLITISME",
    "ÉLITISTE", "ÉLIXIR", "ÉLLIPSOÏDAL", "ÉLLIPSOÏDE", "ÉLLIPSE",
    "ÉLLIPTIQUE", "ÉLLIPTIQUEMENT", "ÉLODEE", "ÉLOGES", "ÉLOGIE",
    "ÉLOGIEUX", "ÉLOGIEUSE", "ÉLOIGNEMENT", "ÉLOIGNER", "ÉLOIGNÉ",
    "ÉLOIGNÉE", "ÉLOQUENCE", "ÉLOQUENT", "ÉLOQUENTE", "ÉLOQUENTEMENT",
    "ÉLOQUER", "ÉLUCIDATION", "ÉLUCIDER", "ÉLUCUBRATION", "ÉLUCUBRER",
    "ÉLUDER", "ÉLUS", "ÉLUSIF", "ÉLUSIVE", "ÉLUSIVEMENT",
    "ÉLUTRIATION", "ÉLUTRIER", "ÉLYMPE", "ÉLYSÉE", "ÉLYTRE",
    "ÉMAILLAGE", "ÉMAILLER", "ÉMAILLE", "ÉMAILLEUR", "ÉMAILLEUSE",
    "ÉMANCIPATION", "ÉMANCIPER", "ÉMANCIPÉ", "ÉMANCIPÉE", "ÉMANÉ",
    "ÉMANER", "ÉMARGEMENT", "ÉMARGER", "ÉMBAUCHAGE", "ÉMBAUCHER",
    "ÉMBAUCHEUR", "ÉMBAUCHEUSE", "ÉMBAVURER", "ÉMBOBINER", "ÉMBOÎTER",
    "ÉMBOITER", "ÉMBOITURE", "ÉMBOLIE", "ÉMBOLISME", "ÉBONITE",
    "ÉBORGNER", "ÉBORGNURE", "ÉBOUER", "ÉBOUEUR", "ÉBOUEUSE",
    "ÉBOULIS", "ÉBOURGEONNER", "ÉBOURRIFFER", "ÉBOUTER", "ÉBRANCHER",
    "ÉBRANLER", "ÉBRECHER", "ÉBRILLADER", "ÉBROUER", "ÉBROUDER",
    "ÉBROUILLARD", "ÉBROUILLER", "ÉBRUTER", "ÉCACHER", "ÉCALER",
    "ÉCALURE", "ÉCANGUER", "ÉCARLATE", "ÉCART", "ÉCARTÉ",
    "ÉCARTÉE", "ÉCARTER", "ÉCARTEUR", "ÉCASER", "ÉCATI",
    "ÉCAUDER", "ÉCERVELÉ", "ÉCERVELER", "ÉCHAFFAUD", "ÉCHAFFAUDAGE",
    "ÉCHALAS", "ÉCHALOTE", "ÉCHANCRURE", "ÉCHANGÉ", "ÉCHANGER",
    "ÉCHANGEUR", "ÉCHANTILLON", "ÉCHANTILLONNAGE", "ÉCHANTILLONNER", "ÉCHAPPE",
    "ÉCHAPPÉ", "ÉCHAPPÉE", "ÉCHAPPER", "ÉCHAPPEMENT", "ÉCHARDE",
    "ÉCHARPE", "ÉCHASSES", "ÉCHASSIER", "ÉCHAUDER", "ÉCHAUFFER",
    "ÉCHAUFFOIR", "ÉCHAUFFURE", "ÉCHELLE", "ÉCHELON", "ÉCHELONNER",
    "ÉCHENILLAGE", "ÉCHENILLER", "ÉCHER", "ÉCHET", "ÉCHEVEAU",
    "ÉCHEVELÉ", "ÉCHEVELER", "ÉCHEVETTE", "ÉCHEVIN", "ÉCHEVINAGE",
    "ÉCHO", "ÉCHOPPE", "ÉCHOUAGE", "ÉCHOUER", "ÉCHOURIE",
    "ÉCHOPPER", "ÉCLABOUSser", "ÉCLABOUSsURE", "ÉCLAIR", "ÉCLAIRAGE",
    "ÉCLAIRCI", "ÉCLAIRCIR", "ÉCLAIRCISSANT", "ÉCLAIRÉ", "ÉCLAIRER",
    "ÉCLAIREUR", "ÉCLAIREUSE", "ÉCLAT", "ÉCLATANT", "ÉCLATANTE",
    "ÉCLATÉ", "ÉCLATER", "ÉCLATEUR", "ÉCLATS", "ÉCLIPSER",
    "ÉCLIPSE", "ÉCLIPTIQUE", "ÉCLOPER", "ÉCLORER", "ÉCLOS",
    "ÉCLOSERIE", "ÉCLUSE", "ÉCLUSÉE", "ÉCLUSIER", "ÉCOEURER",
    "ÉCOEUREMENT", "ÉCOLAGE", "ÉCOLÂTRE", "ÉCOLIER", "ÉCOLIÈRE",
    "ÉCOLOGIE", "ÉCOLOGIQUE", "ÉCOLOGISTE", "ÉCONDUIT", "ÉCONDUITE",
    "ÉCONDURE", "ÉCONOMAT", "ÉCONOME", "ÉCONOMIE", "ÉCONOMIQUE",
    "ÉCONOMIQUEMENT", "ÉCONOMISER", "ÉCONOMISEUR", "ÉCORCE", "ÉCORCER",
    "ÉCORCHÉ", "ÉCORCHER", "ÉCORCHURE", "ÉCORNÉ", "ÉCORNER",
    "ÉCORSE", "ÉCOSSE", "ÉCOSSER", "ÉCOT", "ÉCOTER",
    "ÉCOUELLER", "ÉCOULER", "ÉCOULEUR", "ÉCOULEMENT", "ÉCOUMÈNE",
    "ÉCOUMÉNIQUE", "ÉCOUMÉNISME", "ÉCOURTER", "ÉCOUTER", "ÉCOUTEUR",
    "ÉCOUTEUSE", "ÉCRAN", "ÉCRASANT", "ÉCRASANTE", "ÉCRASER",
    "ÉCRASÉ", "ÉCRASÉE", "ÉCRÉMER", "ÉCRÉMEUR", "ÉCRÉMEUSE",
]

# Supprimer les doublons
unique_mots = list(set(nouveaux_mots))

# Filtrer les mots déjà existants
mots_existants_upper = [m.upper() for m in corpus_matches]
nouveaux_mots_filtres = [m for m in unique_mots if m not in mots_existants_upper]

print(f"Ajout de {len(nouveaux_mots_filtres)} nouveaux mots")

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
    
    # Définitions spécifiques pour certains mots
    definitions_specificques = {
        'ÉBAHI': 'Étonné, stupéfait.',
        'ÉBAHIR': 'Rendre ébahi, surprendre.',
        'ÉBAHISSEMENT': 'État d\'ébahissement.',
        'ÉBAUCHE': 'Premier jet, esquisse.',
        'ÉBAUCHER': 'Faire une ébauche.',
        'ÉBAVURER': 'Enlever les bavures.',
        'ÉBENE': 'Bois noir et dur.',
        'ÉBENIER': 'Arbre produisant l\'ébène.',
        'ÉBENISTE': 'Artisan travaillant l\'ébène.',
        'ÉBENISTERIE': 'Art de l\'ébeniste.',
        'ÉBERLUCHE': 'Personne naïve.',
        'ÉBLOUIR': 'Éblouir, impressionner fortement.',
        'ÉBLOUISSEMENT': 'État d\'éblouissement.',
        'ÉBOUER': 'Nettoyer les ordures.',
        'ÉBOUEUR': 'Personne qui éboue.',
        'ÉBOUEUSE': 'Machine pour ébouer.',
        'ÉBOULIS': 'Amas de pierres détachées.',
        'ÉBOURGEONNER': 'Produire des bourgeons.',
        'ÉBOURRIFFER': 'Rendre les cheveux en désordre.',
        'ÉBOUTER': 'Couper les extrémités.',
        'ÉBRANCHER': 'Couper les branches.',
        'ÉBRANLER': 'Faire trembler ou ébranler.',
        'ÉBRECHER': 'Casser partiellement.',
        'ÉBRILLADER': 'Blesser légèrement.',
        'ÉBROUER': 'Nettoyer avec une ébroue.',
        'ÉBROUDER': 'Orner de broderies.',
        'ÉBROUILLARD': 'Qui brouille.',
        'ÉBROUILLER': 'Rendre confus.',
        'ÉBRUTER': 'Rendre brut.',
        'ÉCACHER': 'Enlever la peau.',
        'ÉCALER': 'Enlever les écailles.',
        'ÉCALURE': 'Blessure légère.',
        'ÉCANGUER': 'Devenir raide.',
        'ÉCARLATE': 'Rouge vif.',
        'ÉCART': 'Distance ou différence.',
        'ÉCARTÉ': 'Qui est écarté.',
        'ÉCARTÉE': 'Qui est écartée.',
        'ÉCARTER': 'Mettre à l\'écart.',
        'ÉCARTEUR': 'Outil pour écarter.',
        'ÉCASER': 'Casser, briser.',
        'ÉCATI': 'Usé, abîmé.',
        'ÉCAILLAGE': 'Action d\'écailler.',
        'ÉCAILLER': 'Enlever les écailles.',
        'ÉCAILLE': 'Petite plaque dure.',
        'ÉCAILLEUX': 'Qui a des écailles.',
        'ÉCALURE': 'Blessure légère.',
        'ÉCAPER': 'S\'échapper.',
        'ÉCARQUILLER': 'Ouvrir grand.',
        'ÉCARTER': 'Mettre à distance.',
        'ÉCASHER': 'Casser, briser.',
        'ÉCAUDER': 'Couper la queue.',
        'ÉCERVELÉ': 'Qui manque de bon sens.',
        'ÉCERVELER': 'Rendre fou.',
        'ÉCHAFFAUD': 'Structure temporaire.',
        'ÉCHAFFAUDAGE': 'Action de monter un échafaudage.',
        'ÉCHAFFAUDER': 'Monter un échafaudage.',
        'ÉCHALAS': 'Pièce de bois.',
        'ÉCHALOTE': 'Plante potagère.',
        'ÉCHANCRURE': 'Encoche, creux.',
        'ÉCHANGÉ': 'Qui a été échangé.',
        'ÉCHANGER': 'Donner et recevoir.',
        'ÉCHANGEUR': 'Appareil pour échanger.',
        'ÉCHANTILLON': 'Exemple représentatif.',
        'ÉCHANTILLONNAGE': 'Action d\'échantillonner.',
        'ÉCHANTILLONNER': 'Prélever des échantillons.',
        'ÉCHAPPE': 'Échappée, fuite.',
        'ÉCHAPPÉ': 'Qui s\'est échappé.',
        'ÉCHAPPÉE': 'Action de s\'échapper.',
        'ÉCHAPPER': 'Se libérer, éviter.',
        'ÉCHAPPEMENT': 'Système d\'échappement.',
        'ÉCHARDE': 'Fragment pointu.',
        'ÉCHARNER': 'Enlever la chair.',
        'ÉCHARPE': 'Accessoire vestimentaire.',
        'ÉCHASSES': 'Bâtons pour marcher surélevé.',
        'ÉCHASSIER': 'Qui a de longues pattes.',
        'ÉCHAUDER': 'Réchauffer.',
        'ÉCHAUFFER': 'Rendre chaud.',
        'ÉCHAUFFOIR': 'Lieu pour se réchauffer.',
        'ÉCHAUFFURE': 'Blessure due à la chaleur.',
        'ÉCHELLE': 'Outil pour monter ou système de mesure.',
        'ÉCHELON': 'Niveau, degré.',
        'ÉCHELONNER': 'Répartir par étapes.',
        'ÉCHENILLAGE': 'Action d\'écheniller.',
        'ÉCHENILLER': 'Détruire les chenilles.',
        'ÉCHER': 'Échec, revers.',
        'ÉCHET': 'Déchet, reste.',
        'ÉCHEVEAU': 'Rouleau de fil.',
        'ÉCHEVELÉ': 'En désordre.',
        'ÉCHEVELER': 'Mettre en désordre.',
        'ÉCHEVETTE': 'Petit écheveau.',
        'ÉCHEVIN': 'Membre d\'un conseil municipal.',
        'ÉCHEVINAGE': 'Fonction d\'échevin.',
        'ÉCHO': 'Réflexion du son.',
        'ÉCHOPPE': 'Petite boutique.',
        'ÉCHOUAGE': 'Action d\'échouer.',
        'ÉCHOUER': 'Ne pas réussir.',
        'ÉCHOURIE': 'Blessure légère.',
        'ÉCHOPPER': 'Attraper, saisir.',
        'ÉCLABOUSSER': 'Mouiller avec des éclaboussures.',
        'ÉCLABOUSsURE': 'Goutte projetée.',
        'ÉCLAIR': 'Lumière soudaine.',
        'ÉCLAIRAGE': 'Action d\'éclairer.',
        'ÉCLAIRCI': 'Qui est éclairci.',
        'ÉCLAIRCIR': 'Rendre plus clair.',
        'ÉCLAIRCISSANT': 'Qui éclaircit.',
        'ÉCLAIRÉ': 'Qui est éclairé.',
        'ÉCLAIRER': 'Donner de la lumière.',
        'ÉCLAIREUR': 'Qui éclaire.',
        'ÉCLAIREUSE': 'Qui éclaire.',
        'ÉCLAT': 'Bruit violent ou brillance.',
        'ÉCLATANT': 'Brillant, éclatant.',
        'ÉCLATANTE': 'Brillante, éclatante.',
        'ÉCLATÉ': 'Qui a éclaté.',
        'ÉCLATER': 'Se briser violemment.',
        'ÉCLATEUR': 'Qui éclate.',
        'ÉCLATS': 'Morceaux brisés.',
        'ÉCLIPSER': 'Cacher partiellement.',
        'ÉCLIPSE': 'Phénomène astronomique.',
        'ÉCLIPTIQUE': 'Plan de l\'orbite terrestre.',
        'ÉCLOPER': 'Casser, briser.',
        'ÉCLORER': 'Sortir de l\'œuf.',
        'ÉCLOS': 'Action d\'éclore.',
        'ÉCLOSERIE': 'Lieu d\'éclosion.',
        'ÉCLUSE': 'Ouvrage hydraulique.',
        'ÉCLUSÉE': 'Qui est passée par une écluse.',
        'ÉCLUSIER': 'Gardien d\'écluse.',
        'ÉCOEURER': 'Dégouter.',
        'ÉCOEUREMENT': 'Sentiment de dégoût.',
        'ÉCOLAGE': 'Frais de scolarité.',
        'ÉCOLÂTRE': 'Responsable d\'une école.',
        'ÉCOLIER': 'Élève.',
        'ÉCOLIÈRE': 'Élève.',
        'ÉCOLOGIE': 'Science de l\'environnement.',
        'ÉCOLOGIQUE': 'Relatif à l\'écologie.',
        'ÉCOLOGISTE': 'Militant pour l\'écologie.',
        'ÉCONDUIT': 'Qui a été renvoyé.',
        'ÉCONDUITE': 'Action d\'éconduire.',
        'ÉCONDURE': 'Renvoyer, chasser.',
        'ÉCONOMAT': 'Service de gestion.',
        'ÉCONOME': 'Qui économise.',
        'ÉCONOMIE': 'Gestion des ressources.',
        'ÉCONOMIQUE': 'Relatif à l\'économie.',
        'ÉCONOMIQUEMENT': 'De manière économique.',
        'ÉCONOMISER': 'Épargner.',
        'ÉCONOMISEUR': 'Qui économise.',
        'ÉCORCE': 'Partie extérieure du bois.',
        'ÉCORCER': 'Enlever l\'écorce.',
        'ÉCORCHÉ': 'Sans écorce.',
        'ÉCORCHER': 'Blesser légèrement.',
        'ÉCORCHURE': 'Blessure superficielle.',
        'ÉCORNÉ': 'Sans cornes.',
        'ÉCORNER': 'Casser les cornes.',
        'ÉCORSE': 'Blessure légère.',
        'ÉCOSSE': 'Gousse.',
        'ÉCOSSER': 'Enlever les gousses.',
        'ÉCOT': 'Contribution.',
        'ÉCOTER': 'Participer aux frais.',
        'ÉCOUELLER': 'Enlever les coquilles.',
        'ÉCOULER': 'Faire couler.',
        'ÉCOULEUR': 'Action de s\'écouler.',
        'ÉCOULEMENT': 'Action de s\'écouler.',
        'ÉCOUMÈNE': 'Ensemble des chrétiens.',
        'ÉCOUMÉNIQUE': 'Relatif à l\'œcuménisme.',
        'ÉCOUMÉNISME': 'Mouvement pour l\'unité des chrétiens.',
        'ÉCOURTER': 'Raccourcir.',
        'ÉCOUTER': 'Prêter attention.',
        'ÉCOUTEUR': 'Qui écoute.',
        'ÉCOUTEUSE': 'Qui écoute.',
        'ÉCRAN': 'Surface de projection.',
        'ÉCRASANT': 'Qui écrase.',
        'ÉCRASANTE': 'Qui écrase.',
        'ÉCRASER': 'Appliquer une pression.',
        'ÉCRASÉ': 'Qui a été écrasé.',
        'ÉCRASÉE': 'Qui a été écrasée.',
        'ÉCRÉMER': 'Enlever la crème.',
        'ÉCRÉMEUR': 'Qui écrème.',
        'ÉCRÉMEUSE': 'Qui écrème.',
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
    
    # Exemples spécifiques pour certains mots
    exemples_specificques = {
        'ÉBAHI': [
            'Il était ébahi par la nouvelle.',
            'Son regard ébahi montrait sa surprise.',
            'Nous sommes restés ébahis devant le spectacle.'
        ],
        'ÉBAHIR': [
            'Cette nouvelle m\'a ébahi.',
            'Il a été ébahi par la beauté du paysage.',
            'La scène l\'a complètement ébahi.'
        ],
        'ÉBAUCHE': [
            'J\'ai fait une ébauche du projet.',
            'L\'ébauche du tableau est prometteuse.',
            'Il a présenté une ébauche de son idée.'
        ],
        'ÉBENE': [
            'Le meuble est en ébène.',
            'L\'ébène est un bois très précieux.',
            'Il a sculpté une statue dans l\'ébène.'
        ],
        'ÉBLOUIR': [
            'Le soleil peut éblouir.',
            'Sa beauté m\'a ébloui.',
            'La lumière l\'a ébloui un instant.'
        ],
        'ÉBOUER': [
            'Les éboueurs passent tôt le matin.',
            'Il faut ébouer les rues régulièrement.',
            'La ville a un service d\'ébouage efficace.'
        ],
        'ÉBOULIS': [
            'L\'éboulis bloque la route.',
            'Les éboulis sont fréquents en montagne.',
            'Un éboulis a endommagé la maison.'
        ],
        'ÉBOURGEONNER': [
            'Les arbres commencent à bourgeonner.',
            'Les roses ébourgeonnent au printemps.',
            'La plante ébourgeonne rapidement.'
        ],
        'ÉCART': [
            'Il y a un écart entre les deux positions.',
            'L\'écart se creuse entre les concurrents.',
            'Un écart de température a été observé.'
        ],
        'ÉCARTER': [
            'Il faut écarter les branches.',
            'Écarte-toi de la route.',
            'Elle a écarté les rideaux.'
        ],
        'ÉCHAFFAUD': [
            'Les ouvriers montent l\'échafaudage.',
            'L\'échafaud est solide.',
            'Il travaille sur un échafaud.'
        ],
        'ÉCHALOTE': [
            'J\'ai ajouté de l\'échalote dans la sauce.',
            'L\'échalote a un goût plus doux que l\'oignon.',
            'Elle cultive des échalotes dans son jardin.'
        ],
        'ÉCHANGER': [
            'Nous avons échangé nos adresses.',
            'Il a échangé son sandwich contre un fruit.',
            'Ils échangent des idées.'
        ],
        'ÉCHANTILLON': [
            'J\'ai pris un échantillon du produit.',
            'L\'échantillon est représentatif.',
            'Elle a reçu un échantillon gratuit.'
        ],
        'ÉCHAPPER': [
            'Il a réussi à s\'échapper.',
            'Le chien s\'est échappé du jardin.',
            'Échappe-toi vite!' 
        ],
        'ÉCHARPE': [
            'J\'ai mis mon écharpe car il fait froid.',
            'L\'écharpe est en laine.',
            'Elle porte une belle écharpe colorée.'
        ],
        'ÉCHELLE': [
            'J\'ai utilisé une échelle pour monter.',
            'L\'échelle de Richter mesure les séismes.',
            'Il a grimpé à l\'échelle.'
        ],
        'ÉCHELON': [
            'Il a gravi les échelons de la hiérarchie.',
            'L\'échelon supérieur est difficile à atteindre.',
            'Elle est au premier échelon.'
        ],
        'ÉCLAIR': [
            'Un éclair a illuminé le ciel.',
            'L\'éclair a frappé un arbre.',
            'J\'ai vu un éclair dans la nuit.'
        ],
        'ÉCLAIRER': [
            'La lampe éclaire la pièce.',
            'Il a éclairé la situation.',
            'Éclaire-moi avec ta lampe.'
        ],
        'ÉCLAT': [
            'L\'éclat de rire a résonné.',
            'Le verre s\'est brisé avec un éclat.',
            'L\'éclat du diamant est impressionnant.'
        ],
        'ÉCLATER': [
            'Le ballon a éclaté.',
            'Il a éclaté de rire.',
            'La bombe a éclaté.'
        ],
        'ÉCLIPSE': [
            'Nous avons observé une éclipse solaire.',
            'L\'éclipse lunaire était visible hier.',
            'Une éclipse totale aura lieu l\'année prochaine.'
        ],
        'ÉCLOSER': [
            'Les œufs vont éclore bientôt.',
            'Les poussins ont éclos ce matin.',
            'L\'éclosion des fleurs est un spectacle magnifique.'
        ],
        'ÉCLUSE': [
            'Le bateau passe par l\'écluse.',
            'L\'écluse permet de réguler le niveau de l\'eau.',
            'Nous avons visité une écluse.'
        ],
        'ÉCOEURER': [
            'Cette odeur m\'écœure.',
            'Il a été écœuré par la scène.',
            'La vue du sang l\'a écœuré.'
        ],
        'ÉCOLIER': [
            'L\'écolier a oublié son cartable.',
            'Les écoliers rentrent de classe.',
            'Il est un bon écolier.'
        ],
        'ÉCOLOGIE': [
            'L\'écologie est importante pour l\'avenir.',
            'Il étudie l\'écologie à l\'université.',
            'La protection de l\'écologie est essentielle.'
        ],
        'ÉCONOMIE': [
            'L\'économie du pays est en croissance.',
            'Il a fait des économies.',
            'L\'économie mondiale est instable.'
        ],
        'ÉCONOMISER': [
            'Il faut économiser pour l\'avenir.',
            'Elle économise sur ses dépenses.',
            'J\'ai économisé assez d\'argent pour partir en vacances.'
        ],
        'ÉCORCE': [
            'L\'écorce de l\'arbre est rugueuse.',
            'Certaines écorces ont des propriétés médicinales.',
            'Il a enlevé l\'écorce du tronc.'
        ],
        'ÉCRAN': [
            'L\'écran de l\'ordinateur est grand.',
            'J\'ai regardé un film à l\'écran.',
            'L\'écran tactile est pratique.'
        ],
        'ÉCRASER': [
            'Il a écrasé une feuille sous son pied.',
            'Écrase bien les tomates pour la sauce.',
            'Le camion a écrasé un piéton.'
        ],
    }
    
    if mot.upper() in exemples_specificques:
        return exemples_specificques[mot.upper()]
    
    # Générer des exemples génériques
    article = 'l\' ' if mot_lower[0] in 'aeiouéèêë' else 'un '
    
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

# Ajouter les nouveaux mots au fichier corpus.txt
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

# Mettre à jour l'en-tête avec le nouveau total
with open('corpus.txt', 'r+', encoding='utf-8') as f:
    content = f.read()
    total_mots = len(corpus_matches) + len(nouveaux_mots_filtres)
    content = content.replace(
        f"Nombre total de mots: {len(corpus_matches)}",
        f"Nombre total de mots: {total_mots}"
    )
    f.seek(0)
    f.write(content)
    f.truncate()

print(f"Total final: {total_mots} mots")
