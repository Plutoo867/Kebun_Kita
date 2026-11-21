import os
import json
from prettytable import PrettyTable
from colored import fore, Style

id_terakhir = 0

def load_data():
    if not os.path.exists("ensiklopedia.json"):
        return {}
    try:
        with open("ensiklopedia.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

ensiklopedia = load_data()

def daftar_tanaman(ensiklopedia):
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(197)}"
    table = PrettyTable()

    table.title = (f"{warna_judul}DAFTAR TANAMAN{Style.reset}")
    table.field_names = ["No", "Nama Tanaman"]
    table.header = False
    table.max_width["No"] = 3
    table.min_width["Nama Tanaman"] = 35
    table.align["Nama Tanaman"] = "l"


    for nomor, tanaman in enumerate(ensiklopedia.values(), start=1):
        tanaman = (f"{warna_isi}{tanaman["nama"]}{Style.reset}")
        table.add_row([nomor, tanaman])

    print(table)

def table_detail(data):
    table = PrettyTable()

    table.title = "DETAIL TAMANAN"
    table.field_names = ["Label", "Isi"]

    table.header = False
    table.align = "l"
    table.max_width["Label"] = 15
    table.min_width["Isi"] = 25
    table.max_width["Isi"] = 25

    for label, isi in data.items():
        table.add_row([label, isi])

    print(table)

def read_ensiklopedia():
    while True:
        print("0. Kembali ke menu utama")
        daftar_tanaman(ensiklopedia)
        try:
            detail = int(input("Masukkan nomor tanaman untuk melihat detail: "))
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
            elif detail == 0:
                break
            else:
                print(f"{fore(124)}Koleksi tidak tersedia!{Style.reset}")
        except ValueError:
            print(f"{fore(124)}Input Tidak Valid!{Style.reset}")

def cek_tanaman(nama):
    for tanaman in ensiklopedia.values():
        if nama.lower() == tanaman["nama"].lower():
            return True
    return False

def id_tanaman():
    global id_terakhir
    id_terakhir += 1
    return f"id{id_terakhir}"

def create_ensiklopedia():
    while True:
        try:
            nama = input("Masukkan nama tanaman             : ")
            ilmiah = input("Masukkan nama ilmiah tanaman    : ")
            desk = input("Masukkan deskripsi tanaman        : ")
            manfaat = input("Masukkan manfaat tanaman       : ")

            if cek_tanaman(nama):
                print(f"{fore(124)}Koleksi sudah tersedia, silahkan input ulang!{Style.reset}")
                continue

            elif nama == "" or desk == "" or manfaat == "" or ilmiah == "":
                print(f"{fore(124)}Kolom tidak boleh kosong!{Style.reset}")
                continue

            else:
                ensiklopedia[id_tanaman()] =({
                                "nama": nama,
                                "nama_ilmiah": ilmiah,
                                "deskripsi": desk, 
                                "manfaat": manfaat,
                                "harga": "0",
                                "stock": "0",
                                "funfact": "0"
                                })

                with open("ensiklopedia.json", "w", encoding="utf-8") as file:
                    json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)

                print(f"{fore(29)}Koleksi berhasil di tambahkan!{Style.reset}")
                break
        except ValueError:
            print(f"{fore(124)}Input Tidak Valid!{Style.reset}")
        
def update_ensiklopedia():
    print("0. Kembali ke menu utama")
    daftar_tanaman(ensiklopedia)
    try:
        edit = int(input("Masukkan nomor tanaman yang ingin diedit: "))

        if edit == 0:
            pass
        elif edit >= 1 and edit <= len(ensiklopedia):
            id_tanaman = list(ensiklopedia.keys()) 
            tanaman_edit = ensiklopedia[id_tanaman[edit - 1]]

            print(f"{fore(29)}(Tekan Enter jika tidak ingin mengubah){Style.reset}")

            while True:   
                nama_baru = input(f"Nama Tanaman [{tanaman_edit["nama"]}]: ")
                ilmiah_baru = input(f"Nama Ilmiah [{tanaman_edit["nama_ilmiah"]}]: ")
                deskripsi_baru = input(f"Deskripsi [{tanaman_edit["deskripsi"]}]: ")
                manfaat_baru = input(f"Manfaat Bunga [{tanaman_edit["manfaat"]}]: ")

                if nama_baru != "" and cek_tanaman(nama_baru):
                    print(f"{fore(124)}Koleksi sudah tersedia, silahkan input ulang!{Style.reset}")
                    continue

                if nama_baru != "":
                    tanaman_edit["nama"] = nama_baru
                if ilmiah_baru != "":
                    tanaman_edit["nama_ilmiah"] = ilmiah_baru
                if deskripsi_baru != "":
                    tanaman_edit["deskripsi"] = deskripsi_baru
                if manfaat_baru != "":
                    tanaman_edit["makna"] = manfaat_baru

                with open("ensiklopedia.json", "w", encoding="utf-8") as file:
                    json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)

                print(f"{fore(29)}Koleksi berhasil diedit!{Style.reset}")
                break
        else:
            print(f"{fore(124)}Koleksi tidak tersedi!{Style.reset}")
    except ValueError:
        print(f"{fore(124)}Input Tidak Valid!{Style.reset}")

def delete_ensiklopedia():
    print("0. Kembali ke menu utama")
    daftar_tanaman(ensiklopedia)
    try:
        hapus = int(input("Masukkan nomor tanaman yang ingin dihapus: "))
        if hapus == 0:
            pass
        elif hapus >= 1 and hapus <= len(ensiklopedia):
            id_tanaman = list(ensiklopedia.keys()) 
            tanaman_hapus = ensiklopedia[id_tanaman[hapus - 1]]
            konfirmasi = input(f"Yakin hapus '{tanaman_hapus['nama']}'(y/t)?: ").lower()
            if konfirmasi == "y":
                ensiklopedia.pop(id_tanaman[hapus - 1])

                with open("ensiklopedia.json", "w", encoding="utf-8") as file:
                    json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)
                
                print(f"{fore(29)}Koleksi berhasil dihapus!{Style.reset}")
            elif konfirmasi == "t":
                print(f"{fore(29)}Penghapusan dibatalkan.{Style.reset}")
            else:
                print(f"{fore(124)}Input tidak valid! pilih antara y/t{Style.reset}")
        else:
            print(f"{fore(124)}Koleksi tidak tersedi!{Style.reset}")
    except ValueError:
        print(f"{fore(124)}Input Tidak Valid!{Style.reset}")

# delete_ensiklopedia()