# Layer 4 - Output Format

Keluarkan jawaban dengan urutan:

1. **Ringkasan requirement** (daftar REQ-n)
2. **Asumsi & pertanyaan klarifikasi** (jika ada)
3. **Tabel test case** dengan kolom persis:

| ID | Req | Judul | Kategori | Prioritas | Precondition | Langkah | Data Uji | Expected Result |

   - ID berformat TC-001, TC-002, dst.
   - Langkah ditulis bernomor dalam satu sel, dipisah `<br>`.
4. **Coverage summary**: jumlah test case per kategori dan per requirement.
5. **Opsional**: bila pengguna meminta "gherkin", sertakan versi Given/When/Then untuk test case High.
