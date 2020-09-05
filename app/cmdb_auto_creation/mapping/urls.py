from django.urls import path

from . import views

app_name = 'mapping'

urlpatterns = [
    path('', views.mapping_setup, name='mapping_setup'),
    path('cmdb_setup', views.cmdb_setup, name='cmdb_setup'),
    path('ci_types', views.ci_types, name='ci_types'),
    path('process_cmdb_setup', views.process_cmdb_setup, name='process_cmdb_setup'),
    # path('vault_password/', views.vault_password, name='vault_password'),
]
