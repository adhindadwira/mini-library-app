import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from search import sequential_search
from sort import bubble_sort

file_path = "buku.xlsx"

# Fungsi untuk muat data dan isi dropdown
def muat_data():
    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"File {file_path} tidak ditemukan.")
        return

    global df
    df = pd.read_excel(file_path)

    data_dicts = df.to_dict("records")
    data_sorted = bubble_sort(data_dicts, key="Kode Buku")
    kode_dropdown['values'] = [buku["Kode Buku"] for buku in data_sorted]

# Saat kode dipilih, isi form
def isi_form(event=None):
    kode = kode_var.get()
    data_list = df["Kode Buku"].astype(str).tolist()

    idx = sequential_search(data_list, kode)

    if idx != -1:
        row = df.loc[idx]
        judul_var.set(row["Judul Buku"])
        penulis_var.set(row["Penulis"])
        kategori_var.set(row["Kategori"])
        tahun_var.set(str(row["Tahun"]))
        status_var.set(row["Status"])
    else:
        messagebox.showerror("Error", "Kode buku tidak ditemukan.")

# Simpan perubahan
def perbarui_data():
    kode = kode_var.get()
    data_list = df["Kode Buku"].astype(str).tolist()
    idx = sequential_search(data_list, kode)

    if idx == -1:
        messagebox.showerror("Error", "Kode buku tidak ditemukan.")
        return

    try:
        tahun = int(tahun_var.get())
    except ValueError:
        messagebox.showwarning("Peringatan", "Tahun harus berupa angka!")
        return

    df.at[idx, "Judul Buku"] = judul_var.get()
    df.at[idx, "Penulis"] = penulis_var.get()
    df.at[idx, "Kategori"] = kategori_var.get()
    df.at[idx, "Tahun"] = tahun
    df.at[idx, "Status"] = status_var.get()

    try:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        muat_data()  
    except PermissionError:
        messagebox.showerror("Gagal", f"File '{file_path}' sedang dibuka. Tutup file terlebih dahulu.")

# Data status
status_options = ["Tersedia", "Dipinjam", "Tidak Tersedia"]

# GUI setup
root = tk.Tk()
root.title("Edit Data Buku")
root.geometry("400x460")
root.configure(bg="white")

# Variabel
kode_var = tk.StringVar()
judul_var = tk.StringVar()
penulis_var = tk.StringVar()
kategori_var = tk.StringVar()
tahun_var = tk.StringVar()
status_var = tk.StringVar(value=status_options[0])

frame = ttk.Frame(root, padding=10)
frame.pack(fill="x", expand=True)

ttk.Label(frame, text="Pilih atau Cari Kode Buku").pack(anchor="w")
kode_dropdown = ttk.Combobox(frame, textvariable=kode_var)
kode_dropdown.pack(fill="x", pady=5)
kode_dropdown.bind("<<ComboboxSelected>>", isi_form)

def buat_input(label, var, dropdown=False, options=None):
    ttk.Label(frame, text=label).pack(anchor="w", pady=2)
    if dropdown:
        ttk.Combobox(frame, textvariable=var, values=options, state="readonly").pack(fill="x")
    else:
        ttk.Entry(frame, textvariable=var).pack(fill="x")

# Input form
buat_input("Judul Buku", judul_var)
buat_input("Penulis", penulis_var)
buat_input("Kategori", kategori_var)
buat_input("Tahun", tahun_var)
buat_input("Status", status_var, dropdown=True, options=status_options)

ttk.Button(frame, text="Perbarui Data", command=perbarui_data).pack(pady=10)

# Load data awal
muat_data()

# Jalankan GUI
root.mainloop()
