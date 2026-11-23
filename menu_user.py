import os, inquirer
from crud_jual_beli import beli_tanaman
from crud_ensiklopedia import read_ensiklopedia
from crud_funfact import random_funfact
from crud_ensiklopedia import ensiklopedia

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
                    "3. Funfact",
                    "4. Logout",
                ],
            )
        ])
        if jawaban is None or jawaban["menu"].startswith("4."):
            break

        if jawaban["menu"].startswith("1."):
            beli_tanaman()
        elif jawaban["menu"].startswith("2."):
            read_ensiklopedia()
        elif jawaban["menu"].startswith("3."):
            random_funfact(ensiklopedia)