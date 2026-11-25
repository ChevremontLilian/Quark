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

# Liste de mots en F (environ 500)
nouveaux_mots = [
    "FABACEES", "FABACÉES", "FABLE", "FABLIAU", "FABLIER",
    "FABRIQUANT", "FABRIQUER", "FABRIQUE", "FABRIQUÉ", "FABRIQUÉE",
    "FABULEUX", "FABULEUSE", "FABULISTE", "FACADE", "FACÉTIE",
    "FACÉTIEUX", "FACÉTIEUSE", "FACHER", "FACHEUX", "FACHEUSE",
    "FACILE", "FACILEMENT", "FACILITÉ", "FACILITER", "FACON",
    "FACONNAGE", "FACONNER", "FACONNIER", "FACONNIÈRE", "FACTAGE",
    "FACTEUR", "FACTICE", "FACTION", "FACTIONNAIRE", "FACTITIF",
    "FACTITIVE", "FACTO", "FACTORER", "FACTORIEL", "FACTORIELLE",
    "FACTORISATION", "FACTORISER", "FACTORY", "FACTOTUM", "FACTUEL",
    "FACTUELLE", "FACTURE", "FACTURER", "FACTURIER", "FACTURIÈRE",
    "FACULTATIF", "FACULTATIVE", "FACULTATIVEMENT", "FACULTÉ", "FACULTÉS",
    "FADAIS", "FADAISER", "FADE", "FADER", "FADEUR",
    "FADEUSE", "FADING", "FAGACEES", "FAGACÉES", "FAGOT",
    "FAGOTAGE", "FAGOTER", "FAGOTEUR", "FAGOTEUSE", "FAGOTIER",
    "FAIBLE", "FAIBLEMENT", "FAIBLESSE", "FAIENCE", "FAIENCIER",
    "FAIENCIÈRE", "FAIGNANT", "FAIGNANTE", "FAIGNANTISE", "FAIGNER",
    "FAILLE", "FAILLER", "FAILLI", "FAILLITE", "FAILLITIER",
    "FAIN", "FAINE", "FAINÉANT", "FAINÉANTE", "FAINÉANTISE",
    "FAIRE", "FAIRE-PART", "FAIRE-VALOIR", "FAISABILITÉ", "FAISABLE",
    "FAISAN", "FAISANDAGE", "FAISANDER", "FAISANE", "FAISEUR",
    "FAISEUSE", "FAIT", "FAITE", "FAITAGE", "FAÎTIER",
    "FAÎTIÈRE", "FAITS", "FAITOUT", "FAKIR", "FALAFEL",
    "FALAISE", "FALBALA", "FALBALAS", "FALCON", "FALCONIDÉS",
    "FALCONNERIE", "FALCONNIER", "FALE", "FALLACIE", "FALLACIEUX",
    "FALLACIEUSE", "FALLOIR", "FALOT", "FALOTE", "FALOURDE",
    "FALSIFIABLE", "FALSIFICATION", "FALSIFIER", "FALSIFICATEUR", "FALSIFICATRICE",
    "FALSITÉ", "FALUN", "FALUNS", "FAMÉLIQUE", "FAMÉLUS",
    "FAMILIAL", "FAMILIALE", "FAMILIALEMENT", "FAMILIARISATION", "FAMILIARISER",
    "FAMILIARITÉ", "FAMILIER", "FAMILIÈRE", "FAMILIÈREMENT", "FAMILLE",
    "FAMILLES", "FAMINE", "FAMINÉ", "FAMINÉE", "FANAGE",
    "FANAISON", "FANANT", "FANATE", "FANATIQUE", "FANATISME",
    "FANATISER", "FANÉ", "FANER", "FANFAN", "FANFARON",
    "FANFARONNADE", "FANFARONNER", "FANFARONNEUR", "FANFARONNEUSE", "FANION",
    "FANON", "FANONS", "FANTASIA", "FANTASIE", "FANTASIER",
    "FANTASMAGORIE", "FANTASMAGORIQUE", "FANTASMATIQUE", "FANTASME", "FANTASMER",
    "FANTASQUE", "FANTASSIN", "FANTASSINS", "FANTIN", "FANTOCHE",
    "FANTOMATIQUE", "FANTÔME", "FANTÔMES", "FAON", "FAONNER",
    "FAQUIN", "FARAD", "FARADAY", "FARANDOLE", "FARANDOLER",
    "FARCE", "FARCEUR", "FARCEUSE", "FARCIN", "FARCIR",
    "FARCISSURE", "FARD", "FARDER", "FARDEAU", "FARDEAUX",
    "FARDIER", "FARE", "FARFADET", "FARFADETS", "FARIBOLE",
    "FARIGOULE", "FARINACE", "FARINACÉ", "FARINACÉE", "FARINE",
    "FARINER", "FARINIER", "FARINIÈRE", "FARINOSITÉ", "FARIO",
    "FARLOUSE", "FARMER", "FAROUCHE", "FAROUCHEMENT", "FARRAGO",
    "FARTASSIER", "FARTASSIÈRE", "FARTER", "FASCE", "FASCES",
    "FASCIA", "FASCIATION", "FASCICULE", "FASCICULÉ", "FASCICULER",
    "FASCINANT", "FASCINANTE", "FASCINATION", "FASCINER", "FASCIE",
    "FASCISME", "FASCISTE", "FASÉOLA", "FASÉOLE", "FASEYER",
    "FASEYEUR", "FASEYEUSE", "FASSER", "FASTE", "FASTES",
    "FASTIDIEUX", "FASTIDIEUSE", "FASTIDIEUSEMENT", "FASTIGIE", "FASTUEUX",
    "FASTUEUSE", "FASTUEUSEMENT", "FAT", "FATAL", "FATALE",
    "FATALEMENT", "FATALISME", "FATALISTE", "FATALITÉ", "FATIGABLE",
    "FATIGANT", "FATIGANTE", "FATIGANTEMENT", "FATIGUE", "FATIGUER",
    "FATRAS", "FATRASIE", "FATU", "FATUITÉ", "FATUITÉS",
    "FAUBERG", "FAUBOURG", "FAUBOURGS", "FAUCARD", "FAUCARDE",
    "FAUCARDER", "FAUCHAGE", "FAUCHARD", "FAUCHER", "FAUCHET",
    "FAUCHEUX", "FAUCHEUR", "FAUCHEUSE", "FAUCILLE", "FAUCON",
    "FAUCONNER", "FAUCONNERIE", "FAUCONNIER", "FAUDRA", "FAUDRAIT",
    "FAUNE", "FAUNES", "FAUNIQUE", "FAUNISTE", "FAUNISTIQUE",
    "FAUSSE", "FAUSSEMENT", "FAUSSETÉ", "FAUSSAIRE", "FAUSSARIAT",
    "FAUSSE-COUCHE", "FAUSSE-MONNAIE", "FAUSSE-NOUVELLE", "FAUSSE-NOUVELLES", "FAUSSE-PASSE",
    "FAUSSE-POSTE", "FAUSSE-TREIZE", "FAUSSER", "FAUST", "FAUSTIEN",
    "FAUSTIENNE", "FAUT", "FAUTE", "FAUTEUX", "FAUTEUIL",
    "FAUTEUILS", "FAUTER", "FAUTES", "FAUTIF", "FAUTIVE",
    "FAUTIVEMENT", "FAUVE", "FAUVES", "FAUVETTE", "FAUVISME",
    "FAUVISTE", "FAUX", "FAUX-BOURDON", "FAUX-COL", "FAUX-FUYANT",
    "FAUX-JETON", "FAUX-NEZ", "FAUX-PAS", "FAUX-PLOI", "FAUX-SEMBLANT",
    "FAUX-SEMBLANTS", "FAVEUR", "FAVEURS", "FAVORABLE", "FAVORABLEMENT",
    "FAVORI", "FAVORIS", "FAVORISER", "FAVORITISME", "FAYARD",
    "FAYOT", "FAYOTAGE", "FAYOTER", "FAYOTTE", "FAYOTTER",
    "FÉAL", "FÉALE", "FÉALITÉ", "FÉCAL", "FÉCALE",
    "FÉCALITÉ", "FÉCOND", "FÉCONDANT", "FÉCONDANTE", "FÉCONDER",
    "FÉCONDITÉ", "FÉCULE", "FÉCULENT", "FÉCULENTE", "FÉCULERIE",
    "FÉCULIER", "FÉCULIÈRE", "FÉDÉRAL", "FÉDÉRALE", "FÉDÉRALISME",
    "FÉDÉRALISTE", "FÉDÉRATION", "FÉDÉRATIVE", "FÉDÉRÉ", "FÉDÉRER",
    "FÉERIE", "FÉERIQUE", "FÉERIQUEMENT", "FÉE", "FÉES",
    "FÉLIN", "FÉLINS", "FÉLINITÉ", "FÉLOCITÉ", "FÉLON",
    "FÉLONIE", "FÉLONNEMENT", "FÉLY", "FÉMININ", "FÉMININE",
    "FÉMININITÉ", "FÉMINISATION", "FÉMINISER", "FÉMINISME", "FÉMINISTE",
    "FÉMORAL", "FÉMORALE", "FÉMUR", "FENÊTRE", "FENÊTRAGE",
    "FENÊTRER", "FENIL", "FENNEC", "FENTE", "FENTES",
    "FÉODAL", "FÉODALE", "FÉODALISME", "FÉODALITÉ", "FÉODAUX",
    "FÉRALE", "FÉRALITÉ", "FÉRIAL", "FÉRIALE", "FÉRIE",
    "FÉRIÉ", "FÉRIÉE", "FÉROCE", "FÉROCEMENT", "FÉROCITÉ",
    "FÉRODO", "FÉRONIA", "FÉRONIE", "FÉRRE", "FERRAGE",
    "FERRAND", "FERRANDIÈRE", "FERRARA", "FERRARI", "FERRARISTE",
    "FERRE", "FERRER", "FERRET", "FERRETER", "FERRETERIE",
    "FERREUX", "FERREUSE", "FERRURE", "FERRURES", "FERVEUR",
    "FERVENT", "FERVENTE", "FERVENTEMENT", "FESSE", "FESSES",
    "FESSIER", "FESSU", "FESSUE", "FESTIN", "FESTINER",
    "FESTIVAL", "FESTIVALIER", "FESTIVALIÈRE", "FESTIVITÉ", "FESTIVITÉS",
    "FESTOIEMENT", "FESTOYER", "FESTOYEUR", "FESTOYEUSE", "FÊTARD",
    "FÊTARDE", "FÊTE", "FÊTER", "FÊTES", "FÊTICHE",
    "FÊTICHISME", "FÊTICHISTE", "FÊTU", "FÊTUE", "FEU",
    "FEUILLAGE", "FEUILLARD", "FEUILLARDE", "FEUILLE", "FEUILLET",
    "FEUILLETAGE", "FEUILLETÉ", "FEUILLETÉE", "FEUILLETER", "FEUILLETIS",
    "FEUILLETON", "FEUILLETONISTE", "FEUILLEUSE", "FEUILLU", "FEUILLUE",
    "FEULER", "FEUTRAGE", "FEUTRER", "FEUTRE", "FEUTRES",
    "FEUTRINE", "FEUX", "FÉVRIER", "FIABILITÉ", "FIABLE",
    "FIACRE", "FIANCÉ", "FIANCÉE", "FIANCER", "FIANCÉS",
    "FIANCÉES", "FIASCO", "FIBRE", "FIBRES", "FIBREUX",
    "FIBREUSE", "FIBRILLAIRE", "FIBRILLATION", "FIBRILLER", "FIBROBLASTE",
    "FIBROME", "FIBRONECTINE", "FIBROSE", "FIBROSER", "FIBROUS",
    "FICELAGE", "FICELER", "FICELEUR", "FICELEUSE", "FICHAGE",
    "FICHE", "FICHER", "FICHIER", "FICHIERS", "FICHISTE",
    "FICHU", "FICHUE", "FICUS", "FIEFFÉ", "FIEFFÉE",
    "FIEL", "FIÈRE", "FIÈREMENT", "FIER", "FIERTÉ",
    "FIÈVRE", "FIÈVREUX", "FIÈVREUSE", "FIÈVREUSEMENT", "FIFRE",
    "FIFRES", "FIGARO", "FIGE", "FIGÉ", "FIGÉE",
    "FIGER", "FIGNOLER", "FIGNOLERIE", "FIGUE", "FIGUIER",
    "FIGUER", "FIGUISTE", "FIGURANT", "FIGURANTE", "FIGURATION",
    "FIGURATIF", "FIGURATIVE", "FIGURATIVEMENT", "FIGURE", "FIGURÉ",
    "FIGURÉE", "FIGURER", "FIGURINISTE", "FIGURINE", "FIL",
    "FILAGE", "FILAMENT", "FILAMENTEUX", "FILAMENTS", "FILANDRE",
    "FILANDRIER", "FILANDRIÈRE", "FILANTE", "FILANTES", "FILASSIER",
    "FILASSIÈRE", "FILATURE", "FILDEFER", "FILE", "FILEMENT",
    "FILER", "FILET", "FILETAGE", "FILETER", "FILETS",
    "FILEUR", "FILEUSE", "FILIAL", "FILIALE", "FILIALES",
    "FILIATION", "FILIATRE", "FILIBUSTIER", "FILICINÉE", "FILIGRANE",
    "FILIGRANER", "FILIN", "FILING", "FILIOQUE", "FILLE",
    "FILLEUL", "FILLEULE", "FILLES", "FILLETTE", "FILLEUL",
    "FILM", "FILMAGE", "FILMER", "FILMEUR", "FILMEUSE",
    "FILMOGRAPHIE", "FILMOGRAPHIQUE", "FILON", "FILONIEN", "FILONIENNE",
    "FILOSOPHIE", "FILOSOPHER", "FILOSOPHIQUE", "FILOSOPHIQUEMENT", "FILOSOPHES",
    "FILOU", "FILOUTER", "FILOUTERIE", "FILS", "FILTRE",
    "FILTRAGE", "FILTRANT", "FILTRANTE", "FILTRAT", "FILTRATION",
    "FILTRE-PRESSE", "FILTRER", "FIN", "FINALEMENT", "FINAL",
    "FINALE", "FINALES", "FINALISATION", "FINALISER", "FINALISTE",
    "FINANCE", "FINANCÉ", "FINANCÉE", "FINANCER", "FINANCES",
    "FINANCIER", "FINANCIÈRE", "FINANCIÈREMENT", "FINANCIERS", "FINANCIÈRES",
    "FINASSER", "FINASSERIE", "FINASSIER", "FINASSIÈRE", "FINAUD",
    "FINAUDE", "FINAUDER", "FINAUDERIE", "FINE", "FINEMENT",
    "FINESSE", "FINETTE", "FINI", "FINIR", "FINISSAGE",
    "FINISSEUR", "FINISSEUSE", "FINISTÈRE", "FINITION", "FINLAND",
    "FINLANDAIS", "FINLANDAISE", "FINNOIS", "FINNOISE", "FINS",
    "FIOLE", "FIOLES", "FION", "FIORD", "FIORDS",
    "FIRMAMENT", "FIRME", "FIRMES", "FIRMWARE", "FISC",
    "FISCAL", "FISCALE", "FISCALEMENT", "FISCALISATION", "FISCALISER",
    "FISCALITÉ", "FISCAUX", "FISCHER", "FISSE", "FISSILE",
    "FISSION", "FISSIONNER", "FISSURAIT", "FISSURE", "FISSURER",
    "FISTON", "FISTONS", "FISTULE", "FIXATION", "FIXE",
    "FIXEMENT", "FIXER", "FIXES", "FIXETTE", "FIXISME",
    "FIXISTE", "FIXITÉ", "FLAC", "FLACON", "FLACONS",
    "FLAGELLAIRE", "FLAGELLANT", "FLAGELLANTE", "FLAGELLATION", "FLAGELLER",
    "FLAGELLET", "FLAGORNER", "FLAGORNERIE", "FLAGORNEUR", "FLAGORNEUSE",
    "FLAGRANT", "FLAGRANTE", "FLAGRANTEMENT", "FLAGRER", "FLAIR",
    "FLAIRER", "FLAIREUR", "FLAIREUSE", "FLAME", "FLAMES",
    "FLAMENCO", "FLAMER", "FLAMME", "FLAMMES", "FLAMMÈCHE",
    "FLAMMÈCHES", "FLAMMEUR", "FLAMMEUSE", "FLAN", "FLANC",
    "FLANC-GARDE", "FLANC-GARDER", "FLANELLE", "FLANER", "FLANEUR",
    "FLANEUSE", "FLANQUER", "FLAP", "FLASH", "FLASH-BACK",
    "FLASHER", "FLASQUE", "FLAT", "FLATTER", "FLATTEUR",
    "FLATTEUSE", "FLATTEUSEMENT", "FLATULENCE", "FLATULENT", "FLATULENTE",
    "FLAVEUR", "FLAVOR", "FLAW", "FLECHE", "FLÈCHE",
    "FLÈCHER", "FLÈCHES", "FLECHETTE", "FLECHETTES", "FLEGMATIQUE",
    "FLEGMATIQUEMENT", "FLEGME", "FLEMMARD", "FLEMMARDE", "FLEMMARDER",
    "FLEMMARDERIE", "FLEMMATIQUE", "FLEMMATIQUEMENT", "FLEMMING", "FLEMMINGITE",
    "FLENNE", "FLÉOLE", "FLERTE", "FLERTER", "FLETTRI",
    "FLETTRIR", "FLEUR", "FLEURAGE", "FLEURDELISÉ", "FLEURDELISÉE",
    "FLEURET", "FLEURETER", "FLEURETTE", "FLEURI", "FLEURIE",
    "FLEURIR", "FLEURISTE", "FLEURON", "FLEURONS", "FLEUVE",
    "FLEUVES", "FLEXIBILITÉ", "FLEXIBLE", "FLEXION", "FLEXIONNER",
    "FLEXUEL", "FLEXUELLE", "FLEXUM", "FLEXURA", "FLIC",
    "FLICS", "FLINGOT", "FLINGOTS", "FLINGUE", "FLINGUER",
    "FLINT", "FLIP", "FLIPPER", "FLIPPOT", "FLIPPOTER",
    "FLIQUER", "FLIRT", "FLIRTER", "FLIRTEUR", "FLIRTEUSE",
    "FLOC", "FLOCAGE", "FLOCON", "FLOCONS", "FLOCONNER",
    "FLOCONNEUX", "FLOCONNEUSE", "FLORE", "FLORENTIN", "FLORENTINE",
    "FLORÈS", "FLORICOLE", "FLORICULTURE", "FLORIDIEN", "FLORIDIENNE",
    "FLORILÈGE", "FLORIN", "FLORINS", "FLORISSANT", "FLORISSANTE",
    "FLORISTE", "FLOSS", "FLOSSER", "FLOT", "FLOTS",
    "FLOTTABILITÉ", "FLOTTANT", "FLOTTANTE", "FLOTTARD", "FLOTTARDE",
    "FLOTTE", "FLOTTER", "FLOTTEUR", "FLOTTILLE", "FLOTTIS",
    "FLOU", "FLOUE", "FLOUER", "FLOUS", "FLOUSE",
    "FLOUX", "FLOW", "FLOW-CHART", "FLUAGE", "FLUER",
    "FLUET", "FLUETTE", "FLUIDE", "FLUIDES", "FLUIDIFIANT",
    "FLUIDIFIER", "FLUIDITÉ", "FLUO", "FLUOR", "FLUORÉ",
    "FLUORER", "FLUORESCENCE", "FLUORESCENT", "FLUORESCENTE", "FLUORHYDRIQUE",
    "FLUORITE", "FLUOROSE", "FLUORURER", "FLUSH", "FLUSHING",
    "FLUTE", "FLÛTE", "FLÛTEAU", "FLÛTES", "FLÛTISTE",
    "FLUX", "FLUXION", "FLUXIONS", "FLY", "FLYING",
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
        'FABLE': 'Récit court à visée morale.',
        'FABLIAU': 'Récit médiéval comique.',
        'FABLIER': 'Recueil de fables.',
        'FABRIQUER': 'Produire, fabriquer.',
        'FABRIQUE': 'Usine ou lieu de fabrication.',
        'FABULEUX': 'Extraordinaire, merveilleux.',
        'FABULISTE': 'Auteur de fables.',
        'FACADE': 'Partie avant d\'un bâtiment.',
        'FACÉTIE': 'Plaisanterie, trait d\'esprit.',
        'FACÉTIEUX': 'Qui aime faire des plaisanteries.',
        'FACHER': 'Mettre en colère.',
        'FACHEUX': 'Qui fâche, désagréable.',
        'FACILE': 'Qui est aisé, sans difficulté.',
        'FACILEMENT': 'Sans difficulté.',
        'FACILITÉ': 'Aisance, absence de difficulté.',
        'FACILITER': 'Rendre plus facile.',
        'FACON': 'Manière de faire.',
        'FAÇONNER': 'Donner une forme.',
        'FACTAGE': 'Action de facturer.',
        'FACTEUR': 'Personne qui distribue le courrier.',
        'FACTICE': 'Artificiel, faux.',
        'FACTION': 'Groupe organisé.',
        'FACTIONNAIRE': 'Membre d\'une faction.',
        'FACTITIF': 'Artificiel, non naturel.',
        'FACTO': 'De fait, en réalité.',
        'FACTORER': 'Décomposer en facteurs.',
        'FACTORIEL': 'Produit des entiers de 1 à n.',
        'FACTORISATION': 'Décomposition en facteurs.',
        'FACTORISER': 'Décomposer en facteurs.',
        'FACTORY': 'Usine en anglais.',
        'FACTOTUM': 'Personne à tout faire.',
        'FACTUEL': 'Basé sur des faits.',
        'FACTURE': 'Document commercial ou manière de jouer.',
        'FACTURER': 'Établir une facture.',
        'FACULTATIF': 'Qui n\'est pas obligatoire.',
        'FACULTÉ': 'Capacité ou établissement d\'enseignement.',
        'FADAIS': 'Absurde, déraisonnable.',
        'FADAISER': 'Dire des fadaises.',
        'FADE': 'Sans goût, terne.',
        'FADER': 'Devenir fade.',
        'FAGOT': 'Liaison de branches.',
        'FAGOTAGE': 'Action de faire des fagots.',
        'FAGOTER': 'Faire des fagots.',
        'FAIBLE': 'Qui manque de force ou d\'intensité.',
        'FAIBLEMENT': 'De manière faible.',
        'FAIBLESSE': 'Manque de force.',
        'FAIENCE': 'Céramique émaillée.',
        'FAIENCIER': 'Fabricant de faïence.',
        'FAIGNANT': 'Qui évite le travail.',
        'FAIGNANTE': 'Qui évite le travail.',
        'FAIGNANTISE': 'Paresse.',
        'FAIRE': 'Action de faire.',
        'FAISABILITÉ': 'Possibilité de réaliser.',
        'FAISABLE': 'Qui peut être fait.',
        'FAISAN': 'Oiseau gallinacé.',
        'FAISANDAGE': 'Action de faisander.',
        'FAISANDER': 'Laisser se décomposer légèrement.',
        'FAISANE': 'Femelle du faisan.',
        'FAISEUR': 'Personne qui fait quelque chose.',
        'FAIT': 'Action accomplie.',
        'FAITAGE': 'Partie supérieure d\'un toit.',
        'FAÎTIER': 'Ouvrier qui pose les faîtages.',
        'FAITOUT': 'Récipient de cuisine.',
        'FAKIR': 'Ascète musulman.',
        'FALAFEL': 'Spécialité culinaire.',
        'FALAISE': 'Paroi rocheuse verticale.',
        'FALBALA': 'Ornement, fanfreluche.',
        'FALCON': 'Oiseau de proie.',
        'FALCONIDÉS': 'Famille des faucons.',
        'FALCONNERIE': 'Art de chasser avec des faucons.',
        'FALCONNIER': 'Personne qui pratique la fauconnerie.',
        'FALLACIE': 'Raisonnement erroné.',
        'FALLACIEUX': 'Qui contient des fallacies.',
        'FALLOIR': 'Devoir, être nécessaire.',
        'FALOT': 'Lumière faible.',
        'FALSIFIABLE': 'Qui peut être falsifié.',
        'FALSIFICATION': 'Action de falsifier.',
        'FALSIFIER': 'Rendre faux.',
        'FALSITÉ': 'Caractère de ce qui est faux.',
        'FALUN': 'Terre colorante.',
        'FAMÉLIQUE': 'Relatif à la famille.',
        'FAMILIAL': 'Relatif à la famille.',
        'FAMILIALE': 'Relatif à la famille.',
        'FAMILIARISATION': 'Action de familiariser.',
        'FAMILIARISER': 'Rendre familier.',
        'FAMILIARITÉ': 'Connaissance intime.',
        'FAMILIER': 'Qui est connu, habituel.',
        'FAMILLE': 'Groupe de personnes apparentées.',
        'FAMINE': 'Pénurie de nourriture.',
        'FAMINÉ': 'Qui souffre de la famine.',
        'FANAGE': 'Action de faner.',
        'FANAISON': 'Action de faner.',
        'FANANT': 'Qui fane.',
        'FANATE': 'Qui fane.',
        'FANATIQUE': 'Qui est fanatique.',
        'FANATISME': 'Adhésion excessive à une croyance.',
        'FANATISER': 'Rendre fanatique.',
        'FANÉ': 'Qui a perdu sa fraîcheur.',
        'FANER': 'Perder sa fraîcheur.',
        'FANFARON': 'Qui se vante.',
        'FANFARONNADE': 'Vantardise.',
        'FANFARONNER': 'Se vanter.',
        'FANFARONNEUR': 'Qui fanfaronne.',
        'FANION': 'Petit drapeau.',
        'FANON': 'Pli de peau.',
        'FANTASIA': 'Composition musicale.',
        'FANTASIE': 'Imagination créatrice.',
        'FANTASIER': 'Créer des fantasies.',
        'FANTASMAGORIE': 'Spectacle de prestidigitateur.',
        'FANTASMAGORIQUE': 'Qui relève de la fantasmagorie.',
        'FANTASMATIQUE': 'Relatif aux fantasmes.',
        'FANTASME': 'Image mentale.',
        'FANTASMER': 'Avoir des fantasmes.',
        'FANTASQUE': 'Bizarre, extravagant.',
        'FANTASSIN': 'Soldat d\'infanterie.',
        'FANTIN': 'Marionnette.',
        'FANTOCHE': 'Personnage grotesque.',
        'FANTOMATIQUE': 'Relatif aux fantômes.',
        'FANTÔME': 'Esprit, apparition.',
        'FAON': 'Jeune cerf.',
        'FAONNER': 'Donner une forme.',
        'FAQUIN': 'Personnage grotesque.',
        'FARAD': 'Unité de capacité électrique.',
        'FARANDOLE': 'Danse traditionnelle.',
        'FARANDOLER': 'Danser la farandole.',
        'FARCE': 'Pièce comique.',
        'FARCEUR': 'Qui aime faire des farces.',
        'FARCEUSE': 'Qui aime faire des farces.',
        'FARCIN': 'Champignon parasite.',
        'FARCIR': 'Remplir.',
        'FARD': 'Cosmétique.',
        'FARDER': 'Appliquer du fard.',
        'FARDEAU': 'Charge lourde.',
        'FARDIER': 'Charrette.',
        'FARE': 'Repas en anglais.',
        'FARFADET': 'Lutin.',
        'FARIBOLE': 'Parole creuse.',
        'FARIGOULE': 'Plante aromatique.',
        'FARINACE': 'Riche en farine.',
        'FARINE': 'Poudre obtenue par la mouture des céréales.',
        'FARINER': 'Recouvrir de farine.',
        'FARINIER': 'Marchand de farine.',
        'FARINOSITÉ': 'Qualité de ce qui est farineux.',
        'FARIO': 'Truite.',
        'FARLOUSE': 'Trompeuse.',
        'FARMER': 'Louer une ferme.',
        'FAROUCHE': 'Sauvage, timide.',
        'FAROUCHEMENT': 'De manière farouche.',
        'FARRAGO': 'Mélange confus.',
        'FARTASSIER': 'Paresseux.',
        'FARTER': 'Appliquer un fard.',
        'FASCE': 'Bande.',
        'FASCIA': 'Bande de tissu.',
        'FASCIATION': 'Anomalie végétale.',
        'FASCICULE': 'Petit faisceau.',
        'FASCICULÉ': 'En fascicules.',
        'FASCICULER': 'Diviser en fascicules.',
        'FASCINANT': 'Qui fascine.',
        'FASCINANTE': 'Qui fascine.',
        'FASCINATION': 'État de fascination.',
        'FASCINER': 'Attirer irrésistiblement.',
        'FASCIE': 'Bande.',
        'FASCISME': 'Idéologie autoritaire.',
        'FASCISTE': 'Partisan du fascisme.',
        'FASÉOLA': 'Plante.',
        'FASÉOLE': 'Haricot.',
        'FASEYER': 'Parler de manière affectée.',
        'FASEYEUR': 'Qui faseye.',
        'FASEYEUSE': 'Qui faseye.',
        'FASSER': 'Se fâcher.',
        'FASTE': 'Splendeur.',
        'FASTES': 'Cérémonies solennelles.',
        'FASTIDIEUX': 'Ennuyeux.',
        'FASTIDIEUSE': 'Ennuyeuse.',
        'FASTIDIEUSEMENT': 'De manière fastidieuse.',
        'FASTIGIE': 'Ornement architectural.',
        'FASTUEUX': 'Somptueux.',
        'FASTUEUSE': 'Somptueuse.',
        'FASTUEUSEMENT': 'De manière fastueuse.',
        'FAT': 'Destin.',
        'FATAL': 'Inévitable.',
        'FATALE': 'Inévitable.',
        'FATALEMENT': 'De manière fatale.',
        'FATALISME': 'Croyance en la fatalité.',
        'FATALISTE': 'Partisan du fatalisme.',
        'FATALITÉ': 'Caractère de ce qui est fatal.',
        'FATIGABLE': 'Qui peut être fatigué.',
        'FATIGANT': 'Qui fatigue.',
        'FATIGANTE': 'Qui fatigue.',
        'FATIGANTEMENT': 'De manière fatigante.',
        'FATIGUE': 'État de lassitude.',
        'FATIGUER': 'Rendre fatigué.',
        'FATRAS': 'Amas confus.',
        'FATRASIE': 'Style confus.',
        'FATU': 'Prétentieux.',
        'FATUITÉ': 'Caractère de ce qui est fat.',
        'FAUBERG': 'Quartier périphérique.',
        'FAUBOURG': 'Quartier périphérique.',
        'FAUCARD': 'Outil agricole.',
        'FAUCARDE': 'Outil agricole.',
        'FAUCARDER': 'Travail avec la faucarde.',
        'FAUCHAGE': 'Action de faucher.',
        'FAUCHARD': 'Outil pour faucher.',
        'FAUCHER': 'Couper l\'herbe.',
        'FAUCHEUR': 'Personne qui fauche.',
        'FAUCHEUSE': 'Machine pour faucher.',
        'FAUCILLE': 'Outil pour couper.',
        'FAUCON': 'Oiseau de proie.',
        'FAUCONNER': 'Chasser avec des faucons.',
        'FAUCONNERIE': 'Art de la fauconnerie.',
        'FAUCONNIER': 'Pratiquant de la fauconnerie.',
        'FAUDRA': 'Futur de falloir.',
        'FAUDRAIT': 'Conditionnel de falloir.',
        'FAUNE': 'Ensemble des animaux.',
        'FAUNIQUE': 'Relatif à la faune.',
        'FAUNISTE': 'Spécialiste de la faune.',
        'FAUNISTIQUE': 'Relatif à la faune.',
        'FAUSSE': 'Féminin de faux.',
        'FAUSSEMENT': 'De manière fausse.',
        'FAUSSETÉ': 'Caractère de ce qui est faux.',
        'FAUSSAIRE': 'Qui commet des faux.',
        'FAUSSARIAT': 'Action de fausser.',
        'FAUSSE-COUCHE': 'Avortement spontané.',
        'FAUSSE-MONNAIE': 'Monnaie contrefaite.',
        'FAUSSE-NOUVELLE': 'Nouvelle fausse.',
        'FAUSSE-PASSE': 'Passe faux.',
        'FAUSSE-POSTE': 'Poste fausse.',
        'FAUSSE-TREIZE': 'Jeu de cartes.',
        'FAUSSER': 'Rendre faux.',
        'FAUST': 'Personnage légendaire.',
        'FAUSTIEN': 'Relatif à Faust.',
        'FAUSTIENNE': 'Relatif à Faust.',
        'FAUT': 'Il faut.',
        'FAUTE': 'Erreur ou manquement.',
        'FAUTEUIL': 'Siège confortable.',
        'FAUTEUX': 'Qui commet des fautes.',
        'FAUTIF': 'Qui contient des fautes.',
        'FAUTIVE': 'Qui contient des fautes.',
        'FAUTIVEMENT': 'De manière fautive.',
        'FAUVE': 'Animal sauvage.',
        'FAUVES': 'Mouvement artistique.',
        'FAUVETTE': 'Petit oiseau.',
        'FAUVISME': 'Mouvement artistique.',
        'FAUVISTE': 'Partisan du fauvisme.',
        'FAUX': 'Qui n\'est pas vrai.',
        'FAUX-BOURDON': 'Abeille mâle.',
        'FAUX-COL': 'Col faux.',
        'FAUX-FUYANT': 'Qui fuit.',
        'FAUX-JETON': 'Qui joue un rôle.',
        'FAUX-NEZ': 'Nez postiche.',
        'FAUX-PAS': 'Erreur de conduite.',
        'FAUX-PLOI': 'Pli mal fait.',
        'FAUX-SEMBLANT': 'Apparence trompeuse.',
        'FAVEUR': 'Bienveillance.',
        'FAVEURS': 'Bienveillances.',
        'FAVORABLE': 'Qui est propice.',
        'FAVORABLEMENT': 'De manière favorable.',
        'FAVORI': 'Préféré.',
        'FAVORIS': 'Préférés.',
        'FAVORISER': 'Rendre favorable.',
        'FAVORITISME': 'Préférence injuste.',
        'FAYARD': 'Arbre.',
        'FAYOT': 'Élève qui cherche à plaire.',
        'FAYOTAGE': 'Action de fayoter.',
        'FAYOTER': 'Chercher à plaire.',
        'FAYOTTE': 'Féminin de fayot.',
        'FAYOTTER': 'Fayoter.',
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
        'FABLE': [
            'La fable du corbeau et du renard est célèbre.',
            'J\'aime lire des fables avant de dormir.',
            'Cette fable a une morale intéressante.'
        ],
        'FABRIQUER': [
            'Il fabrique des meubles en bois.',
            'Cette usine fabrique des voitures.',
            'Elle a fabriqué une robe elle-même.'
        ],
        'FABRIQUE': [
            'La fabrique de chocolat est très connue.',
            'Il travaille dans une fabrique.',
            'La fabrique a fermé ses portes.'
        ],
        'FABULEUX': [
            'Le spectacle était fabuleux.',
            'C\'est une histoire fabuleuse.',
            'Il a gagné un fabuleux cadeau.'
        ],
        'FACADE': [
            'La façade de l\'immeuble est en pierre.',
            'Il faut nettoyer la façade.',
            'La façade a été rénovée.'
        ],
        'FACILE': [
            'Ce problème est facile à résoudre.',
            'C\'est une question facile.',
            'Il a trouvé une solution facile.'
        ],
        'FACILEMENT': [
            'Il résout les problèmes facilement.',
            'Elle s\'adapte facilement aux changements.',
            'On peut facilement se tromper.'
        ],
        'FAIRE': [
            'Je vais faire un gâteau.',
            'Il faut faire attention.',
            'Qu\'est-ce que tu fais?'
        ],
        'FAISAN': [
            'Le faisan est un oiseau magnifique.',
            'Nous avons vu un faisan dans la forêt.',
            'Le faisan est souvent chassé.'
        ],
        'FAIT': [
            'C\'est un fait avéré.',
            'Le fait est indéniable.',
            'Il a accompli un fait remarquable.'
        ],
        'FAMILLE': [
            'Ma famille est très unie.',
            'Nous avons passé les vacances en famille.',
            'La famille est importante.'
        ],
        'FAMINE': [
            'La famine frappe de nombreux pays.',
            'Il y a eu une famine au XIXe siècle.',
            'La famine est une tragédie.'
        ],
        'FANFARON': [
            'C\'est un fanfaron qui se vante toujours.',
            'Le fanfaron a été ridiculisé.',
            'Il joue les fanfarons.'
        ],
        'FANTASIE': [
            'Il a une imagination débordante de fantasie.',
            'Cette histoire est pure fantasie.',
            'La fantasie peut être créative.'
        ],
        'FANTASME': [
            'Le fantasme est une création de l\'esprit.',
            'Il a des fantasmes étranges.',
            'Le fantasme peut devenir réalité.'
        ],
        'FANTÔME': [
            'Il croit aux fantômes.',
            'Le fantôme hante cette maison.',
            'J\'ai vu un fantôme dans mes rêves.'
        ],
        'FARCE': [
            'Il a fait une farce à son ami.',
            'La farce était très drôle.',
            'Les enfants aiment les farces.'
        ],
        'FARINE': [
            'J\'ai besoin de farine pour faire un gâteau.',
            'La farine est un ingrédient essentiel.',
            'Il a acheté un sac de farine.'
        ],
        'FAROUCHE': [
            'L\'animal est farouche et difficile à approcher.',
            'Il a un regard farouche.',
            'La farouche beauté de la nature.'
        ],
        'FASCISTE': [
            'Le fascisme est une idéologie dangereuse.',
            'Il combat les idées fascistes.',
            'Le fascisme a causé de grands malheurs.'
        ],
        'FATIGUE': [
            'Je suis très fatigué aujourd\'hui.',
            'La fatigue me terrase.',
            'Il souffre de fatigue chronique.'
        ],
        'FAUTE': [
            'J\'ai fait une faute d\'orthographe.',
            'C\'est de ma faute.',
            'Il a reconnu sa faute.'
        ],
        'FAUTEUIL': [
            'J\'aime me reposer dans mon fauteuil.',
            'Le fauteuil est très confortable.',
            'Il a acheté un nouveau fauteuil.'
        ],
        'FAUX': [
            'C\'est un faux document.',
            'Il porte une fausse barbe.',
            'Le faux est interdit.'
        ],
        'FAVEUR': [
            'Il a obtenu une faveur spéciale.',
            'Je te demande une faveur.',
            'La faveur du public est importante.'
        ],
        'FÉLICITATION': [
            'Félicitations pour ta réussite!',
            'Il a reçu des félicitations.',
            'Les félicitations sont méritées.'
        ],
        'FÉLICITER': [
            'Je te félicite pour ton travail.',
            'Il a été félicité par son patron.',
            'Félicitez-le pour son succès.'
        ],
        'FÉMININ': [
            'Le genre féminin est important.',
            'Elle a une beauté féminine.',
            'Le féminin l\'emporte.'
        ],
        'FÉODAL': [
            'Le système féodal était hiérarchisé.',
            'L\'époque féodale a duré des siècles.',
            'Les seigneurs féodaux avaient beaucoup de pouvoir.'
        ],
        'FÉROCE': [
            'Le lion est un animal féroce.',
            'Il a un regard féroce.',
            'La bataille a été féroce.'
        ],
        'FER': [
            'Le fer est un métal très utilisé.',
            'Il a un caractère de fer.',
            'Le fer à repasser est chaud.'
        ],
        'FERME': [
            'La ferme produit du lait et des œufs.',
            'Il travaille à la ferme.',
            'La ferme est bien tenue.'
        ],
        'FERMER': [
            'Ferme la porte, s\'il te plaît.',
            'Il a fermé les fenêtres.',
            'Fermez les yeux.'
        ],
        'FESTIN': [
            'Nous avons fait un festin pour son anniversaire.',
            'Le festin était somptueux.',
            'Il a organisé un grand festin.'
        ],
        'FESTIVAL': [
            'Le festival de musique a attiré beaucoup de monde.',
            'J\'aime aller aux festivals.',
            'Le festival de Cannes est célèbre.'
        ],
        'FÊTE': [
            'Nous avons fait une grande fête.',
            'C\'est mon anniversaire, je fais la fête.',
            'La fête était très animée.'
        ],
        'FEU': [
            'Le feu crée une atmosphère chaleureuse.',
            'Il a allumé un feu de camp.',
            'Attention au feu!' 
        ],
        'FEUILLE': [
            'La feuille de l\'arbre est verte.',
            'J\'ai ramassé une feuille d\'érable.',
            'Les feuilles tombent en automne.'
        ],
        'FIDÈLE': [
            'Il est fidèle à ses principes.',
            'C\'est un ami fidèle.',
            'La fidélité est importante.'
        ],
        'FIDÉLITÉ': [
            'La fidélité est une valeur importante.',
            'Il a juré fidélité.',
            'La fidélité conjugale est essentielle.'
        ],
        'FIER': [
            'Il est fier de son travail.',
            'Je suis fier de toi.',
            'Elle est fière de ses enfants.'
        ],
        'FIÈVRE': [
            'Il a de la fièvre.',
            'La fièvre peut être dangereuse.',
            'J\'ai eu une forte fièvre.'
        ],
        'FIGUE': [
            'J\'aime manger des figues.',
            'La figue est un fruit délicieux.',
            'Il a planté un figuier.'
        ],
        'FIGURER': [
            'Il figure parmi les meilleurs.',
            'Son nom figure sur la liste.',
            'Il figure en bonne place.'
        ],
        'FIL': [
            'Le fil est cassé.',
            'J\'ai besoin d\'un fil pour coudre.',
            'Le fil électrique est dangereux.'
        ],
        'FILE': [
            'Nous sommes en file d\'attente.',
            'La file avance lentement.',
            'Il a rejoint la file.'
        ],
        'FILER': [
            'Il file à toute vitesse.',
            'Le temps file.',
            'Elle a filé sans dire au revoir.'
        ],
        'FILLE': [
            'Ma fille a 10 ans.',
            'C\'est une belle fille.',
            'Il a une fille et un garçon.'
        ],
        'FILM': [
            'J\'aime regarder des films.',
            'Le film était très bon.',
            'Il a tourné un film.'
        ],
        'FILON': [
            'Il a trouvé un filon d\'or.',
            'C\'est un bon filon.',
            'Le filon est épuisé.'
        ],
        'FILS': [
            'Mon fils a 5 ans.',
            'C\'est mon fils aîné.',
            'Il a deux fils.'
        ],
        'FILTRE': [
            'Le filtre à café est nécessaire.',
            'Il a changé le filtre de la voiture.',
            'Le filtre à eau est important.'
        ],
        'FIN': [
            'C\'est la fin du film.',
            'La fin de l\'année approche.',
            'À la fin, tout s\'est bien passé.'
        ],
        'FINAL': [
            'C\'est le match final.',
            'La finale aura lieu demain.',
            'Il a atteint la finale.'
        ],
        'FINANCE': [
            'Les finances du pays sont saines.',
            'Il gère les finances de l\'entreprise.',
            'La finance est un domaine complexe.'
        ],
        'FINIR': [
            'Il faut finir le travail.',
            'J\'ai fini mon livre.',
            'Elle va finir ses études.'
        ],
        'FIOLE': [
            'La fiole contient un liquide mystérieux.',
            'Il a cassé la fiole.',
            'La fiole est en verre.'
        ],
        'FIRME': [
            'La firme est très connue.',
            'Il travaille pour une grande firme.',
            'La firme a fait faillite.'
        ],
        'FISCAL': [
            'La fiscalité est complexe.',
            'Il est inspecteur fiscal.',
            'Les impôts fiscaux sont élevés.'
        ],
        'FIXE': [
            'Le téléphone fixe est toujours utile.',
            'Il a un regard fixe.',
            'Le prix est fixe.'
        ],
        'FIXER': [
            'Il faut fixer une date.',
            'J\'ai fixé le rendez-vous.',
            'Fixez bien les règles.'
        ],
        'FLAMME': [
            'La flamme de la bougie vacille.',
            'La flamme olympique est un symbole.',
            'Il a allumé une flamme.'
        ],
        'FLAN': [
            'J\'aime le flan au caramel.',
            'Le flan est un dessert délicieux.',
            'Elle a préparé un flan.'
        ],
        'FLANC': [
            'Il a été blessé au flanc.',
            'Le flanc de la montagne est escarpé.',
            'Il se tient à mon flanc.'
        ],
        'FLASH': [
            'Le flash de l\'appareil photo est puissant.',
            'Il a eu un flash de génie.',
            'Le flash a éclairé la pièce.'
        ],
        'FLECHE': [
            'La flèche a atteint la cible.',
            'Il a tiré une flèche.',
            'La flèche du temps.'
        ],
        'FLEUR': [
            'La fleur est belle.',
            'J\'aime les fleurs.',
            'Il lui a offert une fleur.'
        ],
        'FLEUVE': [
            'Le fleuve coule vers la mer.',
            'Le fleuve Amazone est immense.',
            'Nous avons navigué sur le fleuve.'
        ],
        'FLOT': [
            'Le flot des vagues est puissant.',
            'Il a été emporté par le flot.',
            'Le flot de la marée.'
        ],
        'FLOTTE': [
            'La flotte est en mer.',
            'Il commande une flotte.',
            'La flotte de pêche.'
        ],
        'FLOU': [
            'L\'image est floue.',
            'C\'est un peu flou.',
            'Le flou artistique.'
        ],
        'FLUIDE': [
            'L\'eau est un fluide.',
            'Le mouvement est fluide.',
            'Un fluide visqueux.'
        ],
        'FLUTE': [
            'Il joue de la flûte.',
            'La flûte est un instrument à vent.',
            'J\'aime écouter la flûte.'
        ],
        'FLUX': [
            'Le flux de données est continu.',
            'Il y a un flux constant de visiteurs.',
            'Le flux sanguin.'
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
