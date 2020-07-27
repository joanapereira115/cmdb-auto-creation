from django.urls import path

from . import views

app_name = 'discovery'

urlpatterns = [
    path('', views.vault_setup, name='vault_setup'),
    path('vault_password/', views.vault_password, name='vault_password'),
    path('range/', views.range, name='range'),
    path('handle_range/', views.handle_range, name='handle_range'),
    path('primary_discovery/', views.primary_discovery, name='primary_discovery'),
    path('basic_discovery/', views.basic_discovery, name='basic_discovery'),
    # path('vaultCreation/', views.vaultCreation, name='vaultCreation'),
    
]
