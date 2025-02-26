import json
from datetime import datetime

class Partie:
    #initialisation
    def __init__(self, datePartie, NomParticipantP1, NomParticipantP2):
        self.datePartie = datePartie
        self.NomParticipantP1 = NomParticipantP1
        self.NomParticipantP2 = NomParticipantP2
        self.listeReponsesP1 = []
        self.listeReponsesP2 = []
        self.PointageP1 = 0
        self.PointageP2 = 0

    def __repr__(self):
        return f"Partie du {self.datePartie}"

    def enregistrer_reponse(self, joueur, question, reponse, bonne_reponse, points):
        est_correct = reponse.lower() == bonne_reponse.lower()
        reponse_data = {"question": question, "reponse": reponse, "correct": est_correct}
        
        if joueur == 1:
            self.listeReponsesP1.append(reponse_data)
            if est_correct:
                self.PointageP1 += points
        else:
            self.listeReponsesP2.append(reponse_data)
            if est_correct:
                self.PointageP2 += points

    def poser_question(self, question):
        print(f"\n{question['q']}")
        choix = {"a": question['a'], "b": question['b'], "c": question['c'], "d": question['d']}
        for key, value in choix.items():
            print(f"{key}: {value}")
        #Participant 1 choisie une reponse
        reponseP1 = input(f"{self.NomParticipantP1}, quelle est ta réponse (a, b, c ou d) ? ").strip().lower()
        #Si autre que a b c ou d lui demande de rechoisir
        while reponseP1 not in choix:
            print("Réponse invalide.")
            reponseP1 = input(f"{self.NomParticipantP1}, quelle est ta réponse (a, b, c ou d) ? ").strip().lower()
        #Pareil
        reponseP2 = input(f"{self.NomParticipantP2}, quelle est ta réponse (a, b, c ou d) ? ").strip().lower()
        while reponseP2 not in choix:
            print("Réponse invalide.")
            reponseP2 = input(f"{self.NomParticipantP2}, quelle est ta réponse (a, b, c ou d) ? ").strip().lower()
        #Donne la bonne réponse ensuite
        bonne_reponse = question['rep']
        print(f"La bonne réponse est {bonne_reponse}: {choix[bonne_reponse]}")
        #Enregistre les réponses des 2 participants
        self.enregistrer_reponse(1, question['q'], reponseP1, bonne_reponse, question['pts'])
        self.enregistrer_reponse(2, question['q'], reponseP2, bonne_reponse, question['pts'])

        if reponseP1 == bonne_reponse:
            print(f"Bonne réponse {self.NomParticipantP1} !")
        else:
            print(f"Mauvaise réponse {self.NomParticipantP1}.")

        if reponseP2 == bonne_reponse:
            print(f"Bonne réponse {self.NomParticipantP2} !")
        else:
            print(f"Mauvaise réponse {self.NomParticipantP2}.")
    #Affiche le résultat des pointages ainsi que la date
    def afficherResultat(self):
        print(f"\nRésultats de la partie du {self.datePartie} :")
        print(f"{self.NomParticipantP1} : {self.PointageP1} points")
        print(f"{self.NomParticipantP2} : {self.PointageP2} points")
        
    #Sauvegarde les résultats dans un fichier Json
    def sauvegarderJson(self, filename="resultats.json"):
        try:
            with open(filename, "r", encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append({
            "datePartie": self.datePartie,
            "NomParticipantP1": self.NomParticipantP1,
            "NomParticipantP2": self.NomParticipantP2,
            "listeReponsesP1": self.listeReponsesP1,
            "listeReponsesP2": self.listeReponsesP2,
            "PointageP1": self.PointageP1,
            "PointageP2": self.PointageP2
        })
        
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Les résultats ont été sauvegardés dans {filename}.")
