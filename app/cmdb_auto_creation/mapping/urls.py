from django.urls import path

from . import views

app_name = 'mapping'

urlpatterns = [
    path('', views.mapping_setup, name='mapping_setup'),
    path('cmdb_setup', views.cmdb_setup, name='cmdb_setup'),
    path('process_idoit_info', views.process_idoit_info, name='process_idoit_info'),
    path('process_cmdb_data_model', views.process_cmdb_data_model,
         name='process_cmdb_data_model'),
    path('process_app_data_model', views.process_app_data_model,
         name='process_app_data_model'),
    path('loading_mapping', views.loading_mapping,
         name='loading_mapping'),
    path('process_mapping', views.process_mapping,
         name='process_mapping'),

    # path('vault_password/', views.vault_password, name='vault_password'),
]
