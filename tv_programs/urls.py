from django.urls import path
from . import views

app_name = "tv"
urlpatterns = [
    path('', views.tv_schedule, name='tv_schedule'),
    path('<int:id>/', views.channel_schedule, name='channel_schedule'),
    path('tv_program/create/', views.tv_program_create, name='tv_program_create'),
    path('tv_program/create/<int:id>', views.tv_program_create, name='tv_program_create'),
    path('tv_program/update/<int:id>', views.tv_program_update, name='tv_program_update'),
    path('tv_program/delete/<int:id>', views.tv_program_delete, name='tv_program_delete'),
    path('tv_channel/delete/<int:id>', views.tv_channel_delete, name='tv_channel_delete'),
    path('tv_channel/create/', views.tv_channel_create, name='tv_channel_create'),
    path('tv_channel/update/<int:id>', views.tv_channel_update, name='tv_channel_update'),
    path('tv_channel/autocomplete/',
         views.TVChannelAutocomplete.as_view(), name='tv_channel_autocomplete'),
]