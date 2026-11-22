import json, inquirer
import os
from datetime import datetime
from prettytable import PrettyTable
from crud_ensiklopedia import read_ensiklopedia
from crud_funfact import random_funfact

ENSIKLOPEDIA_FILE = "ensiklopedia.json"
REKAP_FILE = "rekap.json"

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

def beli_tanaman():
    while True:
        ensiklopedia = muat_ensiklopedia()
        daftar_id = list(ensiklopedia.keys())

        if not daftar_id:
            print("\nBelum ada data tanaman di ensiklopedia.json.")
            return

        keranjang_item = []
        total_belanja = 0

        while True:
            print("\nBerikut daftar tanaman yang bisa di pesan:")
            table = PrettyTable()
            table.field_names = ["No", "Nama Tanaman", "Harga", "Stock"]

            pilihan_menu = []
            for no, id_tanaman in enumerate(daftar_id, start=1):
                info = ensiklopedia[id_tanaman]
                nama = info.get("nama", "-")
                harga = int(info.get("harga", 0))
                stock = int(info.get("stock", 0))
                table.add_row([no, nama, f"Rp{harga}", stock])
                pilihan_menu.append(f"{no}. {nama} (Rp{harga} | Stock: {stock})")

            print(table)
            pilihan_menu.append("0. Selesai / Kembali")

            jawaban_pilih = inquirer.prompt([
                inquirer.List(
                    "tanaman",
                    message="Pilih nomor tanaman yang ingin dibeli",
                    choices=pilihan_menu,
                )
            ])

            if jawaban_pilih is None or jawaban_pilih["tanaman"].startswith("0."):
                break

            idx = pilihan_menu.index(jawaban_pilih["tanaman"])
            id_terpilih = daftar_id[idx]
            info_terpilih = ensiklopedia[id_terpilih]

            nama_tanaman = info_terpilih.get("nama", "Tanaman")
            harga_satuan = int(info_terpilih.get("harga", 0))
            stok_saat_ini = int(info_terpilih.get("stock", 0))

            if stok_saat_ini <= 0:
                print(f"Maaf, stock tanaman {nama_tanaman} sedang habis!")
                continue

            try:
                jumlah_beli = int(input("Input jumlah yg ingin di beli: ").strip())
            except ValueError:
                print("Jumlah harus berupa angka! Silakan coba lagi.")
                continue

            if jumlah_beli <= 0:
                print("Jumlah harus lebih dari 0! Silakan coba lagi.")
                continue

            if jumlah_beli > stok_saat_ini:
                print(f"Stock tanaman tidak mencukupi. Stock saat ini: {stok_saat_ini}.")
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

            print(f"Berhasil memasukkan {jumlah_beli} {nama_tanaman} (Subtotal: Rp{subtotal}).")

            jawaban_tambah = inquirer.prompt([
                inquirer.Confirm(
                    "tambah_lain",
                    message="Ingin input tanaman lain?",
                    default=True,
                )
            ])
            if jawaban_tambah is None or not jawaban_tambah["tambah_lain"]:
                break

        if keranjang_item:
            simpan_ensiklopedia(ensiklopedia)

            data_rekap = muat_rekap()
            data_rekap.append({
                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "items": keranjang_item,
                "total_belanja": total_belanja,
            })
            simpan_rekap(data_rekap)

            print("\nBerikut adalah total belanja anda:")
            for item in keranjang_item:
                print(f"- {item['nama']} x{item['jumlah']} = Rp{item['subtotal']}")
            print(f"Total Belanja: Rp{total_belanja}")
        else:
            print("\nTidak ada tanaman yang dibeli.")

        jawaban_transaksi = inquirer.prompt([
            inquirer.Confirm(
                "transaksi_lagi",
                message="Ingin melakukan pembelian lagi?",
                default=False,
            )
        ])
        if jawaban_transaksi is None or not jawaban_transaksi["transaksi_lagi"]:
            print("Terima kasih telah berbelanja di Kebun Kita!")
            break

def menu_user():
    while True:
        jawaban = inquirer.prompt([
            inquirer.List(
                "menu",
                message="Menu Kebun Kita",
                choices=[
                    "1. Beli Tanaman",
                    "2. Ensiklopedia",
                    "3. Funfact",
                    "4. Logout",
                ],
            )
        ])
        if jawaban is None or jawaban["menu"].startswith("4."):
            break

        if jawaban["menu"].startswith("1."):
            beli_tanaman()
        elif jawaban["menu"].startswith("2."):
            read_ensiklopedia()
        elif jawaban["menu"].startswith("3."):
            random_funfact()