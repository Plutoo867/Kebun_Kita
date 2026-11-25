import os 
import inquirer
from crud_jual_beli import beli_tanaman
from crud_ensiklopedia import read_ensiklopedia, search_ensiklopedia, enter
from crud_funfact import random_funfact

def menu_user():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        jawaban = inquirer.prompt([
            inquirer.List(
                "menu",
                message="Menu Kebun Kita",
                choices=[
                    "1. Beli Tanaman",
                    "2. Ensiklopedia",
                    "3. Search Koleksi",
                    "4. Funfact",
                    "5. Logout",
                ],
            )
        ])
        if jawaban is None or jawaban["menu"].startswith("5."):
            print("Terima kasih telah menggunakan Kebun Kita!")
            enter()
            break

        if jawaban["menu"].startswith("1."):
            beli_tanaman()
        elif jawaban["menu"].startswith("2."):
            read_ensiklopedia()
        elif jawaban["menu"].startswith("3."):
            search_ensiklopedia()
        elif jawaban["menu"].startswith("4."):
            random_funfact()