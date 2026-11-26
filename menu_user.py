import os 
import inquirer
from crud_jual_beli import beli_tanaman
from crud_ensiklopedia import read_ensiklopedia, search_ensiklopedia
from crud_funfact import random_funfact
from utilis import enter, bersihkan_terminal, pesan_sukses

def menu_user():
    while True:
        bersihkan_terminal()
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
            pesan_sukses("Terima kasih telah menggunakan Kebun Kita!")
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