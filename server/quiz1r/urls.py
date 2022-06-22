from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('users_json', views.users_json, name='users_json'),
    path('peserta_json', views.peserta_json, name='peserta_json'),
    path('banksoal_json', views.banksoal_json, name='banksoal_json'),
    
    path('login', csrf_exempt(views.login), name='login'),
    path('check_evaluasi', views.check_evaluasi, name='check_evaluasi'),
    path('check_jawaban', csrf_exempt(views.check_jawaban), name='check_jawaban'),
    path('insert_evaluasi', csrf_exempt(views.insert_evaluasi), name='insert_evaluasi'),
    path('insert_nilaiexam', csrf_exempt(views.insert_nilaiexam), name='insert_nilaiexam'),
    path('arsipniai_client', csrf_exempt(views.arsipniai_client), name='arsipniai_client'),
    path('show_rank',views.show_rank, name='show_rank'),
]