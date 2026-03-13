import random # Importăm biblioteca pentru a folosi funcții random
import tkinter as tk # Importăm Tkinter pentru interfața grafică
from tkinter import messagebox  # Importăm pentru a afișa mesaje pop-up
import json #Importăm biblioteca JSON pentru a folosi datele JSON

# Încarcă întrebările din fișierul JSON
def incarca_intrebari(fisier, numar_intrebari):
    try:
        with open(fisier, 'r', encoding='utf-8') as f:
            toate_intrebari = json.load(f)  # Citim toate întrebările
            print(f"Întrebări încărcate: {toate_intrebari}")  # Afișează întrebările
            if len(toate_intrebari) >= numar_intrebari:  # Verificăm dacă sunt suficiente întrebări disponibile
                return random.sample(toate_intrebari, numar_intrebari)   # Alegem un număr specificat de întrebări aleatorii
            else:
                messagebox.showerror("Eroare", "Fișierul nu conține suficiente întrebări.")
                return []
    except FileNotFoundError:
        messagebox.showerror("Eroare", f"Fișierul {fisier} nu a fost găsit.")
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Eroare", f"Fișierul {fisier} nu este un fișier JSON valid.")
        return []

NUMAR_INTREBARI = 7
intrebari = incarca_intrebari("intrebari.json", NUMAR_INTREBARI)  # Încărcăm întrebările folosind funcția definită

if not intrebari:
    exit() # Dacă lista de întrebări este goală, închidem programul


class TestPersonalitate:
    def __init__(self, root):
        self.root = root
        self.root.title("Test de personalitate")
        self.root.geometry("800x700")
        self.root.configure(bg="#E4F1AC")

        self.index = 0
        # Inițializăm scorurile pentru fiecare personaj
        self.scoruri = {"Tinkerbell": 0, "Rosetta": 0, "Fawn": 0, "Iridessa": 0, "Silvermist": 0, "Vidia": 0}
        self.numar_alegeri = {"Tinkerbell": 0, "Rosetta": 0, "Fawn": 0, "Iridessa": 0, "Silvermist": 0, "Vidia": 0}

        self.title_label = tk.Label(
            root,    # Inițializăm fereastra principală
            text="Test de Personalitate", # Setăm titlul
            font=("Comic Sans MS", 20, "bold"),
            fg="#F72C5B",
            bg="#E4F1AC"
        )
        self.title_label.pack(pady=10)

        self.contor_label = tk.Label(
            root,
            text="Întrebarea 1 din " + str(len(intrebari)),
            font=("Comic Sans MS", 12),
            bg="#E4F1AC",
            fg="#A7D477"
        )
        self.contor_label.pack(pady=5)

        self.intrebare_label = tk.Label(
            root,
            text="",
            wraplength=500,
            justify="center",
            font=("Comic Sans MS", 14),
            bg="#E4F1AC",
            fg="#F72C5B"
        )
        self.intrebare_label.pack(pady=20)

        self.butoane = []
        for i in range(6):
            buton = tk.Button(
                root,
                text="",
                wraplength=300,
                font=("Comic Sans MS", 12),
                bg="#FF748B",
                fg="white",
                activebackground="#A7D477",
                command=lambda i=i: self.raspunde(i)
            )
            buton.config(
                activebackground="#A7D477",
                relief="flat",
                width=20,
                height=2,
                bd=0,
            )
            buton.pack(pady=10, fill="x", padx=50)
            self.butoane.append(buton)

        # Nu mai afișăm mesajul cu răspunsul ales
        self.raspuns_label = tk.Label(
            root,
            text="",
            wraplength=500,
            justify="center",
            font=("Comic Sans MS", 12),
            bg="#E4F1AC",
            fg="#F72C5B"
        )
        self.raspuns_label.pack(pady=20)

        self.afiseaza_intrebare()   # Afișăm prima întrebare

    def afiseaza_intrebare(self):
        if self.index < len(intrebari):
            intrebare = intrebari[self.index]  # Obținem întrebarea curentă
            self.intrebare_label.config(text=intrebare["intrebare"])
            self.contor_label.config(text=f"Întrebarea {self.index + 1} din {len(intrebari)}")

            optiuni = intrebare["optiuni"]
            for i in range(6):
                if i < len(optiuni):
                    self.butoane[i].config(text=optiuni[i]["text"], state="normal") # Setăm textul opțiunilor pentru fiecare buton
                else:
                    self.butoane[i].config(state="disabled")  # Dezactivăm butoanele nefolosite
        else:
            self.afiseaza_rezultatul()

    def raspunde(self, indice):
        if self.index < len(intrebari):  # Asigură-te că indexul este valid
            intrebare = intrebari[self.index]
            scoruri = intrebare["scoruri"]

            # Extragem scorul pentru opțiunea aleasă
            scor_alegere = scoruri[indice]
            print(f"Opțiunea aleasă are scorul: {scor_alegere}")

            # Încercăm să găsim personajul asociat scorului din opțiune
            optiune = intrebare["optiuni"][indice]
            personaj = optiune["personaj"]  # Numele personajului este un câmp al opțiunii
            print(f"Personajul ales: {personaj}")

            # Adăugăm scorul corespunzător pentru personajul ales
            if personaj in self.scoruri:
                self.scoruri[personaj] += scor_alegere
                self.numar_alegeri[personaj] += 1  # Incrementăm numărul de alegeri pentru acest personaj
                print(f"Alegeți {personaj}, adăugând {scor_alegere} la scorul său.")
            else:
                print(f"Personajul {personaj} nu a fost găsit în scoruri.")

            # Trecem la următoarea întrebare doar dacă mai există întrebări
            self.index += 1
            if self.index < len(intrebari):  # Verificăm dacă nu am ajuns la sfârșitul întrebărilor
                self.afiseaza_intrebare()
            else:
                self.afiseaza_rezultatul()

    def afiseaza_rezultatul(self):
        # Calculăm scorul total pentru fiecare personaj
        scoruri_medii = {}
        alegeri_count = {}  #  pentru a număra alegerile pentru fiecare personaj

        for personaj in self.scoruri:
            scor_total = self.scoruri[personaj]
            numar_alegeri = self.numar_alegeri.get(personaj, 0)  # Numărul de alegeri pentru personaj

            # Asigurăm că nu împărțim la zero
            if numar_alegeri == 0:
                scoruri_medii[personaj] = 0
            else:
                # Calculăm scorul mediu pe baza alegerilor efectuate
                scoruri_medii[personaj] = scor_total / numar_alegeri

            alegeri_count[personaj] = numar_alegeri  # Salvăm numărul de alegeri pentru fiecare personaj

        # Verificăm dacă toate alegerile sunt 0 (nicio opțiune selectată)
        if all(value == 0 for value in alegeri_count.values()):
            messagebox.showinfo("Rezultatul Testului", "Nu ai ales nicio opțiune!")
            self.root.quit()
            return

        # Găsim personajul cu cel mai mare număr de alegeri
        max_alegeri_personaj = max(alegeri_count, key=alegeri_count.get)

        # Creăm un mesaj cu numele zânei alese cel mai mult
        rezultat = f"Felicitări! Ești: {max_alegeri_personaj} (Alegeri: {alegeri_count[max_alegeri_personaj]})"

        # Afișăm rezultatul într-o fereastră de mesaj
        print(f"Scoruri finale: {scoruri_medii}")  # Debugging: Afișăm scorurile finale
        messagebox.showinfo("Rezultatul Testului", rezultat)

        self.root.quit()


# Initializarea interfatei grafice
if __name__ == "__main__":
    root = tk.Tk()
    test = TestPersonalitate(root)
    root.mainloop()