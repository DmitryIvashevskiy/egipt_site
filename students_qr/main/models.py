from django.db import models
from django.core.validators import RegexValidator

class Student(models.Model):
    # Основная информация
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    STATUS_CHOICES = [
        ('studying', 'Обучается'),
        ('graduate', 'Выпускник'),
        ('academic_leave', 'Академ. отпуск'),
        ('expelled', 'Отчислен'),
    ]
    
    # ФИО
    full_name_english = models.CharField(max_length=200, verbose_name="ФИО на английском")
    full_name_arabic = models.CharField(max_length=200, verbose_name="ФИО на арабском")
    
    # Паспортные данные
    passport_number = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name="Номер паспорта"
    )
    
    # Личные данные
    birth_date = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        verbose_name="Пол"
    )
    citizenship = models.CharField(max_length=100, verbose_name="Гражданство")
    country_of_residence = models.CharField(max_length=100, verbose_name="Страна проживания")
    
    # Образовательная информация
    major = models.CharField(max_length=200, verbose_name="Направление подготовки / специальность")
    study_duration = models.PositiveIntegerField(verbose_name="Срок обучения (количество лет)")
    current_status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='studying',
        verbose_name="Текущий статус студента"
    )
    start_date = models.DateField(verbose_name="Дата начала обучения")
    expected_end_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Предполагаемая дата окончания"
    )
    actual_end_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Фактическая дата окончания"
    )
    
    # Контактные данные
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. Максимум 15 цифр."
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        verbose_name="Номер телефона"
    )
    email = models.EmailField(verbose_name="Адрес электронной почты")
    
    # Документы
    passport_scan = models.FileField(
        upload_to='passport_scans/',
        verbose_name="Скан паспорта"
    )
    
    # Методы
    def __str__(self):
        return f"{self.full_name_english} ({self.passport_number})"
    
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"



class StudentUniversity(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='universities')
    university = models.CharField(max_length=200, verbose_name="Университет")
    start_date = models.DateField(verbose_name="Дата начала обучения в вузе")
    end_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Дата окончания обучения в вузе"
    )
    is_current = models.BooleanField(default=False, verbose_name="Текущий университет")
    
    class Meta:
        verbose_name = "Университет студента"
        verbose_name_plural = "Университеты студентов"


class Diploma(models.Model):
    DIPLOMA_TYPES = [
        ('bachelor', 'Бакалавриат'),
        ('master', 'Магистратура'),
        ('phd', 'PhD'),
        ('specialized', 'Специализированная программа'),
    ]
    
    EDUCATION_LEVELS = [
        ('bachelor', 'Бакалавр'),
        ('master', 'Магистр'),
        ('phd', 'Доктор философии'),
        ('specialist', 'Специалист'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Действующий'),
        ('replaced', 'Заменён'),
        ('cancelled', 'Аннулирован'),
    ]
    
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='diplomas',
        verbose_name="Студент"
    )
    
    # Основная информация

    diploma_type = models.CharField(
        max_length=20, 
        choices=DIPLOMA_TYPES,
        verbose_name="Тип диплома"
    )
    
    # Реквизиты диплома
    diploma_number = models.CharField(max_length=50, verbose_name="Номер диплома")
    diploma_series = models.CharField(max_length=50, verbose_name="Серия диплома")
    registration_number = models.CharField(max_length=100, verbose_name="Регистрационный номер")
    issue_date = models.DateField(verbose_name="Дата выдачи")
    
    # Образовательная информация
    major = models.CharField(max_length=200, verbose_name="Направление / специальность")
    education_level = models.CharField(
        max_length=20, 
        choices=EDUCATION_LEVELS,
        verbose_name="Уровень образования"
    )
    issuing_organization = models.CharField(
        max_length=300, 
        verbose_name="Организация / университет выдавший диплом"
    )
    
    # Статус и файл
    document_status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Статус документа"
    )
    diploma_scan = models.FileField(
        upload_to='diploma_scans/',
        verbose_name="Скан диплома",
        null=True, 
        blank=True
    )

    diploma_qr = models.FileField(
        upload_to='diploma_qr/',
        verbose_name="qr диплома",
        null=True, 
        blank=True,
    )
    
    
    def __str__(self):
        return f"Диплом {self.diploma_number}"
    
    class Meta:
        verbose_name = "Диплом"
        verbose_name_plural = "Дипломы"


class Certificate(models.Model):
    CERTIFICATE_TYPES = [
        ('enrollment', 'О зачислении'),
        ('studying', 'Об обучении'),
        ('academic_leave', 'Академ. отпуск'),
        ('completion', 'Об окончании программы'),
        ('transfer', 'О переводе'),
        ('archive', 'Архивная'),
    ]
    
    EDUCATION_LEVELS = [
        ('bachelor', 'Бакалавриат'),
        ('master', 'Магистратура'),
        ('phd', 'PhD'),
        ('specialized', 'Специализированная программа'),
    ]
    
    STUDY_FORMS = [
        ('full_time', 'Очная'),
        ('part_time', 'Заочная'),
        ('mixed', 'Смешанная'),
    ]
    
    PURPOSE_CHOICES = [
        ('university', 'Университет'),
        ('employer', 'Работодатель'),
        ('embassy', 'Посольство'),
        ('migration', 'Миграционные органы'),
        ('other', 'Другое'),
    ]
    
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='certificates',
        verbose_name="Студент"
    )
    
    # Основная информация

    certificate_type = models.CharField(
        max_length=20, 
        choices=CERTIFICATE_TYPES,
        verbose_name="Тип справки"
    )
    
    # Реквизиты справки
    certificate_number = models.CharField(max_length=50, verbose_name="Номер справки")
    issue_date = models.DateField(verbose_name="Дата выдачи")
    issuing_institution = models.CharField(
        max_length=300, 
        verbose_name="Учебное учреждение, выдавшее справку"
    )
    
    # Образовательная информация
    major = models.CharField(max_length=200, verbose_name="Направление / специальность")
    education_level = models.CharField(
        max_length=20, 
        choices=EDUCATION_LEVELS,
        verbose_name="Уровень образования"
    )
    course = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name="Курс обучения"
    )
    study_form = models.CharField(
        max_length=20, 
        choices=STUDY_FORMS,
        verbose_name="Форма обучения"
    )
    
    # Периоды
    study_period_start = models.DateField(verbose_name="Дата начала обучения")
    study_period_end = models.DateField(verbose_name="Дата завершения обучения")
    certificate_validity_period = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Период действия справки"
    )
    
    # Цель выдачи
    purpose = models.CharField(
        max_length=20, 
        choices=PURPOSE_CHOICES,
        verbose_name="Цель выдачи справки"
    )
    
    # Файл
    certificate_scan = models.FileField(
        upload_to='certificate_scans/',
        verbose_name="Скан справки",
        null=True, 
        blank=True
    )

    certificate_qr = models.FileField(
        upload_to='certificate_qr/',
        verbose_name="qr справки",
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return f"Справка {self.certificate_number}"
    
    class Meta:
        verbose_name = "Справка"
        verbose_name_plural = "Справки"

class PaymentReceipt(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='payment_receipts',
        verbose_name="Студент"
    )
    payment_receipt = models.FileField(
        upload_to='payment_receipts/',
        verbose_name="Чек оплаты",
        null=True, 
        blank=True
    )
    upload_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки"
    )
    
    def __str__(self):
        return f"Чек #{self.id} - {self.student.full_name_english}"
    
    class Meta:
        verbose_name = "Чек оплаты"
        verbose_name_plural = "Чеки оплаты"
        ordering = ['-upload_date']

