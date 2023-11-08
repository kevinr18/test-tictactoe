# tictactoe/serializers.py
from rest_framework import serializers
from .models import Game, GameLog
from tictactoe_users.serializers import UserSerializer


class GameSerializer(serializers.ModelSerializer):
    # boards_row: Es solo para visualizar mejor el tablero. 
    board_row_1 = serializers.SerializerMethodField()
    board_row_2 = serializers.SerializerMethodField()
    board_row_3 = serializers.SerializerMethodField()

    def get_board_row_1(self, obj):
        # Obtenemos los primeros 3 caracteres de 'board'
        return obj.board[:3]

    def get_board_row_2(self, obj):
        # Obtenemos los caracteres 3 al 5 de 'board'
        return obj.board[3:6]
    
    def get_board_row_3(self, obj):
        # Obtenemos los caracteres 3 al 5 de 'board'
        return obj.board[6:]
    
    class Meta:
        model = Game
        fields = '__all__'


class GameLogSerializer(serializers.ModelSerializer):
    player = UserSerializer(read_only=True)
    class Meta:
        model = GameLog
        fields = ('player', 'move', 'date')