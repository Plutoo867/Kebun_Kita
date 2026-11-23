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
id_terakhir = len(ensiklopedia)

def cek_tanaman(nama):
    for tanaman in ensiklopedia.values():
        if nama.lower() == tanaman["nama"].lower():
            return True
    return False

def id_tanaman():
    global id_terakhir
    id_terakhir += 1
    return f"id{id_terakhir}"

def daftar_tanaman(ensiklopedia):
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(197)}"
    table = PrettyTable()

    table.title = f"{warna_judul}DAFTAR TANAMAN{Style.reset}"
    table.field_names = ["No", "Nama Tanaman"]
    table.header = False
    table.max_width["No"] = 3
    table.min_width["Nama Tanaman"] = 35
    table.align["Nama Tanaman"] = "l"

    for nomor, tanaman in enumerate(ensiklopedia.values(), start=1):
        tanaman = f"{warna_isi}{tanaman['nama']}{Style.reset}"
        table.add_row([nomor, tanaman])

    print(table)


def table_detail(data):
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(197)}"
    table = PrettyTable()

    table.title = f"{warna_judul}DETAIL TANAMAN{Style.reset}"
    table.field_names = ["Label", "Isi"]
    table.header = False
    table.align = "l"
    table.max_width["Label"] = 15
    table.min_width["Isi"] = 25
    table.max_width["Isi"] = 25

    for label, isi in data.items():
        table.add_row([label, isi])

    print(table)

def pesan_error(teks):
    print(f"{fore(124)}{teks}{Style.reset}")

def pesan_sukses(teks):
    print(f"{fore(29)}{teks}{Style.reset}")

def read_ensiklopedia():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        daftar_tanaman(ensiklopedia)
        print("0. Kembali ke menu utama")
        try:
            detail = int(input("Masukkan nomor tanaman untuk melihat detail: ").strip())
            if detail >= 1 and detail <= len(ensiklopedia):
                id_tanaman = list(ensiklopedia.keys())
                tanaman_terpilih = ensiklopedia[id_tanaman[detail - 1]]
                detail_tanaman = {
                    "Nama Tanaman": tanaman_terpilih["nama"],
                    "Nama Ilmiah": tanaman_terpilih["nama_ilmiah"],
                    "Deskripsi": tanaman_terpilih["deskripsi"],
                    "Manfaat Tanaman": tanaman_terpilih["manfaat"],
                }
                table_detail(detail_tanaman)
                input("\nTekan Enter untuk kembali ke daftar tanaman...")
            elif detail == 0:
                break
            else:
                pesan_error("Koleksi tidak tersedia!")
                input("\nTekan Enter untuk melanjutkan...")
        except ValueError:
            pesan_error("Input Tidak Valid!")
            input("\nTekan Enter untuk melanjutkan...")


def create_ensiklopedia():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        try:
            nama = input("Masukkan nama tanaman          : ").strip()
            ilmiah = input("Masukkan nama ilmiah tanaman   : ").strip()
            desk = input("Masukkan deskripsi tanaman     : ").strip()
            manfaat = input("Masukkan manfaat tanaman       : ").strip()

            if cek_tanaman(nama):
                pesan_error("Koleksi sudah tersedia, silahkan input ulang!")
                input("\nTekan Enter untuk melanjutkan...")
                continue

            if nama == "" or desk == "" or manfaat == "" or ilmiah == "":
                pesan_error("Kolom tidak boleh kosong!")
                input("\nTekan Enter untuk melanjutkan...")
                continue

            ensiklopedia[id_tanaman()] = {
                "nama": nama,
                "nama_ilmiah": ilmiah,
                "deskripsi": desk,
                "manfaat": manfaat,
                "harga": "0",
                "stock": "0",
                "funfact": "0",
            }
            simpan_data()

            pesan_sukses("Koleksi berhasil di tambahkan!")
            input("\nTekan Enter untuk melanjutkan...")
            break
        except ValueError:
            pesan_error("Input Tidak Valid!")
            input("\nTekan Enter untuk melanjutkan...")
            
def update_ensiklopedia():
    os.system("cls" if os.name == "nt" else "clear")
    print("0. Kembali ke menu utama")
    daftar_tanaman(ensiklopedia)
    try:
        edit = int(input("Masukkan nomor tanaman yang ingin diedit: ").strip())

        if edit == 0:
            return
        
        elif edit >= 1 and edit <= len(ensiklopedia):
            id_tanaman = list(ensiklopedia.keys()) 
            tanaman_edit = ensiklopedia[id_tanaman[edit - 1]]

            pesan_sukses("(Tekan Enter jika tidak ingin mengubah)")

            while True:   
                nama_baru      = input(f"Nama Tanaman [{tanaman_edit['nama']}]: ").strip()
                ilmiah_baru    = input(f"Nama Ilmiah [{tanaman_edit['nama_ilmiah']}]: ").strip()
                deskripsi_baru = input(f"Deskripsi [{tanaman_edit['deskripsi']}]: ").strip()
                manfaat_baru   = input(f"Manfaat Tanaman [{tanaman_edit['manfaat']}]: ").strip()

# yakin ingin mengubah daftar

                if nama_baru != "" and cek_tanaman(nama_baru):
                    pesan_error("Koleksi sudah tersedia, silahkan input ulang!")
                    continue

                if nama_baru != "":
                    tanaman_edit["nama"] = nama_baru
                if ilmiah_baru != "":
                    tanaman_edit["nama_ilmiah"] = ilmiah_baru
                if deskripsi_baru != "":
                    tanaman_edit["deskripsi"] = deskripsi_baru
                if manfaat_baru != "":
                    tanaman_edit["makna"] = manfaat_baru

                simpan_data()

                pesan_sukses("Koleksi berhasil diedit!")
                break
        else:
            pesan_error("Koleksi tidak tersedi!")
    except ValueError:
        pesan_error("Input Tidak Valid!")

def delete_ensiklopedia():
    print("0. Kembali ke menu utama")
    daftar_tanaman(ensiklopedia)
    try:
        hapus = int(input("Masukkan nomor tanaman yang ingin dihapus: ").strip())
        if hapus == 0:
            return
        
        elif hapus >= 1 and hapus <= len(ensiklopedia):
            id_tanaman = list(ensiklopedia.keys()) 
            tanaman_hapus = ensiklopedia[id_tanaman[hapus - 1]]
            konfirmasi = input(f"Yakin hapus '{tanaman_hapus['nama']}'(y/t)?: ").strip().lower()
            if konfirmasi == "y":
                ensiklopedia.pop(id_tanaman[hapus - 1])
                simpan_data()
                pesan_sukses("Koleksi berhasil dihapus!")
            elif konfirmasi == "t":
                pesan_sukses("Penghapusan dibatalkan.")
            else:
                pesan_error("Input tidak valid! pilih antara y/t")
        else:
            pesan_error("Koleksi tidak tersedia!")
    except ValueError:
        pesan_error("Input Tidak Valid!")

def search_awal(data, keyword):
    keyword = keyword.lower()
    return {
        id_: info
        for id_, info in data.items()
        if info["nama"].lower().startswith(keyword)
    }

def search_ensiklopedia():
    while True:
        print("0. Kembali ke menu utama")
        keyword = input("Cari nama tanaman (ketik 0 untuk kembali): ").strip()

        if keyword == "0":
            break

        hasil = search_awal(ensiklopedia, keyword)

        if not hasil:
            pesan_error("Tanaman tidak ditemukan.")
            continue

        for data in hasil.values():
            detail_tanaman = {
                "Nama Tanaman": data["nama"],
                "Nama Ilmiah": data["nama_ilmiah"],
                "Deskripsi": data["deskripsi"],
                "Manfaat Tanaman": data["manfaat"],
            }
            table_detail(detail_tanaman)

