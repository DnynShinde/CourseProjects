import socket
import re
import time

def send_http_request_to_proxy(proxy_host, proxy_port, server_host, server_port, path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((proxy_host, proxy_port))

    # Record the start time
    start_time = time.time()

    request = f"GET {path} HTTP/1.1\r\nServer_Host: {server_host}\r\nServer_port: {server_port}\r\n\r\nConnection: close\r\n\r\n"
    client_socket.send(request.encode())

    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    client_socket.close()

    # Calculate the elapsed time for this request
    elapsed_time = time.time() - start_time

    return response.decode(), elapsed_time

def send_http_request(host, port, path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    start_time = time.time()

    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    client_socket.send(request.encode())

    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    client_socket.close()

    elapsed_time = time.time() - start_time

    return response.decode(), elapsed_time

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)} minutes and {seconds:.2f} seconds"

def main():
    user_input = input("Do you want to use the Web Proxy Server (Y/N): ")

    if user_input == "Y":
        proxy_address = input("Proxy Address: ")
        proxy_port = int(input("Proxy Port: "))
        server_address = input("Server Address: ")
        server_port = int(input("Server Port: "))
        path = input("File Path: ")

        # Send the request to the web proxy server and measure the time
        response, proxy_elapsed_time = send_http_request_to_proxy(proxy_address, proxy_port, server_address, server_port, path)
    else:
        server_address = input("Server Address: ")
        server_port = int(input("Server Port: "))
        path = input("File Path: ")

        # Send the request to the web server and measure the time
        response, direct_elapsed_time = send_http_request(server_address, server_port, path)

    print(response)

    # Check for references to other objects in the HTML response
    if path.endswith(".html"):
        links = re.findall(r'href="(.*?)"', response)
        for link in links:
            print(f"Fetching: {link}")
            response, elapsed_time = send_http_request(proxy_address, proxy_port, server_address, server_port, link)
            print(response)
            print(f"Elapsed Time: {format_time(elapsed_time)}")

    if user_input == "Y":
        print(f"Proxy Elapsed Time: {format_time(proxy_elapsed_time)}")
        if "direct_elapsed_time" in locals():
            print(f"Direct Elapsed Time: {format_time(direct_elapsed_time)}")
        if "direct_elapsed_time" in locals() and proxy_elapsed_time < direct_elapsed_time:
            print(f"Latency Reduced: {format_time(direct_elapsed_time - proxy_elapsed_time)}")

if __name__ == '__main__':
    main()
