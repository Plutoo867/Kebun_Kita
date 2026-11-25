import os
import json
import inquirer
from prettytable import PrettyTable
from colored import fore, Style
from datetime import datetime

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

def simpan_rekap(data_rekap):
    with open("rekap.json", "w", encoding="utf-8") as file:
        json.dump(data_rekap, file, indent=4, ensure_ascii=False)

def cek_tanaman(nama):
    for item in ensiklopedia.values():
        if nama.lower() == item["nama"].lower():
            print("Bunga ditemukan dalam daftar stock!")
            return True
        else:
            print("Bunga tidak ditemukan dalam daftar stock!")
            return False

def format_rp(nominal):
    return f"Rp{int(nominal):,}".replace(",", ".")

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

def tampilkan_struk(keranjang_item, total_belanja, waktu_transaksi):
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(197)}"
    lebar = 44
    print("\n" + "=" * lebar)
    print(f"{warna_judul}{'STRUK PEMBELIAN - KEBUN KITA'.center(lebar)}{Style.reset}")
    print(f"Waktu : {waktu_transaksi}".ljust(lebar))
    print("=" * lebar)
    for item in keranjang_item:
        nama = item["nama"]
        jumlah = item["jumlah"]
        harga = format_rp(item["harga"])
        subtotal = format_rp(item["subtotal"])
        print(f"{warna_isi}{nama}{Style.reset} ({jumlah} x {harga})")
        print("  Subtotal".ljust(lebar - 14) + f": {subtotal}")
    print("-" * lebar)
    print(f"{warna_judul}{'TOTAL BELANJA'.ljust(lebar - 14)}{Style.reset}" + f": {format_rp(total_belanja)}")
    print("=" * lebar)
    print(f"{warna_judul}{'Terima kasih telah berbelanja!'.center(lebar)}{Style.reset}")
    print("=" * lebar)

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

def read_jual_beli():
    bersihkan_terminal()
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(197)}"
    id_kosong = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["harga"] != "0" and ensiklopedia[id_data]["stock"] != "0":
            id_kosong.append(id_data)

    if not id_kosong:
        pesan_error("Tidak ada tanaman yang bisa dijual!")
        enter()
        return

    table = PrettyTable()
    table.title = f"{warna_judul}DAFTAR TANAMAN TERSEDIA{Style.reset}"
    table.field_names = ["No", "Nama Tanaman", "Harga", "Stock"]
    table.align = "c"
    table.align["Nama Tanaman"] = "l"
    table.max_width["No"] = 3

    for no, id_tanaman in enumerate(id_kosong, start=1):
        info = ensiklopedia[id_tanaman]
        nama = f"{warna_isi}{info.get('nama', '-')}{Style.reset}"
        harga = int(info.get("harga", 0))
        stock = int(info.get("stock", 0))
        table.add_row([
            no,
            nama,
            f"{warna_isi}{format_rp(harga)}{Style.reset}",
            f"{warna_isi}{stock}{Style.reset}",
        ])

    print(table)
    enter()

def create_jual_beli():
    id_kosong = []
    
    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["harga"] == "0" and ensiklopedia[id_data]["stock"] == "0":
            id_kosong.append(id_data)     
    
    if not id_kosong:
        pesan_error("Tidak ada tanaman yang bisa dijual!")
        enter()
        return
    
    while True:
        bersihkan_terminal()
        tampilkan_daftar(id_kosong, "Daftar Tanaman Yang Bisa Dijual")
            
        try:
            pilihan = int(input("Pilih nomor tanaman: ").strip())
            
            if pilihan == 0:
                break
            elif pilihan < 1 or pilihan > len(id_kosong):
                pesan_error("Nomor tanaman tidak tersedia")
                enter()
                continue
            
            id_pilihan = id_kosong[pilihan - 1]
            
            harga = int(input("Masukkan harga tanaman: ").strip())
            stock = int(input("Masukkan stock tanaman: ").strip())
            if harga == "" and stock == "":
                pesan_error("Harga dan stock tidak boleh kosong!")
                enter()
                continue
            elif harga < 1000 or stock < 0:
                pesan_error("Harga minimal 1000!")
                enter()
                continue
            else:
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
                    simpan_data()
                    pesan_sukses("data berhasil dibuat")
                    enter()
                    return
                elif jawaban["konfirmasi"] == "Tidak":
                    pesan_sukses("data tidak dibuat")
                    enter()
                    break
        except ValueError:
            pesan_error("Harga dan stock harus berupa angka!")
            enter()

def update_jual_beli():
    id_dengan_harga_dan_stock = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["harga"] != "0" and ensiklopedia[id_data]["stock"] != "0":
            id_dengan_harga_dan_stock.append(id_data)

    if not id_dengan_harga_dan_stock:
        pesan_error("Tidak ada penjualan yang bisa diedit!")
        enter()
        return

    while True:
        bersihkan_terminal()
        tampilkan_daftar(id_dengan_harga_dan_stock, "Daftar Penjualan Yang Bisa Diedit")
        try:
            edit = int(input("Masukkan nomor tanaman yang ingin diedit: ").strip())
            if edit == 0:
                break
            if edit < 1 or edit > len(id_dengan_harga_dan_stock):
                pesan_error("Nomor tanaman tidak valid!")
                enter()
                continue

            id_pilihan = id_dengan_harga_dan_stock[edit - 1]

            while True:
                harga_input = int(input("Masukkan harga yang baru (kosongkan jika tidak ingin mengubah): ").strip())
                if harga_input == "":
                    harga_baru = ensiklopedia[id_pilihan]["harga"]
                    break
                try:
                    harga_baru = int(harga_input)
                    if harga_baru < 1000:
                        pesan_error("Harga minimal 1000!")
                        enter()
                        continue
                    break
                except ValueError:
                    pesan_error("Harga hanya boleh berupa angka!")
                    enter()
            while True:
                stock_input = int(input("Masukkan stock yang baru (kosongkan jika tidak ingin mengubah): ").strip())
                if stock_input == "":
                    stock_baru = ensiklopedia[id_pilihan]["stock"]
                    break
                try:
                    stock_baru = int(stock_input)
                    if stock_baru < 0:
                        pesan_error("Stock tidak boleh negatif!")
                        enter()
                        continue
                    break
                except ValueError:
                    pesan_error("Stock hanya boleh berupa angka!")
                    
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
                simpan_data()
                pesan_sukses("Data tanaman berhasil diperbarui!")
                enter()
                return
            elif jawaban["konfirmasi"] == "Tidak":
                pesan_sukses("data tidak diedit")
                enter()
        except ValueError:
            pesan_error("Masukkan nomor berupa angka!")
            enter()
        
def delete_jual_beli():
    id_dengan_harga_dan_stock = []
    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["harga"] != "0" and ensiklopedia[id_data]["stock"] != "0":
            id_dengan_harga_dan_stock.append(id_data)     
    
    if not id_dengan_harga_dan_stock:
        pesan_error("Tidak ada penjualan yang bisa dihapus!")
        enter()
        return
    while True:
        bersihkan_terminal()
        tampilkan_daftar(id_dengan_harga_dan_stock, "Daftar Penjualan Yang Bisa Dihapus")
            
        try:
            pilihan = int(input("Pilih nomor tanaman: ").strip())            
            if pilihan == 0:
                break
            elif pilihan < 1 or pilihan > len(id_dengan_harga_dan_stock):
                pesan_error("Nomor tanaman tidak tersedia")
                enter()
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
                simpan_data()
                pesan_sukses("data berhasil dihapus!")
                enter()
                return
            elif jawaban["konfirmasi"] == "Tidak":
                pesan_sukses("data tidak dihapus")
                enter()
                break
        except ValueError:
            pesan_error("Harga dan stock harus berupa angka!")
            enter()

def beli_tanaman():
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(197)}"
    while True:
        bersihkan_terminal()
        id_kosong = []
        
        for id_data in ensiklopedia:
            if ensiklopedia[id_data]["harga"] != "0" and ensiklopedia[id_data]["stock"] != "0":
                id_kosong.append(id_data)
    
        if not id_kosong:
            pesan_error("Tidak ada tanaman yang bisa dijual!")
            enter()
            return

        keranjang_item = []
        total_belanja = 0

        while True:
            bersihkan_terminal()
            print("Berikut daftar tanaman yang bisa di pesan:")
            print("0. Selesai / Kembali")
            table = PrettyTable()
            table.title = f"{warna_judul}DAFTAR TANAMAN TERSEDIA{Style.reset}"
            table.field_names = ["No", "Nama Tanaman", "Harga", "Stock"]
            table.align = "c"
            table.align["Nama Tanaman"] = "l"
            table.max_width["No"] = 3

            for no, id_tanaman in enumerate(id_kosong, start=1):
                info = ensiklopedia[id_tanaman]
                nama = f"{warna_isi}{info.get('nama', '-')}{Style.reset}"
                harga = int(info.get("harga", 0))
                stock = int(info.get("stock", 0))
                table.add_row([
                    no,
                    nama,
                    f"{warna_isi}{format_rp(harga)}{Style.reset}",
                    f"{warna_isi}{stock}{Style.reset}",
                ])

            print(table)

            try:
                nomor = int(input("Pilih nomor tanaman yang ingin dibeli: ").strip())
            except ValueError:
                pesan_error("Nomor harus berupa angka! Silakan coba lagi.")
                enter()
                continue

            if nomor == 0:
                break

            if not (1 <= nomor <= len(id_kosong)):
                pesan_error("Pilihan nomor tanaman tidak tersedia! Silakan coba lagi.")
                enter()
                continue

            id_terpilih = id_kosong[nomor - 1]
            info_terpilih = ensiklopedia[id_terpilih]

            nama_tanaman = info_terpilih.get("nama", "Tanaman")
            harga_satuan = int(info_terpilih.get("harga", 0))
            stok_saat_ini = int(info_terpilih.get("stock", 0))

            if stok_saat_ini <= 0:
                pesan_error(f"Maaf, stock tanaman {nama_tanaman} sedang habis!")
                enter()
                continue

            try:
                jumlah_beli = int(input("Input jumlah yg ingin di beli: ").strip())
            except ValueError:
                pesan_error("Jumlah harus berupa angka! Silakan coba lagi.")
                enter()
                continue

            if jumlah_beli <= 0:
                pesan_error("Jumlah harus lebih dari 0! Silakan coba lagi.")
                enter()
                continue

            if jumlah_beli > stok_saat_ini:
                pesan_error(f"Stock tanaman tidak mencukupi. Stock saat ini: {stok_saat_ini}.")
                enter()
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

            pesan_sukses(
                f"Berhasil memasukkan {jumlah_beli} {nama_tanaman} "
                f"(Subtotal: {format_rp(subtotal)})."
            )

            konfirmasi = [
                inquirer.List(
                    "konfirmasi",
                    message=f"Ingin input tanaman lain?",
                    choices=["Ya", "Tidak"],
                )
            ]
            jawaban = inquirer.prompt(konfirmasi)

            if jawaban is None or jawaban["konfirmasi"] == "Tidak":
                break
        bersihkan_terminal()

        if keranjang_item:
            simpan_data()

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
            pesan_error("\nTidak ada tanaman yang dibeli.")

        jawaban_transaksi = inquirer.prompt([
            inquirer.List(
                "transaksi_lagi",
                message="Ingin melakukan pembelian lagi?",
                choices=["Ya", "Tidak"],
            )
        ])
        if jawaban_transaksi is None or jawaban_transaksi["transaksi_lagi"] != "Ya":
            print("Terima kasih telah berbelanja di Kebun Kita!")
            enter()
            break

