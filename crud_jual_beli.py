import json, inquirer, os 
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
        
    
    
def menu_admin():
    pertanyaan = [
        inquirer.List(
            "menu",
            message="Pilih menu jual beli",
            choices=["Lihat koleksi", "Tambah koleksi", "Edit Koleksi", "Hapus koleksi", "keluar"]
        )
    ]
    jawaban = inquirer.prompt(pertanyaan)
    return jawaban["menu"]

while True:
    os.system("cls")
    pilihan = menu_admin()
    if pilihan == "Lihat koleksi":
        lihat_stok()
        input("Tekan Enter untuk kembali ke menu...")
    elif pilihan == "Tambah koleksi":
        tambah_data()
        input("Tekan Enter untuk kembali ke menu...")
    elif pilihan == "Edit Koleksi":
        edit_data()
        input("Tekan Enter untuk kembali ke menu...")
    elif pilihan == "Hapus koleksi":
        hapus_data()
        input("Tekan Enter untuk kembali ke menu...")