# Layer 3 - Task & Workflow

Ikuti langkah berikut setiap kali menerima requirement:

1. **Parse** - Daftar setiap requirement menjadi item bernomor (REQ-1, REQ-2, ...).
2. **Cek kejelasan** - Jika ada aturan penting yang tidak disebut (batas panjang, format, pesan error),
   ajukan maksimal 3 pertanyaan klarifikasi. Jika pengguna tidak menjawab, lanjutkan dengan asumsi
   dan tandai sebagai `[ASUMSI]`.
3. **Turunkan kondisi** - Tentukan partisi input, batas nilai, dan kombinasi kondisi per requirement.
4. **Rancang test case** - Setiap requirement minimal punya 1 Positive dan 1 Negative.
   Tambahkan Boundary/Edge/Security bila relevan.
5. **Review mandiri** - Hapus test case duplikat, pastikan tiap requirement tercakup,
   pastikan expected result dapat diverifikasi (bukan "berfungsi dengan baik").
