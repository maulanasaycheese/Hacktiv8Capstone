(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const SAMPLE = [
    "Aplikasi: Toko online berbasis web.",
    "",
    "REQ-1: Pengguna dapat login dengan email dan password yang terdaftar.",
    "REQ-2: Password minimal 8 karakter.",
    "REQ-3: Setelah 5 kali password salah berturut-turut, akun dikunci selama 15 menit.",
    "REQ-4: Pengguna dapat memilih \"Ingat saya\" agar sesi bertahan 7 hari."
  ].join("\n");

  let state = { markdown: "", cases: [] };

  function setStatus(msg, isError) {
    const el = $("status");
    el.textContent = msg;
    el.classList.toggle("error", Boolean(isError));
  }

  function cell(tag, className, text) {
    const td = document.createElement("td");
    if (className) td.className = className;
    td.textContent = text || "";
    return td;
  }

  function renderRow(c) {
    const tr = document.createElement("tr");
    tr.appendChild(cell("td", "id", c.id));
    tr.appendChild(cell("td", "req", c.req));
    tr.appendChild(cell("td", "", c.judul));

    const cat = document.createElement("td");
    const tag = document.createElement("span");
    tag.className = "tag " + (c.kategori || "").split(" ")[0];
    tag.textContent = c.kategori || "";
    cat.appendChild(tag);
    tr.appendChild(cat);

    tr.appendChild(cell("td", "prio-" + (c.prioritas || ""), c.prioritas));
    tr.appendChild(cell("td", "", c.precondition));

    const steps = document.createElement("td");
    steps.className = "steps";
    (c.langkah || "").split(/<br\s*\/?>/i).forEach((line) => {
      const d = document.createElement("div");
      d.textContent = line.trim();
      steps.appendChild(d);
    });
    tr.appendChild(steps);

    tr.appendChild(cell("td", "data", c.data_uji));
    tr.appendChild(cell("td", "", c.expected));
    return tr;
  }

  function renderSummary(summary) {
    const box = $("summary");
    box.replaceChildren();
    const add = (label, value) => {
      const chip = document.createElement("span");
      chip.className = "chip";
      chip.append(label + " ");
      const b = document.createElement("b");
      b.textContent = value;
      chip.appendChild(b);
      box.appendChild(chip);
    };
    add("Total", summary.total);
    Object.entries(summary.per_kategori || {}).forEach(([k, v]) => add(k, v));
    box.hidden = false;
  }

  function render(result) {
    state = { markdown: result.markdown, cases: result.cases };
    const body = document.querySelector("#cases tbody");
    body.replaceChildren(...result.cases.map(renderRow));
    const hasCases = result.cases.length > 0;
    $("table-wrap").hidden = !hasCases;
    $("empty").hidden = true;
    $("raw").textContent = result.markdown;
    $("raw-wrap").hidden = false;
    $("copy").disabled = false;
    $("export").disabled = !hasCases;
    if (hasCases) renderSummary(result.summary);
    else $("summary").hidden = true;
    $("mode").textContent = result.demo
      ? "Mode demo: output contoh, belum terhubung ke model"
      : "Model aktif";
  }

  async function generate() {
    const requirement = $("requirement").value.trim();
    if (!requirement) {
      setStatus("Isi requirement terlebih dahulu.", true);
      return;
    }
    $("generate").disabled = true;
    setStatus("Membuat test case...");
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ requirement, context: $("context").value })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Permintaan gagal.");
      render(data);
      setStatus(data.cases.length + " test case dibuat" + (data.demo ? " (contoh demo)." : "."));
    } catch (err) {
      setStatus(err.message, true);
    } finally {
      $("generate").disabled = false;
    }
  }

  async function exportCsv() {
    const res = await fetch("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cases: state.cases })
    });
    if (!res.ok) { setStatus("Gagal mengekspor CSV.", true); return; }
    const url = URL.createObjectURL(await res.blob());
    const a = document.createElement("a");
    a.href = url;
    a.download = "test-cases.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  async function copyMarkdown() {
    try {
      await navigator.clipboard.writeText(state.markdown);
      setStatus("Markdown disalin.");
    } catch (_) {
      setStatus("Tidak bisa menyalin otomatis. Buka respons mentah lalu salin manual.", true);
    }
  }

  $("generate").addEventListener("click", generate);
  $("export").addEventListener("click", exportCsv);
  $("copy").addEventListener("click", copyMarkdown);
  $("sample").addEventListener("click", () => {
    $("requirement").value = SAMPLE;
    $("context").value = "Toko online berbasis web";
    setStatus("Contoh login diisi. Pilih Buat test case.");
  });
})();
