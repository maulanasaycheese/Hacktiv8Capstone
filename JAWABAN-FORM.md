# Jawaban Form Capstone (siap salin)

## Judul Topic Use Case mu
Pilih: **Test Case Generator**
Tools yang digunakan: **IBM Bob**

## Judul Capstone Project
QA Buddy: AI Agent Test Case Generator untuk Mempercepat dan Menstandarkan Pengujian Perangkat Lunak

## Ringkasan Project
QA Buddy adalah AI Agent yang dikembangkan di IBM Bob untuk mengubah requirement atau user story menjadi test case yang terstruktur, konsisten, dan dapat ditelusuri ke requirement asalnya. Agent menganalisis requirement, mengajukan pertanyaan klarifikasi bila ada aturan yang tidak jelas, lalu menghasilkan test case Positive, Negative, Boundary, Edge Case, dan Security dalam format tabel beserta ringkasan cakupan (coverage summary).

Proyek ini menyelesaikan masalah penulisan test case manual yang lambat, tidak seragam antar penguji, dan sering melewatkan skenario batas atau negatif. Target penggunanya adalah QA engineer, developer, dan product owner pada tim pengembangan perangkat lunak. Fungsi utama agent adalah menurunkan kondisi uji dengan teknik desain test (equivalence partitioning, boundary value analysis, decision table, state transition), menandai asumsi secara eksplisit agar tidak mengarang aturan bisnis, dan menyajikan hasil yang siap dipakai di tim.

## Problem Statement
Dalam pengembangan perangkat lunak, pengujian menjadi penentu kualitas sebelum rilis, tetapi penyusunan test case masih banyak dilakukan manual dari dokumen requirement. Prosesnya memakan waktu, bergantung pada pengalaman masing-masing penguji, dan hasilnya tidak seragam: ada tim yang hanya menguji alur sukses, ada yang tidak mencatat data uji dan expected result secara jelas. Requirement yang ambigu juga sering langsung diuji berdasarkan tebakan, sehingga kesalahan baru ketahuan setelah fitur dipakai pengguna.

Kondisi ini penting diselesaikan karena cacat yang lolos ke produksi jauh lebih mahal diperbaiki daripada yang ditemukan saat pengujian. Bila tidak ditangani, tim menghadapi siklus rilis yang lebih lambat, bug pada kasus batas dan kasus negatif yang tidak teruji, serta test case yang sulit ditelusuri ke requirement sehingga sulit diaudit dan dipelihara. Terutama pada tim kecil atau penguji pemula, kebutuhan akan test case yang lengkap dan konsisten sering tidak terpenuhi karena keterbatasan waktu dan pengalaman.

## Target Users
1. QA engineer / penguji perangkat lunak (terutama junior) yang perlu menyusun test case dengan cepat dan konsisten dari requirement.
2. Developer yang ingin menulis atau memeriksa test untuk fiturnya sendiri tetapi belum terbiasa dengan teknik desain test.
3. Product owner / business analyst yang ingin memastikan requirement dapat diuji dan semua aturan tercakup.
Karakteristik umum: bekerja dengan tenggat sprint yang ketat, memiliki requirement dalam bentuk teks atau user story, dan membutuhkan output terstruktur yang dapat langsung dimasukkan ke dokumen atau alat manajemen test.

## Arsitektur Prompt (Prompt Layering)
Prompt disusun dalam enam layer terpisah agar mudah dirawat dan diuji per bagian:
1. Role & Identity - menetapkan agent sebagai Senior QA Engineer bernama QA Buddy, termasuk gaya bahasa. Tujuan: membuat perilaku dan nada jawaban konsisten.
2. Context & Knowledge - membekali teknik desain test (equivalence partitioning, boundary value analysis, decision table, state transition, error guessing) serta kategori dan prioritas test. Tujuan: membuat cakupan berbasis teknik, bukan sekadar tebakan.
3. Task & Workflow - langkah kerja berurutan: parse requirement, cek kejelasan (maksimal 3 pertanyaan klarifikasi, sisanya ditandai [ASUMSI]), turunkan kondisi, rancang test case, review mandiri. Tujuan: proses yang dapat diulang dan mencegah test case duplikat atau tidak terverifikasi.
4. Output Format - tabel dengan kolom tetap (ID, Req, Judul, Kategori, Prioritas, Precondition, Langkah, Data Uji, Expected Result) plus coverage summary dan opsi Gherkin. Tujuan: keluaran seragam dan siap pakai.
5. Guardrails & Constraints - tidak mengarang aturan bisnis, memakai data dummy, batas 25 test case per respons, tidak membuat payload serangan fungsional, menolak permintaan di luar tugas. Tujuan: keamanan, kejujuran, dan fokus.
6. Few-shot Example - contoh baris test case boundary yang benar. Tujuan: mengunci gaya dan tingkat detail output.

## Iterasi Prompt
Versi 1 hanya berisi satu kalimat, misalnya "buatkan test case untuk fitur login". Hasilnya cenderung generik, dominan alur sukses, dan formatnya berubah-ubah antar permintaan.

Versi 2 menambahkan layer Role dan Output Format (tabel dengan kolom tetap). Format menjadi konsisten dan mudah dibaca, tetapi agent masih menambahkan aturan yang tidak ada di requirement (misalnya batas karakter atau pesan error tertentu) sehingga test case berisiko salah.

Versi 3 menambahkan layer Guardrails dan Workflow: aturan penandaan [ASUMSI], pertanyaan klarifikasi maksimal tiga, serta batas jumlah test case. Perubahan ini dilakukan untuk mengurangi pengarangan aturan bisnis; hasilnya lebih jujur dan dapat ditelusuri, namun cakupan kasus batas masih belum merata.

Versi 4 menambahkan layer Context (teknik desain test), langkah review mandiri, coverage summary, dan satu contoh few-shot. Tujuannya meningkatkan kelengkapan kasus Boundary, Edge, dan Security serta membuktikan bahwa setiap requirement tercakup. Dampaknya jawaban lebih lengkap, tidak duplikat, dan konsisten dengan format.

## Potensi Pengembangan Lanjutan (Opsional)
- Integrasi dengan alat manajemen test seperti Jira, TestRail, atau Xray untuk mengunggah test case otomatis.
- Menghasilkan skrip pengujian otomatis (Selenium, Playwright, atau pytest) dari test case yang dibuat.
- Mendukung masukan dokumen requirement (PDF/Word) dan spesifikasi API (OpenAPI) secara langsung.
- Menambah mode regresi yang menyarankan test case terdampak ketika requirement berubah.
- Membuat mekanisme penilaian kualitas test case (skor cakupan dan duplikasi) serta memori konteks proyek antar sesi.

## Screenshot Prompt pada IBM Bob
(WAJIB screenshot asli dari IBM Bob milikmu - lihat catatan di chat.)

## Screenshot Playground / Hasil Pengujian
(WAJIB screenshot asli dari hasil run di IBM Bob - lihat catatan di chat. Gunakan input examples/input-login.md.)

## Link Project
(Isi dengan link GitHub / Google Drive setelah folder qa-buddy diunggah, dan atur akses "Anyone with the link can view".)
