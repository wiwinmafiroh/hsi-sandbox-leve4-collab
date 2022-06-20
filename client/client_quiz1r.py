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
  username = input('Masukkan NIP: ').upper()
  password = pwinput("Masukkan Password: ")
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
    print("Login Berhasil!")
    print("Selamat Datang, {}\n".format(peserta_nama_lengkap))
    
  else:
    print("NIP atau Password Salah!\n")
    input_login()

def check_evaluasi(peserta_id):
  url = 'http://localhost:8000/check_evaluasi'
  payload = {'peserta_id': peserta_id}
  r = requests.get(url, params=payload)
  res = json.loads(r.text)
  # print(res)
  
  if res['status'] == False:
    print("SI000.EHO01")
    print("-----------------------------------------------------------------------")
    print("Jumlah Soal: 2")
    print("-----------------------------------------------------------------------")
    print("Lembar evaluasi sudah siap!\n")
    
    pilih_kerjakan = input("Kerjakan (y/n)? ")
    
    if pilih_kerjakan.lower() == "n":
      exit()
      
    print(" ")
    
  else:
    print("Evaluasi Harian Sudah Dikerjakan!")
    exit()
    
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
  print("----------------- Evaluasi Harian Selesai ----------------------------")
  print("Total Nilai Anda: {}".format(nilai_akhir))
  print("----------------- Tetap Semangat, dan Terus Belajar! -----------------")
  
def arsipnilai_client(peserta_id):
    # print(nip + " / " +peserta_nama_lengkap)
    print(" / " +peserta_nama_lengkap)
    
    url_arsipniai_client = 'http://localhost:8000/arsipniai_client'
    param_arsipnilai_c = {'peserta_id':peserta_id}
    r_arsipnilai_c = requests.post(url_arsipniai_client, json=param_arsipnilai_c)
    json_arsipnilai_c = json.loads(r_arsipnilai_c.text)
    print(json_arsipnilai_c.get("message"))

    if json_arsipnilai_c.get("is_exam") == 1:
        time.sleep(1)
        print("\n------------------------------------------------")
        print("\n--------ARSIP NILAI EVALUASI HARIAN KE-1--------\n")
        print("------------------------------------------------")
        time.sleep(1)
        
        hasileval = json_arsipnilai_c.get("hasileval")
        # duasoal = json_arsipnilai_c.get("duasoal")
        # duasoal = duasoal[0]
        pertanyaan = json_arsipnilai_c.get("pertanyaan")
        kj = json_arsipnilai_c.get("kunci_jawaban")
        textkj = json_arsipnilai_c.get("textkj")
        textjawaban = json_arsipnilai_c.get("textjawaban")

        for a in range(2):

            # soal = duasoal[a]
            # pilihan_a = soal.get("pilihan_a")
            # print(pilihan_a)
            
            # pilihan_c = soal.get("pilihan_a")
            # print(pilihan_c)

            arsipnilai = hasileval[a]
            jwb = arsipnilai.get("jawaban")
            # if jwb == "C":
            #   txt = pilihan_c
            # txt = arsipnilai.get("textjawaban")
            stt = arsipnilai.get("status")
            # soalcoba = arsipnilai.get("pertanyaan")
            # print("nyoba dulu yaaa " +str(soalcoba))

            
            print(f"\n{a+1}. {pertanyaan[a]} \n Jawaban anda : {jwb.lower()}. {textjawaban[a]} --> {stt}")
            if stt == "SALAH":
                print(f"\n Jawaban yang benar adalah : {kj[a].lower()}. {textkj[a]}")
            # print("\Nilai : "+str(hasileval[a].get("nilai"))+"\n")
            print("\n----------------------------------------------------")
                
        print("\nTotal Nilai : "+str(hasileval[0].get("nilai")+hasileval[1].get("nilai"))+"\n")
    
    # proses()
    time.sleep(2)

# evaluasi_harian()
def pilihan_menu():
    
    os.system("cls")
    # print(pesanlogin)
    while True:
        print("\nPilihan Menu : \n")
        print("1. Evaluasi\n2. Arsip Nilai\n3. Keluar")
        time.sleep(1)
        menu = input("\nMasukkan pilihan menu anda (1/2/3) : ")
        if menu == "1":
            os.system("cls")
            # check_isexam()
            # menu_evaluasi()
        elif menu == "2":
            os.system("cls")
            arsipnilai_client(peserta_id)
            print("\n")
        elif menu == "3":
            print("\n--------- Terimakasih telah mengakses aplikasi ini ---------")
            time.sleep(1)
            quit()
        else:
            print("\Inputan anda salah\n")
            time.sleep(1)
            pilihan_menu()

# main menu()
# login()
input_login()
pilihan_menu()