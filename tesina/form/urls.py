from django.conf.urls import url
from . import views

app_name = 'form'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<document_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^new/$', views.new, name='new'),
    url(r'^(?P<pk>[0-9]+)/submit/$', views.SubmitView.as_view(), name='submit'),
    url(r'^(?P<document_id>[0-9]+)/pdf/$', views.create_pdf, name='create_pdf'),
    url(r'^(?P<document_id>[0-9]+)/iscrizioni/$', views.registrations, name='registrations'),
    url(r'^(?P<document_id>[0-9]+)/export_xlsx/$', views.export_xlsx, name='export_xlsx'),
    url(r'^(?P<document_id>[0-9]+)/export_csv/$', views.export_csv, name='export_csv'),
    url(r'^(?P<document_id>[0-9]+)/export_xls/$', views.export_xls, name='export_xls'),
    url(r'^(?P<document_id>[0-9]+)/edit/$', views.edit, name='edit'),
]
