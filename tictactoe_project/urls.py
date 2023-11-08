from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('tictactoe.urls')),  # Incluye las URLs de la aplicación 'tictactoe'
    path('api/v1/', include('tictactoe_users.urls')) # Incluye las URLs de la aplicación 'tictactoe_users'
    # Otras rutas de tu proyecto aquí
]