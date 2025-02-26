import json
import tkinter as tk
from tkinter import filedialog, ttk

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Travail Pratique 1 Interface - Youssef Chakib")
        self.root.geometry("700x500")
        
        # Bouton pour importer un fichier JSON contenant les résultats
        self.btn_import = tk.Button(root, text="Importer les résultats", command=self.importer_resultats)
        self.btn_import.pack(pady=10)
        
        # Sélection de la date
        self.label_date = tk.Label(root, text="Sélectionnez une date :")
        self.label_date.pack()
        
        self.combo_dates = ttk.Combobox(root, state="readonly")
        self.combo_dates.pack()
        self.combo_dates.bind("<<ComboboxSelected>>", self.afficher_participants)
        
        # Sélection du participant
        self.label_participants = tk.Label(root, text="Sélectionnez un participant :")
        self.label_participants.pack()
        
        self.list_participants = tk.Listbox(root)
        self.list_participants.pack()
        self.list_participants.bind("<<ListboxSelect>>", self.afficher_reponses)
        
        # Zone d'affichage des réponses
        self.text_reponses = tk.Text(root, height=10, width=50)
        self.text_reponses.pack(pady=10)
        
        # Affichage du score
        self.label_score = tk.Label(root, text="Score : --", font=("Arial", 12, "bold"))
        self.label_score.pack()
        
        self.resultats = []
    
    def importer_resultats(self):
        #Permet d'importer un fichier JSON contenant les résultats
        fichier = filedialog.askopenfilename(title="Sélectionnez le fichier de résultats", filetypes=[("JSON files", "*.json")])
        if fichier:
            with open(fichier, "r", encoding="utf-8") as f:
                self.resultats = json.load(f)
            # Remplir le ComboBox avec les dates des parties
            self.combo_dates["values"] = [r["datePartie"] for r in self.resultats]
            
    #Affiche les participants de la partie sélectionnée
    def afficher_participants(self, event):
        self.list_participants.delete(0, tk.END)
        date_selectionnee = self.combo_dates.get()
        
        partie = None
        for r in self.resultats:
            if r["datePartie"] == date_selectionnee:
                partie = r
                break
        
        if partie:
            self.list_participants.insert(tk.END, partie["NomParticipantP1"])
            self.list_participants.insert(tk.END, partie["NomParticipantP2"])
    #Affiche les réponses du participant sélectionné
    def afficher_reponses(self, event):
        # Effacer le texte s'il y en a
        self.text_reponses.delete("1.0", tk.END)
        #retourne indice de l'élément selectionné
        choix = self.list_participants.curselection()
        #si rien n'est selectionné la fonction retourne et arrête
        if not choix:
            return
        #recupère le nom
        nom = self.list_participants.get(choix[0])
        date_selectionnee = self.combo_dates.get()
        
        #recherche partie
        partie = None
        for r in self.resultats:
            if r["datePartie"] == date_selectionnee:
                partie = r
                break
        #éxécute si la partie est trouvée (pas None)
        if partie:
            if nom == partie["NomParticipantP1"]:
                reponses = partie["listeReponsesP1"]
                #get retourne la valeur entrée
                score = partie.get("PointageP1", 0)
            else:
                reponses = partie["listeReponsesP2"]
                score = partie.get("PointageP2", 0)
            
            for r in reponses:
                couleur = "vert" if r["correct"] else "rouge"
                # Insérer la question et la réponse avec la couleur associée
                self.text_reponses.insert(tk.END, f"Question {r['num_question']} : {r['reponse']}\n", couleur)
                self.text_reponses.tag_configure("vert", foreground="green")
                self.text_reponses.tag_configure("rouge", foreground="red")
            #met à jour score du label pour donner le score actuel du participant
            self.label_score.config(text=f"Score : {score}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
