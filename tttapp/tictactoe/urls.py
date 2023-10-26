from django.urls import path
from . import views

urlpatterns = [
    path('create-game/', views.create_game, name='create_game'),
    path('submit-move/<int:game_id>/', views.submit_move, name='submit_move'),
    path('list-games/', views.list_games, name='list_games'),
    path('retrieve-game/<int:game_id>/', views.retrieve_game, name='retrieve_game'),
    path('delete-game/<int:game_id>/', views.delete_game, name='delete_game'),
]
