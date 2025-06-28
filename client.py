import requests
import threading
import time
from datetime import datetime

# NAMA : FATHI ARDIAN
# NPM 50424439
# KELAS : 1IA17

BASE_API_URL = "http://127.0.0.1:5000/check_book_status"
ISBNS_TO_CHECK = ["978-3-16-148410-0", "978-0-26-110221-7", "999-9-99-999999-9", "978-1-40-885565-2"]
NUM_REQUESTS = len(ISBNS_TO_CHECK)
CLIENT_LOG_FILE = "library_client_log.txt"

client_log_lock = threading.Lock()

with open(CLIENT_LOG_FILE, "w", encoding="utf-8") as f:
    f.write(f"--- Library Client Log Started: {datetime.now()} ---\n")

# ==============================================================================
# SOAL 1: Implementasi Logging Thread-Safe
# ==============================================================================
def log_client_activity_safe(thread_name, message):
    """
    TUGAS ANDA (Soal 1):
    Lengkapi fungsi ini untuk mencatat 'message' dari 'thread_name' ke
    CLIENT_LOG_FILE secara thread-safe menggunakan 'client_log_lock'.

    Langkah-langkah:
    1. Dapatkan 'client_log_lock' (gunakan 'with' statement untuk kemudahan).
    2. Buat timestamp (contoh: datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")).
    3. Format pesan log (contoh: f"[{timestamp}] [{thread_name}] {message}\n").
    4. Tulis pesan log ke CLIENT_LOG_FILE (mode append 'a', encoding 'utf-8').
    5. (Opsional) Cetak pesan log ke konsol juga.
    """
   try:
      with client_log_lock:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        log_message = f"[{timestamp}] [{thread_name}] {message}\n"
      with open(CLIENT_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message)
      print(log_message.strip())
    except Exception as e:
      print(f" [ERROR] Gagal mencatat log {e}")


# ==============================================================================
# SOAL 2: Implementasi Fungsi Permintaan API
# ==============================================================================
def request_book_status_from_api(isbn, current_thread_name):
    """
    TUGAS ANDA (Soal 2):
    Lengkapi fungsi ini untuk mengirim permintaan GET ke API perpustakaan
    dan mencatat hasilnya menggunakan fungsi 'log_client_activity_safe' yang
    telah Anda implementasikan di Soal 1.

    Langkah-langkah:
    1. Bentuk 'target_url' dengan menggunakan BASE_API_URL dan 'isbn' yang diberikan.
    2. Catat (menggunakan 'log_client_activity_safe') bahwa permintaan akan dikirim.
    3. Gunakan blok 'try-except' untuk menangani potensi error saat request.
       a. Di dalam 'try':
          i.  Kirim permintaan GET ke 'target_url' menggunakan 'requests.get()'. Sertakan timeout.
          ii. Periksa 'response.status_code':
          
              - Jika 200 (sukses):
                  - Dapatkan JSON dari 'response.json()'.
                  - Catat pesan sukses. Contoh: f"Berhasil! Buku '{data.get('title', 'N/A')}' status: {data.get('status', 'N/A')}"
              - Jika 404 (ISBN tidak ditemukan):
                  - Dapatkan JSON dari 'response.json()'.
                  - Catat pesan error. Contoh: f"Error: ISBN {isbn} tidak ditemukan. Pesan: {data.get('message', 'Not found')}"
              - Untuk status code lain:
                  - Catat pesan error umum. Contoh: f"Menerima status error dari API: {response.status_code} - {response.text[:100]}"
       b. Di blok 'except requests.exceptions.Timeout':
          - Catat pesan timeout.
       c. Di blok 'except requests.exceptions.RequestException as e':
          - Catat pesan error permintaan umum.
       d. Di blok 'except Exception as e':
          - Catat pesan kesalahan tak terduga.
    4. Setelah blok try-except, catat bahwa tugas untuk ISBN ini selesai.
    """
    target_url = f"{BASE_API_URL}?isbn={isbn}"
    log_client_activity_safe(current_thread_name, f" Permintaan API akan dikirim untuk isbn: {isbn} ")
    try:
        response = requests.get(target_url, timeout=5)
      
        if response.status_code == 200:
          data = response.json()
          log_client_activity_safe(current_thread_name,  f"Berhasil! Buku '{data.get('title', 'N/A')}' status: {data.get('status', 'N/A')}")
        elif response.status_code == 404:
           data = response.json()
           log_client_activity_safe(current_thread_name, f"Error: ISBN {isbn} tidak ditemukan. Pesan: {data.get('message', 'Not found')}")
        else:
           log_client_activity_safe(current_thread_name, f"Menerima status error dari API: {response.status_code} - {response.text[:100]}")
    
    except requests.exceptions.Timeout:
      log_client_activity_safe(current_thread_name, f"timeout saat mengakses API untuk asbn: {asbn}")
      
    except requests.exceptions.RequestException as e:
       log_client_activity_safe(current_thread_name, f"Permintaan gagal untuk asbn : {asbn} {str(e)}")
      
    except Exception as e:
      log_client_activity_safe(current_thread_name, f"Terjadi Kesalahan untuk asbn : {asbn} {str(e)}")
    finally:
      log_client_activity_safe(current_thread_name, f"Tugas selesai untuk asbn")



def worker_thread_task(isbn, task_id):
    """Fungsi yang dijalankan oleh setiap worker thread."""
    thread_name = f"Worker-{task_id}"
    log_client_activity_safe(thread_name, f"Memulai pekerjaan untuk ISBN: {isbn}")
    request_book_status_from_api(isbn, thread_name)
    log_client_activity_safe(thread_name, f"Selesai pekerjaan untuk ISBN: {isbn}")

if __name__ == "__main__":
    log_client_activity_safe("MainClient", f"Memulai {NUM_REQUESTS} pengecekan status buku secara concurrent.")
    
    threads = []
    start_time = time.time()

    for i, book_isbn in enumerate(ISBNS_TO_CHECK):
        thread = threading.Thread(target=worker_thread_task, args=(book_isbn, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    
    log_client_activity_safe("MainClient", f"Semua pengecekan buku selesai dalam {total_time:.2f} detik.")
    print(f"\nLog aktivitas klien disimpan di: {CLIENT_LOG_FILE}")
    print(f"Total waktu eksekusi: {total_time:.2f} detik.")
