# tictactoe/urls.py
from django.urls import path

from .views import (GameListCreate, GameDetail, MakeMove, GameLogList)

urlpatterns = [
    path('games/', GameListCreate.as_view(), name='game-list'),
    path('games/<int:pk>/', GameDetail.as_view(), name='game-detail'),
    path('games/<int:game_id>/make_move/', MakeMove.as_view(), name='make-move'),
    path('games/<int:game_id>/log/', GameLogList.as_view(), name='game-log'),
]