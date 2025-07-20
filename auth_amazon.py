import socket

dns_records = {
    "www.amazon.in": "192.168.2.10",
    "deals.amazon.in": "192.168.2.11",
    "seller.amazon.in": "192.168.2.12",
    "prime.amazon.in": "192.168.2.13",
    "aws.amazon.in": "192.168.2.14"
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
    start_authoritative_server(port=5402, domain_records=dns_records)
