# websocket_test.py
import websocket

def on_message(ws, message):
    print(f"Received message: {message}")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/vacancies/")
    ws.on_message = on_message

    ws.run_forever()
