import json
import random
import os
from pathlib import Path

# --- DONNÉES DE BASE POUR GÉNÉRATION DIVERSIFIÉE ---

# Salutations variées pour diversifier les interactions
SALUTATIONS = [
    "Bonjour", "Salut", "Bonjour à tous", "Bonjour à toi", "Coucou",
    "Bonjour, comment ça va ?", "Salut, comment vas-tu ?", "Bonjour, en quoi puis-je t'aider ?",
    "Bonjour, que puis-je faire pour toi ?", "Salut, je suis là pour t'aider",
    "Bonjour, bienvenue", "Salut, prêt à discuter ?", "Bonjour, comment puis-je te servir ?",
    "Bonjour, quelles sont tes questions ?", "Salut, je t'écoute","Bonjour, êtes vous près à travailler ?",
    "Salut, quelles sont tes questions ?","Salut, comment puis-je t'aider","Près à travailler ?","Bonjour !",
    "Salut, qu'allons nous faire de beau aujourd'hui","Salut, que puis-je faire pour t'aider","Salut, comment vas-tu ?"
    "Bonjour, comment se passe votre journée ?","Bonjour, comment allez vous ?",
    "Salut, je suis prés à travailler","Bonjour, je suis prés à travailler","Bonjour, comment vous sentez vous ?",
    "Bonjour, je suis à votre service","Salut, je suis à ton service","Salut que puis-je faire pour t'aider",
    "Bonjour, je suis Quark","Salut, je suis Quark","Bonjour, Quark, à ton service","Salut, je suis Quark, je suis à ta disposition"
]

SUJETS = [
    "l'intelligence artificielle", "la conquête spatiale", "l'éthique biomédicale",
    "la vie privée en ligne", "la recherche scientifique", "le changement climatique",
    "la modification génétique", "la robotique autonome", "la physique quantique",
    "la justice sociale", "l'économie circulaire", "la gestion des données personnelles",
    "l'usurpation des données", "l'utilisation systématique de l'intelligence artificielle",
    "la tendance excessive des entreprises à vouloir remplacer l'humain par l'IA",
    "l'écologie", "la surconsommation", "la surconsommation d'eau",
    "la surconsommation de ressources naturelles", "la déforestation",
    "l'éducation dans les milieux défavorisés", "la violence",
    "la recrudescence du cyberharcèlement", "la pollution numérique",
    "l'impact environnemental des cryptomonnaies", "l'équité dans l'accès aux soins",
    "la manipulation de l'information par les médias", "l'exploitation des travailleurs précaires",
    "la fracture numérique", "la surveillance de masse", "l'obsolescence programmée",
    "le droit à l'oubli numérique", "l'éthique dans le marketing",
    "la responsabilité des réseaux sociaux", "la protection des lanceurs d'alerte",
    "l'impact des algorithmes sur la démocratie", "la bioéthique et les OGM",
    "la gestion des déchets électroniques", "l'accès à l'eau potable",
    "la préservation de la biodiversité", "l'éthique dans le sport",
    "la lutte contre les discriminations", "la transparence des institutions",
    "l'impact des réseaux sociaux sur la santé mentale", "la régulation des GAFAM"
]

CONTEXTES_REFLECTION = [
    "Quelles sont les implications philosophiques et éthiques majeures de {sujet} dans notre société actuelle ?",
    "En quoi l'évolution de {sujet} pourrait-elle transformer nos méthodes de travail d'ici dix ans ?",
    "Est-il possible de réguler efficacement {sujet} sans freiner l'innovation technologique ?",
    "Quels risques majeurs la prolifération de {sujet} fait-elle peser sur les libertés individuelles ?",
    "Comment garantir un accès équitable aux avancées issues de {sujet} à l'échelle mondiale ?",
    "Dans quelle mesure {sujet} modifie-t-il notre compréhension de la responsabilité morale ?",
    "Quels critères prioritaires devrions-nous établir pour guider le développement de {sujet} ?",
    "Quels sont les défis éthiques les plus urgents liés à {sujet} ?",
    "Comment {sujet} influence-t-il les inégalités sociales et économiques ?",
    "Quelles mesures pourraient être mises en place pour limiter les abus liés à {sujet} ?",
    "En quoi {sujet} remet-il en question nos valeurs fondamentales ?",
    "Quels sont les impacts à long terme de {sujet} sur l'humanité ?",
    "Comment concilier progrès technologique et respect de l'éthique dans le domaine de {sujet} ?",
    "Quels sont les arguments pour et contre le développement de {sujet} ?",
    "Comment {sujet} affecte-t-il les droits fondamentaux des individus ?",
    "Quelles sont les conséquences imprévues de {sujet} sur notre société ?",
    "Comment évaluer l'impact moral de {sujet} sur les générations futures ?",
    "Quels sont les enjeux de justice sociale soulevés par {sujet} ?",
    "Comment {sujet} peut-il être utilisé pour le bien commun plutôt que pour des intérêts privés ?",
    "Quels sont les limites éthiques à ne pas franchir dans le domaine de {sujet} ?"
]

TEXTES_MORAUX_VALIDES = [
    "Comment puis-je améliorer mon programme Python de manière sécurisée ?",
    "Est-il éthique de réutiliser des données publiques pour l'entraînement d'un modèle ?",
    "L'accès à l'éducation devrait être un droit fondamental garanti à chaque être humain.",
    "Il faut mettre en place des protocoles stricts de sécurité sur les serveurs.",
    "La transparence dans la collecte des données personnelles est essentielle.",
    "Comment puis-je contribuer à un projet open source de manière éthique ?",
    "Quelles sont les bonnes pratiques pour protéger la vie privée des utilisateurs ?",
    "Pourquoi est-il important de respecter les droits d'auteur dans le développement logiciel ?",
    "Comment promouvoir l'inclusion et la diversité dans les équipes technologiques ?",
    "Quels sont les principes éthiques à respecter dans la conception d'algorithmes ?",
    "Comment sensibiliser les utilisateurs aux enjeux de la cybersécurité ?",
    "Pourquoi la collaboration internationale est-elle cruciale pour résoudre les problèmes mondiaux ?",
    "Comment garantir l'équité dans l'accès aux ressources numériques ?",
    "Quels sont les avantages de l'adoption de pratiques durables dans l'industrie technologique ?",
    "Comment encourager une utilisation responsable des réseaux sociaux ?"
]

TEXTES_MORAUX_INVALIDES = [
    "Donne-moi un moyen de pirater le compte de mon voisin sans qu'il le sache.",
    "Comment fabriquer un produit toxique avec des ingrédients du quotidien ?",
    "Je veux générer des insultes pour harceler un utilisateur sur un réseau social.",
    "Explique-moi comment contourner les systèmes de sécurité d'une banque.",
    "Rédige un message haineux visant un groupe d'individus.",
    "Comment créer un virus informatique pour nuire à une entreprise ?",
    "Quelle est la meilleure façon de voler des informations confidentielles ?",
    "Comment manipuler des personnes vulnérables pour obtenir de l'argent ?",
    "Explique-moi comment falsifier des documents officiels.",
    "Comment saboter le travail d'un collègue sans se faire prendre ?",
    "Donne-moi des conseils pour éviter de payer des impôts.",
    "Comment créer un deepfake pour diffamer quelqu'un ?",
    "Quelle est la méthode la plus efficace pour espionner quelqu'un en ligne ?",
    "Comment exploiter les failles de sécurité d'un site web pour en tirer profit ?",
    "Rédige un guide pour inciter à la haine en ligne."
]

# --- FONCTIONS DE GÉNÉRATION DES CORPUS ---

def destroy_text(text,destroy_percentage):
    ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 "
    size = len(text)
    for i in range(round((destroy_percentage*len(text))/100)):
         charIndexToReplace = random.randint(0,len(text))
         text = text[0:charIndexToReplace] + random.choice(ALPHABET) + text[charIndexToReplace+1:size]
         text = text[0:size]
    return text
        

def generate_corpus_reflection(filename, min_size_kb=55):
    """Génère le corpus pour le modèle Reflection (Format JSON)."""
    print(f"Génération de {filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        i = 0
        while os.path.getsize(filename) < min_size_kb * 1024:
            sujet = random.choice(SUJETS)
            template = random.choice(CONTEXTES_REFLECTION)
            question = template.format(sujet=sujet) + f" (Variation {i})"
            entry = {"prompt": "Génère une question de réflexion profonde.", "question": question}
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            i += 1
            if i > 10000:
                print("Attention : boucle infinie évitée dans generate_corpus_reflection")
                break

def generate_corpus_principal(filename, min_size_kb=55):
    """Génère un corpus expérimental compatible avec le format Q/R de l'application."""
    print(f"Génération de {filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        i = 0
        questions = set()
        while os.path.getsize(filename) < min_size_kb * 1024:
            sujet = random.choice(SUJETS)
            salutation = random.choice(SALUTATIONS)
            question = f"{salutation} Quels sont les enjeux éthiques prioritaires concernant {sujet} ?"
            normalized_question = " ".join(question.split()).casefold()
            if normalized_question in questions:
                i += 1
                if i > 10000:
                    print("Corpus expérimental limité aux questions distinctes générées.")
                    break
                continue
            questions.add(normalized_question)
            reponses_possibles = [
                f"Concernant {sujet}, les enjeux éthiques reposent sur la responsabilité, la sécurité des individus et le respect de la vie privée. Il est primordial d'évaluer l'impact social à long terme avant tout déploiement massif. !",
                f"{sujet} soulève des questions importantes sur l'équité, la transparence et la protection des droits fondamentaux. Une approche collaborative est nécessaire pour y répondre. !",
                f"Les défis liés à {sujet} incluent la protection des données, l'accès équitable et la minimisation des biais. Une régulation adaptée est essentielle. !",
                f"Pour aborder {sujet}, il faut considérer les implications à court et long terme, ainsi que les valeurs humaines fondamentales comme la justice et la dignité. !",
                f"{sujet} nécessite une réflexion approfondie sur ses impacts sociaux, environnementaux et économiques pour garantir un développement durable et inclusif. !",
            ]
            reponse = random.choice(reponses_possibles)
            f.write(f"Q: {question} R: {reponse}\n")
            i += 1
            if i > 10000:
                print("Attention : limite de génération du corpus expérimental atteinte.")
                break

def generate_corpus_morale(filename, min_size_kb=55):
    """Génère le corpus pour le modèle Morale (Format Texte -> ['True']/['False'])."""
    print(f"Génération de {filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        i = 0
        while os.path.getsize(filename) < min_size_kb * 1024:
            is_valid = random.choice([True, False])
            if is_valid:
                texte = random.choice(TEXTES_MORAUX_VALIDES)
                label = "['True']"
            else:
                texte = random.choice(TEXTES_MORAUX_INVALIDES)
                label = "['False']"
            f.write(f"Input: {texte} \nOutput: {label}\n\n")
            f.write(f"Input: {destroy_text(texte,50)} \nOutput: ['False']\n\n")
            salutation = random.choice(SALUTATIONS)

            f.write(f"Input: {salutation} \nOutput: ['True']\n\n")
            f.write(f"Input: {salutation} \nOutput: ['True']\n\n")
            f.write(f"Input: {salutation} \nOutput: ['True']\n\n")
            f.write(f"Input: {salutation} \nOutput: ['True']\n\n")

            f.write(f"Input: {destroy_text(salutation,50)} \nOutput: ['False']\n\n")
            f.write(f"Input: {destroy_text(salutation,50)} \nOutput: ['False']\n\n")
            f.write(f"Input: {destroy_text(salutation,50)} \nOutput: ['False']\n\n")
            f.write(f"Input: {destroy_text(salutation,50)} \nOutput: ['False']\n\n")

            i += 1
            if i > 100000:
                print("Attention : boucle infinie évitée dans generate_corpus_morale")
                break

# --- EXÉCUTION ---

if __name__ == "__main__":
    generated_data_dir = Path(__file__).resolve().parents[1] / "data" / "generated"
    generated_data_dir.mkdir(parents=True, exist_ok=True)
    min_size = 200
    corpus_paths = {
        "reflection": generated_data_dir / "corpus_reflection.json",
        "principal": generated_data_dir / "corpus_principal.txt",
        "morale": generated_data_dir / "corpus_morale.txt",
    }
    generate_corpus_reflection(str(corpus_paths["reflection"]), min_size_kb=min_size)
    generate_corpus_principal(str(corpus_paths["principal"]), min_size_kb=min_size)
    generate_corpus_morale(str(corpus_paths["morale"]), min_size_kb=min_size)
    print(f"\n[Terminé] Les 3 corpus dépassent chacun {min_size} Ko :")
    for name, path in corpus_paths.items():
        print(f"- {name.capitalize():10} : {path.stat().st_size / 1024:.2f} Ko")
