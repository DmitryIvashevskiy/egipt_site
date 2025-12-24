from django.contrib import admin
from .models import Student, StudentUniversity, Diploma, Certificate

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name_english', 'passport_number', 'birth_date', 'current_status')
    list_filter = ('current_status', 'gender', 'country_of_residence')
    search_fields = ('full_name_english', 'full_name_arabic', 'passport_number')

@admin.register(Diploma)
class DiplomaAdmin(admin.ModelAdmin):
    list_display = ('diploma_type', 'issue_date', 'document_status')
    list_filter = ('diploma_type', 'document_status')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_type', 'issue_date', 'purpose')
    list_filter = ('certificate_type', 'purpose')

admin.site.register(StudentUniversity)
