import os
import inquirer
from crud_jual_beli import read_data, create_data, edit_data, delete_data
from crud_ensiklopedia import read_ensiklopedia, create_ensiklopedia, update_ensiklopedia, delete_ensiklopedia, search_ensiklopedia
from crud_funfact import create_funfact, update_funfact, delete_funfact, read_funfact

def menu_admin():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        jawaban = inquirer.prompt([
            inquirer.List(
                "menu",
                message="Pilih Menu Jual Beli",
                choices=[
                    "1. Ensiklopedia",
                    "2. Jual Beli",
                    "3. Funfact",
                    "4. Logout",
                ],
            )
        ])
        if jawaban is None or jawaban["menu"].startswith("4."):
            break

        if jawaban["menu"].startswith("1."):
            menu_ensiklopedia()
        elif jawaban["menu"].startswith("2."):
            menu_jual_beli()
        elif jawaban["menu"].startswith("3."):
            menu_funfact()

def menu_ensiklopedia():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        jawaban = inquirer.prompt([
            inquirer.List(
                "menu",
                message="Pilih Menu Ensiklopedia",
                choices=[
                    "1. Lihat Ensiklopedia",
                    "2. Tambah Ensiklopedia",
                    "3. Ubah Ensiklopedia",
                    "4. Hapus Ensiklopedia",
                    "5. Cari Ensiklopedia",
                    "6. Kembali ke Menu Admin",
                ],
            )
        ])
        if jawaban is None or jawaban["menu"].startswith("6."):
            break

        if jawaban["menu"].startswith("1."):
            read_ensiklopedia()
        elif jawaban["menu"].startswith("2."):
            create_ensiklopedia()
        elif jawaban["menu"].startswith("3."):
            update_ensiklopedia()
        elif jawaban["menu"].startswith("4."):
            delete_ensiklopedia()
        elif jawaban["menu"].startswith("5."):
            search_ensiklopedia()

def menu_funfact():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        jawaban = inquirer.prompt([
            inquirer.List(
                "menu",
                message="Pilih Menu Funfact",
                choices=[
                    "1. Lihat Funfact",
                    "2. Tambah Funfact",
                    "3. Ubah Funfact",
                    "4. Hapus Funfact",
                    "5. Kembali ke Menu Admin",
                ],
            )
        ])
        if jawaban is None or jawaban["menu"].startswith("5."):
            break

        if jawaban["menu"].startswith("1."):
            read_funfact()
        elif jawaban["menu"].startswith("2."):
            create_funfact()
        elif jawaban["menu"].startswith("3."):
            update_funfact()
        elif jawaban["menu"].startswith("4."):
            delete_funfact()

def menu_jual_beli():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        jawaban = inquirer.prompt([
            inquirer.List(
                "menu",
                message="Pilih Menu Jual Beli",
                choices=[
                    "1. Lihat Data Jual Beli",
                    "2. Tambah Data Jual Beli",
                    "3. Ubah Data Jual Beli",
                    "4. Hapus Data Jual Beli",
                    "5. Kembali ke Menu Admin",
                ],
            )
        ])
        if jawaban is None or jawaban["menu"].startswith("5."):
            break

        if jawaban["menu"].startswith("1."):
            read_data()
        elif jawaban["menu"].startswith("2."):
            create_data()
        elif jawaban["menu"].startswith("3."):
            edit_data()
        elif jawaban["menu"].startswith("4."):
            delete_data()