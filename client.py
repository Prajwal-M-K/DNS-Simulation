import socket

def send_dns_query_to_server(server_ip, server_port):
    while True:
        domain = input("Enter domain name (or type 'exit' to quit): ").strip()
        if domain.lower() == 'exit':
            break

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                sock.sendto(domain.encode(), (server_ip, server_port))
                response, _ = sock.recvfrom(1024)
                ip_address = response.decode()
                print(f"IP address for {domain}: {ip_address}\n")
            except Exception as e:
                print(f"Error communicating with DNS server: {e}\n")

if __name__ == "__main__":
    DNS_SERVER_IP = '127.0.0.1'  
    DNS_SERVER_PORT = 5200

    print("DNS Client Started")
    send_dns_query_to_server(DNS_SERVER_IP, DNS_SERVER_PORT)
