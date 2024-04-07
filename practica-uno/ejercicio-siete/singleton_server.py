from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class Game:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.games = []
        return cls._instance

    def create_game(self, player_element):
        game_id = len(self.games) + 1
        server_element = random.choice(["piedra", "papel", "tijera"])
        result = get_game_result(player_element, server_element)
        game_data = {
            "id": game_id,
            "elemento": player_element,
            "elemento_servidor": server_element,
            "resultado": result
        }
        self.games.append(game_data)
        return game_data

    def list_games(self, result=None):
        if result:
            return [game for game in self.games if game["resultado"] == result]
        return self.games

def get_game_result(player_element, server_element):
    if player_element == server_element:
        return "empate"
    elif (player_element == "piedra" and server_element == "tijera") or \
         (player_element == "tijera" and server_element == "papel") or \
         (player_element == "papel" and server_element == "piedra"):
        return "gano"
    else:
        return "perdio"

class GameHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/partidas":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            player_element = json.loads(post_data.decode("utf-8"))["elemento"]
            game_data = game.create_game(player_element)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/partidas":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            games = game.list_games()
            self.wfile.write(json.dumps(games).encode("utf-8"))
        elif self.path == "/partidas?resultado=ganó":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            games = game.list_games(result="ganó")
            self.wfile.write(json.dumps(games).encode("utf-8"))
        elif self.path == "/partidas?resultado=perdió":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            games = game.list_games(result="perdió")
            self.wfile.write(json.dumps(games).encode("utf-8"))
        elif self.path == "/partidas?resultado=empate":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            games = game.list_games(result="empate")
            self.wfile.write(json.dumps(games).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GameHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    game = Game()
    run_server()
