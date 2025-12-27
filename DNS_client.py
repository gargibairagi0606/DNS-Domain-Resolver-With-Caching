import socket
import struct
import time

cache = {}

CACHE_TTL = 60
DNS_SERVER = '8.8.8.8'
DNS_PORT = 53


def build_query(domain):
    transaction_id = 0x1234
    flags = 0x0100
    qdcount = 1
    header = struct.pack('>HHHHHH', transaction_id, flags, qdcount, 0, 0, 0)

    qname = b''.join(bytes([len(part)]) + part.encode() for part in domain.split('.')) + b'\x00'
    qtype = 1
    qclass = 1
    question = qname + struct.pack('>HH', qtype, qclass)

    return header + question, transaction_id


def parse_response(data):
    resp_id, flags, qdcount, ancount, nscount, arcount = struct.unpack(">HHHHHH", data[:12])

    if resp_id != 0x1234:
        return None

    rcode = flags & 0x000F
    if rcode != 0 or ancount == 0:
        return None

    index = 12

    for _ in range(qdcount):
        while data[index] != 0:
            index += 1
        index += 1
        index += 4
    if data[index] & 0xC0 == 0xC0:
        index += 2
    else:
        while data[index] != 0:
            index += 1
        index += 1

    rtype, rclass, ttl, rdlength = struct.unpack(">HHIH", data[index:index + 10])
    index += 10

    if rtype == 1 and rclass == 1 and rdlength == 4:
        ip_bytes = data[index:index + 4]
        return ".".join(str(b) for b in ip_bytes)

    return None


def resolve_domain(domain):
    if domain in cache:
        ip, timestamp = cache[domain]
        if time.time() - timestamp < CACHE_TTL:
            print(f"[CACHE] {domain} → {ip}")
            return ip
        else:
            print(f"[CACHE EXPIRED] {domain} → Querying again...")

    query, _ = build_query(domain)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)

    try:
        sock.sendto(query, (DNS_SERVER, DNS_PORT))
        data, _ = sock.recvfrom(512)

        ip = parse_response(data)
        if ip:
            print(f"[DNS] {domain} → {ip}")
            cache[domain] = (ip, time.time())
        else:
            print(f"[DNS ERROR] No valid A record found for {domain}")

    except socket.timeout:
        print(f"[TIMEOUT] No response for {domain}")
    finally:
        sock.close()


if __name__ == "__main__":
    while True:
        domain = input("\nEnter domain name (or 'exit' to quit): ").strip()
        if domain.lower() == "exit":
            break
        resolve_domain(domain)
