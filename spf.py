# this program should take IP address of the email sender and the email address
# search in the SPF records and determine if the IP is among the authorized senders

# mechanisms documentation https://dmarcian.com/spf-syntax-table/        

"""
/////////////////////////////////////////////////////////////////////////////////////////////////////
DISCLAIMER TO DEVELOPERS
/////////////////////////////////////////////////////////////////////////////////////////////////////
    every critical function that has effect on the SPF should be implemented in a separate function 
    to allow quick debugging and tweaking in the future for possible intergrations and allowing 
    resusability of code instead of reinvinting the wheel.
////////////////////////////////////////////////////////////////////////////////////////////////////
"""

import util


# SPF mechanism handlers

def include(mechanism:str, verbose=False):
    
    output = None

    # filter output
    try:
        domain = mechanism.split(':')[1]
    except IndexError:
        if util.domain(mechanism): domain = mechanism
        else:
            cli.log.error("Unable to parse " + mechanism + " as an [include] mechanism")
            raise ValueError("Unable to parse " + mechanism + " as an [include] mechanism")

    try:
        cli.log.comment(f"{domain} DNS TXT records", end='\r', verbose=verbose)
        output = util.domainNameQuery.txt(domain)
        cli.log.acknowledge(f"{domain} DNS TXT records" , end='\n')
    except ConnectionError:
        cli.log.error(f"{domain} DNS TXT records", end='\n')
    return output


def ip(ip,subnet, verbose=False):
    try:
        cli.log.comment(f"checking {ip} in premitted subnet {subnet}", end='\r', verbose=verbose)
        if util.checkNetworkRange(ip, subnet[4:]):
            cli.log.acknowledge(f"{ip} belongs to premitted subnet {subnet}", end='\n')
            return True
        else:
            cli.log.comment(f"IP {ip} does not belong to subnet {subnet}", end='\n', verbose=verbose)
    except ValueError:
        cli.log.error(f"Failed comparing {ip} to {subnet}")

def ptr(record:str, domain:str = '', verbose:bool=False):
    if len(record) > 3:
        prefix = None
        if record[4] == ':':
            domain = record.split(':')[1].split['/'][0]
            try: prefix = '/' + record.split('/')[1]
            except IndexError: pass
    A = util.domainNameQuery.a(domain)
    output = []
    for ip in A:
        output.append(util.domainNameQuery.ptr(ip))


# SPF Check Function
# the script uses the mechanisms in the TXT records in the sequence

def SPF(sender_domain, sender_address, v=False) -> bool:
    
    # get SPF mechanisms
    cli.log.comment("quering DNS TXT records for " + sender_domain + "\n", verbose=v)
    TXTrecords = include(sender_domain)
    
    
    # test each mechanism
    for record in TXTrecords:
        
        # [include] mechanism
        
        if record.startswith("include"):
            try: 
                tmp = include(record, verbose=v)
                TXTrecords += tmp
            except TypeError: pass
            except ValueError: pass

        # [ip4] and [ip6] mechanism
        
        elif record.startswith("ip4") or record.startswith("ip6"):
            if ip(sender_address, record, v) : return True  # return on the 1st true    
        
        #TODO [mx] mechanism not applied
        
        elif record.startswith("mx"): pass
        
        #TODO [ptr] mechanism not working right

        elif record.startswith("ptr"):
            #print(ptr(record, sender_domain, v))  # FOR TESTING
            pass
            
        
        #TODO [exists] mechanism not applied

        elif record.startswith("exists"): pass

    # IP was not designated by any mechanism in the TXT records
   
    return False







# Code for CLI usage

if __name__ == "__main__":
    
    import cli
    
    # Driver Code 
    try:
        if SPF(cli.arg['domain'], cli.arg['ip_address'], cli.arg['verbose']):
            cli.log.acknowledge(f"{cli.arg['domain']}: designates {cli.arg['ip_address']} as permitted sender", end='\t')
        else:
            cli.log.error(f"{cli.arg['domain']}: designates {cli.arg['ip_address']} as spoofed sender", end='\t')  
    except KeyboardInterrupt:
        print("")
        cli.log.mark("Process Interrupted by user")
    print()    
    quit()

# Syntax Example: 
# python3 spf.py --email-address someone@coordinatesme.com --sender-address 209.85.210.198
# python3 spf.py -v --email-address someone@coordinatesme.com --sender-address 209.85.210.198
