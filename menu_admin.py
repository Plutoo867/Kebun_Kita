import os
import inquirer
from crud_jual_beli import read_jual_beli, create_jual_beli, update_jual_beli, delete_jual_beli
from crud_ensiklopedia import read_ensiklopedia, create_ensiklopedia, update_ensiklopedia, delete_ensiklopedia, search_ensiklopedia, enter
from crud_funfact import create_funfact, update_funfact, delete_funfact, read_funfact

def menu_admin():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        jawaban = inquirer.prompt([
            inquirer.List(
                "menu",
                message="Menu Admin Kebun Kita:",
                choices=[
                    "1. Ensiklopedia",
                    "2. Jual Beli",
                    "3. Funfact",
                    "4. Logout",
                ],
            )
        ])
        if jawaban is None or jawaban["menu"].startswith("4."):
            print("Terima kasih telah menggunakan Kebun Kita!")
            enter()
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
                    "1. Lihat Koleksi",
                    "2. Tambah Koleksi",
                    "3. Update Koleksi",
                    "4. Hapus Koleksi",
                    "5. Cari Koleksi",
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
                    "3. Update Funfact",
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
                    "3. Update Data Jual Beli",
                    "4. Hapus Data Jual Beli",
                    "5. Kembali ke Menu Admin",
                ],
            )
        ])
        if jawaban is None or jawaban["menu"].startswith("5."):
            break

        if jawaban["menu"].startswith("1."):
            read_jual_beli()
        elif jawaban["menu"].startswith("2."):
            create_jual_beli()
        elif jawaban["menu"].startswith("3."):
            update_jual_beli()
        elif jawaban["menu"].startswith("4."):
            delete_jual_beli()