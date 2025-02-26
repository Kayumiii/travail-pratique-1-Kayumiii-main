import json
import random
from datetime import datetime
from Partie import Partie

def charger_questions(fichier="question.json"):
    try:
        with open(fichier, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Erreur: fichier de questions introuvable ou mal formaté.")
        return []

def jouer_partie():
    print("Travail pratique 1 - Youssef Chakib\n")
    print("-----------------------------------\n")
    print("Bienvenue au jeu-questions, vous devez choisir la bonne réponse pour chaque question (a/b/c/d), 2 participants maximum et chacun répond a tour de rôle\n")
    nom1 = input("Nom du Joueur 1: ").strip()
    nom2 = input("Nom du Joueur 2: ").strip()

    date_partie = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    partie = Partie(date_partie, nom1, nom2)

    questions = charger_questions()
    #Questions choisies au hasard
    random.shuffle(questions)

    for question in questions:
        partie.poser_question(question)

    partie.afficherResultat()
    partie.sauvegarderJson()
    #Option de rejouer
    rejouer = input("Voulez-vous rejouer ? (O/N): ").strip().lower()
    while rejouer not in ["o", "n"]:
        rejouer = input("Réponse invalide. Veuillez entrer O ou N: ").strip().lower()
    if rejouer == "o":
        jouer_partie()
    else:
        print("Merci d'avoir joué !")

if __name__ == "__main__":
    jouer_partie()
