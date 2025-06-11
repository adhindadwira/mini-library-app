import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from search import sequential_search
from sort import bubble_sort

# Path file
file_path = "buku.xlsx"

# Load data dari Excel
if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=["Kode Buku", "Judul Buku", "Penulis", "Kategori", "Tahun", "Status"])

# Fungsi hapus data
def hapus_data():
    global df

    kode = kode_var.get().strip()

    if not kode:
        messagebox.showwarning("Peringatan", "Masukkan kode buku yang ingin dihapus.")
        return

    # Gunakan sequential_search untuk mencari kode
    kode_list = df["Kode Buku"].astype(str).tolist()
    index_ditemukan = sequential_search(kode_list, kode)

    if index_ditemukan == -1:
        messagebox.showerror("Error", f"Kode buku '{kode}' tidak ditemukan.")
        return

    konfirmasi = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus buku dengan kode '{kode}'?")
    if not konfirmasi:
        return

    # Hapus data
    df = df.drop(index=index_ditemukan).reset_index(drop=True)

    # Urutkan ulang data setelah penghapusan
    data_sorted = bubble_sort(df.to_dict("records"), key="Kode Buku")
    df = pd.DataFrame(data_sorted)

    try:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Sukses", f"Buku dengan kode '{kode}' berhasil dihapus.")
        kode_var.set("")  
    except PermissionError:
        messagebox.showerror("Gagal", f"File '{file_path}' sedang dibuka. Tutup file terlebih dahulu.")

# GUI setup
root = tk.Tk()
root.title("Hapus Data Buku")
root.geometry("350x180")
root.configure(bg='white')

frame = ttk.Frame(root, padding=10)
frame.pack(fill="x", expand=True)

# Variabel input
kode_var = tk.StringVar()

ttk.Label(frame, text="Masukkan Kode Buku yang akan dihapus:").pack(anchor="w", pady=5)
ttk.Entry(frame, textvariable=kode_var).pack(fill="x")

ttk.Button(frame, text="Hapus Data", command=hapus_data).pack(pady=20)

root.mainloop()
