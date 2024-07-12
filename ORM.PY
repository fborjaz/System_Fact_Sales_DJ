from django.contrib.auth import get_user_model

def get_user():
    User = get_user_model()
    user = User.objects.get(username='gabriel')
    print(f"Usuario: {user}")
    
    # --permissions-- #
    print(f"Permisos: {user.get_all_permissions()}")
get_user()