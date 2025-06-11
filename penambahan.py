import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from search import sequential_search
from sort import bubble_sort

# Fungsi untuk simpan data ke Excel
def simpan_data():
    kode = kode_var.get()
    judul = judul_var.get()
    penulis = penulis_var.get()
    kategori = kategori_var.get()
    tahun = tahun_var.get()
    status = status_var.get()

    if not all([kode, judul, penulis, kategori, tahun, status]):
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
        return

    try:
        tahun = int(tahun)
    except ValueError:
        messagebox.showwarning("Peringatan", "Tahun harus berupa angka!")
        return

    data_baru = {
        "Kode Buku": kode,
        "Judul Buku": judul,
        "Penulis": penulis,
        "Kategori": kategori,
        "Tahun": tahun,
        "Status": status
    }

    file_path = "buku.xlsx"
    try:
        # Baca atau buat file
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
        else:
            df = pd.DataFrame(columns=["Kode Buku", "Judul Buku", "Penulis", "Kategori", "Tahun", "Status"])

        # Cek duplikasi kode
        kode_list = df["Kode Buku"].astype(str).tolist()
        if sequential_search(kode_list, kode) != -1:
            messagebox.showwarning("Peringatan", f"Kode buku '{kode}' sudah ada!")
            return

        df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)

        # Urutkan data berdasarkan kode buku sebelum simpan
        df_sorted = bubble_sort(df.to_dict("records"), key="Kode Buku")
        df = pd.DataFrame(df_sorted)

        # Simpan ke Excel
        with open(file_path, 'a'):
            pass
        df.to_excel(file_path, index=False)

        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")

        # Reset input
        kode_var.set("")
        judul_var.set("")
        penulis_var.set("")
        kategori_var.set("")
        tahun_var.set("")
        status_var.set(status_options[0])

    except PermissionError:
        messagebox.showerror("Gagal Menyimpan", f"Tidak bisa menyimpan ke '{file_path}'. Pastikan file tidak sedang dibuka.")

# Data dropdown untuk status
status_options = ["Tersedia", "Dipinjam", "Tidak Tersedia"]

# GUI setup
root = tk.Tk()
root.title("Input Data Buku")
root.geometry("400x420")
root.configure(bg='white')

# Variabel input
kode_var = tk.StringVar()
judul_var = tk.StringVar()
penulis_var = tk.StringVar()
kategori_var = tk.StringVar()
tahun_var = tk.StringVar()
status_var = tk.StringVar(value=status_options[0])

# Frame input
frame = ttk.Frame(root, padding=10)
frame.pack(fill="x", expand=True)

def buat_input(label, var, dropdown=False, options=None):
    ttk.Label(frame, text=label).pack(anchor="w", pady=2)
    if dropdown:
        ttk.Combobox(frame, textvariable=var, values=options, state="readonly").pack(fill="x")
    else:
        ttk.Entry(frame, textvariable=var).pack(fill="x")

# Input field
buat_input("Kode Buku", kode_var)
buat_input("Judul Buku", judul_var)
buat_input("Penulis", penulis_var)
buat_input("Kategori", kategori_var)
buat_input("Tahun", tahun_var)
buat_input("Status", status_var, dropdown=True, options=status_options)

# Tombol Simpan
ttk.Button(frame, text="Simpan Data", command=simpan_data).pack(pady=10)

# Jalankan
root.mainloop()
