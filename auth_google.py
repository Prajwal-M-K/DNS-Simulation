import socket

dns_records = {
    "www.google.in": "192.168.2.20",
    "mail.google.in": "192.168.2.21",
    "drive.google.in": "192.168.2.22",
    "ads.google.in": "192.168.2.23",
    "maps.google.in": "192.168.2.24"
}

def start_authoritative_server(port, domain_records):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', port))  
    print(f"[Authoritative Server for pes.edu] Listening on port {port}...")

    while True:
        message, client_address = server_socket.recvfrom(1024)  
        domain = message.decode()  
        print(f"[Request] Received query for {domain}")

        ip = domain_records.get(domain, "NOT_FOUND")  
        
        server_socket.sendto(ip.encode(), client_address)
        print(f"[Response] Sent IP {ip} for {domain} to {client_address}")

if __name__ == "__main__":
    start_authoritative_server(port=5403, domain_records=dns_records)
