import os
import json
import re
import inquirer
import pwinput
from utilis import (pesan_sukses, 
                    pesan_error,
                    bersihkan_terminal,
                    enter, 
                    header, 
                    data_user)

def cek_username(username):
    for user in data_user.values():
        if username== user["username"].lower():
            return True
    return False

def regis():
    while True:
        bersihkan_terminal()
        header("Register", "Buat akun baru untuk masuk kebun kita")
        lebar = 45
        garis = "+" + "-" * (lebar + 2) + "+"
        print(f"| {'Username dan Password minimal 3 karakter'.center(lebar)} |")
        print(f"| {'Username hanya boleh huruf dan angka'.center(lebar)} |")
        print(f"| {'(input 0 untuk kembali)'.center(lebar)} |")
        print(garis)

        try:
            username = input("Silakan masukkan Username anda: ").strip()
            if username == "0":
                return
            password =  pwinput.pwinput(prompt='Silakan masukkan Password anda: ').strip()
            if password == "0":
                return
            konfirmasi_password = pwinput.pwinput(prompt='Silakan masukkan ulang Password anda: ').strip()
            if konfirmasi_password == "0":
                return

            if username == "" or password == "" or konfirmasi_password == "":
                pesan_error("Username dan Password tidak boleh kosong!")
                enter()
                continue

            if password != konfirmasi_password:
                pesan_error("Password tidak sama!")
                enter()
                continue

            if len(username) < 3 and len(password) < 3 and len(konfirmasi_password) < 3:
                pesan_error("Username dan Password minimal 3 karakter!")
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
        except ValueError:
            pesan_error("\nNomor harus berupa angka! Silakan coba lagi.")
            enter()
            continue
        except KeyboardInterrupt:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()
            continue
        except EOFError:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()
            continue

def login():
    maks_percobaan = 3

    for percobaan in range(maks_percobaan):
        bersihkan_terminal()
        header("Login", "Silakan masuk ke akun anda")
        lebar = 45
        garis = "+" + "-" * (lebar + 2) + "+"
        print(f"| {'(input 0 untuk kembali)'.center(lebar)} |")
        print(garis)

        try:
            input_username = input("Silakan masukkan Username anda: ").strip()
            if input_username == "0":
                return
            
            input_password = pwinput.pwinput(prompt="Silakan masukkan Password anda: ").strip()
            if input_password == "0":
                return
            
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
        except ValueError:
            pesan_error("\nNomor harus berupa angka! Silakan coba lagi.")
            enter()
        except KeyboardInterrupt:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()
        except EOFError:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()

    pesan_error("Terlalu banyak percobaan gagal, kembali ke menu utama.")
    enter()
    return None