from django.urls import path
from . import views
from django.conf.urls.static import static, settings


urlpatterns = [
    path('generate_histogram/', views.generate_histogram, name='generate_histogram'),
    path('', views.index, name="index"),
    path('update-table/', views.update_table, name='update_table'),
    path('stat_analysis/', views.stat_analysis, name='stat_analysis'),
    path('correlation/', views.correlation, name='correlation'),
    path('betting_strategie/', views.betting_strategie, name='betting_strategie'),
    path('KPI_creation/', views.KPI_creation, name='KPI_creation'),
    path('all_games/', views.all_games, name='all_games'),
    path('generate_games/', views.generate_games, name='generate_games'),
    path('generate_correl/', views.generate_correl, name='generate_correl'),
    path('basic_table/', views.basic_table, name='basic_table'),
    
]

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)