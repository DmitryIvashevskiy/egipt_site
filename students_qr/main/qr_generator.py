# students/qr_generator.py
import qrcode
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
import datetime
import os
from django.conf import settings

def generate_qr_code(link, qr_size=300):
    """
    Генерирует QR-код из ссылки
    
    Args:
        link (str): Ссылка для кодирования в QR-код
        qr_size (int): Размер QR-кода в пикселях
    
    Returns:
        BytesIO: Объект с изображением QR-кода
    """
    # Создаем объект QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Добавляем данные
    qr.add_data(link)
    qr.make(fit=True)
    
    # Создаем изображение
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Изменяем размер если нужно
    if qr_size != 300:
        qr_image = qr_image.resize((qr_size, qr_size))
    
    # Сохраняем в BytesIO
    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer

def add_qr_to_template(template_path, link):
    """
    Добавляет QR-код и дату-время (слитно) на шаблонное изображение
    
    Args:
        template_path (str): Путь к шаблонному изображению
        link (str): Ссылка для QR-кода
    
    Returns:
        BytesIO: Объект с финальным изображением
    """
    # Открываем шаблонное изображение
    template = Image.open(template_path)
    
    # Генерируем QR-код
    qr_buffer = generate_qr_code(link, qr_size=250)
    qr_image = Image.open(qr_buffer)
    
    # Получаем текущую дату и время и объединяем слитно
    current_time = datetime.datetime.now()
    datetime_string = current_time.strftime("%d%m%Y%H%M%S")
    
    # Позиция для QR-кода (центрируем по горизонтали)
    qr_x = (template.width - qr_image.width) // 2
    qr_y = 100  # Отступ сверху
    
    # Вставляем QR-код на шаблон
    template.paste(qr_image, (qr_x, qr_y))
    
    # Добавляем текст с датой-временем
    draw = ImageDraw.Draw(template)
    
    try:
        # Пробуем использовать системный шрифт
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            # Пробуем другой распространенный шрифт
            font = ImageFont.truetype("DejaVuSans.ttf", 24)
        except:
            # Если системные шрифты недоступны, используем стандартный
            font = ImageFont.load_default()
    
    # Рассчитываем позицию для текста (под QR-кодом)
    text_x = (template.width - draw.textlength(datetime_string, font=font)) // 2
    text_y = qr_y + qr_image.height + 20
    
    # Рисуем текст
    draw.text((text_x, text_y), datetime_string, fill="black", font=font)
    
    # Возвращаем BytesIO
    buffer = BytesIO()
    template.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def generate_certificate_qr(certificate, request):
    """
    Генерирует QR-код для справки и сохраняет в модель
    
    Args:
        certificate: Объект справки
        request: HttpRequest для построения абсолютного URL
    """
    try:
        # Создаем абсолютный URL для справки
        certificate_url = request.build_absolute_uri(
            f'/student/{certificate.student.id}/certificate/{certificate.id}/'
        )
        
        # Путь к шаблону
        template_path = os.path.join(settings.MEDIA_ROOT, 'shablon', 'best.png')
        
        # Проверяем существование шаблона
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Шаблон не найден: {template_path}")
        
        # Генерируем изображение с QR-кодом
        qr_image_buffer = add_qr_to_template(template_path, certificate_url)
        
        # Создаем имя файла
        filename = f"certificate_qr_{certificate.certificate_number}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        # Сохраняем в поле модели
        certificate.certificate_qr.save(filename, ContentFile(qr_image_buffer.read()), save=True)
        
        return True
    except Exception as e:
        print(f"Ошибка при генерации QR-кода для справки: {e}")
        return False

def generate_diploma_qr(diploma, request):
    """
    Генерирует QR-код для диплома и сохраняет в модель
    
    Args:
        diploma: Объект диплома
        request: HttpRequest для построения абсолютного URL
    """
    try:
        # Создаем абсолютный URL для диплома
        diploma_url = request.build_absolute_uri(
            f'/student/{diploma.student.id}/diploma/{diploma.id}/'
        )
        
        # Путь к шаблону
        template_path = os.path.join(settings.MEDIA_ROOT, 'shablon', 'best.png')
        
        # Проверяем существование шаблона
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Шаблон не найден: {template_path}")
        
        # Генерируем изображение с QR-кодом
        qr_image_buffer = add_qr_to_template(template_path, diploma_url)
        
        # Создаем имя файла
        filename = f"diploma_qr_{diploma.diploma_number}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        # Сохраняем в поле модели
        diploma.diploma_qr.save(filename, ContentFile(qr_image_buffer.read()), save=True)
        
        return True
    except Exception as e:
        print(f"Ошибка при генерации QR-кода для диплома: {e}")
        return False