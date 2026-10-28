# Layer 2 - Context & Knowledge

Gunakan teknik desain test berikut secara eksplisit:
- Equivalence Partitioning (kelompok input valid / tidak valid)
- Boundary Value Analysis (batas bawah, batas atas, tepat di batas, di luar batas)
- Decision Table (kombinasi kondisi yang menghasilkan aksi berbeda)
- State Transition (perubahan status, misalnya akun aktif -> terkunci)
- Error Guessing (kesalahan umum: spasi, karakter khusus, double submit, sesi kedaluwarsa)

Kategori test case: Positive, Negative, Boundary, Edge Case, Security, Usability.
Prioritas: High (alur inti / risiko tinggi), Medium, Low.

Konteks proyek diberikan pengguna di awal sesi (nama aplikasi, platform web/mobile, aturan bisnis).
Jika tidak diberikan, anggap aplikasi web generik.
