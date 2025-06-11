import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess

# Fungsi untuk membuka fitur
def jalankan_fitur(nama_file):
    if os.path.exists(nama_file):
        subprocess.Popen(["python", nama_file])
    else:
        messagebox.showerror("Error", f"File '{nama_file}' tidak ditemukan.")

# Fungsi setelah login
def tampilkan_menu(fitur_lengkap):
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="Pilih Fitur:", font=("Arial", 14)).pack(pady=10)

    ttk.Button(root, text="Pencarian Buku", width=30, command=lambda: jalankan_fitur("pencarian.py")).pack(pady=5)

    if fitur_lengkap:
        ttk.Button(root, text="Penambahan Buku", width=30, command=lambda: jalankan_fitur("penambahan.py")).pack(pady=5)
        ttk.Button(root, text="Pengubahan Buku", width=30, command=lambda: jalankan_fitur("pengubahan.py")).pack(pady=5)
        ttk.Button(root, text="Penghapusan Buku", width=30, command=lambda: jalankan_fitur("penghapusan.py")).pack(pady=5)

# Fungsi login
def proses_login():
    email = email_var.get().strip()
    password = password_var.get().strip()

    if not email or "@" not in email:
        messagebox.showwarning("Peringatan", "Masukkan email yang valid.")
        return

    if "@admin" in email.lower():
        if password == "admin123":
            tampilkan_menu(fitur_lengkap=True)
        else:
            messagebox.showerror("Login Gagal", "Password admin salah.")
    else:
        # user biasa, tidak perlu password khusus
        tampilkan_menu(fitur_lengkap=False)

# GUI Login Awal
root = tk.Tk()
root.title("Login Perpustakaan")
root.geometry("350x240")
root.configure(bg="white")

frame_login = ttk.Frame(root, padding=20)
frame_login.pack(expand=True)

email_var = tk.StringVar()
password_var = tk.StringVar()

ttk.Label(frame_login, text="Masukkan Email:", font=("Arial", 11)).pack(anchor="w", pady=5)
ttk.Entry(frame_login, textvariable=email_var).pack(fill="x")

ttk.Label(frame_login, text="Masukkan Password:", font=("Arial", 11)).pack(anchor="w", pady=5)
ttk.Entry(frame_login, textvariable=password_var, show="*").pack(fill="x")

ttk.Button(frame_login, text="Login", command=proses_login).pack(pady=15)

root.mainloop()
