from ipaddress import ip_address, ip_network
import dnspython as dns
from dns.resolver import resolve , LifetimeTimeout , NXDOMAIN
from dns.reversename import from_address
from validators import domain, email

def checkNetworkRange(address:str, subnet:str):
    return ip_address(address) in ip_network(subnet.strip('"'))

# collecting all the DNS queries
# in one place for clear mind

class domainNameQuery:
    
    # get TXT records
    
    def txt(domain:str) -> list: 
        try:
            for line in resolve(domain, 'TXT'):
                if str(line).strip('"').startswith('v=spf1'):
                    return str(line).split(' ')
        except LifetimeTimeout:
            raise ConnectionError
    
    # get domain IP address
    
    def a(domain:str) -> list:
        output = []
        try:
            for ip in resolve(domain, 'A'): output.append(str(ip))
        except LifetimeTimeout:
            raise ConnectionError
        return output

    # TODO PARSING OUTPUT
    def ptr(ip:str) -> list:
        output = []
        try:
            return resolve(ip, 'ptr')
        except NXDOMAIN:
            return None
    
    # TODO
    def mx(domain:str): pass

