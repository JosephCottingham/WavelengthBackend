from Wavelength import app
from socketio.server import SocketIOServer

if __name__ == "__main__":
   ws = SocketIOServer(('0.0.0.0', 8000), app, resource="socket.io", policy_server=False)
   ws.serve_forever()
