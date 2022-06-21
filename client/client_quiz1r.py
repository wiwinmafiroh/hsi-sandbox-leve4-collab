import requests
import json

from pwinput import pwinput

def evaluasi_harian():
  ##### QUIZ #####
  # Check Evaluasi Sudah Dikerjakan/Belum
  check_evaluasi(peserta_id)
  
  # Bank Soal
  url_banksoal = 'http://localhost:8000/banksoal_json'
  r = requests.get(url_banksoal)
  res = json.loads(r.text)
  # cek apakah bank soal ada isinya
  if res['status'] == True : #eva
    no = 0
    total_nilai = 0
      
    for banksoal in res['bsr']:
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
    
    #munculkan data peringkat, nanti masukkan ke menu
    show_rank()
  else : #eva
    print("Data bank soal kosong\n") #eva

def show_rank ():
  url_showrank = 'http://localhost:8000/show_rank'
  r = requests.get(url_showrank)
  res = json.loads(r.text)
  print (res)
  if res['status'] == True :
    no=0
    print("Daftar Peringkat")
    print("-----------------------------------------------------------------------")
    print("No.   Nip             Nama                                   Nilai")
    print("-----------------------------------------------------------------------")
    for rank in res['list_rank']:
      no += 1
      nip = rank['nip']
      nama = rank['nama_lengkap']
      total_nilai= rank['total_nilai']
      print("{}     {}          {}                                 {}".format(no, nip, nama, total_nilai))
  else :
    print("Belum ada data ranking\n") #eva

  

def login(username, password):
  global peserta_id, peserta_nama_lengkap
  
  url = 'http://localhost:8000/login'
  payload = {'username': username, 'password': password}
  r = requests.post(url, json=payload)
  res = json.loads(r.text)
  
  if res['status'] == True:
    if res['peserta'] == 'admin' :
      print ('Maaf.. Anda adalah admin, silakan akses web Admin')
      exit()
    else :  
      peserta_id = res['peserta']['id']
      peserta_nama_lengkap = res['peserta']['nama_lengkap']
      print("Login Berhasil!")
      print("Selamat Datang, {}\n".format(peserta_nama_lengkap))
  elif res['status'] == False:
    print("NIP atau Password Salah!\n")
    username = input("Masukkan NIP: ").upper()
    password = pwinput("Masukkan Password: ")
    return login(username, password)
    
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
  
evaluasi_harian()
