# 🚀 Quick Start Guide

## Setup Cepat dalam 5 Menit

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Buat File Demo
```bash
# Buat folder secure_files jika belum ada
mkdir secure_files

# Tambahkan beberapa file contoh
echo "Hello World" > secure_files/demo.txt
echo "Secret Data" > secure_files/data.txt
```

### 3️⃣ Inisialisasi Baseline
```bash
python init_baseline.py
```

Output:
```
[2025-11-06T10:30:00] Baseline saved to hash_db.json, 2 files.
```

### 4️⃣ Jalankan Monitoring (Pilih salah satu)

#### Opsi A: Manual Monitoring
```bash
python monitor.py
```

#### Opsi B: Real-time Monitoring ⭐ (Recommended)
```bash
python monitor_realtime.py
```

### 5️⃣ Buka Web Dashboard 🎨
```bash
# Di terminal baru
python app.py
```

Buka browser: **http://127.0.0.1:5000**

---

## 🧪 Test Sistem

### Test 1: Ubah File
```bash
echo "Modified content" > secure_files/demo.txt
```

**Expected Result:**
- Monitor mendeteksi perubahan
- Log menampilkan: `WARNING: File "demo.txt" integrity failed!`
- Dashboard menunjukkan file rusak bertambah

### Test 2: Tambah File Baru
```bash
echo "Hacker was here" > secure_files/malicious.js
```

**Expected Result:**
- Monitor mendeteksi file baru
- Log menampilkan: `ALERT: Unknown file "malicious.js" detected.`
- Dashboard menunjukkan alert

### Test 3: Hapus File
```bash
del secure_files\data.txt      # Windows
rm secure_files/data.txt       # Linux/Mac
```

**Expected Result:**
- Monitor mendeteksi penghapusan
- Log menampilkan: `ALERT: File "data.txt" missing (possibly deleted).`
- Dashboard menunjukkan alert

---

## 💡 Tips & Tricks

### Menjalankan Kedua Service Bersamaan

**Windows (PowerShell):**
```powershell
# Terminal 1
python monitor_realtime.py

# Terminal 2
python app.py
```

**Linux/Mac:**
```bash
# Background monitoring
python monitor_realtime.py &

# Foreground dashboard
python app.py
```

### Melihat Log Secara Real-time

**Windows:**
```powershell
Get-Content security.log -Wait -Tail 20
```

**Linux/Mac:**
```bash
tail -f security.log
```

### Reset Baseline

Jika ingin reset dan mulai dari awal:

```bash
# Hapus baseline lama
del hash_db.json         # Windows
rm hash_db.json          # Linux/Mac

# Buat baseline baru
python init_baseline.py
```

### Export Logs

```bash
# Copy logs dengan timestamp
copy security.log security_backup_2025-11-06.log      # Windows
cp security.log security_backup_$(date +%Y%m%d).log   # Linux/Mac
```

---

## 🎯 Use Cases

### Case 1: Monitoring Production Files
```bash
# Setup
mkdir secure_files
cp /path/to/production/* secure_files/
python init_baseline.py

# Monitor
python monitor_realtime.py
```

### Case 2: Detecting Unauthorized Changes
```bash
# Sistem berjalan, file diubah unauthorized
# Monitor otomatis detect dan log

# Cek laporan
python log_reader.py
```

### Case 3: Audit Trail
```bash
# Lihat semua aktivitas
cat security.log

# Filter hanya warnings dan alerts
grep "WARNING\|ALERT" security.log
```

---

## ⚙️ Configuration

### Ubah Interval Auto-Refresh Dashboard

Edit `app.py`, cari baris:
```javascript
refreshInterval = setInterval(updateDashboard, 5000); // 5000ms = 5 detik
```

Ubah `5000` ke nilai yang diinginkan (dalam milidetik).

### Ubah Jumlah Log yang Ditampilkan

Edit `app.py`, cari baris:
```python
lines = f.readlines()[-200:]  # 200 entries terakhir
```

Ubah `200` ke nilai yang diinginkan.

### Ubah Port Dashboard

Edit `app.py`, cari baris:
```python
app.run(debug=True, port=5000)
```

Ubah `5000` ke port yang diinginkan.

---

## 🔧 Troubleshooting

### Problem: "No module named 'flask'"
**Solution:**
```bash
pip install flask
```

### Problem: "No module named 'watchdog'"
**Solution:**
```bash
pip install watchdog
```

### Problem: Dashboard tidak bisa diakses
**Solution:**
1. Cek apakah Flask sudah running
2. Pastikan port 5000 tidak digunakan aplikasi lain
3. Coba akses: http://localhost:5000

### Problem: Monitor tidak deteksi perubahan
**Solution:**
1. Pastikan `monitor_realtime.py` masih berjalan
2. Cek apakah file dalam folder `secure_files/`
3. Restart monitor: Ctrl+C lalu jalankan ulang

### Problem: Baseline error
**Solution:**
```bash
# Hapus dan buat ulang
del hash_db.json
python init_baseline.py
```

---

## 📚 Dokumentasi Lengkap

- **README.md** - Dokumentasi utama proyek
- **REALTIME_GUIDE.md** - Panduan real-time monitoring
- **DASHBOARD_GUIDE.md** - Panduan lengkap dashboard
- **DASHBOARD_PREVIEW.md** - Preview visual dashboard

---

## ✅ Checklist Setup

- [ ] Dependencies terinstall (`pip install -r requirements.txt`)
- [ ] Folder `secure_files/` dibuat
- [ ] Files untuk monitoring ditambahkan
- [ ] Baseline dibuat (`python init_baseline.py`)
- [ ] Monitor berjalan (`python monitor_realtime.py`)
- [ ] Dashboard berjalan (`python app.py`)
- [ ] Browser dibuka ke http://127.0.0.1:5000
- [ ] Test perubahan file berhasil

---

**Selamat! Sistem monitoring Anda siap digunakan!** 🎉

Untuk pertanyaan atau masalah, lihat dokumentasi lengkap atau buka issue di GitHub repository.
