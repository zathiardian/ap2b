

# 🧾 Soal Pemrograman: Pengecek Ketersediaan Buku Concurrent

## 🧠 Latar Belakang

Seorang mahasiswa kutu buku memiliki daftar panjang buku yang ingin ia pinjam dari perpustakaan. Mengecek ketersediaan setiap buku satu per satu di situs web perpustakaan sangat memakan waktu. Dia ingin membuat sebuah skrip untuk **mengecek status ketersediaan semua buku dalam daftarnya secara otomatis** dari API perpustakaan. Skrip ini harus:

- Melakukan pengecekan untuk banyak nomor ISBN sekaligus secara *concurrent* (paralel) agar prosesnya cepat.
- Mencatat semua hasil pengecekan (berhasil, dipinjam, atau tidak ditemukan) ke dalam file log secara **aman dari race condition**.
- Dapat menangani jika API memberikan error, misalnya jika ISBN tidak ada dalam katalog atau server sedang sibuk.

Anda diminta untuk melengkapi kode Python yang sudah disiapkan untuk membangun skrip impian mahasiswa tersebut.

---

## 🎯 Tujuan

1. Mengaplikasikan **threading dan lock** untuk mempercepat proses I/O-bound seperti permintaan API berganda.
2. Menerapkan **logging yang thread-safe** untuk memastikan integritas data log dalam eksekusi paralel.
3. Membangun client API yang andal dan dapat menangani berbagai skenario respons dan error dengan baik.
