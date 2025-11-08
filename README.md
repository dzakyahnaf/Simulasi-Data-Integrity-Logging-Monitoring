# 🔒 Simulasi Data Integrity, Logging & Monitoring

## Anggota Kelompok 9:

- Muhammad Dzaky Ahnaf (5027231039)
- Daffa Rajendra P. (5027231009)
- Muhamad Arrayyan (5027231014)
- Naufal Syafi’ H. (5027231022)
- RM. Novian Malcolm (5027231035)

---

Proyek ini merupakan tugas mata kuliah **Keamanan Web dan Aplikasi** dengan fokus pada **OWASP 2021 A08 & A09**, yaitu:

- **A08 – Software and Data Integrity Failures**
- **A09 – Security Logging and Monitoring Failures**

Tujuan dari simulasi ini adalah **membangun sistem sederhana untuk memantau integritas file, melakukan logging aktivitas, serta menampilkan hasil monitoring** dalam bentuk konsol dan (opsional) web mini berbasis Flask.

---

## 🧩 Fitur Utama

1. **Pemantauan Folder**

   - Memantau folder `./secure_files/`
   - Mendeteksi file yang:
     - Diubah (hash berbeda)
     - Dihapus
     - Ditambahkan (file baru)

2. **Verifikasi Integritas File**

   - Menyimpan _baseline hash_ setiap file di `hash_db.json`
   - Setiap dijalankan, sistem membandingkan hash saat ini dengan baseline
   - Jika berbeda → dicatat di `security.log` dan muncul _alert simulasi_ di konsol

3. **Logging Komprehensif**

   - Semua aktivitas tercatat dalam `security.log` dengan format:
     ```
     [2025-10-30 13:25:11] INFO: File "config.json" verified OK.
     [2025-10-30 13:26:02] WARNING: File "data.txt" integrity failed!
     [2025-10-30 13:27:15] ALERT: Unknown file "hacked.js" detected.
     ```
   - Level logging: `INFO`, `WARNING`, `ALERT`

4. **Monitoring Ringkas**

   - Menampilkan jumlah file aman dan rusak
   - Menampilkan waktu terakhir anomali terdeteksi

5. **Bonus (Opsional)**
   - Mini web UI dengan **Flask** untuk menampilkan hasil monitoring melalui browser
   - **Modern Dashboard** dengan Bootstrap 5, color-coded logs, dan auto-refresh
   - **Real-time updates** melalui AJAX API
   - **Responsive design** yang bekerja di semua devices

---

## 🛠️ Persiapan & Instalasi

### 1. Clone Repositori

```bash
git clone https://github.com/dzakyahnaf/Simulasi-Data-Integrity-Logging-Monitoring.git
cd simulasi-integritas
```

### 2. Siapkan Virtual Environment (Opsional tapi disarankan)

```bash
python -m venv venv
source venv/bin/activate   # di Linux/Mac
venv\Scripts\activate      # di Windows
```

### 3. Instal Dependensi

```bash
pip install -r requirements.txt
```

atau secara manual:

```bash
pip install flask watchdog
```

---

## 🚀 Cara Pakai (Urutan Perintah)

### 1. Buat Folder & File Contoh

```bash
mkdir secure_files
echo "hello world" > secure_files/readme.txt
```

### 2. Inisialisasi Baseline

Buat _hash baseline_ awal untuk semua file di folder `secure_files`.

```bash
python init_baseline.py
```

Output contoh:

```
[2025-10-30T13:25:11] Baseline saved to hash_db.json, 1 files.
```

### 3. Jalankan Monitoring Sekali

Menjalankan pemeriksaan integritas dan mencatat hasil ke `security.log`.

```bash
python monitor.py
```

Contoh output di konsol:

```
[2025-10-30 13:25:11] INFO: File "readme.txt" verified OK.
Monitoring run complete. Check security.log
```

### 3b. 🔴 Jalankan Monitoring Real-Time (BARU!)

Untuk monitoring otomatis yang langsung mendeteksi perubahan tanpa harus menjalankan `monitor.py` berulang kali:

```bash
python monitor_realtime.py
```

Program akan:
- ✅ Melakukan full scan pertama kali
- ✅ Terus berjalan dan memantau folder `secure_files/`
- ✅ **Otomatis** mendeteksi perubahan, penambahan, atau penghapusan file
- ✅ Langsung menulis ke log dan memberikan alert

Contoh output:

```
============================================================
Real-time monitoring started for: secure_files
Logs written to: security.log
Press Ctrl+C to stop monitoring
============================================================

[2025-11-06 15:30:45] INFO: Detected modification: secure_files\demo.txt
[2025-11-06 15:30:45] WARNING: File "demo.txt" integrity failed!
[SIMULATED ALERT] WARNING: demo.txt hash mismatch
```

**Tekan Ctrl+C untuk menghentikan monitoring.**

### 4. Baca Hasil Monitoring

Gunakan skrip log reader untuk melihat ringkasan hasil pemeriksaan.

```bash
python log_reader.py
```

Output contoh:

```
Summary:
  Jumlah file yang aman : 1
  Jumlah file rusak     : 0
  Tidak ada anomali tercatat.
```

### 5. (Opsional) Jalankan Web Mini Dashboard

Jika ingin menampilkan hasil monitoring lewat browser dengan **tampilan modern**:

```bash
python app.py
```

Buka di browser:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

#### Fitur Dashboard:
- ✅ **Modern Dark Theme** dengan gradients dan animations
- ✅ **Real-time Statistics Cards** - Files verified, compromised, last anomaly
- ✅ **Auto-Refresh** - Update otomatis setiap 5 detik
- ✅ **Color-Coded Logs** - INFO (hijau), WARNING (orange), ALERT (merah)
- ✅ **Responsive Design** - Bekerja di mobile, tablet, desktop
- ✅ **Interactive UI** - Hover effects, smooth transitions

---

## ✨ Menambahkan Verified Files (BARU!)

Jika ada file baru yang sah atau ingin memverifikasi file yang terdeteksi "unknown":

```bash
# Tambah file tunggal
python add_to_baseline.py add filename.txt

# Tambah semua file sekaligus
python add_to_baseline.py add-all

# Lihat daftar verified files
python add_to_baseline.py list

# Hapus file dari baseline
python add_to_baseline.py remove filename.txt
```

---

## 🧪 Untuk Menguji (Simulasi Serangan / Anomali)

### 6. Uji Deteksi Perubahan, Penambahan, dan Penghapusan File

| Jenis Uji                              | Cara Melakukan                                                                        | Hasil yang Diharapkan                                                           |
| -------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **a. Ubah isi file**                   | Edit `secure_files/readme.txt` lalu jalankan `python monitor.py` lagi                 | `WARNING: File "readme.txt" integrity failed!` muncul di log dan konsol         |
| **b. Tambahkan file baru**             | Buat file baru: `echo "x" > secure_files/hacked.js` lalu jalankan `python monitor.py` | `ALERT: Unknown file "hacked.js" detected.` muncul di log dan konsol            |
| **c. Hapus file yang ada di baseline** | Hapus file `secure_files/readme.txt`, lalu jalankan `python monitor.py`               | `ALERT: File "readme.txt" missing (possibly deleted).` muncul di log dan konsol |

Setelah itu, jalankan `python log_reader.py` untuk melihat hasil ringkasan terakhir.

Contoh hasil:

```
Summary:
  Jumlah file yang aman : 0
  Jumlah file rusak     : 1
  Waktu terakhir anomali: 2025-10-30 13:26:02
```

---

## 📄 Struktur Folder Proyek

```
simulasi-integritas/
│
├── secure_files/           # Folder yang dipantau
├── hash_db.json            # Baseline hash tiap file
├── security.log            # File log aktivitas
│
├── init_baseline.py        # Membuat baseline awal
├── add_to_baseline.py      # ✨ Tambah/update verified files (BARU!)
├── monitor.py              # Memantau dan mencatat perubahan (manual)
├── monitor_realtime.py     # 🔴 Monitoring real-time otomatis (BARU!)
├── log_reader.py           # Membaca dan merangkum hasil log
├── app.py                  # 🎨 Modern web dashboard dengan Flask (UPGRADED!)
├── requirements.txt        # Dependencies yang dibutuhkan
├── README.md               # Dokumentasi utama
├── QUICKSTART.md           # Setup cepat 5 menit
├── REALTIME_GUIDE.md       # Panduan real-time monitoring
├── DASHBOARD_GUIDE.md      # Panduan lengkap dashboard UI
└── ADD_VERIFIED_FILES_GUIDE.md  # Panduan menambah verified files
```

---

## 🧠 Konsep yang Dipelajari

| Konsep                    | Penjelasan Singkat                                                                            |
| ------------------------- | --------------------------------------------------------------------------------------------- |
| **Data Integrity**        | Menjamin bahwa file tidak dimodifikasi tanpa izin dengan menggunakan hash (SHA-256).          |
| **Baseline Hashing**      | Snapshot “kondisi aman” pertama yang digunakan sebagai pembanding di setiap pemeriksaan.      |
| **Security Logging**      | Mencatat semua aktivitas dan insiden agar bisa dilakukan audit forensik jika terjadi anomali. |
| **Monitoring & Alerting** | Sistem sederhana untuk mendeteksi perubahan mencurigakan dan memberikan peringatan.           |

---

## 🏷️ Teknologi yang Digunakan

- **Python 3.8+**
- **Flask** (opsional untuk tampilan web)
- **hashlib, logging, json** (library standar Python)

---


