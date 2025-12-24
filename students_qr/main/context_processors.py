def user_permissions(request):
    """
    Добавляет переменные прав пользователя в контекст шаблонов
    """
    return {
        'is_admin': request.user.is_authenticated and request.user.is_staff,
        'is_superuser': request.user.is_authenticated and request.user.is_superuser,
    }