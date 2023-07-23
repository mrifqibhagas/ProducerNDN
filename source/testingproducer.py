# import pyrebase // Library untuk berinteraksi dengan Firebase menggunakan Python.
import json # Library untuk bekerja dengan data JSON.
import firebase_admin # Library Firebase Admin SDK untuk berinteraksi dengan Firebase menggunakan Python.
from firebase_admin import credentials, db # Submodul dari firebase_admin untuk mengelola kredensial dan akses ke database Firebase.
from typing import Optional # Digunakan untuk memberikan tipe data opsional dalam tanda kurung siku ([])
from ndn.app import NDNApp # Membuat dan mengelola aplikasi Named Data Networking (NDN) // Beberapa fungsi mirip seperti faces ndn-cxx.
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo # Modul untuk bekerja dengan encoding NDN.
import logging

cred = credentials.Certificate("ndn-firebase-cubit-firebase-adminsdk-lkrlf-b2de4ea5a5.json")
firebase_admin.initialize_app(cred)
#firebase_admin.initialize_app(cred, {'databaseURL': "https://medical-record-7557a-default-rtdb.asia-southeast1.firebasedatabase.app"})

db = firestore.client()
app = NDNApp()

@app.route('/data/getuser')
def on_interest(name: FormalName, param: InterestParam, ap: Optional[BinaryStr]):
    nama_to_search = str(bytes(ap)).split('b\'')[1].split('\'')[0]
    print(f'>> I: {Name.to_str(name)}, {param}')

    doc_ref = db.collection("datapasien").document(doc_id)
    doc = doc_ref.get()

    if doc:
        matching_data = []
        for list_data in data.items():
        # Access and check the "nama" parameter
            nama = list_data.get("nama")
            print(nama)
            if nama and nama == nama_to_search:
             matching_data.append({
                #   "ID": record_id,
                  "Nama": list_data.get("nama"),
                  "Umur": list_data.get("umur"),
                  "Penyakit": list_data.get("penyakit"),
                })
             
    # Print or process the matching records
        if matching_data:
         print(f"Data yang terkait dengan nama '{nama_to_search}':")
         for record in matching_data:
            # Menggunakan json.dumps untuk mengubah data menjadi string format JSON
                record_str = json.dumps(record)
                print(record_str)
        else:
            print(f"Tidak ditemukan data dengan nama '{nama_to_search}'.")
    else:
        print("No data available in the 'records' folder.") # Jika data tidak ada di folder db

    content = record_str.encode()
    app.put_data(name, content=content, freshness_period=10000)
    print(f'<< D: {Name.to_str(name)}')
    print(MetaInfo(freshness_period=10000))
    print(f'Content: (size: {len(content)})')
    print('')

print("Producer running, press CTRL+C to stop")