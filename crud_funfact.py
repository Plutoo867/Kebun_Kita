import os
import random
import textwrap
import json
import inquirer
from prettytable import PrettyTable
from colored import fore, Style

def load_data():
    if not os.path.exists("ensiklopedia.json"):
        return {}
    try:
        with open("ensiklopedia.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def simpan_data():
    with open("ensiklopedia.json", "w", encoding="utf-8") as file:
        json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)

ensiklopedia = load_data()

def tampilkan_daftar(daftar_id, judul):
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(197)}"

    print("0. Kembali ke Menu Utama")
    table = PrettyTable()

    table.title = f"{warna_judul}{judul.upper()}{Style.reset}"
    table.field_names = ["No", "Nama Tanaman"]
    table.header = False
    table.max_width["No"] = 3
    table.min_width["Nama Tanaman"] = 35
    table.align["Nama Tanaman"] = "l"

    for nomor, id_data in enumerate(daftar_id, start=1):
        tanaman = f"{warna_isi}{ensiklopedia[id_data]['nama']}{Style.reset}"
        table.add_row([nomor, tanaman])

    print(table)

def table_funfact(data):
    warna_judul: str = f"{fore(204)}"
    table = PrettyTable()

    table.title = f"{warna_judul}FUNFACT TANAMAN{Style.reset}"
    table.field_names = ["Label", "Isi"]
    table.header = False
    table.align = "l"
    table.max_width["Label"] = 15
    table.min_width["Isi"] = 25

    for label, isi in data.items():
        table.add_row([label, isi])

    print(table)

def pesan_error(teks):
    print(f"{fore(124)}{teks}{Style.reset}")

def pesan_sukses(teks):
    print(f"{fore(29)}{teks}{Style.reset}")

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

def random_funfact():
    os.system("cls" if os.name == "nt" else "clear")
    funfacts = []

    for id_data in ensiklopedia:
        funfact = ensiklopedia[id_data]["funfact"]

        if funfact != "0":
            funfacts.append({
                "Nama_tanaman": ensiklopedia[id_data]["nama"],
                "Funfact": funfact
            })

    if funfacts:
        random_data = random.choice(funfacts)

        funfact_wrapped = textwrap.fill(random_data["Funfact"], width=50)
        table_funfact({
            "Nama Tanaman": random_data["Nama_tanaman"],
            "Funfact": funfact_wrapped
        })
        enter()

    else:
        pesan_error("Tidak ada funfact yang tersedia")
        enter()

def read_funfact():
    os.system("cls" if os.name == "nt" else "clear")
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(197)}"
    id_kosong = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["funfact"] != "0":
            id_kosong.append(id_data)

    if not id_kosong:
        pesan_error("Tidak ada tanaman yang memiliki funfact!")
        enter()
        return

    table = PrettyTable()

    table.title = f"{warna_judul}DAFTAR FUNFACT{Style.reset}"
    table.field_names = ("No", "Nama Tanaman", "Funfact")
    table.align = "l"
    table.max_width["No"] = 3
    table.max_width["Funfact"] = 50

    no = 1
    for id_data in id_kosong:
        tanaman = f"{warna_isi}{ensiklopedia[id_data]['nama']}{Style.reset}"
        funfact = f"{warna_isi}{ensiklopedia[id_data]['funfact']}{Style.reset}"
        table.add_row([
            no,
            tanaman,
            funfact
        ])
        no += 1

    print(table)
    enter()

def create_funfact():
    os.system("cls" if os.name == "nt" else "clear")
    id_kosong = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["funfact"] == "0":
            id_kosong.append(id_data)

    if not id_kosong:
        pesan_error("Tidak ada tanaman yang membutuhkan funfact!")
        enter()
        return

    while True:
        tampilkan_daftar(id_kosong, "Daftar Tanaman Tanpa Funfact")
        try:
            pilihan = int(input("Masukkan nomor tanaman untuk menambah Funfact: ").strip())

            if pilihan == 0:
                break

            elif pilihan < 1 or pilihan > len(id_kosong):
                pesan_error("Nomor tanaman tidak tersedia!")
                enter()
                continue

            id_pilihan = id_kosong[pilihan - 1]

            while True:
                funfact = input("Masukkan funfact: ").strip()

                if not funfact:
                    pesan_error("Funfact tidak boleh kosong!")
                    continue
                elif funfact == "0":
                    pesan_error("Funfact tidak boleh '0'!")
                    continue

                konfirmasi = [
                    inquirer.List(
                        "konfirmasi",
                        message="Apakah Anda yakin ingin menambahkan funfact ini?",
                        choices=["Ya", "Tidak"],
                    )
                ]
                jawaban = inquirer.prompt(konfirmasi)

                if jawaban["konfirmasi"] == "Ya":
                    ensiklopedia[id_pilihan]["funfact"] = funfact
                    simpan_data()
                    pesan_sukses("Funfact berhasil ditambahkan!")
                    enter()
                    return

                elif jawaban["konfirmasi"] == "Tidak":
                    pesan_sukses("Tambah Funfact dibatalkan.")
                    enter()
                    break

        except ValueError:
            pesan_error("Input Tidak Valid! Silahkan masukkan angka yang valid")
            enter()

def update_funfact():
    os.system("cls" if os.name == "nt" else "clear")
    id_dengan_funfact = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["funfact"] != "0":
            id_dengan_funfact.append(id_data)

    if not id_dengan_funfact:
        pesan_error("Tidak ada tanaman yang memiliki funfact!")
        enter()
        return

    while True:
        tampilkan_daftar(id_dengan_funfact, "Daftar Tanaman Dengan Funfact")
        try:
            pilihan = int(input("\nMasukkan nomor tanaman yang ingin di update: ").strip())

            if pilihan == 0:
                break
            elif pilihan < 1 or pilihan > len(id_dengan_funfact):
                pesan_error("Nomor tanaman tidak tersedia!")
                enter()
                continue

            id_pilihan = id_dengan_funfact[pilihan - 1]

            while True:
                funfact_baru = input(f"Funfact [{ensiklopedia[id_pilihan]['funfact']}]: ").strip()

                if not funfact_baru:
                    pesan_error("Funfact tidak boleh kosong!")
                    enter()
                    continue
                elif funfact_baru == "0":
                    pesan_error("Funfact tidak boleh '0'!")
                    enter()
                    continue

                konfirmasi = [
                    inquirer.List(
                        "konfirmasi",
                        message="Apakah Anda yakin ingin memperbarui funfact ini?",
                        choices=["Ya", "Tidak"],
                    )
                ]
                jawaban = inquirer.prompt(konfirmasi)

                if jawaban["konfirmasi"] == "Ya":
                    ensiklopedia[id_pilihan]["funfact"] = funfact_baru
                    simpan_data()
                    pesan_sukses("Funfact berhasil diperbarui!")
                    enter()
                    return

                elif jawaban["konfirmasi"] == "Tidak":
                    pesan_sukses("Funfact tidak diperbarui.")
                    enter()
                    break
        except ValueError:
            pesan_error("Input Tidak Valid! Silahkan masukkan angka yang valid")
            enter()

def delete_funfact():
    os.system("cls" if os.name == "nt" else "clear")
    id_dengan_funfact = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["funfact"] != "0":
            id_dengan_funfact.append(id_data)

    if not id_dengan_funfact:
        pesan_error("Tidak ada tanaman yang memiliki funfact!")
        enter()
        return

    while True:
        tampilkan_daftar(id_dengan_funfact, "Daftar Tanaman Dengan Funfact")
        try:
            pilihan = int(input("\nMasukkan nomor tanaman yang ingin di hapus: ").strip())

            if pilihan == 0:
                break
            elif pilihan < 1 or pilihan > len(id_dengan_funfact):
                pesan_error("Nomor tanaman tidak tersedia!")
                enter()
                continue

            id_pilihan = id_dengan_funfact[int(pilihan) - 1]
            konfirmasi = [
                inquirer.List(
                    "konfirmasi",
                    message=f"Apakah Anda yakin ingin menghapus funfact [{ensiklopedia[id_pilihan]['nama']}] ini?",
                    choices=["Ya", "Tidak"],
                )
            ]
            jawaban = inquirer.prompt(konfirmasi)
            if jawaban["konfirmasi"] == "Ya":
                ensiklopedia[id_pilihan]["funfact"] = "0"
                simpan_data()
                pesan_sukses("Funfact berhasil dihapus!")
                enter()
                return
            elif jawaban["konfirmasi"] == "Tidak":
                pesan_sukses("Funfact tidak dihapus")
                enter()
        except ValueError:
            pesan_error("Input Tidak Valid! Silahkan masukkan angka yang valid")
            enter()