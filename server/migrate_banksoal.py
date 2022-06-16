import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hsi_sandbox.settings")
import django
django.setup()
from quiz1r.models import *

def insert_banksoal(soal_id, pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, kunci_jawaban):
  # Simpan data
  bank_soal = BankSoal(id=soal_id, pertanyaan=pertanyaan, pilihan_a=pilihan_a, pilihan_b=pilihan_b, pilihan_c=pilihan_c, pilihan_d=pilihan_d, kunci_jawaban=kunci_jawaban)
  bank_soal.save()
  print("Soal dengan ID {} Berhasil Disimpan.".format(soal_id))

def migrate_banksoal():
  with open('csv/banksoal.csv', 'r') as banksoal:
    lines = banksoal.readlines()
    
    for line in lines:
      arr = line.split('|')
      soal_id = arr[0].strip()
      pertanyaan = arr[1].strip()
      pilihan_a = arr[2].strip()
      pilihan_b = arr[3].strip()
      pilihan_c = arr[4].strip()
      pilihan_d = arr[5].strip()
      kunci_jawaban = arr[6].strip()
      
      insert_banksoal(soal_id, pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, kunci_jawaban)
      
migrate_banksoal()