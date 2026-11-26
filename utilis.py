import os
import json
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

def muat_rekap():
    if not os.path.exists("rekap.json"):
        return []
    try:
        with open("rekap.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []

def simpan_rekap():
    with open("rekap.json", "w", encoding="utf-8") as file:
        json.dump(data_rekap, file, indent=4, ensure_ascii=False)

data_rekap = muat_rekap()

def load_data_user():
    if not os.path.exists("data_user.json"):
        return {}
    try:
        with open("data_user.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

data_user = load_data_user()

def format_rp(nominal):
    return f"Rp{int(nominal):,}".replace(",", ".")

def pesan_error(teks):
    print(f"{fore(124)}{teks}{Style.reset}")

def pesan_sukses(teks):
    print(f"{fore(29)}{teks}{Style.reset}")

def bersihkan_terminal():
    os.system("cls" if os.name == "nt" else "clear")

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

def header(judul, keterangan):
    table = PrettyTable()

    warna_judul = fore(19)
    warna_isi = fore(33)
    table.title = f"{warna_judul}{judul.upper()}{Style.reset}"
    table.field_names = ["Info"]
    table.header = False
    table.min_width["Info"] = 45
    table.align["Info"] = "c"
    table.add_row([f"{warna_isi}{keterangan}{Style.reset}"])

    print(table)

def daftar_tanaman(ensiklopedia):
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(198)}"
    table = PrettyTable()

    table.title = f"{warna_judul}DAFTAR TANAMAN{Style.reset}"
    table.field_names = ["No", "Nama Tanaman"]
    table.header = False
    table.max_width["No"] = 3
    table.min_width["Nama Tanaman"] = 35
    table.align["Nama Tanaman"] = "l"

    for nomor, tanaman in enumerate(ensiklopedia.values(), start=1):
        tanaman = f"{warna_isi}{tanaman['nama'].capitalize()}{Style.reset}"
        table.add_row([nomor, tanaman])

    print(table)

def table_detail_tanaman(data):
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(198)}"
    table = PrettyTable()

    table.title = f"{warna_judul}DETAIL TANAMAN{Style.reset}"
    table.field_names = ["Label", "Isi"]
    table.header = False
    table.align = "l"
    table.max_width["Label"] = 15
    table.min_width["Isi"] = 25
    table.max_width["Isi"] = 25

    for label, isi, in data.items():
        table.add_row([label, isi])

    print(table)

def daftar_funfact(daftar_id, judul):
    warna_judul: str = f"{fore(214)}"
    warna_isi: str = f"{fore(215)}"

    print("0. Kembali ke Menu Utama")
    table = PrettyTable()

    table.title = f"{warna_judul}{judul.upper()}{Style.reset}"
    table.field_names = ["No", "Nama Tanaman"]
    table.header = False
    table.max_width["No"] = 3
    table.min_width["Nama Tanaman"] = 35
    table.align["Nama Tanaman"] = "l"

    for nomor, id_data in enumerate(daftar_id, start=1):
        tanaman = f"{warna_isi}{ensiklopedia[id_data]['nama'].capitalize()}{Style.reset}"
        table.add_row([nomor, tanaman])

    print(table)

def table_detail_funfact(data):
    warna_judul: str = f"{fore(214)}"
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

def daftar_jual_beli(daftar_id, judul):
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(9)}"

    print("0. Kembali ke Menu Utama")
    table = PrettyTable()

    table.title = f"{warna_judul}{judul.upper()}{Style.reset}"
    table.field_names = ["No", "Nama Tanaman"]
    table.header = False
    table.max_width["No"] = 3
    table.min_width["Nama Tanaman"] = 35
    table.align["Nama Tanaman"] = "l"

    for nomor, id_data in enumerate(daftar_id, start=1):
        tanaman = f"{warna_isi}{ensiklopedia[id_data]['nama'].capitalize()}{Style.reset}"
        table.add_row([nomor, tanaman])

    print(table)

def table_detail_jual_beli(daftar_id):
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(9)}"

    table = PrettyTable()
    table.title = f"{warna_judul}DAFTAR TANAMAN TERSEDIA{Style.reset}"
    table.field_names = ["No", "Nama Tanaman", "Harga", "Stock"]
    table.align = "c"
    table.align["Nama Tanaman"] = "l"
    table.max_width["No"] = 3

    for no, id_tanaman in enumerate(daftar_id, start=1):
        info = ensiklopedia[id_tanaman]
        nama = f"{warna_isi}{info.get('nama', '-').capitalize()}{Style.reset}"
        harga = int(info.get("harga", 0))
        stock = int(info.get("stock", 0))
        table.add_row([
            no,
            nama,
            f"{warna_isi}{format_rp(harga)}{Style.reset}",
            f"{warna_isi}{stock}{Style.reset}",
        ])

    print(table)