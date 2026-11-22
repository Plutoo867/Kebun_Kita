import os
import json
from colored import fore, Style

# belum di baikin

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

def regis():
    while True:
        username = input("Silakan masukkan Username anda: ").strip()
        password = input("Silakan masukkan Password anda: ")

        if username == "" or password == "":
            print(f"{fore(124)}Username dan Password tidak boleh kosong!{Style.reset}")
            continue

        if cek_username(username):
            print(f"{fore(124)}Username sudah dipakai!{Style.reset}")
            continue

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

        print(f"{fore(29)}Register berhasil! Silakan login.{Style.reset}")
        break

def login(percobaan = 0):
    if percobaan == 3:                    
        print(f"{fore(124)}Terlalu banyak percobaan gagal, kembali ke menu utama.{Style.reset}")
        return None

    input_username = input("Silakan masukkan Username anda: ").strip()
    input_password = input("Silakan masukkan Password anda: ")

    for user in data_user.values():
        if input_username == user["username"] and input_password == user["password"]:
            print(f"{fore(29)}Anda berhasil login!{Style.reset}")
            return user["role"]            

    print(f"{fore(124)}Username atau Password salah! Sisa percobaan: {2 - percobaan}{Style.reset}")
    return login(percobaan + 1)

# login()
