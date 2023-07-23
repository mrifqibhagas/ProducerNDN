# import pyrebase // Library untuk berinteraksi dengan Firebase menggunakan Python.
import json # Library untuk bekerja dengan data JSON.
import firebase_admin # Library Firebase Admin SDK untuk berinteraksi dengan Firebase menggunakan Python.
from firebase_admin import credentials, db # Submodul dari firebase_admin untuk mengelola kredensial dan akses ke database Firebase.
from typing import Optional # Digunakan untuk memberikan tipe data opsional dalam tanda kurung siku ([])
from ndn.app import NDNApp # Membuat dan mengelola aplikasi Named Data Networking (NDN) // Beberapa fungsi mirip seperti faces ndn-cxx.
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo # Modul untuk bekerja dengan encoding NDN.
import logging

cred = credentials.Certificate("ndn-firebase-cubit-firebase-adminsdk-lkrlf-b2de4ea5a5.json") # mendefinisikan kredensial Firebase yang digunakan untuk otentikasi dan berinteraksi dengan layanan Firebase
firebase_admin.initialize_app(cred, {'databaseURL': "https://medical-record-7557a-default-rtdb.asia-southeast1.firebasedatabase.app"}) # menginisialisasi aplikasi Firebase menggunakan kredensial yang telah didefinisikan sebelumnya, dan menyediakan URL database Firebase yang akan diakses

# Mengatur konfigurasi logging untuk mencatat pesan log dengan format tertentu, termasuk timestamp dan level logging
logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

app = NDNApp()

@app.route('/data/getuser')
# Fungsi on_interest dijalankan ketika ada permintaan (interest) yang masuk ke route '/data/getuser'
def on_interest(name: FormalName, param: InterestParam, ap: Optional[BinaryStr]):
    nama_to_search = str(bytes(ap)).split('b\'')[1].split('\'')[0]
    print(f'>> I: {Name.to_str(name)}, {param}')
    
    # Get a reference to the root of the database
    root_ref = db.reference()
    # Get a reference to the "records" folder in the database
    records_ref = root_ref.child("records")
    # Read data from the "records" folder
    data = records_ref.get()
# Print the data or perform further processing.
# print(data)
# Check if data is not None (data exists)
    if data:
    # Input nama yang ingin Anda cari dari terminal
        # nama_to_search = input("Masukkan nama yang ingin Anda cari: ")
    # List untuk menyimpan data yang sesuai dengan nama yang dicari
        matching_records = []
        for record_id, record_data in data.items():
        # Access and check the "nama" parameter
            nama = record_data.get("nama")
            print(nama)
            if nama and nama == nama_to_search:
             matching_records.append({
                #   "ID": record_id,
                  "Nama": record_data.get("nama"),
                  "Umur": record_data.get("umur"),
                  "Sex": record_data.get("sex"),
                  "Diagnosis": record_data.get("Diagnosis"),
                  "DBP": record_data.get("DBP"),
                  "SBP": record_data.get("SBP"),
                })

    # Print or process the matching records
        if matching_records:
         print(f"Data yang terkait dengan nama '{nama_to_search}':")
         for record in matching_records:
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


@app.route('/data/adduser')
def on_data(name: FormalName, param: InterestParam, ap: Optional[BinaryStr]):
    data_to_save = str(bytes(ap)).split('b\'')[1].split('\'')[0]
    print(f'>> I: {Name.to_str(name)}, {param}')

    # Mendapatkan data dari body permintaan
    # data = request.get_json()

    data_dict = json.loads(data_to_save)
    data = json.dumps(data_dict)

    # Simpan data ke Firebase Realtime Database
    records_ref = db.reference('records')  # Ganti 'records' sesuai dengan nama folder Anda di database
    new_record_ref = records_ref.push(data)

    response_data = {"record_id": new_record_ref.key}
    print(response_data)
    content = str(response_data).encode()
    app.put_data(name, content=content, freshness_period=5000)
    print(f'<< D: {Name.to_str(name)}')
    print(MetaInfo(freshness_period=10000))
    print(f'Content: (size: {len(content)})')
    response_data = {"record_id": new_record_ref.key}
    print('')

    # # Lakukan pemrosesan data di sini (misalnya menyimpan data ke database atau melakukan tindakan lainnya)
    # print(data)
    # return jsonify({"message": "Data berhasil diterima di server backend Python."})

if __name__ == '__main__':
    app.run_forever()

# id		name
# nopasien	noPasien
# nama		nama
# umur		umur
# bmi		bmi
# heartrate	heartrate
# height		height
# weight		weight

{"noPasien":"75", "nama":"Radara", "umur": "35", "bmi": "25", "heartrate": "60", "height": "158", "weight": "60"}