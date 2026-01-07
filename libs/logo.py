# coding=utf-8
#!/usr/bin/env python3
from colorama import Fore, Back, Style
from random import choice

logo = """

██╗███╗░░██╗░██████╗████████╗░█████╗░░██████╗░██████╗░░█████╗░███╗░░░███╗
██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝░██╔══██╗██╔══██╗████╗░████║
██║██╔██╗██║╚█████╗░░░░██║░░░███████║██║░░██╗░██████╔╝███████║██╔████╔██║
██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║██║░░╚██╗██╔══██╗██╔══██║██║╚██╔╝██║
██║██║░╚███║██████╔╝░░░██║░░░██║░░██║╚██████╔╝██║░░██║██║░░██║██║░╚═╝░██║
╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝

        ░░██╗  ████████╗░█████╗░░█████╗░██╗░░░░░  ██╗░░
        ░██╔╝  ╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░  ╚██╗░
        ██╔╝░  ░░░██║░░░██║░░██║██║░░██║██║░░░░░  ░╚██╗
        ╚██╗░  ░░░██║░░░██║░░██║██║░░██║██║░░░░░  ░██╔╝
        ░╚██╗  ░░░██║░░░╚█████╔╝╚█████╔╝███████╗  ██╔╝░
        ░░╚═╝  ░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝  ╚═╝░░ """

urls = [
    "GitHub - https://github.com/otterai",
    "Instagram - https://instagram.com/foileds",
    "Facebook - https://fb.com/zuck",
    "Twitter - https://twitter.com/Panwala_",
    "InstaReporter Tool - https://github.com/otterai/Instagram-tool",
    "Gmail - mailto:chutpaglu@duck.com"
    ]

def print_logo():
    print(Fore.RED + Style.BRIGHT + logo + Style.RESET_ALL + Style.BRIGHT +"\n")
    print(Fore.MAGENTA + "      Producer: Muneeb"+ Style.RESET_ALL + Style.BRIGHT)
    print(Fore.CYAN + "\n", "-> Follow me On Instagram @muneebwanee.")
    print ("\n", "-> Special For Hackers:\n    " + choice(urls))
    print(Style.RESET_ALL + Style.BRIGHT, Style.BRIGHT)

