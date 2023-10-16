# Styling Console Output

import util

try:

    import console
    log = console.log()

except ImportError:

    # dummy class to replace console import if decided to not used

    class dummy:
        def comment(self, msg, verbose=False): 
            if verbose: print(msg, end='')
        def acknowledge(self, msg, end='\n'): print(msg, end=end)
        def highlight(self, msg, end=''): print(msg, end='')
        def alert(self, msg, end='\n'): print(msg, end=end)
        def error(self, msg, end= '\n'): print(msg, end=end)
	
    log = dummy()















# User Input Parsing

import argparse


# ARGUMENT CONFIGURATIONS
    
parser = argparse.ArgumentParser(
        prog = "SPF",
        description = "This program/script was made to do the spf checks",                             
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
)
    
# sender email address argument
    
parser.add_argument('-e', '--email',
	action = 'store',   # default action is store but I do not trust defaults
	help = "sender's email address)")
    
    
parser.add_argument('-d', '--domain',
	action = 'store',   # default action is store but I do not trust defaults
	help = "sender's domain )")
    
    
    # sender ip address argument
    
parser.add_argument('-ip', '--ip-address',   
    action = 'store',   # default action is store but I do not trust defaults
    help = "sender's IP address") 
    
    # verbose option for debugging

parser.add_argument('-v', '--verbose',   
	default = False,
	action = 'store_true',   # switch key
    help = "observe checks in details (for debugging)")











    
    
# Handle User Input
    
arg = vars(parser.parse_args())
    
# IP address provided?

if arg["ip_address"] != None:
        
    # Valid IP address? 

    if util.ip_address(arg["ip_address"]):
        
        # domain was given?
        
        if arg['domain'] == None: 

            # email was given?    

            if  arg['email'] != None:
                
                # valid email?

                if util.email(arg['email']):
                       
                    # get the domain from email

                    arg['domain'] = arg["email"].split('@')[1]
                    
                else: raise ValueError("Invalid Email address")
            
            else: raise SyntaxError("No email address nor domain were given")

        else:

            if util.domain(arg['domain']): pass 
            else: raise ValueError("Invalid Domain")

    else: raise ValueError("Invalid IP address")
else: raise SyntaxError("No IP address was given")
    
