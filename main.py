import inquirer
from auth import login, regis
from menu_admin import menu_admin
from menu_user import menu_user
from utilis import pesan_sukses, bersihkan_terminal

def main():
    while True:
        bersihkan_terminal()
        jawaban = inquirer.prompt([
            inquirer.List(
                "awal",
                message="Selamat Datang di Kebun Kita",
                choices=[
                    "1. Login",
                    "2. Register",
                    "3. Keluar",
                ],
            )
        ])

        if jawaban is None or jawaban["awal"].startswith("3."):
            pesan_sukses("Terima kasih telah menggunakan Kebun Kita!")
            break

        if jawaban["awal"].startswith("2."):
            regis()
        elif jawaban["awal"].startswith("1."):
            role = login()
            if role == "user":
                menu_user()
            elif role == "admin":
                menu_admin()


if __name__ == "__main__":
    main()