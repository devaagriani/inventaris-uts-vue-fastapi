# UTS Web Application Development - Dashboard Inventaris (Soal B)

**Nama:** Deva Agriani  
**NIM:** 25120300026 (NIM Genap - Soal B: Dashboard Inventaris)  

---

## 📌 Deskripsi Proyek
Aplikasi Dashboard Inventaris Gudang Full-Stack yang dibangun menggunakan **FastAPI (Python)** untuk Backend dan **Vue 3 (Composition API)** untuk Frontend.

---

## 📏 Ambang Batas Status Stok (Threshold)
Status stok barang pada dashboard ditentukan secara otomatis dengan aturan berikut:
- **Aman**: Jumlah stok > 5 unit
- **Menipis**: Jumlah stok 1 - 5 unit
- **Habis**: Jumlah stok = 0 unit

---

## 🚀 Cara Menjalankan Proyek

### 1. Menjalankan Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Di Windows use: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

* Backend berjalan di: `http://127.0.0.1:8000`
* API Endpoint: `http://127.0.0.1:8000/api/barang`
* OpenAPI Docs: `http://127.0.0.1:8000/docs`

### 2. Menjalankan Frontend (Vue 3)

```bash
cd frontend
npm install
npm run dev
```

* Frontend berjalan di: `http://localhost:5173`