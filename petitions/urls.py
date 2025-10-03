from django.urls import path
from . import views

app_name = 'petitions'
urlpatterns = [
    path('', views.PetitionListView.as_view(), name='list'),
    path('create/', views.PetitionCreateView.as_view(), name='create'),
    path('create/movie/<int:movie_id>/', views.PetitionCreateView.as_view(), name='create_for_movie'),
    path('<int:pk>/', views.PetitionDetailView.as_view(), name='detail'),
    path('<int:pk>/vote/<str:action>/', views.vote, name='vote'),
]