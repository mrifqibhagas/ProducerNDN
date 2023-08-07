import json
from firebase_admin import firestore

# Inisialisasi koneksi dengan Firestore (pastikan Anda sudah terhubung sebelumnya)
# Misalnya, Anda telah menginisialisasi koneksi menggunakan service account key.
db = firestore.client()

# Mendapatkan referensi ke koleksi "datapasien"
collection_ref = db.collection("datapasien")

# Mendapatkan semua dokumen dalam koleksi "datapasien"
all_documents = collection_ref.stream()

# Inisialisasi list untuk menyimpan semua nama isi dokumen
document_names = []

# Loop melalui semua dokumen dan menyimpan nama dokumen dalam list document_names
for doc in all_documents:
    document_names.append(doc.id)

# Ubah list document_names menjadi format JSON
json_data = json.dumps(document_names)

# Cetak data dalam format JSON
print(json_data)
