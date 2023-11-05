import socket
import sys
import re


# function to connect webproxy server
def send_http_request_to_proxy(proxy_host, proxy_port, server_host, server_port, path):
    # Create a new socket for each request
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((proxy_host, proxy_port))
    
    print("[CONNECTED] Connected To the Web Proxy Server")

    # Construct and send the HTTP GET request
    request = f"GET {path} HTTP/1.1\r\nServer_Host: {server_host}\r\nServer_port: {server_port}\r\n\r\nConnection: close\r\n\r\n"
    client_socket.send(request.encode())
    
    # Receive and display the response
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data
    
    client_socket.close()
    return response.decode()

# Function to connect server
def send_http_request(host, port, path):
    # Create a new socket for each request
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    print("[CONNECTED] Connected To the Web Server")
    # Construct and send the HTTP GET request
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    client_socket.send(request.encode())
    
    # Receive and display the response
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data
    
    client_socket.close()
    return response.decode()



def main():
    
    user_input = input("Do want to use Web Proxy Server (Y/N):")

    if user_input == "Y":
        proxy_address = "127.0.0.2"
        proxy_port = int(12347)
        server_address = "192.168.135.246"
        server_port = int(15200)
        path = input("File Path:")
        
        # Send the request to the web proxy server
        response = send_http_request_to_proxy(proxy_address, proxy_port, server_address, server_port, path)
    else:
        server_address = input("Server Address:")
        server_port = int(input("Server Port:"))
        path = input("File Path:")
        
        # Send the request to the web Server
        response = send_http_request(server_address, server_port, path)



    # Display the response
    print(response)
    
    # Check for references to other objects in the HTML response

    for i in range(0):
        if path.endswith(".html"):
            links = re.findall(r'href="(.*?)"', response)
        for link in links:
            print(f"Fetching: {link}")
            response = send_http_request(proxy_address, proxy_port, link)
            print(response)

if __name__ == '__main__':
    main()
