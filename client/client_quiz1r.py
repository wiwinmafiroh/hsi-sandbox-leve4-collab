import requests
import json
import time
import os

from pwinput import pwinput

def evaluasi_harian():
  ##### QUIZ #####
  # Check Evaluasi Sudah Dikerjakan/Belum
  check_evaluasi(peserta_id)
  
  # Bank Soal
  url_banksoal = 'http://localhost:8000/banksoal_json'
  r = requests.get(url_banksoal)
  res = json.loads(r.text)
  no = 0
  total_nilai = 0
  
  for banksoal in res:
    no += 1
    banksoal_id = banksoal['id']
    pertanyaan = banksoal['pertanyaan']
    pilihan_a = banksoal['pilihan_a']
    pilihan_b = banksoal['pilihan_b']
    pilihan_c = banksoal['pilihan_c']
    pilihan_d = banksoal['pilihan_d']
    
    print("{}. {} ...".format(no, pertanyaan))
    print("{}A. {}".format(" " * 3, pilihan_a))
    print("{}B. {}".format(" " * 3, pilihan_b))
    print("{}C. {}".format(" " * 3, pilihan_c))
    print("{}D. {}".format(" " * 3, pilihan_d))
    
    jawaban_user = input("{}Masukkan Pilihan Jawaban Anda (A/B/C/D): ".format(" " * 3))
    while jawaban_user.upper() not in ['A', 'B', 'C', 'D']:
      print("{}Pilihan Jawaban Tidak Valid!".format(" " * 3))
      jawaban_user = input("{}Masukkan Pilihan Jawaban Anda (A/B/C/D): ".format(" " * 3))
  
    # Check Jawaban User
    check_jawaban(banksoal_id, jawaban_user)
    
    # Total Nilai
    total_nilai += nilai
    print(" ")
    
    # Insert Hasil Evaluasi
    insert_evaluasi(peserta_id, banksoal_id, jawaban_user, status, nilai)
  
  # Insert Total Nilai Evaluasi
  insert_nilaiexam(peserta_id, total_nilai)
  
  # Bottom Section
  nilai_akhir(total_nilai)
  
  ##### SELESAI QUIZ #####

def input_login():
  ##### LOGIN #####
  username = input('\n  Masukkan NIP : ').upper()
  password = pwinput("  Masukkan Password : ")
  login(username, password)

def login(username, password):
  global peserta_id, peserta_nama_lengkap
  
  url = 'http://localhost:8000/login'
  payload = {'username': username, 'password': password}
  r = requests.post(url, json=payload)
  res = json.loads(r.text)
  # print(res)
  
  if res['status'] == True:
    peserta_id = res['peserta']['id']
    peserta_nama_lengkap = res['peserta']['nama_lengkap']
    print("\n{}Login Berhasil!".format(" " * 2))
    print("\n{}Selamat Datang , {} , di HSI Sandbox".format(" " * 2, peserta_nama_lengkap))
    time.sleep(2)
    
  else:
    print("{}NIP atau Password Salah!\n".format(" " * 2))
    input_login()

def check_evaluasi(peserta_id):
  url = 'http://localhost:8000/check_evaluasi'
  payload = {'peserta_id': peserta_id}
  r = requests.get(url, params=payload)
  res = json.loads(r.text)
  # print(res)
  
  if res['status'] == False:
    print("\n{}HSI Sandbox, {}\n".format(" " * 2, peserta_nama_lengkap))
    print("{}SI000.EHO01".format(" " * 2))
    print("{}-----------------------------------------------------------------------".format(" " * 2))
    print("{}Jumlah Soal: 2")
    print("{}-----------------------------------------------------------------------".format(" " * 2))
    print("{}Lembar evaluasi sudah siap!\n".format(" " * 2))
    
    pilih_kerjakan = input("{}Kerjakan (y/n)? ".format(" " * 2))
    
    if pilih_kerjakan.lower() == "n":
      pilihan_menu()
      
    print(" ")
    
  else:
    print("\n{}HSI Sandbox, {}\n".format(" " * 2, peserta_nama_lengkap))
    time.sleep(2)
    print("\n{}Evaluasi Harian Sudah Dikerjakan!".format(" " * 2))
    time.sleep(2)
    pilihan_menu()
    
def check_jawaban(banksoal_id, jawaban_user):
  global status, nilai
  
  url = 'http://localhost:8000/check_jawaban'
  payload = {'banksoal_id': banksoal_id, 'jawaban_user': jawaban_user}
  r = requests.post(url, json=payload)
  res = json.loads(r.text)
  # print(res)
  
  status = res['status']
  nilai = res['nilai']
  
  if res['status'] == "Benar":
    print("{}Alhamdulillaah, Jawaban Anda Benar!".format(" " * 3))
    print("{}Nilai Anda: {}".format(" " * 3, nilai))
    
  else:
    kunci_jawaban = res['kunci_jawaban']
    print("{}Maaf, Jawaban Anda Salah!".format(" " * 3))
    print("{}Jawaban Benar Adalah: {}".format(" " * 3, kunci_jawaban))
    print("{}Nilai Anda: {}".format(" " * 3, nilai))
    
def insert_evaluasi(peserta, bank_soal, jawaban, status, nilai):
  url = 'http://localhost:8000/insert_evaluasi'
  payload = {
    'peserta': peserta,
    'bank_soal': bank_soal,
    'jawaban': jawaban,
    'status': status,
    'nilai': nilai
  }
  r = requests.post(url, json=payload)
  
def insert_nilaiexam(peserta, total_nilai):
  url = 'http://localhost:8000/insert_nilaiexam'
  payload = {
    'peserta': peserta,
    'total_nilai': total_nilai
  }
  r = requests.post(url, json=payload)

def nilai_akhir(nilai_akhir):
  print("\n{}----------------- Evaluasi Harian Selesai ----------------------------".format(" " * 2))
  print("\n  Total Nilai Anda: {}".format(nilai_akhir))
  print("\n{}----------------- Tetap Semangat, dan Terus Belajar! -----------------".format(" " * 2))
  
def arsipnilai_client(peserta_id):
    # print(nip + " / " +peserta_nama_lengkap)
    print("\n{}HSI Sandbox / {} ".format(" " * 2, peserta_nama_lengkap))
    
    url_arsipniai_client = 'http://localhost:8000/arsipniai_client'
    param_arsipnilai_c = {'peserta_id':peserta_id}
    r_arsipnilai_c = requests.post(url_arsipniai_client, json=param_arsipnilai_c)
    json_arsipnilai_c = json.loads(r_arsipnilai_c.text)
    print("{} {}".format(" " * 2, json_arsipnilai_c.get("message")))

    if json_arsipnilai_c.get("is_exam") == 1:
        time.sleep(1)

        print("\n{}------------------------------------------------".format(" " * 2))
        print("\n{}--------ARSIP NILAI EVALUASI HARIAN KE-1--------".format(" " * 2))
        print("\n{}------------------------------------------------".format(" " * 2))
        time.sleep(1)
        
        hasileval = json_arsipnilai_c.get("hasileval")
        pertanyaan = json_arsipnilai_c.get("pertanyaan")
        kj = json_arsipnilai_c.get("kunci_jawaban")
        textkj = json_arsipnilai_c.get("textkj")
        textjawaban = json_arsipnilai_c.get("textjawaban")

        for a in range(2):

            arsipnilai = hasileval[a]
            jwb = arsipnilai.get("jawaban")
            stt = arsipnilai.get("status")
            
            print(f"\n  {a+1}. {pertanyaan[a]} ")
            print(f"\n  Jawaban anda : \n  {jwb.lower()}. {textjawaban[a]}")
            print(f"  --> {stt}")
            if stt == "Salah":
                print("\n{}Jawaban yang benar : \n  {}. {}".format(" " * 2, kj[a].lower(), textkj[a]))
            print("\n{}----------------------------------------------------".format(" " * 2))
                
        print("\n  Total Nilai : "+str(hasileval[0].get("nilai")+hasileval[1].get("nilai"))+"\n")
        print("\n{}----------------- Tetap Semangat, dan Terus Belajar! -----------------".format(" " * 2))
    
    # proses()
    time.sleep(2)

def peringkat():
  print("peringkat")

def pilihan_menu():
    
    os.system("cls")
    print("\n{}HSI Sandbox, {}\n".format(" " * 2, peserta_nama_lengkap))

    while True:
        print("\n{}Pilihan Menu : \n".format(" " * 2))
        print("\n{}1. Evaluasi\n{}2. Arsip Nilai\n{}3. Peringkat\n{}4. Keluar".format(" " * 2, " " * 2, " " * 2, " " * 2))
        time.sleep(1)
        menu = input("\n{}Masukkan pilihan menu anda (1/2/3/4) : ".format(" " * 2))
        if menu == "1":
            os.system("cls")
            evaluasi_harian()
        elif menu == "2":
            os.system("cls")
            arsipnilai_client(peserta_id)
            print("\n")
        elif menu == "3":
            peringkat()
        elif menu == "4":
            print("\n{}--------- Terimakasih telah mengakses aplikasi ini ---------".format(" " * 2))
            time.sleep(1)
            quit()
        else:
            print("\n{}Inputan anda salah\n".format(" " * 2))
            time.sleep(1)
            pilihan_menu()

# main menu
print("\n{}--------------------------------------".format(" " * 2))
print("\n{}    L O G I N   A P L I K A S I  H S I\n".format(" " * 2))
print("\n{}--------------------------------------".format(" " * 2))

input_login()
pilihan_menu()