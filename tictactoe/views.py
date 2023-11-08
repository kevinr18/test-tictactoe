# tictactoe/views.py
from django.contrib.auth.models import User

from .models import Game, GameLog
from .serializers import GameSerializer, GameLogSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GameListCreate(APIView):
    """
        Permite crear juegos (Games), apartir de un usuario registrado
        y el username del jugador oponente (opposing_player)
    """
    def post(self, request):
        player_x = request.user
        opposing_player = request.data.get('opposing_player')

        # Validar que el oponente exista o este registrado.
        try:
            player_o = User.objects.get(username=opposing_player)
        except User.DoesNotExist:
            return Response(
                {
                    'Mensaje': f'El usuario ({opposing_player}) no existe,' +\
                    f'o username incorrecto por favor introduzca un username' +
                    f' correcto para el jugador 2'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valida que el (opposing_player) no sea el mismo que el jugador actual.
        if player_x == player_o:
            return Response({
                'Mensaje': f'El jugador 2 debe ser distinto al jugador actual.'
            })
        
        # Validar si existe una partida inciada sin finalizar.
        game_before = (
            Game.objects.filter(player_x=player_x, winner=None, draw=False) |
            Game.objects.filter(player_o=player_x, winner=None, draw=False)
        )
        if game_before.exists():
            game_before_ser = GameSerializer(game_before[0])
            return Response({
                'Mensaje': 'Ya tienes una partida inciada debes finalizarla'+\
                ' para comenzar otra',
                'Game': game_before_ser.data
            })
        
        # Guarda el (game) y se responde al usuario que ha comenzado
        #  la partida
        game = Game(
            player_x=player_x,
            player_o=player_o,
            player_turn=player_x
        )
        game.save()
        serializer = GameSerializer(game)

        return Response({
            'Mensaje':'La partida ha comenzado',
            'Game': serializer.data
        }, status=status.HTTP_201_CREATED)


class GameDetail(APIView):
    def get(self, request, pk):
        """
            Obtiene un (Game) mediante el (id), previamente creado.
        """
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(
                {'Mensaje': f'Game con el id ({pk}) no existe'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def delete(self, request, pk):
        """
            Elimina un (Game) mediante el id.
        """
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(
            {'Registro de tipo (Game), Eliminado'}
            ,status=status.HTTP_204_NO_CONTENT
        )


class MakeMove(APIView):
    """
        Permite realizar movimiento en el (Game) previamente creado,
        siempre que sea el turno del jugador.
    """
    def post(self, request, game_id):
        # valida que el juego exista.
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response(
                {'Mensaje': f'Game con el id ({game_id}) no existe'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        player_make_move = request.user
        position = request.data.get('position')
        symbol_make_move = 'X' if player_make_move == game.player_x else 'O'

        # Validaciones:
        if game.winner:
            return Response(
                {"Mensaje": f"La partida ya ha finalizado, ganador:" +\
                f" {game.winner.username}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
                
        if game.player_turn != player_make_move:
            return Response(
                {"Mensaje": "No es tu turno, es el turno del oponente."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if position not in range(0, 9):
            return Response(
                {"Mensaje": "Debes colocar una posicion válida para el" +\
                " tablero del 0 al 8."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if game.board[position] != " ":
            return Response(
                {"Mensaje": "La posición del movimiento que desea realizar"+\
                " ya esta ocupada."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Realiza la acción de hacer un movimiento.
        game.make_move(symbol_make_move, position)

        # Registro de partidas
        GameLog.objects.create(
            game=game, player=player_make_move, move=position
        )

        # Mensajes de movimientos realizados, victoria o empate.
        if game.winner:
            return Response({
                'Mensaje': '¡Felicidades has ganado!',
                'winner_combination': game.winner_combination
            })
        elif " " not in game.board:
            return Response({
                'Mensaje': '¡Empate!'
            })
        
        return Response({
            'Mensaje': 'Movimiento realizado',
            'board': game.board
        },status=status.HTTP_200_OK)

        
class GameLogList(APIView):
    """
        Ver partidas mediante un (id) de (Game).
    """
    def get(self, request, game_id):
        game_logs = GameLog.objects.filter(game_id=game_id)
        serializer = GameLogSerializer(game_logs, many=True)
        return Response(serializer.data)