<script setup>
import { ref, computed, onMounted } from 'vue'

// State Data Backend & UI
const barangList = ref([])
const isLoading = ref(true)
const isError = ref(false)
const errorMessage = ref('')

// State Controls (Filter & Sort)
const kataKunci = ref('')
const arahUrutan = ref('asc') // 'asc' | 'desc'

// State Form Tambah Barang
const formBarang = ref({
  nama: '',
  kategori: '',
  jumlah_stok: 0,
  lokasi_gudang: ''
})

const API_URL = 'http://127.0.0.1:8000/api/barang'

// Fetch Data dari FastAPI
const ambilDataBarang = async () => {
  isLoading.value = true
  isError.value = false
  errorMessage.value = ''
  try {
    const response = await fetch(API_URL)
    if (!response.ok) throw new Error('Gagal mengambil data dari server')
    const data = await response.json()
    barangList.value = data
  } catch (err) {
    isError.value = true
    errorMessage.value = err.message || 'Terjadi kesalahan koneksi'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  ambilDataBarang()
})

// 1. Computed: Filtering (Pencarian Nama / Kategori)
const penggunaTersaring = computed(() => {
  const q = kataKunci.value.toLowerCase().trim()
  if (!q) return barangList.value
  return barangList.value.filter(item => 
    item.nama.toLowerCase().includes(q) || 
    item.kategori.toLowerCase().includes(q)
  )
})

// 2. Chained Computed: Sorting A-Z / Z-A berantai di atas hasil filter
const penggunaDiurutkan = computed(() => {
  return [...penggunaTersaring.value].sort((a, b) => {
    const res = a.nama.localeCompare(b.nama)
    return arahUrutan.value === 'asc' ? res : -res
  })
})

// 3. Computed 4 Tile Statistik Ringkasan (JS Native Array Methods)
const totalBarang = computed(() => barangList.value.length)

// Ambang batas stok: Stok <= 0 -> Habis, Stok 1-5 -> Menipis, Stok > 5 -> Aman
const stokMenipisHabis = computed(() => {
  return barangList.value.filter(item => item.jumlah_stok <= 5).length
})

const totalKategori = computed(() => {
  const kategoriUnik = new Set(barangList.value.map(item => item.kategori))
  return kategoriUnik.size
})

const totalUnit = computed(() => {
  return barangList.value.reduce((acc, curr) => acc + curr.jumlah_stok, 0)
})

// Method Handler Status Stok & Class Binding
const getStatusStokInfo = (stok) => {
  if (stok <= 0) return { label: 'Habis', class: 'badge-danger' }
  if (stok <= 5) return { label: 'Menipis', class: 'badge-warning' }
  return { label: 'Aman', class: 'badge-success' }
}

// Action POST: Tambah Barang
const tambahBarang = async () => {
  if (!formBarang.value.nama || !formBarang.value.kategori || !formBarang.value.lokasi_gudang) {
    alert('Mohon lengkapi seluruh field form!')
    return
  }

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...formBarang.value,
        jumlah_stok: Number(formBarang.value.jumlah_stok)
      })
    })

    if (!response.ok) throw new Error('Gagal menambah barang')

    // Reset form & Refresh Data
    formBarang.value = { nama: '', kategori: '', jumlah_stok: 0, lokasi_gudang: '' }
    await ambilDataBarang()
  } catch (err) {
    alert(err.message)
  }
}

// Action DELETE: Hapus Barang
const hapusBarang = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus barang ini?')) return

  try {
    const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' })
    if (!response.ok) throw new Error('Gagal menghapus barang')
    await ambilDataBarang()
  } catch (err) {
    alert(err.message)
  }
}
</script>

<template>
  <div class="dashboard-container">
    <!-- Header Identitas -->
    <header class="app-header">
      <h1>Dashboard Inventaris Gudang</h1>
      <p class="author-info">Deva Agriani — 25120300026 (UTS Web Application Development)</p>
    </header>

    <!-- 4 Tile Ringkasan Statistik -->
    <section class="stats-grid">
      <div class="stat-card">
        <h3>Total Barang</h3>
        <p class="stat-value">{{ totalBarang }}</p>
      </div>
      <div class="stat-card warning">
        <h3>Stok Menipis + Habis</h3>
        <p class="stat-value">{{ stokMenipisHabis }}</p>
      </div>
      <div class="stat-card">
        <h3>Jumlah Kategori</h3>
        <p class="stat-value">{{ totalKategori }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Unit Stok</h3>
        <p class="stat-value">{{ totalUnit }}</p>
      </div>
    </section>

    <!-- Form Tambah Barang -->
    <section class="form-section card">
      <h2>+ Tambah Barang Inventaris</h2>
      <form @submit.prevent="tambahBarang" class="form-grid">
        <div class="form-group">
          <label>Nama Barang</label>
          <input v-model="formBarang.nama" type="text" placeholder="misal: Laptop Dell" required />
        </div>
        <div class="form-group">
          <label>Kategori</label>
          <input v-model="formBarang.kategori" type="text" placeholder="misal: Elektronik" required />
        </div>
        <div class="form-group">
          <label>Jumlah Stok</label>
          <input v-model.number="formBarang.jumlah_stok" type="number" min="0" required />
        </div>
        <div class="form-group">
          <label>Lokasi Gudang</label>
          <input v-model="formBarang.lokasi_gudang" type="text" placeholder="misal: Gudang A1" required />
        </div>
        <button type="submit" class="btn-submit">Simpan Barang</button>
      </form>
    </section>

    <!-- Toolbar Controls (Pencarian & Sort) -->
    <section class="toolbar card">
      <div class="search-box">
        <input 
          v-model="kataKunci" 
          type="text" 
          placeholder="Cari berdasarkan nama atau kategori..." 
        />
      </div>
      <div class="sort-buttons">
        <span>Urutkan Nama:</span>
        <button 
          :class="{ active: arahUrutan === 'asc' }" 
          @click="arahUrutan = 'asc'"
        >
          A-Z
        </button>
        <button 
          :class="{ active: arahUrutan === 'desc' }" 
          @click="arahUrutan = 'desc'"
        >
          Z-A
        </button>
      </div>
    </section>

    <!-- Main Content Area (State UI) -->
    <main class="content-area card">
      <div v-if="isLoading" class="state-message">Memuat data inventaris...</div>
      
      <div v-else-if="isError" class="state-message error">
        {{ errorMessage }}
        <button @click="ambilDataBarang" class="btn-retry">Coba Lagi</button>
      </div>

      <div v-else-if="penggunaDiurutkan.length === 0" class="state-message">
        Tidak ada barang yang sesuai dengan pencarian.
      </div>

      <!-- Tabel Inventaris Responsif -->
      <div v-else class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nama Barang</th>
              <th>Kategori</th>
              <th>Stok</th>
              <th>Status</th>
              <th>Lokasi Gudang</th>
              <th>Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in penggunaDiurutkan" :key="item.id">
              <td>#{{ item.id }}</td>
              <td class="font-bold">{{ item.nama }}</td>
              <td><span class="category-tag">{{ item.kategori }}</span></td>
              <td>{{ item.jumlah_stok }}</td>
              <td>
                <span :class="['badge', getStatusStokInfo(item.jumlah_stok).class]">
                  {{ getStatusStokInfo(item.jumlah_stok).label }}
                </span>
              </td>
              <td>{{ item.lokasi_gudang }}</td>
              <td>
                <button @click="hapusBarang(item.id)" class="btn-delete">Hapus</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<style>
:root {
  --primary: #0f766e;
  --primary-dark: #115e59;
  --bg-gray: #f8fafc;
  --text-dark: #1e293b;
  --border-color: #e2e8f0;
}

* { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
body { background-color: var(--bg-gray); color: var(--text-dark); padding: 20px; }

.dashboard-container { max-width: 1100px; margin: 0 auto; display: flex; flex-direction: column; gap: 20px; }

.app-header { background-color: var(--primary); color: white; padding: 24px; border-radius: 12px; text-align: center; }
.author-info { margin-top: 6px; font-size: 0.95rem; opacity: 0.9; }

/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.stat-card { background: white; padding: 20px; border-radius: 10px; border: 1px solid var(--border-color); text-align: center; }
.stat-card h3 { font-size: 0.85rem; color: #64748b; text-transform: uppercase; margin-bottom: 8px; }
.stat-card .stat-value { font-size: 1.8rem; font-weight: bold; color: var(--primary); }
.stat-card.warning .stat-value { color: #d97706; }

.card { background: white; padding: 20px; border-radius: 10px; border: 1px solid var(--border-color); }

/* Form Section */
.form-section h2 { font-size: 1.1rem; margin-bottom: 14px; color: var(--primary-dark); }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; align-items: end; }
.form-group { display: flex; flex-direction: column; gap: 4px; }
.form-group label { font-size: 0.85rem; font-weight: 600; color: #475569; }
.form-group input { padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.9rem; }

/* Toolbar */
.toolbar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px; }
.search-box input { width: 300px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; }
.sort-buttons { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; }
.sort-buttons button { padding: 6px 14px; border: 1px solid var(--border-color); background: white; border-radius: 6px; cursor: pointer; }
.sort-buttons button.active { background: var(--primary); color: white; border-color: var(--primary); }

/* Table */
.table-responsive { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.95rem; }
th, td { padding: 12px; border-bottom: 1px solid var(--border-color); }
th { background: #f1f5f9; font-weight: 600; color: #475569; }

.category-tag { background: #e0f2fe; color: #0369a1; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; }
.badge { padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
.badge-success { background: #dcfce7; color: #15803d; }
.badge-warning { background: #fef3c7; color: #b45309; }
.badge-danger { background: #fee2e2; color: #b91c1c; }

/* Buttons */
.btn-submit { padding: 9px 16px; background: var(--primary); color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; }
.btn-delete { padding: 5px 10px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.8rem; }
.btn-retry { margin-top: 8px; padding: 6px 12px; background: var(--primary); color: white; border: none; border-radius: 4px; cursor: pointer; }

.state-message { text-align: center; padding: 40px; color: #64748b; }
.state-message.error { color: #dc2626; }

/* Responsif Breakpoint (Mobile < 768px) */
@media (max-width: 768px) {
  .toolbar { flex-direction: column; align-items: stretch; }
  .search-box input { width: 100%; }
  .sort-buttons { justify-content: space-between; }
}
</style>