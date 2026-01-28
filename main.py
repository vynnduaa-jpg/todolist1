import json
import os
from datetime import datetime

# File untuk menyimpan data tugas
DATA_FILE = "tasks.json"

def load_tasks():
    """Membaca data tugas dari file JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_tasks(tasks):
    """Menyimpan data tugas ke file JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def display_menu():
    """Menampilkan menu utama"""
    print("\n" + "="*60)
    print("📝" + " "*(55) + "📝")
    print("     ════════ APLIKASI TODOLIST ════════".center(60))
    print("📝" + " "*(55) + "📝")
    print("="*60)
    print("📋 1. Lihat Semua Tugas")
    print("➕ 2. Tambah Tugas Baru")
    print("✏️  3. Edit Tugas")
    print("🗑️  4. Hapus Tugas")
    print("✅ 5. Tandai Tugas Selesai / Belum")
    print("📚 6. Filter Berdasarkan Mata Pelajaran")
    print("❌ 7. Keluar")
    print("="*60)

def view_all_tasks(tasks):
    """Menampilkan semua tugas dalam format tabel"""
    if not tasks:
        print("\n⚠️  Tidak ada tugas! Silakan tambah tugas baru.")
        return
    
    print("\n" + "="*130)
    # Header tabel
    print(f"{'No':<4} {'Nama Tugas':<25} {'Mata Pelajaran':<15} {'Guru':<20} {'Deadline':<20} {'Status':<18}")
    print("-"*130)
    
    # Isi tabel
    for i, task in enumerate(tasks, 1):
        nama = task['nama_tugas'][:23]  # Potong jika terlalu panjang
        pelajaran = task['mata_pelajaran'][:13]
        guru = task['guru'][:18]
        deadline = f"{task['tanggal']} {task['jam']}"
        status = task['status']
        
        print(f"{i:<4} {nama:<25} {pelajaran:<15} {guru:<20} {deadline:<20} {status:<18}")
    
    print("="*130)
    
    # Tampilkan peringatan deadline
    show_deadline_warnings(tasks)

def show_deadline_warnings(tasks):
    """Menampilkan peringatan deadline untuk tugas yang belum selesai"""
    now = datetime.now()
    warnings = []
    
    for task in tasks:
        if task['status'] == 'Belum Selesai':
            try:
                deadline_str = f"{task['tanggal']} {task['jam']}"
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
                
                diff = deadline - now
                
                if diff.total_seconds() < 0:
                    # Sudah terlambat
                    hours = abs(diff.total_seconds()) // 3600
                    minutes = (abs(diff.total_seconds()) % 3600) // 60
                    warnings.append(f"⛔ Tugas \"{task['nama_tugas']}\" sudah terlambat {int(hours)} jam {int(minutes)} menit")
                else:
                    # Belum deadline
                    hours = diff.total_seconds() // 3600
                    minutes = (diff.total_seconds() % 3600) // 60
                    if hours > 0 or minutes > 0:
                        warnings.append(f"⚠️  Tugas \"{task['nama_tugas']}\" deadline dalam {int(hours)} jam {int(minutes)} menit")
            except:
                pass
    
    if warnings:
        print("\n" + "="*130)
        print("⏰ PERINGATAN DEADLINE:")
        print("-"*130)
        for warning in warnings:
            print(warning)
        print("="*130)

def add_task(tasks):
    """Menambah tugas baru"""
    print("\n📌 Tambah Tugas Baru")
    print("-"*60)
    
    nama_tugas = input("Nama tugas: ").strip()
    if not nama_tugas:
        print("❌ Nama tugas tidak boleh kosong!")
        return
    
    mata_pelajaran = input("Mata pelajaran: ").strip()
    if not mata_pelajaran:
        print("❌ Mata pelajaran tidak boleh kosong!")
        return
    
    guru = input("Nama guru/pemberi tugas: ").strip()
    if not guru:
        print("❌ Guru tidak boleh kosong!")
        return
    
    # Validasi tanggal
    while True:
        tanggal = input("Tanggal deadline (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            break
        except ValueError:
            print("❌ Format tanggal salah! Gunakan format YYYY-MM-DD (contoh: 2026-01-30)")
    
    # Validasi jam
    while True:
        jam = input("Jam deadline (HH:MM): ").strip()
        try:
            datetime.strptime(jam, "%H:%M")
            break
        except ValueError:
            print("❌ Format jam salah! Gunakan format HH:MM (contoh: 14:30)")
    
    # Tambah tugas baru
    new_task = {
        "nama_tugas": nama_tugas,
        "mata_pelajaran": mata_pelajaran,
        "guru": guru,
        "tanggal": tanggal,
        "jam": jam,
        "status": "Belum Selesai"
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print("✅ Tugas berhasil ditambahkan!")

def edit_task(tasks):
    """Mengedit tugas yang ada"""
    if not tasks:
        print("\n⚠️  Tidak ada tugas untuk diedit!")
        return
    
    print("\n✏️  Edit Tugas")
    print("-"*60)
    
    # Tampilkan daftar tugas
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['nama_tugas']}")
    
    try:
        pilihan = int(input("\nPilih nomor tugas yang ingin diedit: "))
        if 1 <= pilihan <= len(tasks):
            task = tasks[pilihan - 1]
            
            print(f"\nEdit Tugas: {task['nama_tugas']}")
            print("-"*60)
            print("(Tekan Enter jika tidak ingin mengubah)")
            
            # Edit masing-masing field
            nama = input(f"Nama tugas [{task['nama_tugas']}]: ").strip()
            if nama:
                task['nama_tugas'] = nama
            
            pelajaran = input(f"Mata pelajaran [{task['mata_pelajaran']}]: ").strip()
            if pelajaran:
                task['mata_pelajaran'] = pelajaran
            
            guru = input(f"Guru [{task['guru']}]: ").strip()
            if guru:
                task['guru'] = guru
            
            tanggal = input(f"Tanggal [{task['tanggal']}]: ").strip()
            if tanggal:
                try:
                    datetime.strptime(tanggal, "%Y-%m-%d")
                    task['tanggal'] = tanggal
                except ValueError:
                    print("❌ Format tanggal salah, tidak diubah!")
            
            jam = input(f"Jam [{task['jam']}]: ").strip()
            if jam:
                try:
                    datetime.strptime(jam, "%H:%M")
                    task['jam'] = jam
                except ValueError:
                    print("❌ Format jam salah, tidak diubah!")
            
            save_tasks(tasks)
            print("✅ Tugas berhasil diedit!")
        else:
            print("❌ Nomor tugas tidak valid!")
    except ValueError:
        print("❌ Input harus berupa angka!")

def delete_task(tasks):
    """Menghapus tugas"""
    if not tasks:
        print("\n⚠️  Tidak ada tugas untuk dihapus!")
        return
    
    print("\n🗑️  Hapus Tugas")
    print("-"*60)
    
    # Tampilkan daftar tugas
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['nama_tugas']}")
    
    try:
        pilihan = int(input("\nPilih nomor tugas yang ingin dihapus: "))
        if 1 <= pilihan <= len(tasks):
            nama_dihapus = tasks[pilihan - 1]['nama_tugas']
            tasks.pop(pilihan - 1)
            save_tasks(tasks)
            print(f"✅ Tugas \"{nama_dihapus}\" berhasil dihapus!")
        else:
            print("❌ Nomor tugas tidak valid!")
    except ValueError:
        print("❌ Input harus berupa angka!")

def toggle_task_status(tasks):
    """Mengubah status tugas (Selesai/Belum Selesai)"""
    if not tasks:
        print("\n⚠️  Tidak ada tugas!")
        return
    
    print("\n✅ Tandai Tugas")
    print("-"*60)
    
    # Tampilkan daftar tugas
    for i, task in enumerate(tasks, 1):
        status_display = "✅" if task['status'] == "Selesai" else "⏳"
        print(f"{i}. {task['nama_tugas']} [{status_display} {task['status']}]")
    
    try:
        pilihan = int(input("\nPilih nomor tugas yang ingin diubah statusnya: "))
        if 1 <= pilihan <= len(tasks):
            task = tasks[pilihan - 1]
            if task['status'] == "Belum Selesai":
                task['status'] = "Selesai"
                print(f"✅ Tugas \"{task['nama_tugas']}\" ditandai SELESAI!")
            else:
                task['status'] = "Belum Selesai"
                print(f"⏳ Tugas \"{task['nama_tugas']}\" ditandai BELUM SELESAI!")
            save_tasks(tasks)
        else:
            print("❌ Nomor tugas tidak valid!")
    except ValueError:
        print("❌ Input harus berupa angka!")

def filter_by_subject(tasks):
    """Menampilkan tugas berdasarkan mata pelajaran"""
    if not tasks:
        print("\n⚠️  Tidak ada tugas!")
        return
    
    # Dapatkan daftar mata pelajaran unik
    subjects = list(set([task['mata_pelajaran'] for task in tasks]))
    
    print("\n📚 Filter Berdasarkan Mata Pelajaran")
    print("-"*60)
    
    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject}")
    
    try:
        pilihan = int(input("\nPilih nomor mata pelajaran: "))
        if 1 <= pilihan <= len(subjects):
            selected_subject = subjects[pilihan - 1]
            filtered_tasks = [task for task in tasks if task['mata_pelajaran'] == selected_subject]
            
            print(f"\n📚 Tugas untuk Mata Pelajaran: {selected_subject}")
            print("="*130)
            print(f"{'No':<4} {'Nama Tugas':<25} {'Guru':<20} {'Deadline':<20} {'Status':<18}")
            print("-"*130)
            
            for i, task in enumerate(filtered_tasks, 1):
                nama = task['nama_tugas'][:23]
                guru = task['guru'][:18]
                deadline = f"{task['tanggal']} {task['jam']}"
                status = task['status']
                print(f"{i:<4} {nama:<25} {guru:<20} {deadline:<20} {status:<18}")
            
            print("="*130)
            show_deadline_warnings(filtered_tasks)
        else:
            print("❌ Nomor mata pelajaran tidak valid!")
    except ValueError:
        print("❌ Input harus berupa angka!")

def main():
    """Fungsi utama aplikasi"""
    print("\n🎉 Selamat datang di Aplikasi To-Do List!")
    
    while True:
        # Load data terbaru
        tasks = load_tasks()
        
        # Tampilkan menu
        display_menu()
        pilihan = input("\nPilih menu (1-7): ").strip()
        
        if pilihan == '1':
            view_all_tasks(tasks)
        elif pilihan == '2':
            add_task(tasks)
        elif pilihan == '3':
            edit_task(tasks)
        elif pilihan == '4':
            delete_task(tasks)
        elif pilihan == '5':
            toggle_task_status(tasks)
        elif pilihan == '6':
            filter_by_subject(tasks)
        elif pilihan == '7':
            print("\n👋 Terima kasih telah menggunakan Aplikasi To-Do List!")
            print("Sampai jumpa lagi!\n")
            break
        else:
            print("❌ Pilihan tidak valid! Silakan pilih menu 1-7.")
        
        if pilihan != '7':
            input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()
