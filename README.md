# Italian Wordle (PyQt5)

A simple **Wordle clone in Italian** with a **PyQt5 GUI** (6 attempts, 5-letter words, colored feedback).

## Features
- 6x5 grid
- Green / Yellow / Grey feedback (Wordle rules)
- Input validation
- "New game" button

## Requirements
- Python 3.10+ recommended
- PyQt5

## Installation
```bash
pip install -r requirements.txt
```

Word list (required)

This project uses an external Italian word list not included in this repository.

1) Download

Download the word list from:
napolux/paroleitaliane (MIT License)
File name:
110000_parole_italiane_con_nomi_propri.txt

2) Create folder

Create this folder in the project root:
data/

3) Put the file inside data/

Move the downloaded file into data/ and rename it to:
wordlist.txt

Final path:
data/wordlist.txt

Run
python 
src/main.py


Word list from napolux/paroleitaliane (MIT License, © Francesco Napoletano).

