import os
import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt5.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "data", "wordlist.txt")


def filtro_parole(word):
    return len(word) == 5 and word.isalpha()


def dizionario():
    try:
        with open(file_path, encoding="utf-8") as file:
            parole = []
            for riga in file:
                p = riga.strip().lower()
                if filtro_parole(p):
                    parole.append(p)
        return parole

    except FileNotFoundError:
        raise FileNotFoundError("Dizionario non trovato nella cartella")


def riconoscimento_parola(utente, word):
    utente = list(utente.lower())
    word = list(word.lower())

    statues = ["grigio"] * len(word)
    lettere_sistemate = [False] * len(word)

    for i in range(len(word)):
        if utente[i] == word[i]:
            statues[i] = "verde"
            lettere_sistemate[i] = True

    for i in range(len(word)):
        if statues[i] == "verde":
            continue

        for j in range(len(word)):
            if (not lettere_sistemate[j]) and utente[i] == word[j]:
                statues[i] = "giallo"
                lettere_sistemate[j] = True
                break

    return statues


class Wordle(QWidget):
    def __init__(self):
        super().__init__()

        self.lista_parole = dizionario()
        self.set_parole = set(self.lista_parole) 

        self.word_giorno = random.choice(self.lista_parole)

        self.tentativi_massimi = 6
        self.lunghezza = 5
        self.tentativi = 0
        self.finito = False

        self.cells = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Italian Wordle (PyQt5)")

        main = QVBoxLayout()

        self.info = QLabel("Inserisci una parola di 5 lettere")
        main.addWidget(self.info)

        grid = QGridLayout()
        grid.setSpacing(6)

        self.cells = []
        for r in range(self.tentativi_massimi):
            row = []
            for c in range(self.lunghezza):
                lab = QLabel("")
                lab.setAlignment(Qt.AlignCenter)
                lab.setFixedSize(50, 50)
                lab.setStyleSheet(self.style_cell("grigio"))
                grid.addWidget(lab, r, c)
                row.append(lab)
            self.cells.append(row)

        main.addLayout(grid)

        bar = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setMaxLength(self.lunghezza)
        self.input.setPlaceholderText("es. salve")
        self.input.returnPressed.connect(self.invia)

        self.btn = QPushButton("Invia")
        self.btn.clicked.connect(self.invia)

        self.btn_reset = QPushButton("Nuova partita")
        self.btn_reset.clicked.connect(self.reset)

        bar.addWidget(self.input)
        bar.addWidget(self.btn)
        bar.addWidget(self.btn_reset)
        main.addLayout(bar)

        self.msg = QLabel("")
        main.addWidget(self.msg)

        self.setLayout(main)
        self.resize(360, 450)

    def style_cell(self, colore):
        if colore == "verde":
            bg = "#2ecc71"
        elif colore == "giallo":
            bg = "#f1c40f"
        else:
            bg = "#bdc3c7"

        return f"""
            QLabel {{
                background-color: {bg};
                border: 1px solid #7f8c8d;
                font-size: 18px;
                font-weight: 600;
            }}
        """

    def invia(self):
        if self.finito:
            return

        guess = self.input.text().strip().lower()

        if not guess:
            self.msg.setText("Inserisci una parola.")
            return

        if len(guess) != self.lunghezza:
            self.msg.setText("La parola deve essere di 5 lettere.")
            return

        if not guess.isalpha():  
            self.msg.setText("Devono esserci solo lettere.")
            return

        if guess not in self.set_parole:
            self.msg.setText("Parola non inclusa nel dizionario.")
            return

        statues = riconoscimento_parola(guess, self.word_giorno)

        r = self.tentativi
        for c in range(self.lunghezza):
            self.cells[r][c].setText(guess[c].upper())
            self.cells[r][c].setStyleSheet(self.style_cell(statues[c]))

        self.tentativi += 1
        self.input.clear()
        self.msg.setText("")

        if guess == self.word_giorno:
            self.msg.setText(f"Hai indovinato! Parola: {self.word_giorno.upper()}")
            self.finito = True
            return

        if self.tentativi >= self.tentativi_massimi:
            self.msg.setText(f"Hai perso! La parola era: {self.word_giorno.upper()}")
            self.finito = True
            return

        self.info.setText(f"Tentativo: {self.tentativi}/{self.tentativi_massimi}")

    def reset(self):
        self.word_giorno = random.choice(self.lista_parole)
        self.tentativi = 0
        self.finito = False
        self.info.setText("Inserisci una parola di 5 lettere")
        self.msg.setText("")
        self.input.clear()
        for r in range(self.tentativi_massimi):
            for c in range(self.lunghezza):
                self.cells[r][c].setText("")
                self.cells[r][c].setStyleSheet(self.style_cell("grigio"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Wordle()
    w.show()
    sys.exit(app.exec_())
