from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, Certificate, Diploma, PaymentReceipt, StudentUniversity
from .forms import CertificateForm, DiplomaForm, PaymentReceiptForm, StudentForm, StudentUniversityFormSet
from .qr_generator import generate_certificate_qr, generate_diploma_qr


def admin_required(function=None):
    """
    Декоратор для проверки, что пользователь является администратором
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_staff or u.is_superuser),
        login_url='students:login'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

@login_required
def student_list(request):
    students = Student.objects.all().order_by('full_name_english')
    is_admin = request.user.is_staff or request.user.is_superuser
    return render(request, 'students/student_list.html', {
        'students': students,
        'is_admin': is_admin
    })

# @login_required
# def student_detail(request, student_id):
#     student = get_object_or_404(Student, id=student_id)
#     certificates = student.certificates.all()
#     diplomas = student.diplomas.all()
#     return render(request, 'students/student_detail.html', {
#         'student': student,
#         'certificates': certificates,
#         'diplomas': diplomas
#     })


from .models import Student, Certificate, Diploma, PaymentReceipt
from .forms import CertificateForm, DiplomaForm, PaymentReceiptForm

@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    certificates = student.certificates.all()
    diplomas = student.diplomas.all()
    payment_receipts = student.payment_receipts.all()
    
    # Добавляем флаг is_admin в контекст
    is_admin = request.user.is_staff or request.user.is_superuser
    
    if request.method == 'POST' and is_admin:
        form = PaymentReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.student = student
            receipt.save()
            return redirect('students:student_detail', student_id=student.id)
    else:
        form = PaymentReceiptForm()
    
    return render(request, 'students/student_detail.html', {
        'student': student,
        'certificates': certificates,
        'diplomas': diplomas,
        'payment_receipts': payment_receipts,
        'form': form,
        'is_admin': is_admin,
    })

@admin_required
def add_certificate(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.student = student
            certificate.save()
            
            # Генерируем QR-код после сохранения справки
            generate_certificate_qr(certificate, request)
            
            return redirect('students:student_detail', student_id=student.id)
    else:
        form = CertificateForm()
    
    return render(request, 'students/add_certificate.html', {
        'form': form,
        'student': student
    })

@admin_required
def add_diploma(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = DiplomaForm(request.POST, request.FILES)
        if form.is_valid():
            diploma = form.save(commit=False)
            diploma.student = student
            diploma.save()
            
            # Генерируем QR-код после сохранения диплома
            generate_diploma_qr(diploma, request)
            
            return redirect('students:student_detail', student_id=student.id)
    else:
        form = DiplomaForm()
    
    return render(request, 'students/add_diploma.html', {
        'form': form,
        'student': student
    })

@login_required
def certificate_detail(request, student_id, certificate_id):
    student = get_object_or_404(Student, id=student_id)
    certificate = get_object_or_404(Certificate, id=certificate_id, student=student)
    return render(request, 'students/certificate_detail.html', {
        'certificate': certificate,
        'student': student
    })

@login_required
def diploma_detail(request, student_id, diploma_id):
    student = get_object_or_404(Student, id=student_id)
    diploma = get_object_or_404(Diploma, id=diploma_id, student=student)
    return render(request, 'students/diploma_detail.html', {
        'diploma': diploma,
        'student': student
    })

@login_required
def receipt_detail(request, student_id, receipt_id):
    student = get_object_or_404(Student, id=student_id)
    receipt = get_object_or_404(PaymentReceipt, id=receipt_id, student=student)
    return render(request, 'students/receipt_detail.html', {
        'receipt': receipt,
        'student': student
    })


@admin_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        university_formset = StudentUniversityFormSet(request.POST, request.FILES)
        
        if form.is_valid():
            student = form.save()
            
            # Сохраняем университеты
            university_formset = StudentUniversityFormSet(request.POST, request.FILES, instance=student)
            if university_formset.is_valid():
                university_formset.save()
            
            return redirect('students:student_detail', student_id=student.id)
    else:
        form = StudentForm()
        university_formset = StudentUniversityFormSet()
    
    return render(request, 'students/add_student.html', {
        'form': form,
        'university_formset': university_formset,
    })