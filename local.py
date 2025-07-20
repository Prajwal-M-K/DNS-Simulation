import socket
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client['dns_cache']
collection = db['queries']
collection.create_index("timestamp", expireAfterSeconds=600)  

def check_cache(domain):
    result = collection.find_one({'domain': domain})
    if result:
        print(f"[CACHE HIT] {domain} → {result['ip_address']}")
        return result['ip_address']
    return None

def update_cache(domain, ip_address):
    collection.update_one(
        {'domain': domain},
        {'$set': {'ip_address': ip_address, 'timestamp': datetime.now()}},
        upsert=True
    )

def query_root_server(domain):
    root_server = ('localhost', 5300)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(domain.encode(), root_server)
        response, _ = sock.recvfrom(1024)
        return int(response.decode())

def query_tld_server(domain, tld_server_port):
    tld_server = ('localhost', tld_server_port)  
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(domain.encode(), tld_server)
        response, _ = sock.recvfrom(1024)
        return int(response.decode())  

def query_authoritative_server(domain, auth_server_port):
    auth_server = ('localhost', auth_server_port)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(domain.encode(), auth_server)
        response, _ = sock.recvfrom(1024)
        return response.decode()

def iterative_dns_query(domain):
    cached_ip = check_cache(domain)
    if cached_ip:
        return cached_ip

    try:
        tld_server_port = query_root_server(domain)
        print(f"[ROOT] TLD server port for {domain}: {tld_server_port}")

        auth_server_port = query_tld_server(domain, tld_server_port)
        print(f"[TLD] Authoritative server port: {auth_server_port}")

        ip_address = query_authoritative_server(domain, auth_server_port)
        print(f"[AUTH] IP address: {ip_address}")

        update_cache(domain, ip_address)
        return ip_address

    except Exception as e:
        print(f"[ERROR] {e}")
        return "Resolution failed"

def start_dns_server():
    server_ip = '0.0.0.0'
    server_port = 5200

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        print(f"DNS Server running on {server_ip}:{server_port}...\n")

        while True:
            data, client_addr = server_socket.recvfrom(1024)
            domain = data.decode().strip()
            print(f"\n[QUERY] Received domain: {domain} from {client_addr}")

            ip = iterative_dns_query(domain)
            server_socket.sendto(ip.encode(), client_addr)

if __name__ == "__main__":
    start_dns_server()
