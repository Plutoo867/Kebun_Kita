import random
import textwrap
import inquirer
import re
from prettytable import PrettyTable
from colored import fore, Style
from utilis import (ensiklopedia, 
                    simpan_data, 
                    pesan_error, 
                    pesan_sukses, 
                    bersihkan_terminal, 
                    enter, 
                    daftar_funfact,
                    table_detail_funfact)

def random_funfact():
    bersihkan_terminal()
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

        funfact_wrapped = textwrap.fill(random_data["Funfact"].capitalize(), width=50)
        table_detail_funfact({
            "Nama Tanaman": random_data["Nama_tanaman"].capitalize(),
            "Funfact": funfact_wrapped
        })
        enter()

    else:
        pesan_error("Tidak ada funfact yang tersedia")
        enter()

def read_funfact():
    bersihkan_terminal()
    warna_judul: str = f"{fore(214)}"
    warna_isi: str = f"{fore(215)}"
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
        tanaman = f"{warna_isi}{ensiklopedia[id_data]['nama'].capitalize()}{Style.reset}"
        funfact = f"{warna_isi}{ensiklopedia[id_data]['funfact'].capitalize()}{Style.reset}"
        table.add_row([
            no,
            tanaman,
            funfact
        ])
        no += 1

    print(table)
    enter()

def create_funfact():
    id_kosong = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["funfact"] == "0":
            id_kosong.append(id_data)

    if not id_kosong:
        pesan_error("Tidak ada tanaman yang membutuhkan funfact!")
        enter()
        return

    while True:
        bersihkan_terminal()
        daftar_funfact(id_kosong, "Daftar Tanaman Tanpa Funfact")
        try:
            pilihan = input("Masukkan nomor tanaman untuk menambah Funfact: ").strip()

            if pilihan == "0":
                break

            elif not re.fullmatch(r"[0-9]+", pilihan):
                pesan_error("Hanya boleh angka valid!")
                enter()
                continue

            pilihan = int(pilihan)
            if pilihan < 1 or pilihan > len(id_kosong):
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
            pesan_error("\nInput Tidak Valid!")
            enter()
        except KeyboardInterrupt:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()
        except EOFError:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()

def update_funfact():
    id_dengan_funfact = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["funfact"] != "0":
            id_dengan_funfact.append(id_data)

    if not id_dengan_funfact:
        pesan_error("Tidak ada tanaman yang memiliki funfact!")
        enter()
        return

    while True:
        bersihkan_terminal()
        daftar_funfact(id_dengan_funfact, "Daftar Tanaman Dengan Funfact")
        try:
            pilihan = input("\nMasukkan nomor tanaman yang ingin di update: ").strip()
            if pilihan == "0":
                break

            elif not re.fullmatch(r"[0-9]+", pilihan):
                pesan_error("Hanya boleh angka valid!")
                enter()
                continue
            
            pilihan = int(pilihan)
            if pilihan < 1 or pilihan > len(id_dengan_funfact):
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
            pesan_error("\nInput Tidak Valid!")
            enter()
        except KeyboardInterrupt:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()
        except EOFError:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()

def delete_funfact():
    id_dengan_funfact = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["funfact"] != "0":
            id_dengan_funfact.append(id_data)

    if not id_dengan_funfact:
        pesan_error("Tidak ada tanaman yang memiliki funfact!")
        enter()
        return

    while True:
        bersihkan_terminal()
        daftar_funfact(id_dengan_funfact, "Daftar Tanaman Dengan Funfact")
        try:
            pilihan = input("\nMasukkan nomor tanaman yang ingin di hapus: ").strip()

            if pilihan == "0":
                break

            elif not re.fullmatch(r"[0-9]+", pilihan):
                pesan_error("Hanya boleh angka valid!")
                enter()
                continue
            
            pilihan = int(pilihan)
            if pilihan < 1 or pilihan > len(id_dengan_funfact):
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
            pesan_error("\nInput Tidak Valid!")
            enter()
        except KeyboardInterrupt:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()
        except EOFError:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()