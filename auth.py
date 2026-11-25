import os
import json
import re
import inquirer
import pwinput
from prettytable import PrettyTable
from colored import fore, Style

def load_data():
    if not os.path.exists("data_user.json"):
        return {}
    try:
        with open("data_user.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

data_user = load_data()

def cek_username(username):
    for user in data_user.values():
        if username == user["username"]:
            return True
    return False

def enter():
    print("\nTekan Enter untuk lanjut...")

    if os.name == "nt":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getwch()
        while True:
            if msvcrt.getwch() in ("\r", "\n"):
                break
    else:
        input()

def pesan_error(teks):
    print(f"{fore(124)}{teks}{Style.reset}")

def pesan_sukses(teks):
    print(f"{fore(29)}{teks}{Style.reset}")

def header(judul, keterangan):
    table = PrettyTable()

    warna_judul = fore(204)
    warna_isi = fore(197)
    table.title = f"{warna_judul}{judul.upper()}{Style.reset}"
    table.field_names = ["Info"]
    table.header = False
    table.min_width["Info"] = 45
    table.align["Info"] = "c"
    table.add_row([f"{warna_isi}{keterangan}{Style.reset}"])

    print(table)

def regis():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        header("Register", "Buat akun baru untuk masuk kebun kita")
        
        username = input("Silakan masukkan Username anda: ").strip()
        password =  pwinput.pwinput(prompt='Silakan masukkan Password anda: ').strip()
        konfirmasi_password = pwinput.pwinput(prompt='Silakan masukkan ulang Password anda: ').strip()

        if username == "" or password == "" or konfirmasi_password == "":
            pesan_error("Username dan Password tidak boleh kosong!")
            enter()
            continue

        if password != konfirmasi_password:
            pesan_error("Password tidak sama!")
            enter()
            continue

        if not re.fullmatch(r"[a-zA-Z0-9]+", username):
            pesan_error("Username hanya boleh huruf dan angka!")
            enter()
            continue

        if cek_username(username):
            pesan_error("Username sudah dipakai!")
            enter()
            continue

        konfirmasi = [
            inquirer.List(
                "konfirmasi",
                message=f"Apakah Anda yakin ingin mendaftar dengan username [{username}]?",
                choices=["Ya", "Tidak"],
            )
        ]

        jawaban = inquirer.prompt(konfirmasi)

        if jawaban["konfirmasi"] == "Ya":
            nomor = len(data_user)
            while f"user{nomor}" in data_user:
                nomor += 1
            id_baru = f"user{nomor}"

            data_user[id_baru] = {
                "role": "user",
                "username": username,
                "password": password
            }

            with open("data_user.json", "w", encoding="utf-8") as file:
                json.dump(data_user, file, indent=4, ensure_ascii=False)

            pesan_sukses("Register berhasil! Silakan login.")
            enter()
            return
        elif jawaban["konfirmasi"] == "Tidak":
            pesan_sukses("Register dibatalkan!")
            enter()
            break

def login():
    maks_percobaan = 3

    for percobaan in range(maks_percobaan):
        os.system("cls" if os.name == "nt" else "clear")
        header("Login", "Silakan masuk ke akun anda")

        input_username = input("Silakan masukkan Username anda: ").strip()
        input_password = pwinput.pwinput(prompt="Silakan masukkan Password anda: ")
        sisa = maks_percobaan - percobaan - 1

        if not input_username or not input_password:
            pesan = "Username dan Password tidak boleh kosong!"
        elif not re.fullmatch(r"[a-zA-Z0-9]+", input_username):
            pesan = "Username hanya boleh huruf dan angka!"
        else:
            for user in data_user.values():
                if input_username == user["username"] and input_password == user["password"]:
                    pesan_sukses("Anda berhasil login!")
                    enter()
                    return user["role"]
            pesan = "Username atau Password salah!"

        pesan_error(f"{pesan} Sisa percobaan: {sisa}")
        enter()

    pesan_error("Terlalu banyak percobaan gagal, kembali ke menu utama.")
    enter()
    return None