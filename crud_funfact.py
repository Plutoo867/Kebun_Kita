import random, textwrap, json
from crud_ensiklopedia import load_data
from prettytable import PrettyTable

ensiklopedia = load_data()

def random_funfact(ensiklopedia):
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

        header_funfact = "Funfact".center(50)

        table = PrettyTable()
        table.field_names = ["Nama Tanaman", header_funfact]
        table.align[header_funfact] = "l"

        funfact_wrapped = textwrap.fill(random_data["Funfact"], width=50)
        table.add_row([random_data["Nama_tanaman"], funfact_wrapped])

        print(table)

    else:
        print("Tidak ada funfact yang tersedia")

def tambah_funfact(ensiklopedia):
    id_kosong = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["funfact"] == "0":
            id_kosong.append(id_data)

    if not id_kosong:
        print("Tidak ada tanaman yang membutuhkan funfact!")
        return

    print("\nDaftar Tanaman Tanpa Funfact")

    for nomor, id_data in enumerate(id_kosong, start=1):
        print(f"{nomor}. {ensiklopedia[id_data]['nama']}")

    while True:
        try:
            pilihan = int(input("\nPilih nomor tanaman: "))

            if 1 <= pilihan <= len(id_kosong):
                break
            else:
                print("Nomor tanaman tidak tersedia!")

        except ValueError:
            print("Input harus berupa angka!")

    id_pilihan = id_kosong[int(pilihan) - 1]

    funfact = input("Masukkan funfact: ").strip()

    while not funfact:
        print("Funfact tidak boleh kosong!")
        funfact = input("Masukkan funfact: ").strip()

    ensiklopedia[id_pilihan]["funfact"] = funfact

    with open("ensiklopedia.json", "w", encoding="utf-8") as file:
        json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)

    print("Funfact berhasil ditambahkan!")

def hapus_funfact(ensiklopedia):
    id_dengan_funfact = []

    for id_data in ensiklopedia:
            if ensiklopedia[id_data]["funfact"] != "0":
                id_dengan_funfact.append(id_data)
    
    if not id_dengan_funfact:
        print("Tidak ada tanaman yang memiliki funfact!")
        return
    
    print("\nDaftar Tanaman ")
    
    for nomor, id_data in enumerate(id_dengan_funfact, start=1):
        print(f"{nomor}. {ensiklopedia[id_data]['nama']}")

    while True:
        try:
            pilihan = int(input("\nPilih nomor tanaman: "))
    
            if 1 <= pilihan <= len(id_dengan_funfact):
                break
            else:
                print("Nomor tanaman tidak tersedia!")
    
        except ValueError:
            print("Input harus berupa angka!")

    id_pilihan = id_dengan_funfact[int(pilihan) - 1]

    ensiklopedia[id_pilihan]["funfact"] = "0"
    
    with open("ensiklopedia.json", "w", encoding="utf-8") as file:
        json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)
    
    print("Funfact berhasil dihapus!")

def update_funfact(ensiklopedia):
    id_dengan_funfact = []

    for id_data in ensiklopedia:
            if ensiklopedia[id_data]["funfact"] != "0":
                id_dengan_funfact.append(id_data)
    
    if not id_dengan_funfact:
        print("Tidak ada tanaman yang memiliki funfact!")
        return
    
    print("\nDaftar Tanaman")
    
    for nomor, id_data in enumerate(id_dengan_funfact, start=1):
        print(f"{nomor}. {ensiklopedia[id_data]['nama']}")

    while True:
        try:
            pilihan = int(input("\nPilih nomor tanaman: "))
    
            if 1 <= pilihan <= len(id_dengan_funfact):
                break
            else:
                print("Nomor tanaman tidak tersedia!")
    
        except ValueError:
            print("Input harus berupa angka!")

    id_pilihan = id_dengan_funfact[int(pilihan) - 1]


    while True:
        try:
            funfact = input("Masukkan funfact baru: ").strip()
            if not funfact:
                raise ValueError("Funfact tidak boleh kosong!")
            elif funfact == "0":
                raise ValueError("Funfact tidak boleh '0'!")
            else:
                break
        except ValueError as pesan_error:
            print(f"Error: {pesan_error}")


    ensiklopedia[id_pilihan]["funfact"] = funfact

    with open("ensiklopedia.json", "w", encoding="utf-8") as file:
        json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)

    print("Funfact berhasil diperbarui!")

update_funfact(ensiklopedia)