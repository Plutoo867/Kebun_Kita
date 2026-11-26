import inquirer
import re
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from colored import fore, Style
from datetime import datetime
from utilis import (ensiklopedia, 
                    data_rekap, 
                    simpan_rekap, 
                    simpan_data, 
                    pesan_error, 
                    pesan_sukses, 
                    bersihkan_terminal, 
                    enter,
                    daftar_jual_beli,
                    format_rp,
                    table_detail_jual_beli)

def cek_tanaman(nama):
    for item in ensiklopedia.values():
        if nama.lower() == item["nama"].lower():
            pesan_sukses("Tanaman ditemukan dalam daftar stock!")
            return True
        else:
            pesan_error("Tanaman tidak ditemukan dalam daftar stock!")
            return False

def tampilkan_struk(keranjang_item, total_belanja, waktu_transaksi):
    warna_judul: str = f"{fore(204)}"
    warna_isi: str = f"{fore(197)}"
    lebar = 44
    print("\n" + "=" * lebar)
    print(f"{warna_judul}{'STRUK PEMBELIAN - KEBUN KITA'.center(lebar)}{Style.reset}")
    print(f"Waktu : {waktu_transaksi}".ljust(lebar))
    print("=" * lebar)
    for item in keranjang_item:
        nama = item["nama"].capitalize()
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
        daftar_jual_beli(id_kosong, "Daftar Tanaman Yang Bisa Dijual")
            
        try:
            pilihan = input("Pilih nomor tanaman: ").strip()
            
            if pilihan == "0":
                break

            elif not re.fullmatch(r"[0-9]+", pilihan):
                pesan_error("Hanya boleh angka valid!")
                enter()
                continue
            
            pilihan = int(pilihan)
            if pilihan < 1 or pilihan > len(id_kosong):
                pesan_error("Nomor tanaman tidak tersedia")
                enter()
                continue
            
            id_pilihan = id_kosong[pilihan - 1]
            
            harga = input("Masukkan harga tanaman: ").strip()
            stock = input("Masukkan stock tanaman: ").strip()

            if harga == "" or stock == "":
                pesan_error("Harga dan stock tidak boleh kosong!")
                enter()
                continue
            elif not re.fullmatch(r"[0-9]+", harga):
                pesan_error("Harga hanya boleh angka!")
                enter()
                continue
            elif not re.fullmatch(r"[0-9]+", stock):
                pesan_error("Stock hanya boleh angka positif!")
                enter()
                continue

            harga_int = int(harga)
            stock_int = int(stock)

            if harga_int < 1000:
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

                if jawaban is None:
                    return

                if jawaban["konfirmasi"] == "Ya":
                    ensiklopedia[id_pilihan]["harga"] = harga_int
                    ensiklopedia[id_pilihan]["stock"] = stock_int
                    simpan_data()
                    pesan_sukses("data berhasil dibuat")
                    enter()
                    return
                elif jawaban["konfirmasi"] == "Tidak":
                    pesan_sukses("data tidak dibuat")
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
        daftar_jual_beli(id_dengan_harga_dan_stock, "Daftar Penjualan Yang Bisa Diedit")
        try:
            edit = input("Masukkan nomor tanaman yang ingin diedit: ").strip()
            if edit == "0":
                break

            elif not re.fullmatch(r"[0-9]+", edit):
                pesan_error("Hanya boleh angka valid!")
                enter()
                continue

            edit = int(edit)
            if edit < 1 or edit > len(id_dengan_harga_dan_stock):
                pesan_error("Nomor tanaman tidak valid!")
                enter()
                continue

            id_pilihan = id_dengan_harga_dan_stock[edit - 1]

            while True:
                try:
                    harga_input = input("Masukkan harga yang baru (kosongkan jika tidak ingin mengubah): ").strip()
                    if harga_input == "":
                        harga_baru = ensiklopedia[id_pilihan]["harga"]
                        break
                
                    harga_baru = int(harga_input)
                    if harga_baru < 1000:
                        pesan_error("Harga minimal 1000!")
                        enter()
                        continue
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
            while True:
                try:
                    stock_input = input("Masukkan stock yang baru (kosongkan jika tidak ingin mengubah): ").strip()
                    if stock_input == "":
                        stock_baru = ensiklopedia[id_pilihan]["stock"]
                        break

                    stock_baru = int(stock_input)
                    if stock_baru < 0:
                        pesan_error("Stock tidak boleh negatif!")
                        enter()
                        continue
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
                    
            konfirmasi = [
                    inquirer.List(
                        "konfirmasi",
                        message="Apakah Anda yakin ingin merubah data ini?",
                        choices=["Ya", "Tidak"],
                        )
                    ]
            jawaban = inquirer.prompt(konfirmasi)

            if jawaban is None:
                return

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
            pesan_error("\nInput Tidak Valid!")
            enter()
        except KeyboardInterrupt:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()
        except EOFError:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
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
        daftar_jual_beli(id_dengan_harga_dan_stock, "Daftar Penjualan Yang Bisa Dihapus")
            
        try:
            pilihan = input("Pilih nomor tanaman: ").strip()         
            if pilihan == "0":
                break

            elif not re.fullmatch(r"[0-9]+", pilihan):
                pesan_error("Hanya boleh angka valid!")
                enter()
                continue
            
            pilihan = int(pilihan)
            if pilihan < 1 or pilihan > len(id_dengan_harga_dan_stock):
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

            if jawaban is None:
                return

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
            pesan_error("\nInput Tidak Valid!")
            enter()
        except KeyboardInterrupt:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()
        except EOFError:
            pesan_error("\nTerjadi error interupsi melalui keyboard!")
            enter()

def beli_tanaman():
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
            print("0. Selesai / Kembali")

            table_detail_jual_beli(id_kosong)

            try:
                nomor = input("Pilih nomor tanaman yang ingin dibeli: ").strip()

                if nomor == "0":
                    break

                elif not re.fullmatch(r"[0-9]+", nomor):
                    pesan_error("Hanya boleh angka valid!")
                    enter()
                    continue
                
                nomor = int(nomor)

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

            try:
                jumlah_beli = input("Input jumlah yg ingin di beli: ").strip()

                if not re.fullmatch(r"[0-9]+", jumlah_beli):
                    pesan_error("Hanya boleh angka valid!")
                    enter()
                    continue
                
                jumlah_beli = int(jumlah_beli)

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
        bersihkan_terminal()

        if keranjang_item:
            simpan_data()

            waktu_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_rekap.append({
                "waktu": waktu_transaksi,
                "items": keranjang_item,
                "total_belanja": total_belanja,
            })
            simpan_rekap()

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
            pesan_sukses("Terima kasih telah berbelanja di Kebun Kita!")
            enter()
            break

def rekap_penjualan():
    bersihkan_terminal()

    if not data_rekap:
        pesan_error("Belum ada data penjualan untuk ditampilkan!")
        enter()
        return

    terjual = {}
    for transaksi in data_rekap:
        for item in transaksi["items"]:
            nama = item["nama"].title()
            if nama in terjual:
                terjual[nama] += item["jumlah"]
            else:
                terjual[nama] = item["jumlah"]

    bars = plt.bar(terjual.keys(), terjual.values())
    plt.bar_label(bars)
    plt.title("Rekap Penjualan Kebun Kita")
    plt.xlabel("Nama Tanaman")
    plt.ylabel("Stok Terjual")
    plt.show()
