from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import src.apps.courses.views as courses_view

urlpatterns = [
    path('ad/', admin.site.urls),
    path('admin/courses/', courses_view.course_list, name='course_list'),
    path('', include('admin_soft.urls')),
    path('quiz/', include('src.apps.quiz.urls')),
    path('account/', include('src.apps.userAuth.urls')),
    path('course/', include('src.apps.courses.urls')),
    path('courses/', courses_view.published_course_list, name='published_course_list')
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
