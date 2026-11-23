import random, textwrap, json, inquirer
from crud_ensiklopedia import load_data
from prettytable import PrettyTable

ensiklopedia = load_data()

def random_funfact():
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

def create_funfact():
    id_kosong = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["funfact"] == "0":
            id_kosong.append(id_data)

    if not id_kosong:
        print("Tidak ada tanaman yang membutuhkan funfact!")
        return

    while True:
        print("0. Kembali ke Menu Utama")
        print("Daftar Tanaman Tanpa Funfact")

        for nomor, id_data in enumerate(id_kosong, start=1):
            print(f"{nomor}. {ensiklopedia[id_data]['nama']}")

        try:
            pilihan = int(input("Pilih nomor tanaman: "))

            if pilihan == 0:
                print("Kembali ke menu utama")
                return
            elif pilihan < 1 or pilihan > len(id_kosong):
                print("Nomor tanaman tidak tersedia!")
                continue

            id_pilihan = id_kosong[pilihan - 1]

            funfact = input("Masukkan funfact: ").strip()

            if not funfact:
                print("Error: Funfact tidak boleh kosong!")
                continue
            elif funfact == "0":
                print("Error: Funfact tidak boleh '0'!")
                continue

            konfirmasi = [
                inquirer.List(
                    "konfirmasi",
                    message="Apakah Anda yakin ingin menambahkan funfact ini?",
                    choices=["Ya", "Tidak"],
                )
            ]

            jawaban = inquirer.prompt(konfirmasi)

            if jawaban["konfirmasi"] == "Ya":
                ensiklopedia[id_pilihan]["funfact"] = funfact

                with open("ensiklopedia.json", "w", encoding="utf-8") as file:
                    json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)

                print("Funfact berhasil ditambahkan!")
                return

            elif jawaban["konfirmasi"] == "Tidak":
                print("Funfact tidak ditambahkan.")

        except ValueError:
            print("Error: Input harus berupa angka!")


def delete_funfact():
    id_dengan_funfact = []

    for id_data in ensiklopedia:
            if ensiklopedia[id_data]["funfact"] != "0":
                id_dengan_funfact.append(id_data)
    
    if not id_dengan_funfact:
        print("Tidak ada tanaman yang memiliki funfact!")
        return

    while True:
        print("0. Kembali ke Menu Utama")
        print("Daftar Tanaman Dengan Funfact")
    
        for nomor, id_data in enumerate(id_dengan_funfact, start=1):
            print(f"{nomor}. {ensiklopedia[id_data]['nama']}")

        try:
            pilihan = int(input("\nPilih nomor tanaman: "))

            if pilihan == 0:
                print("Kembali ke menu utama")
                return
            elif pilihan < 1 or pilihan > len(id_dengan_funfact):
                print("Nomor tanaman tidak tersedia!")
                continue

            id_pilihan = id_dengan_funfact[int(pilihan) - 1]

            konfirmasi = [
                inquirer.List(
                    "konfirmasi",
                    message="Apakah Anda yakin ingin menghapus funfact ini?",
                    choices=["Ya", "Tidak"],
                    )
                ]

            jawaban = inquirer.prompt(konfirmasi)

            if jawaban["konfirmasi"] == "Ya":
                ensiklopedia[id_pilihan]["funfact"] = "0"

                with open("ensiklopedia.json", "w", encoding="utf-8") as file:
                    json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)

                print("Funfact berhasil dihapus!")
                return
            elif jawaban["konfirmasi"] == "Tidak":
                print("Funfact tidak dihapus")

        except ValueError:
            print("Input harus berupa angka!")


def update_funfact():
    id_dengan_funfact = []

    for id_data in ensiklopedia:
        if ensiklopedia[id_data]["funfact"] != "0":
            id_dengan_funfact.append(id_data)

    if not id_dengan_funfact:
        print("Tidak ada tanaman yang memiliki funfact!")
        return

    while True:
        print("0. Kembali ke Menu Utama")
        print("Daftar Tanaman Dengan Funfact")

        for nomor, id_data in enumerate(id_dengan_funfact, start=1):
            print(f"{nomor}. {ensiklopedia[id_data]['nama']}")

        try:
            pilihan = int(input("\nPilih nomor tanaman: "))

            if pilihan == 0:
                print("Kembali ke menu utama")
                return
            elif pilihan < 1 or pilihan > len(id_dengan_funfact):
                print("Nomor tanaman tidak tersedia!")
                continue

            id_pilihan = id_dengan_funfact[pilihan - 1]

            funfact = input("Masukkan funfact baru: ").strip()

            if not funfact:
                print("Error: Funfact tidak boleh kosong!")
                continue
            elif funfact == "0":
                print("Error: Funfact tidak boleh '0'!")
                continue

            konfirmasi = [
                inquirer.List(
                    "konfirmasi",
                    message="Apakah Anda yakin ingin memperbarui funfact ini?",
                    choices=["Ya", "Tidak"],
                )
            ]

            jawaban = inquirer.prompt(konfirmasi)

            if jawaban["konfirmasi"] == "Ya":
                ensiklopedia[id_pilihan]["funfact"] = funfact

                with open("ensiklopedia.json", "w", encoding="utf-8") as file:
                    json.dump(ensiklopedia, file, indent=4, ensure_ascii=False)

                print("Funfact berhasil diperbarui!")
                return

            elif jawaban["konfirmasi"] == "Tidak":
                print("Funfact tidak diperbarui.")

        except ValueError:
            print("Input harus berupa angka!")

random_funfact()