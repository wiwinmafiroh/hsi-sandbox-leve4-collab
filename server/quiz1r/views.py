from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages

from .models import *

import json
import random

# Create your views here.
def users_json(request):
  usq = list(User.objects.values())
  
  return JsonResponse(usq, safe=False)

def peserta_json(request):
  psq = list(Peserta.objects.values())
  
  return JsonResponse(psq, safe=False)

def banksoal_json(request):
  try : #eva
    bsq = list(BankSoal.objects.values())
    bsr = random.sample(bsq, 2)
    status = True #eva 
    context = { #eva
      'bsr' : bsr,#eva
      'status' : status#eva
    }#eva
    
  except :#eva
    status = False#eva
    context = {#eva
      'status' : status#eva
    }#eva
  
  #return JsonResponse(bsr, safe=False) #awal
  return JsonResponse(context, safe=False)#eva
  
def login(request):
  try :
    status = 'error'
    
    if request.method == 'POST':
      data = json.loads(request.body)
      username = data['username'].lower()
      password = data['password']
      
      user = authenticate(request, username=username, password=password)
      
      if user is not None:
        if user.groups.filter(name='admin') :
          status=True
          context = {
            'peserta' : 'admin',
            'status' : status
          }
        else :
          psq = list(Peserta.objects.filter(user=user).values())
          status = True
          context = {
            'peserta': psq[0],
            'status' : status 
          }
      else:
          context = {
            'peserta': '',
            'status' : False 
          }
      return JsonResponse(context, safe=False)
    else:
      context = {
            'peserta': '',
            'status' : False 
          }
      return JsonResponse(context, safe=False)
  except :
    context = {
            'peserta': '',
            'status' : False 
          }
    return JsonResponse(context,safe=False)
    
#eva
def show_rank(request) :
  try : #eva
    rq = NilaiEvaluasi.objects.all().order_by('-total_nilai')
    list_rank=[]
    for rank in rq :
      nip= rank.peserta.nip 
      nama_lengkap= rank.peserta.nama_lengkap 
      total_nilai=rank.total_nilai
      dict={
        'nip' : nip,
        'nama_lengkap' : nama_lengkap,
        'total_nilai' :total_nilai
      }
      list_rank.append(dict)
    if not rq:
      context={
        'status':False
      }
    else:
      # print(list_rank)
      context = { #eva
        'list_rank' : list_rank,#eva
        'status' : True#eva
      }#eva
  except :#eva
    print('masuk server error')
    status = False#eva
    context = {#eva
      'status' : False#eva
    }#eva

  #return JsonResponse(bsr, safe=False) #awal
  return JsonResponse(context, safe=False)#eva


def check_evaluasi(request):
  try:
    if request.method == 'GET':
      peserta_id = request.GET['peserta_id']
      psq = Peserta.objects.get(id=peserta_id)
      heq = HasilEvaluasi.objects.filter(peserta=psq)
      
      if heq.count() > 0:
        status = True
        context = {'status': status}
      else:
        status = False
        context = {'status': status}
  except:
    status = False
    context = {'status': status}
    
  return JsonResponse(context, safe=False)
  
def check_jawaban(request):
  try:
    if request.method == 'POST':
      data = json.loads(request.body)
      bank_soal = data['banksoal_id']
      jawaban_user = data['jawaban_user'].upper()
      
      bsq = BankSoal.objects.get(id=bank_soal)
      
      if jawaban_user == bsq.kunci_jawaban:
        status = "Benar"
        nilai = 2
        context = {
          'status': status, 
          'nilai': nilai,
        }
        
      else:
        status = "Salah"
        kunci_jawaban = bsq.kunci_jawaban
        nilai = 1
        context = {
          'status': status, 
          'kunci_jawaban': kunci_jawaban,
          'nilai': nilai,
        }
  except:
    context={}
    
  return JsonResponse(context, safe=False)
  
def insert_evaluasi(request):
  try:
    if request.method == 'POST':
      data = json.loads(request.body)
      peserta = data['peserta']
      lembar_evaluasi = "EH001"
      bank_soal = data['bank_soal']
      jawaban = data['jawaban'].upper()
      status = data['status']
      nilai = data['nilai']
      
      psq = Peserta.objects.get(id=peserta)
      bsq = BankSoal.objects.get(id=bank_soal)
      
      heq = HasilEvaluasi(peserta=psq, lembar_evaluasi=lembar_evaluasi, bank_soal=bsq, jawaban=jawaban, status=status, nilai=nilai)
      heq.save()
      
      context = {'status': True}
  except:
    context={}

  return JsonResponse(context, safe=False)
  
def insert_nilaiexam(request):
  try:
    if request.method == 'POST':
      data = json.loads(request.body)
      peserta = data['peserta']
      total_nilai = data['total_nilai']
      
      psq = Peserta.objects.get(id=peserta)
      neq = NilaiEvaluasi(peserta=psq, total_nilai=total_nilai)
      neq.save()
      
      context = {'status': True}
  except:
    context={}
  return JsonResponse(context, safe=False)

def arsipniai_client(request):
    context={}
    try:
      if request.method == 'POST':
        data = json.loads(request.body)
        peserta_id = data["peserta_id"]
        hasileval = list(HasilEvaluasi.objects.filter(peserta=peserta_id).values())
        
        id_soal = []
        pertanyaan = []
        kj = []
        textkj = []
        jawaban = []
        textj = []
        for i in range(2):
            
            id_soal.append(hasileval[i].get("bank_soal_id"))
            jawaban.append(hasileval[i].get("jawaban"))

            soal = BankSoal.objects.get(id=id_soal[i])

            if jawaban[i] == "A":
              textj.append(soal.pilihan_a)
            elif jawaban[i] == "B":
              textj.append(soal.pilihan_b)
            elif jawaban[i] == "C":
              textj.append(soal.pilihan_c)
            elif jawaban[i] == "D":
              textj.append(soal.pilihan_d)

            pertanyaan.append(soal.pertanyaan)
            kj.append(soal.kunci_jawaban)
            if kj[i] == "A":
              textkj.append(soal.pilihan_a)
            elif kj[i] == "B":
              textkj.append(soal.pilihan_b)
            elif kj[i] == "C":
              textkj.append(soal.pilihan_c)
            elif kj[i] == "D":
              textkj.append(soal.pilihan_d)

        if not hasileval:
            context={
                'is_exam':0,
                'message':"\n  Anda belum mengerjakan EH 1",
            }   
        else:
            context={
                'pertanyaan':pertanyaan,
                'kunci_jawaban':kj,
                'textkj':textkj,
                'jawaban':jawaban,
                'textjawaban':textj,
                'is_exam':1,
                'hasileval':hasileval,
                'message':("\n  Anda telah mengerjakan EH 1"),
            }
    except:
        context={
            'is_exam':0,
            'message':"\n  Anda belum mengerjakan EH 1",
        }

    return JsonResponse(context, safe=False)

# Wiwin
def login_web(request):
  try:
    if request.method == 'POST':
      username = request.POST['username'].lower()
      password = request.POST['password']
      
      user = authenticate(request, username=username, password=password)
      
      if user is not None:
        if user.groups.filter(name='admin'):
          messages.success(request, 'Anda Berhasil Login!')
          return redirect('dashboard_web')
        else:
          messages.success(request, 'Maaf .. Anda login sebagai Peserta, silakan akses CMD')
          return redirect('login_web')
      else:
        messages.error(request, 'Username atau Password Salah!')
        return redirect('login_web')
  except:
    return redirect('login_web')
  
  return render(request, 'login/login.html')

def logout_web(request):
  logout(request)
  return redirect('login_web')

def dashboard_admin(request):
  username = request.user.username
  jml_peserta = Peserta.objects.count()
  jml_lembar_evaluasi = 1
  jml_soal = BankSoal.objects.count()
  jml_peserta_mengerjakan = NilaiEvaluasi.objects.count()
  
  context = {
    'username': username,
    'jml_peserta': jml_peserta,
    'jml_lembar_evaluasi': jml_lembar_evaluasi,
    'jml_soal': jml_soal,
    'jml_peserta_mengerjakan': jml_peserta_mengerjakan,
  }
  
  return render(request, 'adminhsi/dashboard.html', context)

### Menampilkan Hasil Evaluasi (Novi) ###
def hasil_evaluasi(request):
  hasil_evaluasi = []
  
  try:    
    psq = Peserta.objects.all()
    
    for p in psq:
      hasileval = list(HasilEvaluasi.objects.filter(peserta=p.id))
      nilaieval = list(NilaiEvaluasi.objects.filter(peserta=p.id))      
      hasil_evaluasi.append({
        'peserta':p,
        'hasileval':hasileval,
        'nilaieval':nilaieval,
      })
    
    context = {
      'hasil_evaluasi': hasil_evaluasi,
    }
  except:
    context = {
      'hasil_evaluasi': hasil_evaluasi,
    }

  return render(request, 'adminhsi/hasil_evaluasi.html', context)

### Menampilkan Nilai Peserta Dari Yang Tertinggi (Novi) ######
def peringkat_peserta(request):
  data_peringkat = NilaiEvaluasi.objects.all().order_by('-total_nilai')
  context = {
    'data_peringkat': data_peringkat
  }

  return render(request, 'adminhsi/peringkat_peserta.html', context)