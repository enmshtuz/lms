from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_soft.urls')),
    path('quiz/', include('src.apps.quiz.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    path('account/', include('src.apps.userAuth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT,)