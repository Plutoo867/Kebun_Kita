import os, inquirer
from auth import login, regis
from menu_admin import menu_admin
from menu_user import menu_user

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
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
            print("Terima kasih telah menggunakan Kebun Kita!")
            break

        if jawaban["awal"].startswith("2."):
            regis()
            input("\nTekan Enter untuk melanjutkan...")
        elif jawaban["awal"].startswith("1."):
            role = login()
            if role == "user":
                menu_user()
            elif role == "admin":
                menu_admin()
            else:
                input("\nTekan Enter untuk kembali ke menu awal...")


if __name__ == "__main__":
    main()

