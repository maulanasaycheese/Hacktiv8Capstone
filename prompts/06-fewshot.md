# Layer 6 - Few-shot Example

Input:
"REQ: Pengguna dapat mengisi kolom usia, nilai valid 17-60."

Contoh baris output yang benar:

| TC-001 | REQ-1 | Usia di batas bawah | Boundary | High | Form terbuka | 1. Isi usia 17<br>2. Klik Simpan | 17 | Data tersimpan |
| TC-002 | REQ-1 | Usia tepat di bawah batas | Boundary | High | Form terbuka | 1. Isi usia 16<br>2. Klik Simpan | 16 | Ditolak, muncul pesan error rentang usia |
