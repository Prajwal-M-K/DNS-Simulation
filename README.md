# DNS-Simulation
DNS Simulation mini project, done as a part of the Computer Networks course in the 4th semester.
Uses Python and MongoDB to simulate the iterative resolution of a DNS query.
Request is first sent to local DNS resolver, which checks if query has been stored in cache. If not, the request is forwarded to the root server, which returns the address of the appropriate TLD server. The TLD server is contacted to recieve the address of the authoritative server, which is contacted to resolve the IP address.
Has 2 Top-Level Domains, .edu and .in, and 4 Apex domains - amazon.in, google.in, pes.edu, and mit.edu.
