import os
import inquirer
from crud_jual_beli import lihat_stok, tambah_data, edit_data, hapus_data


def menu_admin():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        pertanyaan = [
            inquirer.List(
                "menu",
                message="Pilih menu jual beli",
                choices=[
                    "Lihat koleksi",
                    "Tambah koleksi",
                    "Edit Koleksi",
                    "Hapus koleksi",
                    "keluar",
                ],
            )
        ]
        jawaban = inquirer.prompt(pertanyaan)

        if jawaban is None or jawaban["menu"] == "keluar":
            break

        pilihan = jawaban["menu"]
        if pilihan == "Lihat koleksi":
            lihat_stok()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == "Tambah koleksi":
            tambah_data()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == "Edit Koleksi":
            edit_data()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == "Hapus koleksi":
            hapus_data()
            input("\nTekan Enter untuk kembali ke menu...")