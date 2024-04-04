import socket
import json
from utils import generate_response

def handle_request(request):
    request_str = request.decode('utf-8')
    print(f"Received request: {request_str}")
    request_lines = request_str.split('\n')
    request_line = request_lines[0]
    method, path, http_version = request_line.split()

    if method == 'OPTIONS':
        print("Handling OPTIONS request")  
        response_str = 'HTTP/1.1 204 No Content\nAccess-Control-Allow-Origin: *\nAccess-Control-Allow-Methods: POST\nAccess-Control-Allow-Headers: Content-Type\n\n'.encode('utf-8')
    elif method == 'POST' and path == '/api/predict':
        print("Handling POST request")  
        content_length = None
        for line in request_lines[1:]:
            if 'Content-Length:' in line:
                content_length = int(line.split()[-1])
        if content_length:
            body = request_lines[-1]
            sentence = json.loads(body)['data']
            response = generate_response(sentence)
            response_str = 'HTTP/1.1 200 OK\nContent-Length: {}\nAccess-Control-Allow-Origin: *\n\n{}'.format(len(response), response).encode('utf-8')
        else:
            response_str = 'HTTP/1.1 400 Bad Request\nContent-Length: 0\nAccess-Control-Allow-Origin: *\n\n'.encode('utf-8')
    else:
        response_str = 'HTTP/1.1 404 Not Found\nContent-Length: 0\nAccess-Control-Allow-Origin: *\n\n'.encode('utf-8')

    print(f"Sending response: {response_str.decode('utf-8')}")
    client_connection.sendall(response_str)

server_address = ('0.0.0.0', 8000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(1)
print('Listening on {}:{}'.format(*server_address))

while True:
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(1024)
    handle_request(request)
    client_connection.close()
