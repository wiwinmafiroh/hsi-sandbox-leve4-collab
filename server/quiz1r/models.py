from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Peserta(models.Model):
  user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
  nip = models.CharField(max_length=20)
  nama_lengkap = models.CharField(max_length=100)
  alamat = models.TextField()
  no_hp = models.CharField(max_length=15)
  
  def __str__(self):
    return "{} - {}".format(self.nip, self.nama_lengkap)
  
  class Meta:
    verbose_name_plural = "Peserta"
    
class BankSoal(models.Model):
  opsi = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
  ]
  
  pertanyaan = models.CharField(max_length=200)
  pilihan_a = models.CharField(max_length=200)
  pilihan_b = models.CharField(max_length=200)
  pilihan_c = models.CharField(max_length=200)
  pilihan_d = models.CharField(max_length=200)
  kunci_jawaban = models.CharField(max_length=1, choices=opsi)
  
  def __str__(self):
    return self.pertanyaan
  
  class Meta:
    verbose_name_plural = "Bank Soal"

class HasilEvaluasi(models.Model):
  status = [
    ('Benar', 'Benar'), 
    ('Salah', 'Salah'), 
  ]
  
  peserta = models.ForeignKey(Peserta, on_delete=models.SET_NULL, null=True)
  lembar_evaluasi = models.CharField(max_length=10)
  bank_soal = models.ForeignKey(BankSoal, on_delete=models.SET_NULL, null=True)
  jawaban = models.CharField(max_length=1, choices=BankSoal.opsi)
  status = models.CharField(max_length=5, choices=status)
  nilai = models.IntegerField()
  
  def __str__(self):
    return "{} - {} - {} - {}".format(self.peserta.nama_lengkap, self.lembar_evaluasi, self.bank_soal.pertanyaan, self.nilai)
  
  class Meta:
    verbose_name_plural = "Hasil Evaluasi"
    
class NilaiEvaluasi(models.Model):
  peserta = models.ForeignKey(Peserta, on_delete=models.SET_NULL, null=True)
  total_nilai = models.IntegerField()
  
  def __str__(self):
    return "{} - {}".format(self.peserta.nama_lengkap, self.total_nilai)
  
  class Meta:
    verbose_name_plural = "Nilai Evaluasi"