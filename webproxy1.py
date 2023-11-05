import socket
import threading
import os
from queue import Queue

HOST = "127.0.0.5"  # Server's IP address
PORT = 12345  # Port to listen on

def handle_server(path, server_add, server_port, queue):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_add, server_port))
    print(f"[CONNECTED] Connected to the server on ('{server_add},{server_port}')")

    request = f"GET {path} HTTP/2\r\nHost: {server_add}\r\nConnection: keep-alive\r\n\r\n"
    server_socket.send(request.encode())

    response = b""
    while True:
        data = server_socket.recv(1024)
        if not data:
            break
        response += data

    server_socket.close()
    queue.put(response)

def parse_base_html(html_content):
    # Parse the base HTML to find and fetch objects
    lines = html_content.splitlines()
    objects = []

    for line in lines:
        if "src=" in line or "href=" in line:
            parts = line.split()
            for part in parts:
                if "src=" in part or "href=" in part:
                    obj = part.split("=")[1]
                    obj = obj.strip('"')
                    objects.append(obj)

    return objects

def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode()
    request_lines = request_data.split("\n")
    request_line = request_lines[0]
    method, path, _ = request_line.split()
    request_line = request_lines[1]
    # _, server_add = request_line.split()
    # request_line = request_lines[2]
    # _, server_port = request_line.split()
    # server_port = int(server_port)

    server_add = '192.168.135.246'
    server_port = 15200

    result_queue = Queue()
    server_thread = threading.Thread(target=handle_server, args=(path, server_add, server_port, result_queue))
    server_thread.start()
    server_thread.join()

    response = result_queue.get()

    if "Content-Type: text/html" in response.decode():
        # If the response is an HTML page, parse it to find and fetch objects
        objects = parse_base_html(response.decode())

        for obj in objects:
            obj_thread = threading.Thread(target=handle_server, args=(obj, server_add, server_port, result_queue))
            obj_thread.start()
            obj_thread.join()
            obj_response = result_queue.get()
            response = response.replace(obj.encode(), obj_response, 1)

    client_socket.send(response)
    client_socket.close()

def start_proxy_server():
    proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server_socket.bind((HOST, PORT))
    proxy_server_socket.listen(5)
    print(f"[LISTENING] Web Proxy Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = proxy_server_socket.accept()
        print(f"[CONNECTED] Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_proxy_server()
