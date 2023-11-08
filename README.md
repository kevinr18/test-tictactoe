
# TicTacToe o Tres en raya Juego.
###### __Autor: Kevin Rodriguez Duarte__
Backend en Django rest framework, para el juego de “Tic-Tac-Toe”  el cual Permite jugar una partida completa. 
Se utilizo como BD Sqlite3 el cual viene por defecto con la versión de Django a instalar, se utilizo para el guardado de las tablas y la persistencia de datos. 

## Instalación

### Versiones utilizadas:
- Python [3.11.6](https://www.python.org/downloads/release/python-3116/).
- Django 4.2.7
- Djangorestframework 3.14.0

### Como crear un entorno virtual usando [virtualenv](https://virtualenv.pypa.io/en/latest/)
```bash
# Install virtualenv
pip install virtualenv

# Create virtualenv
virtualenv -p python3.11.6 "tictatoe_env"

# Activate virtual environment
source atcli_env/bin/activate

# Disable virtual environment
(tictatoe_env) deactivate
```
### Instalación de dependencias.
```bash
# Desde la ruta raiz.
(tictatoe_env)	pip install -r requirements.txt
```

### Primeros pasos:
- Primero debemos ejecutar las migraciones para crear nuestra BD en SQLite3, nos ubicamos en la ruta del proyecto y ejecutamos con nuestro entorno activado:
```bash
(tictatoe_env)	python manage.py  migrate
```
- Ponemos en marcha nuestra aplicación en modo local:
```bash
(tictatoe_env) python manage.py runserver
```
Ya con el servidor activado podemos empezar a realizar solicitudes http ya sea por cualquier navegador, postman o via curl/wget.

### Ruta de los endpoints y funcionalidades:
#### - App Login:
- __Create User__
Crea un usuario o jugador para la aplicación:
	 - Metodo Post:  
		 - __URL:__  
		http://localhost:8000/api/v1/users/
		- __body:__  
		{"username":  "player1",  "password":  "player"}
		- __Response:__  
		{"token":  "699b8ee46510ce1fc53503d7f270ad90d6629d64"}

- __Login User:__
	Inicias sesión con el "username" y "password" para proporcionar un token.
	- Metodo Post:
		- __URL:__  
		http://localhost:8000/api/v1/login/
		- __body:__  
		{"username":  "player1",  "password":  "player"}
		- __Response:__  
		{"token":  "699b8ee46510ce1fc53503d7f270ad90d6629d64"}

- __Logout__ (Requiere autenticación):
	Cierras sesión del usuario, eliminando el token.
	- Metodo Get:
		- __Header:__  
		key= "Authorization"  
		value="Token 20be367e924edfd3c4a9e9ca2694583d8cdb3ed4" 
		- __URL:__  
		http://localhost:8000/api/v1/logout/
		- __Response:__  
		{"message":  "Cierre de sesión exitoso. El token ha sido eliminado."}

#### -  App tictactoe:
- __Game List__ (Requiere autenticación):
Crea o inicia una partida contra un oponente (se debe crear un oponente previamente).
	- Metodo Post:
		- __Header:__  
		key= "Authorization"  
		value="Token 20be367e924edfd3c4a9e9ca2694583d8cdb3ed4"  
	    	- __URL:__  
		http://localhost:8000/api/v1/games/
		- __body:__  
		{"opposing_player":  "player2"}
		- __Response:__  
		{
			"message":  ""Mensaje":  "La partida ha comenzado",
			"Game": object(Game)
		}

- __Game Details__ (Requiere autenticación):
Visualizas una partida previamente creada.
	- Metodo Get:
		- __Header:__  
		key= "Authorization"  
		value="Token 20be367e924edfd3c4a9e9ca2694583d8cdb3ed4"  
	    	- __URL:__
		http://localhost:8000/api/v1/games/{game_id}/
		- __Response:__
		{
			"Game": object(Game)
		}

- __Make Move__ (Requiere autenticación):
Realiza un movimiento el jugador autenticado (posiciones validas: del 0 al 8: donde cada posicion equivale a un tablero de tictactoe de 3x3).
	- Metodo Post:
		- __Header:__  
		key= "Authorization"  
		value="Token 20be367e924edfd3c4a9e9ca2694583d8cdb3ed4"  
	    	- __URL:__  
		http://localhost:8000/api/v1/games/{game_id}/make_move/
		- __body:__  
		{"position":  "0"}
		- __Response:__  
		{
			"Game": object(Game)
		}

- __Game Log__:
Se pueden visualizar los movimientos que realizaron los jugadores en un juego especifico (game_id).
	- Metodo Get:
	    	- __URL:__  
		http://localhost:8000/api/v1/games/{game_id}/log/
		- __Response:__  
		{
			"player": object(User),
			"move": 1,
			"date": "2023-11-08T17:54:40.573369Z"
		}
