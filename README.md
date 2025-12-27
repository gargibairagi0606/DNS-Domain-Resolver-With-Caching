# Domain Name Resolver with Caching
This project implements a DNS client in Python that manually constructs DNS query packets, sends them to a public DNS resolver using UDP, parses the DNS response, and caches results to reduce repeated network lookups.    

## Objective

To demonstrate how DNS resolution works internally using:
- UDP socket programming
- Manual DNS query construction
- DNS response parsing
- Timeout handling
- Caching with expiration

## Requirements

- Basics of socket programming in Python
- Understanding of DNS protocol
- Familiarity with UDP sockets and timeout handling
- Knowledge of domain name parsing and caching techniques

## How It Works

1. The client manually constructs a DNS query packet.
2. The packet is sent to Google DNS (`8.8.8.8`) using UDP.
3. The response is received and parsed to extract the IP address.
4. The resolved domain is stored in cache with a timestamp.
5. If the same domain is queried again within 60 seconds, the cached value is used.
6. If the cache expires, a new DNS query is sent.

## Features

- Manual DNS packet construction
- UDP communication on port 53
- Timeout handling for unresponsive DNS servers
- DNS response parsing
- Domain name caching with expiration

---

## How to Run

```bash
python DNS_client.py
Example Output
text
Copy code
Enter domain name (or 'exit' to quit): google.com
[DNS] google.com → 142.250.190.78

Enter domain name (or 'exit' to quit): google.com
[CACHE] google.com → 142.250.190.78

Enter domain name (or 'exit' to quit): openai.com
[DNS] openai.com → 104.18.12.123
Key Concepts Demonstrated
UDP socket programming

DNS protocol basics

Binary packet parsing

Timeout and error handling

Caching mechanisms

yaml
Copy code

