# module base on colorama

import colorama


# available text colors

class text:

    red = colorama.Fore.RED
    green = colorama.Fore.GREEN
    blue = colorama.Fore.BLUE
    yellow = colorama.Fore.YELLOW
    magenta = colorama.Fore.MAGENTA
    cyan = colorama.Fore.CYAN
    white = colorama.Fore.WHITE
    black= colorama.Fore.BLACK
    reset = colorama.Fore.RESET


# available background colors

class background:

    red = colorama.Back.RED
    green = colorama.Back.GREEN
    blue = colorama.Back.BLUE
    yellow = colorama.Back.YELLOW
    magenta = colorama.Back.MAGENTA
    cyan = colorama.Back.CYAN
    white = colorama.Back.WHITE
    black = colorama.Back.BLACK
    reset = colorama.Back.RESET


class StyleError(ValueError): pass

class style:

    def __init__(self, tcolor:str, bcolor:str):
        self.background_color = bcolor
        self.text_color = tcolor
        if not(self.verify()):
            raise StyleError("Text and Background must be in contrast")


    # no matching background and text colors
    def verify(self):

        # matching colors

        if   self.background_color == background.red     and self.text_color == text.red:     return False
        elif self.background_color == background.magenta and self.text_color == text.magenta: return False
        elif self.background_color == background.yellow  and self.text_color == text.yellow:  return False
        elif self.background_color == background.white   and self.text_color == text.white:   return False
        elif self.background_color == background.black   and self.text_color == text.black:   return False
        elif self.background_color == background.cyan    and self.text_color == text.cyan:    return False
        elif self.background_color == background.blue    and self.text_color == text.blue:    return False
        elif self.background_color == background.green   and self.text_color == text.green:   return False
        
        # low contrast

        elif self.background_color == background.cyan    and self.text_color == text.blue:    return False
        elif self.background_color == background.blue    and self.text_color == text.cyan:    return False

        elif self.background_color == background.red     and self.text_color == text.magenta: return False
        elif self.background_color == background.magenta and self.text_color == text.red:     return False

        elif self.background_color == background.green   and self.text_color == text.blue:    return False
        elif self.background_color == background.blue    and self.text_color == text.green:   return False

        return True

    def colorize(self, message:str) -> str:
        return str(self.background_color + self.text_color + str(message) + background.reset + text.reset ) 




# class that abstracts all colorama syntax to style functions

class log():

    def __init__(self):
        
        # pre-defined styles
        self.alert  = style(text.red, background.reset)
        self.show   = style(text.white, background.blue)
        self.ack    = style(text.green, background.reset)
        self.select = style(text.black, background.white)

    def error(self, msg='', end='\n'):
        msg = self.alert.colorize("[X] "+ str(msg))
        print(msg, end=end)

    def mark(self, msg='', end='\n'):
        msg = self.show.colorize("[#] " + str(msg))
        print(msg, end=end)
    
    def comment(self, msg='', end='', verbose=False):
        if not(verbose): return
        print(colorama.Style.DIM + str(msg) + colorama.Style.RESET_ALL , end=end)

    def acknowledge(self, msg='', end='\n'):
        msg = self.ack.colorize("[✓] " + str(msg)) 
        print(msg, end=end)

    def highlight(self, msg, end=''):
        msg = self.select.colorize(msg)
        print(msg, end=end)

# driver program for testing

if __name__ == "__main__":
    from sys import argv
    verbose = "-v" in argv
    log = log()
    print("ERROR MESSAGE: " , end='\t')
    log.error("error message")
    
    print("NOTICE MESSAGE: " , end='')
    log.mark("notice message")
    
    print("ACK MESSAGE: " , end='\t')
    log.acknowledge("acknowledgement")
    print("\n")
    print("This module is written by Ahmed Mamdouh (DeaDude)")
    log.comment("for following social media links use -v option", verbose=not(verbose), end='\n')
    log.highlight("[LinkedIn]")
    log.comment("\thttps://www.linkedin.com/in/ahmed-mamdouh-b563081b6/", verbose=verbose, end="\n")
    log.highlight("[GitHub]")
    log.comment("\thttps://github.com/DeadDude-glitch/", verbose=verbose, end='\n')
    print()
    print("attempting to use unreadable style")
    style(text.white, background.white)
