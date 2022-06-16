from django.contrib import admin
from .models import *

# Register your models here.
class PesertaDisplay(admin.ModelAdmin):
  list_display = ('user', 'nip', 'nama_lengkap', 'alamat', 'no_hp')
admin.site.register(Peserta, PesertaDisplay)

class BankSoalDisplay(admin.ModelAdmin):
  list_display = ('pertanyaan', 'pilihan_a', 'pilihan_b', 'pilihan_c', 'pilihan_d', 'kunci_jawaban')
admin.site.register(BankSoal, BankSoalDisplay)

class HasilEvaluasiDisplay(admin.ModelAdmin):
  list_display = ('peserta', 'lembar_evaluasi', 'bank_soal', 'jawaban', 'status', 'nilai')
admin.site.register(HasilEvaluasi, HasilEvaluasiDisplay)

class NilaiEvaluasiDisplay(admin.ModelAdmin):
  list_display = ('peserta', 'total_nilai')
admin.site.register(NilaiEvaluasi, NilaiEvaluasiDisplay)