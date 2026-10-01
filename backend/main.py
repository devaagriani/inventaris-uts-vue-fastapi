import json
import os
from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Inventaris Barang UTS",
    description="Endpoint backend untuk mengelola data inventaris barang secara in-memory.",
    version="1.0.0"
)

# Aktifkan CORS agar frontend Vue di localhost dapat mengakses backend ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema Pydantic untuk Input & Output Data
class BarangBase(BaseModel):
    nama: str = Field(..., min_length=1, description="Nama barang inventaris")
    kategori: str = Field(..., min_length=1, description="Kategori barang")
    jumlah_stok: int = Field(..., ge=0, description="Jumlah stok barang (wajib integer >= 0)")
    lokasi_gudang: str = Field(..., min_length=1, description="Lokasi penyimpanan di gudang")

class BarangCreate(BarangBase):
    pass

class Barang(BarangBase):
    id: int

# Storage In-Memory
db_barang: List[dict] = []

def load_seed_data():
    global db_barang
    json_path = os.path.join(os.path.dirname(__file__), "data_seed.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            db_barang = json.load(f)

@app.on_event("startup")
def startup_event():
    load_seed_data()

# 1. Endpoint GET: Mengambil seluruh data barang
@app.get("/api/barang", response_model=List[Barang], summary="Ambil semua barang")
def get_all_barang():
    return db_barang

# 2. Endpoint POST: Menambah barang baru
@app.post("/api/barang", response_model=Barang, status_code=status.HTTP_201_CREATED, summary="Tambah barang baru")
def create_barang(item: BarangCreate):
    next_id = max([b["id"] for b in db_barang], default=0) + 1
    new_barang = {
        "id": next_id,
        "nama": item.nama,
        "kategori": item.kategori,
        "jumlah_stok": item.jumlah_stok,
        "lokasi_gudang": item.lokasi_gudang
    }
    db_barang.append(new_barang)
    return new_barang

# 3. Endpoint DELETE: Menghapus barang berdasarkan ID
@app.delete("/api/barang/{barang_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Hapus barang")
def delete_barang(barang_id: int):
    global db_barang
    index_to_delete = None
    for idx, item in enumerate(db_barang):
        if item["id"] == barang_id:
            index_to_delete = idx
            break
            
    if index_to_delete is None:
        raise HTTPException(status_code=404, detail=f"Barang dengan ID {barang_id} tidak ditemukan")
        
    db_barang.pop(index_to_delete)
    return None