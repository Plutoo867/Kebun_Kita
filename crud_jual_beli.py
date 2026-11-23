import json, inquirer, os, inquirer
from datetime import datetime
from prettytable import PrettyTable

def load_data():
    if not os.path.exists("ensiklopedia.json"):
        return {}
    try:
        with open("ensiklopedia.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

ensiklopedia = load_data()

def cek_tanaman(nama):
    for item in ensiklopedia.values():
        if nama.lower() == item["nama"].lower():
            print("Bunga ditemukan dalam daftar stock!")
            return True
        else:
            print("Bunga tidak ditemukan dalam daftar stock!")
            return False


def read_data():
    id_kosong = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["harga"] == "0" and ensiklopedia[id_data]["stock"] == "0":
            id_kosong.append(id_data)

    if not id_kosong:
        print("Tidak ada tanaman yang bisa dijual!")
        return

    table = PrettyTable()
    table.field_names = ("No", "Nama Tanaman", "Harga", "Stock")
    no = 1
    for id_data in id_kosong:
        tanaman = ensiklopedia[id_data]["nama"]
        harga = ensiklopedia[id_data]["harga"]
        stock = ensiklopedia[id_data]["stock"]
        table.add_row([
            no,
            tanaman,
            harga,
            stock
        ])
        no += 1

    print(table)

def create_data():
    id_kosong = []
    
    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["harga"] == "0" and ensiklopedia[id_data]["stock"] == "0":
            id_kosong.append(id_data)     
    
    if not id_kosong:
        print("Tidak ada tanaman yang bisa dijual!")
        return
    
    while True:
        print("0. Kembali ke Menu Utama")
        print("Daftar Tanaman Yang Bisa Dijual")
        
        for nomor, id_data in enumerate(id_kosong, start=1):
            print(f"{nomor}. {ensiklopedia[id_data]['nama']}")
            
        try:
            pilihan = int(input("Pilih nomor tanaman: "))
            
            if pilihan == 0:
                print("Kembali ke menu utama")
                return
            elif pilihan < 1 or pilihan > len(id_kosong):
                print("Nomor tanaman tidak tersedia")
                continue
            
            id_pilihan = id_kosong[pilihan - 1]
            
            harga = int(input("Masukkan harga tanaman: "))
            stock = int(input("Masukkan stock tanaman: "))
            if harga == "" and stock == "":
                print("Harga dan stock tidak boleh kosong!")
                continue
            elif harga < 1000 or stock < 0:
                print("Harga minimal 1000!")
                continue
            konfirmasi = [
                inquirer.List(
                    "konfirmasi",
                    message="Apakah Anda yakin ingin menambah data ini?",
                    choices=["Ya", "Tidak"],
                    )
                ]
            jawaban = inquirer.prompt(konfirmasi)
            if jawaban["konfirmasi"] == "Ya":
                ensiklopedia[id_pilihan]["harga"] = harga
                ensiklopedia[id_pilihan]["stock"] = stock
                with open("ensiklopedia.json", "w", encoding="utf-8") as file:
                    json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)
                print("data berhasil dibuat")
                return
            elif jawaban["konfirmasi"] == "Tidak":
                print("data tidak dibuat")
        except ValueError:
            print("Harga dan stock harus berupa angka!")
    
        
def delete_data():
    id_dengan_harga_dan_stock = []
    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["harga"] != "0" and ensiklopedia[id_data]["stock"] != "0":
            id_dengan_harga_dan_stock.append(id_data)     
    
    if not id_dengan_harga_dan_stock:
        print("Tidak ada penjualan yang bisa dihapus!")
        return
    while True:
        print("0. Kembali ke Menu Utama")
        print("Daftar Penjualan Yang Bisa Dihapus")
        
        for nomor, id_data in enumerate(id_dengan_harga_dan_stock, start=1):
            print(f"{nomor}. {ensiklopedia[id_data]['nama']}")
            
        try:
            pilihan = int(input("Pilih nomor tanaman: "))            
            if pilihan == 0:
                print("Kembali ke menu utama")
                return
            elif pilihan < 1 or pilihan > len(id_dengan_harga_dan_stock):
                print("Nomor tanaman tidak tersedia")
                continue
            
            id_pilihan = id_dengan_harga_dan_stock[pilihan - 1]
            
            konfirmasi = [
                inquirer.List(
                    "konfirmasi",
                    message="Apakah Anda yakin ingin menghapus data ini?",
                    choices=["Ya", "Tidak"],
                    )
                ]
            jawaban = inquirer.prompt(konfirmasi)
            if jawaban["konfirmasi"] == "Ya":
                ensiklopedia[id_pilihan]["harga"] = "0"
                ensiklopedia[id_pilihan]["stock"] = "0"                
                with open("ensiklopedia.json", "w", encoding="utf-8") as file:
                    json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)
                print("data berhasil dihapus!")
                return
            elif jawaban["konfirmasi"] == "Tidak":
                print("data tidak dihapus")
        except ValueError:
            print("Harga dan stock harus berupa angka!")

def edit_data():
    id_dengan_harga_dan_stock = []
    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["harga"] != "0" and ensiklopedia[id_data]["stock"] != "0":
            id_dengan_harga_dan_stock.append(id_data)
    if not id_dengan_harga_dan_stock:
        print("Tidak ada penjualan yang bisa diedit!")
        return

    while True:
        print("0. Kembali ke Menu Utama")
        print("Daftar Penjualan Yang Bisa Diedit")
        for nomor, id_data in enumerate(id_dengan_harga_dan_stock, start=1):
            print(f"{nomor}. {ensiklopedia[id_data]['nama']}")
        try:
            edit = int(input("Masukkan nomor tanaman yang ingin diedit: "))
            if edit == 0:
                print("Kembali ke menu utama")
                return
            if edit < 1 or edit > len(id_dengan_harga_dan_stock):
                print("Nomor tanaman tidak valid!")
                continue

            id_pilihan = id_dengan_harga_dan_stock[edit - 1]

            while True:
                harga_input = int(input("Masukkan harga yang baru (kosongkan jika tidak ingin mengubah): "))
                if harga_input == "":
                    harga_baru = ensiklopedia[id_pilihan]["harga"]
                    break
                try:
                    harga_baru = int(harga_input)
                    if harga_baru < 1000:
                        print("Harga minimal 1000!")
                        continue
                    break
                except ValueError:
                    print("Harga hanya boleh berupa angka!")
            while True:
                stock_input = int(input("Masukkan stock yang baru (kosongkan jika tidak ingin mengubah): "))
                if stock_input == "":
                    stock_baru = ensiklopedia[id_pilihan]["stock"]
                    break
                try:
                    stock_baru = int(stock_input)
                    if stock_baru < 0:
                        print("Stock tidak boleh negatif!")
                        continue
                    break
                except ValueError:
                    print("Stock hanya boleh berupa angka!")
                    
            konfirmasi = [
                    inquirer.List(
                        "konfirmasi",
                        message="Apakah Anda yakin ingin merubah data ini?",
                        choices=["Ya", "Tidak"],
                        )
                    ]
            jawaban = inquirer.prompt(konfirmasi)
            if jawaban["konfirmasi"] == "Ya":
                ensiklopedia[id_pilihan]["harga"] = harga_baru
                ensiklopedia[id_pilihan]["stock"] = stock_baru
                with open("ensiklopedia.json", "w", encoding="utf-8") as file:
                    json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)
                print("Data tanaman berhasil diperbarui!")
                return
            elif jawaban["konfirmasi"] == "Tidak":
                print("data tidak diedit")
        except ValueError:
            print("Masukkan nomor berupa angka!")

read_data()

ENSIKLOPEDIA_FILE = "ensiklopedia.json"
REKAP_FILE = "rekap.json"

def format_rp(nominal):
    return f"Rp{int(nominal):,}".replace(",", ".")

def bersihkan_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def muat_ensiklopedia():
    if not os.path.exists(ENSIKLOPEDIA_FILE):
        return {}
    try:
        with open(ENSIKLOPEDIA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}

def simpan_ensiklopedia(data):
    with open(ENSIKLOPEDIA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def muat_rekap():
    if not os.path.exists(REKAP_FILE):
        return []
    try:
        with open(REKAP_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []

def simpan_rekap(data_rekap):
    with open(REKAP_FILE, "w", encoding="utf-8") as file:
        json.dump(data_rekap, file, indent=4, ensure_ascii=False)

def tampilkan_struk(keranjang_item, total_belanja, waktu_transaksi):
    lebar = 44
    print("\n" + "=" * lebar)
    print("STRUK PEMBELIAN - KEBUN KITA".center(lebar))
    print(f"Waktu : {waktu_transaksi}".ljust(lebar))
    print("=" * lebar)
    for item in keranjang_item:
        nama = item["nama"]
        jumlah = item["jumlah"]
        harga = format_rp(item["harga"])
        subtotal = format_rp(item["subtotal"])
        print(f"{nama} ({jumlah} x {harga})")
        print("  Subtotal".ljust(lebar - 14) + f": {subtotal}")
    print("-" * lebar)
    print("TOTAL BELANJA".ljust(lebar - 14) + f": {format_rp(total_belanja)}")
    print("=" * lebar)
    print("Terima kasih telah berbelanja!".center(lebar))
    print("=" * lebar)

def beli_tanaman():
    while True:
        bersihkan_terminal()
        ensiklopedia = muat_ensiklopedia()
        daftar_id = list(ensiklopedia.keys())

        if not daftar_id:
            print("\nBelum ada data tanaman di ensiklopedia.json.")
            input("\nTekan Enter untuk kembali...")
            return

        keranjang_item = []
        total_belanja = 0

        while True:
            bersihkan_terminal()
            print("Berikut daftar tanaman yang bisa di pesan:")
            table = PrettyTable()
            table.field_names = ["No", "Nama Tanaman", "Harga", "Stock"]

            for no, id_tanaman in enumerate(daftar_id, start=1):
                info = ensiklopedia[id_tanaman]
                nama = info.get("nama", "-")
                harga = int(info.get("harga", 0))
                stock = int(info.get("stock", 0))
                table.add_row([no, nama, format_rp(harga), stock])

            print(table)
            print("0. Selesai / Kembali")

            try:
                nomor = int(input("Pilih nomor tanaman yang ingin dibeli: ").strip())
            except ValueError:
                print("Nomor harus berupa angka! Silakan coba lagi.")
                input("\nTekan Enter untuk melanjutkan...")
                continue

            if nomor == 0:
                break

            if not (1 <= nomor <= len(daftar_id)):
                print("Pilihan nomor tanaman tidak tersedia! Silakan coba lagi.")
                input("\nTekan Enter untuk melanjutkan...")
                continue

            id_terpilih = daftar_id[nomor - 1]
            info_terpilih = ensiklopedia[id_terpilih]

            nama_tanaman = info_terpilih.get("nama", "Tanaman")
            harga_satuan = int(info_terpilih.get("harga", 0))
            stok_saat_ini = int(info_terpilih.get("stock", 0))

            if stok_saat_ini <= 0:
                print(f"Maaf, stock tanaman {nama_tanaman} sedang habis!")
                input("\nTekan Enter untuk melanjutkan...")
                continue

            try:
                jumlah_beli = int(input("Input jumlah yg ingin di beli: ").strip())
            except ValueError:
                print("Jumlah harus berupa angka! Silakan coba lagi.")
                input("\nTekan Enter untuk melanjutkan...")
                continue

            if jumlah_beli <= 0:
                print("Jumlah harus lebih dari 0! Silakan coba lagi.")
                input("\nTekan Enter untuk melanjutkan...")
                continue

            if jumlah_beli > stok_saat_ini:
                print(f"Stock tanaman tidak mencukupi. Stock saat ini: {stok_saat_ini}.")
                input("\nTekan Enter untuk melanjutkan...")
                continue

            subtotal = jumlah_beli * harga_satuan
            info_terpilih["stock"] = stok_saat_ini - jumlah_beli
            total_belanja += subtotal

            keranjang_item.append({
                "id": id_terpilih,
                "nama": nama_tanaman,
                "harga": harga_satuan,
                "jumlah": jumlah_beli,
                "subtotal": subtotal,
            })

            print(
                f"Berhasil memasukkan {jumlah_beli} {nama_tanaman} "
                f"(Subtotal: {format_rp(subtotal)})."
            )

            tambah_lain = input("Ingin input tanaman lain? (y/n): ").strip().lower()
            if tambah_lain == "n":
                break
            elif tambah_lain != "y":
                print("Input tidak dikenali, dianggap tidak menambah tanaman lain.")
                break

        bersihkan_terminal()
        if keranjang_item:
            simpan_ensiklopedia(ensiklopedia)

            waktu_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_rekap = muat_rekap()
            data_rekap.append({
                "waktu": waktu_transaksi,
                "items": keranjang_item,
                "total_belanja": total_belanja,
            })
            simpan_rekap(data_rekap)

            tampilkan_struk(keranjang_item, total_belanja, waktu_transaksi)
        else:
            print("\nTidak ada tanaman yang dibeli.")

        jawaban_transaksi = inquirer.prompt([
            inquirer.List(
                "transaksi_lagi",
                message="Ingin melakukan pembelian lagi?",
                choices=["Ya", "Tidak"],
            )
        ])
        if jawaban_transaksi is None or jawaban_transaksi["transaksi_lagi"] != "Ya":
            print("Terima kasih telah berbelanja di Kebun Kita!")
            break