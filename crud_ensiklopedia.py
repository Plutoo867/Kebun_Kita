import inquirer
import re
from colored import fore, Style
from utilis import (ensiklopedia, 
                    simpan_data, 
                    pesan_error, 
                    pesan_sukses, 
                    bersihkan_terminal, 
                    enter, 
                    daftar_tanaman, 
                    table_detail_tanaman)

def id_tanaman():
    id_terakhir = 0
    for kunci in ensiklopedia.keys():
        nomor = int(kunci.replace("id", ""))
        if nomor > id_terakhir:
            id_terakhir = nomor
    id_terakhir += 1
    return f"id{id_terakhir}"

def cek_tanaman(nama):
    nama_bersih = "".join(nama.split()).lower()
    for tanaman in ensiklopedia.values():
        if nama_bersih == "".join(tanaman["nama"].split()).lower():
            return True
    return False

def search_awal(data, keyword):
    keyword = keyword.lower()
    return {
        id_: info
        for id_, info in data.items()
        if info["nama"].lower().startswith(keyword)
    }

def read_ensiklopedia():
    if not ensiklopedia:
        bersihkan_terminal
        pesan_error("Belum ada tanaman di ensiklopedia!")
        enter()
        return

    while True:
        bersihkan_terminal()
        print("0. Kembali ke menu utama")
        daftar_tanaman(ensiklopedia)
        try:
            detail = input("Masukkan nomor tanaman untuk melihat detail: ").strip()
            if detail == "0":
                break
            elif not re.fullmatch(r"[0-9]+", detail):
                pesan_error("Hanya boleh angka valid!")
                enter()
                continue
            detail = int(detail)
            if detail >= 1 and detail <= len(ensiklopedia):
                tanaman_id = list(ensiklopedia.keys()) 
                tanaman_terpilih = ensiklopedia[tanaman_id [detail - 1]]
                detail_tanaman = {
                    "Nama Tanaman": tanaman_terpilih["nama"],
                    "Nama Ilmiah": tanaman_terpilih["nama_ilmiah"],
                    "Deskripsi": tanaman_terpilih["deskripsi"],
                    "Manfaat Tanaman": tanaman_terpilih["manfaat"],
                }
                table_detail_tanaman(detail_tanaman)  
                enter()
            else:
                pesan_error("Koleksi tidak tersedia!")
                enter()
        except ValueError:
            pesan_error("Input Tidak Valid! Silahkan masukkan angka yang valid")
            enter()
        except KeyboardInterrupt:
            pesan_error("Terjadi error interupsi melalui keyboard!")
            enter()
        except EOFError:
            pesan_error("Terjadi error interupsi melalui keyboard!")
            enter()

def create_ensiklopedia():
    while True:
        bersihkan_terminal()
        print("0. Kembali ke menu utama")
        lebar = 45
        garis = "+" + "-" * (lebar + 2) + "+"
        print(garis)
        print(f"| {fore(204)}{'TAMBAH KOLEKSI'.center(lebar)}{Style.reset} |")
        print(garis)
        try:
            nama    = input("Masukkan nama tanaman          : ").strip()
            if nama == "0":
                break
            ilmiah  = input("Masukkan nama ilmiah tanaman   : ").strip()
            if ilmiah == "0":
                break
            desk    = input("Masukkan deskripsi tanaman     : ").strip()
            if desk == "0":
                break
            manfaat = input("Masukkan manfaat tanaman       : ").strip()
            if manfaat == "0":
                break

            if nama == "" or desk == "" or manfaat == "" or ilmiah == "":
                pesan_error("Kolom tidak boleh kosong!")
                enter()
                continue

            elif not re.fullmatch(r"[a-zA-Z ]+", nama):
                pesan_error("Nama tanaman hanya boleh huruf!")
                enter()
                continue

            elif not re.fullmatch(r"[a-zA-Z ]+", ilmiah):
                pesan_error("Nama ilmiah tanaman hanya boleh huruf!")
                enter()
                continue

            elif cek_tanaman(nama):
                pesan_error("Koleksi sudah tersedia, silahkan input ulang!")
                enter()
                continue

            else:
                konfirmasi = [
                    inquirer.List(
                        "konfirmasi",
                        message="Apakah Anda yakin ingin menambahkan koleksi ini?",
                        choices=["Ya", "Tidak"],
                        )
                    ]
                jawaban = inquirer.prompt(konfirmasi)

                if jawaban["konfirmasi"] == "Ya":
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
                    pesan_sukses("Koleksi berhasil ditambahkan!")
                    enter()
                    return
                elif jawaban["konfirmasi"] == "Tidak":
                    pesan_sukses("Tambah koleksi di batalkan!")
                    enter()
                    break
        except ValueError:
            pesan_error("Input Tidak Valid! Silahkan masukkan angka yang valid")
            enter()
        except KeyboardInterrupt:
            pesan_error("Terjadi error interupsi melalui keyboard!")
            enter()
        except EOFError:
            pesan_error("Terjadi error interupsi melalui keyboard!")
            enter()
        
def update_ensiklopedia():
    if not ensiklopedia:
        bersihkan_terminal
        pesan_error("Belum ada tanaman di ensiklopedia!")
        enter()
        return
    
    while True:   
        bersihkan_terminal()
        print("0. Kembali ke menu utama")
        daftar_tanaman(ensiklopedia)
        try:
            edit = input("Masukkan nomor tanaman yang ingin diedit: ").strip()

            if edit == "0":
                return
            
            elif not re.fullmatch(r"[0-9]+", edit):
                pesan_error("Hanya boleh angka valid!")
                enter()
                continue
            edit = int(edit)
            if edit >= 1 and edit <= len(ensiklopedia):
                tanaman_id = list(ensiklopedia.keys()) 
                tanaman_edit = ensiklopedia[tanaman_id[edit - 1]]

                pesan_sukses("(Tekan Enter jika tidak ingin mengubah)")

                while True:   
                    nama_baru      = input(f"Nama Tanaman [{tanaman_edit['nama']}]: ").strip()
                    ilmiah_baru    = input(f"Nama Ilmiah [{tanaman_edit['nama_ilmiah']}]: ").strip()
                    deskripsi_baru = input(f"Deskripsi [{tanaman_edit['deskripsi']}]: ").strip()
                    manfaat_baru   = input(f"Manfaat Tanaman [{tanaman_edit['manfaat']}]: ").strip()

                    if nama_baru != "" and not re.fullmatch(r"[a-zA-Z ]+", nama_baru):
                        pesan_error("Nama tanaman hanya boleh huruf!")
                        enter()
                        continue

                    elif ilmiah_baru != "" and not re.fullmatch(r"[a-zA-Z ]+", ilmiah_baru):
                        pesan_error("Nama ilmiah tanaman hanya boleh huruf!")
                        enter()
                        continue

                    elif nama_baru != "" and nama_baru.lower() != tanaman_edit["nama"].lower() and cek_tanaman(nama_baru):
                        pesan_error("Koleksi sudah tersedia, silahkan input ulang!")
                        enter()
                        continue

                    else:
                        konfirmasi = [
                            inquirer.List(
                                "konfirmasi",
                                message="Apakah Anda yakin ingin mengupdate koleksi ini?",
                                choices=["Ya", "Tidak"],
                                )
                            ]
            
                        jawaban = inquirer.prompt(konfirmasi)
            
                        if jawaban["konfirmasi"] == "Ya":
                            if nama_baru != "":
                                tanaman_edit["nama"] = nama_baru
                            if ilmiah_baru != "":
                                tanaman_edit["nama_ilmiah"] = ilmiah_baru
                            if deskripsi_baru != "":
                                tanaman_edit["deskripsi"] = deskripsi_baru
                            if manfaat_baru != "":
                                tanaman_edit["manfaat"] = manfaat_baru
                            simpan_data()
                            pesan_sukses("Koleksi berhasil diupdate!")
                            enter()
                            return
                        elif jawaban["konfirmasi"] == "Tidak":
                            pesan_sukses("Update koleksi di batalkan!")
                            enter()
                            break
            else:
                pesan_error("Koleksi tidak tersedia!")
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

def delete_ensiklopedia():
    if not ensiklopedia:
        bersihkan_terminal
        pesan_error("Belum ada tanaman di ensiklopedia!")
        enter()
        return

    while True:
        bersihkan_terminal()
        print("0. Kembali ke menu utama")
        daftar_tanaman(ensiklopedia)
        try:
            hapus = input("Masukkan nomor tanaman yang ingin dihapus: ").strip()
            if hapus == "0":
                return

            elif not re.fullmatch(r"[0-9]+", hapus):
                pesan_error("Hanya boleh angka valid!")
                enter()
                continue

            hapus = int(hapus)
            if hapus >= 1 and hapus <= len(ensiklopedia):
                tanaman_id = list(ensiklopedia.keys()) 
                tanaman_hapus = ensiklopedia[tanaman_id[hapus - 1]]
                konfirmasi = [
                    inquirer.List(
                        "konfirmasi",
                        message=f"Apakah Anda yakin ingin menghapus koleksi {tanaman_hapus['nama']}?",
                        choices=["Ya", "Tidak"],
                        )
                    ]

                jawaban = inquirer.prompt(konfirmasi)

                if jawaban["konfirmasi"] == "Ya":
                    ensiklopedia.pop(tanaman_id[hapus - 1])
                    simpan_data()
                    pesan_sukses("Koleksi berhasil dihapus!")
                    enter()
                
                elif jawaban["konfirmasi"] == "Tidak":
                    pesan_sukses("Penghapusan koleksi di batalkan!")
                    enter()
            else:
                pesan_error("Koleksi tidak tersedia!")
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

def search_ensiklopedia():
    while True:
        bersihkan_terminal()

        print("0. Kembali ke menu utama")
        lebar = 45
        garis = "+" + "-" * (lebar + 2) + "+"
        print(garis)
        print(f"| {fore(204)}{'PENCARIAN TANAMAN'.center(lebar)}{Style.reset} |")
        print(garis)

        try:
            keyword = input("Cari nama tanaman: ").strip()

            if keyword == "0":
                break

            elif keyword == "":
                pesan_error("Kolom tidak boleh kosong!")
                enter()
                continue

            elif not re.fullmatch(r"[a-zA-Z ]+", keyword):
                pesan_error("Nama tanaman hanya boleh huruf!")
                enter()
                continue

            else:
                hasil = search_awal(ensiklopedia, keyword)

                if not hasil:
                    pesan_error("Tanaman tidak ditemukan.")
                    enter()
                    continue
                pesan_sukses(f"Ditemukan {len(hasil)} tanaman dengan awalan '{keyword}'")

                for data in hasil.values():
                    detail_tanaman = {
                        "Nama Tanaman": data["nama"],
                        "Nama Ilmiah": data["nama_ilmiah"],
                        "Deskripsi": data["deskripsi"],
                        "Manfaat Tanaman": data["manfaat"],
                    }
                    table_detail_tanaman(detail_tanaman)
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