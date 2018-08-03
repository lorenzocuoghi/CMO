from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.main_page),
    url(r'^form/', include('form.urls', namespace='form')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^logout_view/$', views.logout_view, name='logout_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
