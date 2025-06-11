import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import pandas as pd
from search import sequential_search  
from sort import bubble_sort          

# Load data excel
try:
    df = pd.read_excel("buku.xlsx")
except FileNotFoundError:
    df = pd.DataFrame()

# Inisialisasi window
app = tk.Tk()
app.title("Perpustakaan App")
app.geometry("400x400")

# Variabel pilihan dan input
pilihan = tk.StringVar()
input_pencarian = tk.StringVar()

# Fungsi untuk menampilkan hasil pencarian
def tampilkan_hasil(hasil_list):
    if not hasil_list:
        pesan = "Buku tidak ditemukan!"
    else:
        hasil_list = bubble_sort(hasil_list, key="Judul Buku")  
        pesan = ""
        for buku in hasil_list:
            pesan += (
                f"Judul : {buku['Judul Buku']}\n"
                f"Kode : {buku['Kode Buku']}\n"
                f"Penulis : {buku['Penulis']}\n"
                f"Kategori : {buku['Kategori']}\n"
                f"Tahun : {buku['Tahun']}\n"
                f"Status : {buku['Status']}\n\n"
            )
    showinfo("Hasil Pencarian", pesan)

# Fungsi pencarian dari input teks menggunakan sequential search
def cari_dari_input():
    kunci = input_pencarian.get().strip()
    kolom = pilihan.get()

    if kolom and kunci:
        data_list = df[kolom].astype(str).tolist()
        index_ditemukan = sequential_search(data_list, kunci)

        if index_ditemukan != -1:
            hasil = [df.loc[index_ditemukan].to_dict()]
            tampilkan_hasil(hasil)
        else:
            rekomendasi = []
            kunci_lower = kunci.lower()
            for i, item in enumerate(data_list):
                if kunci_lower in item.lower():
                    rekomendasi.append(df.loc[i].to_dict())

            tampilkan_hasil(rekomendasi)



# Fungsi pencarian dari tombol kategori/tahun (exact match)
def cari_dari_tombol(nilai):
    kolom = pilihan.get()
    hasil_df = df[df[kolom].astype(str) == str(nilai)]
    tampilkan_hasil(hasil_df.to_dict("records"))

# Fungsi untuk membuat ulang input atau tombol berdasarkan pilihan dropdown
def ubah_pilihan(*args):
    for widget in frame_input.winfo_children():
        widget.destroy()
    
    kolom = pilihan.get()

    if kolom in ["Judul Buku", "Kode Buku", "Penulis"]:
        ttk.Label(frame_input, text=f"Masukkan {kolom}:").pack()
        ttk.Entry(frame_input, textvariable=input_pencarian).pack(fill='x', padx=5)
        ttk.Button(frame_input, text="Cari", command=cari_dari_input).pack(pady=5)
    
    elif kolom in ["Kategori", "Tahun"]:
        nilai_unik = df[kolom].dropna().unique()
        nilai_unik.sort()

        canvas = tk.Canvas(frame_input)
        scrollbar = ttk.Scrollbar(frame_input, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for val in nilai_unik:
            ttk.Button(scrollable_frame, text=str(val), command=lambda v=val: cari_dari_tombol(v)).pack(fill='x', padx=5, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

# Frame dropdown pilihan
# Bungkus semua ke dalam 1 container di tengah
container = ttk.Frame(app)
container.place(relx=0.5, rely=0.5, anchor="center")

# Frame dropdown pilihan
frame_dropdown = ttk.Frame(container)
frame_dropdown.pack(pady=10, fill='x')
ttk.Label(frame_dropdown, text="Pilih Kolom Pencarian:").pack()
dropdown = ttk.Combobox(frame_dropdown, textvariable=pilihan, state="readonly")
dropdown['values'] = ["Judul Buku", "Kode Buku", "Penulis", "Kategori", "Tahun"]
dropdown.pack(fill='x', padx=5)
pilihan.trace('w', ubah_pilihan)

# Frame untuk input atau tombol dinamis
frame_input = ttk.Frame(container)
frame_input.pack(fill='both', expand=True, padx=10, pady=10)

# Jalankan GUI
app.mainloop()
