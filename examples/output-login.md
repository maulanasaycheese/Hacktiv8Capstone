## 1. Ringkasan Requirement
- REQ-1 Login dengan email + password terdaftar
- REQ-2 Password minimal 8 karakter
- REQ-3 Akun dikunci 15 menit setelah 5 kali salah berturut-turut
- REQ-4 "Ingat saya" mempertahankan sesi 7 hari

## 2. Asumsi & Klarifikasi
- [ASUMSI] Format email divalidasi standar (ada "@" dan domain).
- [ASUMSI] Penghitung salah di-reset setelah login berhasil.
- Pertanyaan: apakah pesan error membedakan "email tidak terdaftar" dan "password salah"?

## 3. Tabel Test Case
| ID | Req | Judul | Kategori | Prioritas | Precondition | Langkah | Data Uji | Expected Result |
|---|---|---|---|---|---|---|---|---|
| TC-001 | REQ-1 | Login berhasil kredensial valid | Positive | High | Akun terdaftar | 1. Buka halaman login<br>2. Isi email & password<br>3. Klik Masuk | user@example.com / Passw0rd123 | Masuk ke dashboard |
| TC-002 | REQ-1 | Password salah | Negative | High | Akun terdaftar | 1. Isi email valid<br>2. Isi password salah<br>3. Klik Masuk | user@example.com / SalahPass1 | Login ditolak, muncul pesan error |
| TC-003 | REQ-1 | Email belum terdaftar | Negative | High | - | 1. Isi email tak terdaftar<br>2. Klik Masuk | baru@example.com / Passw0rd123 | Login ditolak, muncul pesan error |
| TC-004 | REQ-1 | Format email tidak valid | Negative | Medium | - | 1. Isi email tanpa "@"<br>2. Klik Masuk | userexample.com | Validasi format email muncul, request tidak dikirim |
| TC-005 | REQ-1 | Kolom wajib kosong | Negative | Medium | - | 1. Biarkan email & password kosong<br>2. Klik Masuk | (kosong) | Pesan "wajib diisi" pada kedua kolom |
| TC-006 | REQ-2 | Password tepat 8 karakter | Boundary | High | Akun dengan password 8 karakter | 1. Login dengan password 8 karakter | Abcd1234 | Login berhasil |
| TC-007 | REQ-2 | Password 7 karakter saat set password | Boundary | High | Halaman ubah/daftar password | 1. Isi password 7 karakter<br>2. Simpan | Abcd123 | Ditolak, pesan minimal 8 karakter |
| TC-008 | REQ-3 | Akun terkunci pada kegagalan ke-5 | Boundary | High | Akun aktif, counter 0 | 1. Login salah 5 kali berturut-turut<br>2. Login dengan password benar | 5x salah, lalu benar | Pada percobaan ke-6 login ditolak, pesan akun terkunci |
| TC-009 | REQ-3 | Kegagalan ke-4 belum mengunci | Boundary | High | Akun aktif, counter 0 | 1. Login salah 4 kali<br>2. Login dengan password benar | 4x salah, lalu benar | Login berhasil [ASUMSI: counter di-reset] |
| TC-010 | REQ-3 | Akun terbuka setelah 15 menit | State Transition | Medium | Akun terkunci | 1. Tunggu 15 menit<br>2. Login benar | Kredensial valid | Login berhasil |
| TC-011 | REQ-4 | Sesi bertahan dengan "Ingat saya" | Positive | Medium | Akun terdaftar | 1. Login centang "Ingat saya"<br>2. Tutup & buka browser dalam 7 hari | Kredensial valid | Pengguna tetap login |
| TC-012 | REQ-4 | Sesi berakhir setelah 7 hari | Edge Case | Medium | Login dengan "Ingat saya" | 1. Buka aplikasi setelah lebih dari 7 hari | - | Diminta login ulang |
| TC-013 | REQ-1 | Input mengandung karakter script | Security | Medium | - | 1. Isi email dengan teks mengandung tag script<br>2. Klik Masuk | teks berisi tag script | Input ditolak atau di-escape, tidak dieksekusi |

## 4. Coverage Summary
- Per kategori: Positive 2, Negative 4, Boundary 4, State Transition 1, Edge Case 1, Security 1
- Per requirement: REQ-1 = 6, REQ-2 = 2, REQ-3 = 3, REQ-4 = 2 (13 test case, semua requirement tercakup)
