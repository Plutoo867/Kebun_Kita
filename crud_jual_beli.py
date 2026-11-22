import json, inquirer, os 
from datetime import datetime
from prettytable import PrettyTable

def cek_bunga():
    with open("ensiklopedia.json", "r") as file:
        data = json.load(file)

    for item in data["kamus_tanaman"]:
       if item == "bunga":
           print("Bunga ditemukan dalam daftar stock!")
           return True
       else:
           print("Bunga tidak ditemukan dalam daftar stock!")
           return False

def lihat_stok():
    with open("ensiklopedia.json","r") as file:
        data = json.load(file)
    table = PrettyTable()
    table.field_names = ["No", "Nama Barang", "Harga", "Stock"]
    for no, item in enumerate(data["kamus_tanaman"], start=1):
        table.add_row([
            no,
            item["nama_tanaman"], 
            item["harga"], 
            item["stock"]])  
    print(table)
    
def tambah_data():
    with open("ensiklopedia.json", "r") as file:
        data = json.load(file)
    tanaman = input("Tambahkan daftar tanaman: ").strip().lower()
    for item in data["kamus_tanaman"]:
        if item["harga"] == tanaman.lower():
            if item["stock"] == 0 and item["harga"] == 0:
                print("Berikut daftar tanaman dan stock: ")
                table = PrettyTable()
                table.field_names = ["Nama Barang", "Harga", "Stock"]    
                for item in data["kamus_tanaman"]:
                    table.add_row([
                        item["nama_tanaman"],
                        item["harga"], 
                        item["stock"]
                        ]
                        )
                print(table) 
                try:  
                    harga = int(input("Harga tanaman: ").strip())
                    stock = int(input("Stok tanaman: ").strip())
                    for item in data["kamus_tanaman"]:
                        if harga == "" or stock == "":
                            print("Data tidak boleh kosong!")
                            return
                    tanaman_baru = {
                        "nama_tanaman": tanaman,
                        "harga": harga,
                        "stock": stock
                    }
                    data["kamus_tanaman"].append(tanaman_baru)
                    with open("ensiklopedia.json", "w") as file:
                        json.dump(data, file)
                    print(f"Tanaman {tanaman} berhasil ditambahkan ke daftar stock!")
                except ValueError:
                    print("Harga dan stock harus berupa angka!")
                    return
                return 
            else:
                print(f"Tanaman {tanaman} sudah ada dalam daftar stok!")
                return  
        else:
            print(f"Tanaman {tanaman} sudah ada dalam daftar stok!")
            return

def hapus_data():
    with open("ensiklopedia.json", "r") as file:
        data = json.load(file)
    print("Berikut daftar tanaman dan stock: ")
    table = PrettyTable()
    table.field_names = ["Nama Barang", "Harga", "Stock"]
    for item in data["kamus_tanaman"]:
        table.add_row([item["nama_tanaman"],item["harga"], item["stock"]])
    print(table)
    
    tanaman = input("Masukkan nama tanaman yang ingin dihapus: ").strip().lower()
    for item in data["kamus_tanaman"]:
        if item["nama_tanaman"].lower() == tanaman.lower():
            data["kamus_tanaman"].remove(item)
            with open("ensiklopedia.json", "w") as file:
                json.dump(data, file)
            print(f"Tanaman {tanaman} berhasil dihapus dari daftar stock!")
            return
    print(f"Tanaman {tanaman} tidak ditemukan dalam daftar stock!")
    
    
def edit_data():
    with open("ensiklopedia.json", "r") as file:
        data = json.load(file)
    print("Berikut daftar tanaman dan stock: ")
    table = PrettyTable()
    table.field_names = ["Nama Barang", "Harga", "Stock"]
    for item in data["kamus_tanaman"]:
        table.add_row([item["nama_tanaman"],item["harga"], item["stock"]])
    print(table)
    tanaman = input("Masukkan nama tanaman yang ingin diedit: ").strip().lower()
    for item in data["kamus_tanaman"]:
        if item["nama_tanaman"].lower() == tanaman.lower(): 
            harga_baru = input("Masukkan harga baru: ").strip()
            stok_baru = input("Masukkan stock baru: ").strip()
            data_baru = {
                "nama_tanaman": item["nama_tanaman"],
                "harga": int(harga_baru),
                "stock": int(stok_baru)
            }
            data["kamus_tanaman"].append(data_baru)
            with open("ensiklopedia.json", "w") as file:
                json.dump(data, file)
            print(f"Tanaman {tanaman} berhasil diedit!")
        else:
            print(f"Tanaman {tanaman} tidak ditemukan dalam daftar stock!")
            return

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