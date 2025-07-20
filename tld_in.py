import socket

tld_records = {
     "amazon.in": 5402, 
    "google.in": 5403  
}

def start_tld_server(port, tld_records):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', port))  
    print(f"[TLD Server for .edu] Listening on port {port}...")

    while True:
        message, client_address = server_socket.recvfrom(1024)  
        domain = message.decode()  
        print(f"[Request] Received query for {domain}")

        
        apex_domain = domain.split('.', 2)[1] + "." + domain.split('.', 3)[2]  

        
        port_number = tld_records.get(apex_domain, "NOT_FOUND")  

        server_socket.sendto(str(port_number).encode(), client_address)
        print(f"[Response] Sent port {port_number} for {domain} to {client_address}")

if __name__ == "__main__":
    start_tld_server(port=5302, tld_records=tld_records)