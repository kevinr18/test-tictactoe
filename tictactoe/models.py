# tictactoe/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from functools import reduce


class Game(models.Model):
    # Combinación de las posiciones ganadoras en el tablero.
    WINING_COMBINATIONS = [
        (0, 1, 2), (3, 4, 5),
        (6, 7, 8), (0, 3, 6),
        (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    player_x = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player_x')     # Required
    player_o = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player_o')     # Required
    player_turn = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_games') # Required
    board = models.CharField(max_length=9, default=" " * 9)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='won_games')
    winner_combination = models.CharField(max_length=3, null=True, blank=True)
    draw = models.BooleanField(default=False)
    date_started = models.DateTimeField(auto_now_add=True)
    date_ended = models.DateTimeField(null=True, blank=True)

    # Metodo para hacer un movimiento.
    def make_move(self, symbol_make_move, position):
        if 0 <= position < 9 and self.board[position] == " " and not self.winner:
            self.board = self.board[:position] + str(symbol_make_move) + self.board[position + 1:]
            self.check_winner(symbol_make_move)
            
            if not self.winner:
                self.player_turn = self.player_o if symbol_make_move == 'X' else self.player_x
                if " " not in self.board:
                    self.draw = True
            elif " " not in self.board:
                self.date_ended = timezone.now()
            self.save()
    
    # Verificar si existe un ganador en el tablero.
    def check_winner(self, symbol_make_move):
        for combo in self.WINING_COMBINATIONS:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                self.winner = self.player_x if symbol_make_move == 'X' else self.player_o
                self.winner_combination = reduce(lambda a,b: str(a) + str(b), combo)
                self.date_ended = timezone.now()


class GameLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)    # Required
    player = models.ForeignKey(User, on_delete=models.CASCADE)  # Required
    move = models.PositiveSmallIntegerField()                   # Required
    date = models.DateTimeField(auto_now_add=True)