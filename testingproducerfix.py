# import pyrebase // Library untuk berinteraksi dengan Firebase menggunakan Python.
import json # Library untuk bekerja dengan data JSON.
import firebase_admin # Library Firebase Admin SDK untuk berinteraksi dengan Firebase menggunakan Python.
from firebase_admin import credentials, db, firestore # Submodul dari firebase_admin untuk mengelola kredensial dan akses ke database Firebase.
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

    doc_id = nama_to_search

    doc_ref = db.collection("datapasien").document(doc_id)
    doc = doc_ref.get()

    data_str = ""
    matching_data = []  # Initialize matching_data as an empty list

    if doc.exists:
        data = doc.to_dict()

        
        # Access and check the "nama" parameter
        nama = data.get("nama")
        if nama and nama == nama_to_search:
            matching_data.append({
                #   "ID": record_id,
                  "Nama": data.get("nama"),
                  "Umur": data.get("umur"),
                  "Penyakit": data.get("penyakit"),
                })
            print(f"Data yang terkait dengan nama '{nama_to_search}':")
            # Menggunakan json.dumps untuk mengubah data menjadi string format JSON
            data_str = json.dumps(matching_data)
            print(data_str)
        else:
            print(f"Tidak ditemukan data dengan nama '{nama_to_search}'.")
    else:
        print("No data available in the 'records' folder.") # Jika data tidak ada di folder db


    content = data_str.encode()
    app.put_data(name, content=content, freshness_period=10000)
    print(f'<< D: {Name.to_str(name)}')
    print(MetaInfo(freshness_period=10000))
    print(f'Content: (size: {len(content)})')
    print('')

@app.route('/data/inputdata')
def inputdata(name: FormalName, param: InterestParam, ap: Optional[BinaryStr]):
    nama_to_search = str(bytes(ap)).split('b\'')[1].split('\'')[0]
    #print(f'>> I: {Name.to_str(name)}, {param}')
    #print(f'<< D: {Name.to_str(name)}')
    print(f"Data yang terkait dengan nama '{nama_to_search}':")

print("Producer running, press CTRL+C to stop")

if __name__ == '__main__':
    app.run_forever()
