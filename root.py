import socket

root_records = {
    "edu": 5301,  
    "in": 5302    
}

def start_root_server(port, root_records):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', port))  
    print(f"[Root DNS Server] Listening on port {port}...")

    while True:
        message, client_address = server_socket.recvfrom(1024)  
        domain = message.decode()  
        print(f"[Request] Received query for {domain}")

        tld = domain.split('.')[-1]  

        port_number = root_records.get(tld, "NOT_FOUND")  
        
        server_socket.sendto(str(port_number).encode(), client_address)
        print(f"[Response] Sent port {port_number} for TLD {tld} to {client_address}")

if __name__ == "__main__":
    start_root_server(port=5300, root_records=root_records)
