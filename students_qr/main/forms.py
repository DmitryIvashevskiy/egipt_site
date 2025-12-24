# students/forms.py
from django import forms
from .models import Student, Certificate, Diploma, PaymentReceipt, StudentUniversity
from django.forms import inlineformset_factory


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = [
            'certificate_type',
            'certificate_number',
            'issue_date',
            'issuing_institution',
            'major',
            'education_level',
            'course',
            'study_form',
            'study_period_start',
            'study_period_end',
            'certificate_validity_period',
            'purpose',
            'certificate_scan'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'study_period_start': forms.DateInput(attrs={'type': 'date'}),
            'study_period_end': forms.DateInput(attrs={'type': 'date'}),
            'certificate_validity_period': forms.DateInput(attrs={'type': 'date'}),
            'certificate_type': forms.Select(attrs={'class': 'form-select'}),
            'education_level': forms.Select(attrs={'class': 'form-select'}),
            'study_form': forms.Select(attrs={'class': 'form-select'}),
            'purpose': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'certificate_type': 'Тип справки',
            'certificate_number': 'Номер справки',
            'issue_date': 'Дата выдачи',
            'issuing_institution': 'Учебное учреждение',
            'major': 'Направление / специальность',
            'education_level': 'Уровень образования',
            'course': 'Курс обучения',
            'study_form': 'Форма обучения',
            'study_period_start': 'Дата начала обучения',
            'study_period_end': 'Дата завершения обучения',
            'certificate_validity_period': 'Период действия справки',
            'purpose': 'Цель выдачи справки',
            'certificate_scan': 'Скан справки'
        }

class DiplomaForm(forms.ModelForm):
    class Meta:
        model = Diploma
        fields = [
            'diploma_type',
            'diploma_number',
            'diploma_series',
            'registration_number',
            'issue_date',
            'major',
            'education_level',
            'issuing_organization',
            'document_status',
            'diploma_scan'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'diploma_type': forms.Select(attrs={'class': 'form-select'}),
            'education_level': forms.Select(attrs={'class': 'form-select'}),
            'document_status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'diploma_type': 'Тип диплома',
            'diploma_number': 'Номер диплома',
            'diploma_series': 'Серия диплома',
            'registration_number': 'Регистрационный номер',
            'issue_date': 'Дата выдачи',
            'major': 'Направление / специальность',
            'education_level': 'Уровень образования',
            'issuing_organization': 'Организация / университет',
            'document_status': 'Статус документа',
            'diploma_scan': 'Скан диплома'
        }

class PaymentReceiptForm(forms.ModelForm):
    class Meta:
        model = PaymentReceipt
        fields = ['payment_receipt']
        widgets = {
            'payment_receipt': forms.ClearableFileInput(attrs={
                'accept': 'image/*,.pdf,.jpg,.jpeg,.png',
            })
        }
        labels = {
            'payment_receipt': 'Файл чека'
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'full_name_english',
            'full_name_arabic',
            'passport_number',
            'birth_date',
            'gender',
            'citizenship',
            'country_of_residence',
            'major',
            'study_duration',
            'current_status',
            'start_date',
            'expected_end_date',
            'actual_end_date',
            'phone_number',
            'email',
            'passport_scan',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_end_date': forms.DateInput(attrs={'type': 'date'}),
            'actual_end_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'current_status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'full_name_english': 'ФИО на английском *',
            'full_name_arabic': 'ФИО на арабском *',
            'passport_number': 'Номер паспорта *',
            'birth_date': 'Дата рождения *',
            'gender': 'Пол *',
            'citizenship': 'Гражданство *',
            'country_of_residence': 'Страна проживания *',
            'major': 'Направление подготовки / специальность *',
            'study_duration': 'Срок обучения (количество лет) *',
            'current_status': 'Текущий статус студента *',
            'start_date': 'Дата начала обучения *',
            'expected_end_date': 'Предполагаемая дата окончания',
            'actual_end_date': 'Фактическая дата окончания',
            'phone_number': 'Номер телефона *',
            'email': 'Адрес электронной почты *',
            'passport_scan': 'Скан паспорта *',
        }

class StudentUniversityForm(forms.ModelForm):
    class Meta:
        model = StudentUniversity
        fields = ['university', 'start_date', 'end_date', 'is_current']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'university': 'Университет *',
            'start_date': 'Дата начала обучения *',
            'end_date': 'Дата окончания обучения',
            'is_current': 'Текущий университет',
        }

# Создаем formset для университетов
StudentUniversityFormSet = inlineformset_factory(
    Student,
    StudentUniversity,
    form=StudentUniversityForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)