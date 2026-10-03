from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    """Permite acesso apenas a administradores autenticados (is_staff)."""
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='login',
    )(view_func)
