from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add-student/', views.add_student, name='add_student'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student/<int:student_id>/add-certificate/', views.add_certificate, name='add_certificate'),
    path('student/<int:student_id>/add-diploma/', views.add_diploma, name='add_diploma'),
    path('student/<int:student_id>/certificate/<int:certificate_id>/', views.certificate_detail, name='certificate_detail'),
    path('student/<int:student_id>/diploma/<int:diploma_id>/', views.diploma_detail, name='diploma_detail'),
    path('student/<int:student_id>/receipt/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
]

