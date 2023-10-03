
from utilities import clear_screen



#
# ╔╗ ═  ╠ 
# ╚╝║

def GameBanner():
    clear_screen()
    print(
        """\033[96m
╔═══════════════════════════════════════════════════╗
║  _   __    _         _   _ ___     __ ___      _  ║
║ |_  (_    |_   |\ | / \ |_) | |_| (_   |  /\  |_) ║
║ | o __) o |    | \| \_/ | \ | | | __)  | /--\ | \ ║
║        ~o   Story of a stranded crew   o~         ║
╠═══════════════════════════════════════════════════╣
║   Game made as a project in the CompuPhys Master  ║
║     UFR-ST Besancon ~ Léo BECHET ~ 2023/2024      ║
╚═══════════════════════════════════════════════════╝\033[97m
"""
    )





def GameMenu():
    print("""
          
    .1) (P)lay
    .2) (H)ow to play
    .3) (C)redits
    .4) (Q)uit

""")
    
    return input(" > ")






def GameHowToPlay():
    clear_screen()
    print("this section is currently empty")
    input("Press enter to continue\n > ") 



def GameCredits():
    clear_screen()
    print("""

    ~ o ---------------------------------------------- o ~

               Project made by Leo Bechet
               CompuPhys  Master's degree
               UFR-ST Besancon  2023/2024
                   github.com/lele394
           
        Special Thanks to Adam Trigui for the help
                on collisions equations.
    
        Special Thanks to  Einar Forselv for the help
             on moderngl and general knowledge.
          
    ~ o ---------------------------------------------- o ~

    """)
    return input("Press enter to continue \n > ")    


def GameIntroduction(skip=False):

#
# ╔╗ ═  ╠ 
# ╚╝║

    screens = [
"""   
╔════════════════════╗  
║                    ║   \x1B[1mLt Jones\x1B[0m
║       @@@@@@       ║   \x1B[4mShip propulsion specialist\x1B[0m
║     @@@@@@@@@@     ║   
║     @@@@@@@@@@     ║   Sir! It seems our last jumped sent us
║     @@@@@@@@@@     ║   right next to a Black-Hole!
║     @@@@@@@@@@     ║     
║       @@@@@@       ║     
║        @@@@        ║     
║        @@@@        ║     
║    @@@@@@@@@@@@    ║     
║  @@@@@@@@@@@@@@@@  ║    
║                    ║ 
╚════════════════════╝                       
""",

"""   
╔════════════════════╗  
║                    ║   \x1B[1mLt Elias\x1B[0m
║       ######       ║   \x1B[4mShip sensors specialist\x1B[0m
║     ##########     ║   
║     ##########     ║   Black-Hole confirmed sir.
║     ##########     ║   Sensors also detect interferences in the 
║     ##########     ║   fabric of space-time, attempting to jump now
║       ######       ║   would lead to certain death.
║        ####        ║   
║        ####        ║   We're picking a signature from the other side  
║    ############    ║   of the black hole. This should be the source
║  ################  ║   of the interferences. We must destroy it!
║                    ║ 
╚════════════════════╝                       
""",

"""   
╔════════════════════╗  
║                    ║   \x1B[1mLt Eremson\x1B[0m
║       &&&&&&       ║   \x1B[4mShip weapons and firing control specialist\x1B[0m
║     &&&&&&&&&&     ║   
║     &&&&&&&&&&     ║   Weapons section reporting in sir!
║     &&&&&&&&&&     ║   Our battleship is equipped with two types of missiles
║     &&&&&&&&&&     ║    - Heavy missiles   : hitting the target with one will
║       &&&&&&       ║                         change its kinetic energy
║        &&&&        ║    - Explosive missiles:If one of them hits the target, it
║        &&&&        ║                         it will be destroyed
║    &&&&&&&&&&&&    ║   
║  &&&&&&&&&&&&&&&&  ║   Sending the target in the black whole will also destroy it.
║                    ║   Be careful not to send us in aswell.
╚════════════════════╝                       
""",

"""   
╔════════════════════╗  
║                    ║   \x1B[1mLt Elias\x1B[0m
║       ######       ║   \x1B[4mShip sensors specialist\x1B[0m
║     ##########     ║   
║     ##########     ║   Displaying ship sensors on the screen when you're ready sir
║     ##########     ║   
║     ##########     ║   Our \033[92mShip will be in green\033[97m, \033[91mthe Target will be red\033[97m,
║       ######       ║   \033[94mHeavy missiles will be blue\033[97m and \033[33mLight missiles will be orange.\033[97m
║        ####        ║   
║        ####        ║   
║    ############    ║   On your command, sir!
║  ################  ║   
║                    ║ 
╚════════════════════╝                       
""",



    ]



    if not skip:
        for screen in screens:
            clear_screen()
            print(screen)
            input("\n\n\n Enter to continue >")





    clear_screen()
    return  












def GameWin(type: str, master_deltat):
    """
    LT : target collided with an light round

    TS : target collided with the ship

    OOB : target went out of bound

    FIBH: target fell in black hole

    """
    clear_screen()
    match type:
        case "LT":
            print("\n\n         Sir, our calculations were correct! a light round destroyed the inhibitor!\n")

        case 'TS':
            print("""\n\n
        You madlad, you somewhow sent us directly into it! We've suffered minimal
        damage and the gun crew was able to gun down the inhibitor in a heartbeat!\n""")
            
        case 'OOB':
            print("""\n\n
        Sir, the inhibitor is losing power, we threw it off course. Our Engine works again, we're safe!
\n""")
        case 'FIBH':
            print("""\n\n
        Sir, the inhibitor fell into the black hole! We're free!
\n""")

    print(f'        You saved your crew in {round(master_deltat, 3)} minutes!')
    input(" press enter to leave > ")
    quit()



    return








def GameLoss(type: str):
    """
    LS : ship collided with a light round

    OOB : ship went out of bound

    FIBH: ship fell in the blackhole
    """
    clear_screen()
    match type:
        case "LS":
            print("""\n\n
        Sir, it's coming ba-- bzzz...........
        A light round came back and destroyed your ship.\n
""")

        case "OOB":
            print("""\n\n
        Sir, we've deviated too much... We're bound for outer space
        Your ship ventured too far in outer space. You never found 
        a way to leave this system\n
""")

        case "FIBH":
            print("""\n\n
        Sir, we're bound fro the black hole, we're done for...
        You deviated too much from your orbit. Your ship falls 
        in the black hole and you're lost to the void.\n
""")
            
    print("  game lost")
    input(" > ")
    quit()





    return




def ElasticCollision():
    return






def GameNewTurn():
    print("""   
╔════════════════════╗  
║                    ║   \x1B[1mLt Elias\x1B[0m
║       ######       ║   \x1B[4mShip sensors specialist\x1B[0m
║     ##########     ║   
║     ##########     ║   Ship sensors have updated the situation and
║     ##########     ║   the firing crew is on standby, what are your
║     ##########     ║   orders, sir.
║       ######       ║   
║        ####        ║   
║        ####        ║   
║    ############    ║   
║  ################  ║   
║                    ║ 
╚════════════════════╝                       
""",)
    return input("(l)aunch (w)ait (q)uit\n > ")






def GameFiring(inv):
    clear_screen()
    print(f'''  
╔════════════════════╗  
║                    ║   \x1B[1mLt Eremson\x1B[0m
║       &&&&&&       ║   \x1B[4mShip weapons and firing control specialist\x1B[0m
║     &&&&&&&&&&     ║   
║     &&&&&&&&&&     ║   Weapons section reporting in sir!
║     &&&&&&&&&&     ║   Please input our firing settings in the console
║     &&&&&&&&&&     ║   As a reminder we only have {inv["Heavy"]} \033[94m(H)eavy\033[97m and {inv["Light"]}\033[33m(L)ight\033[97m missiles.
║       &&&&&&       ║   
║        &&&&        ║   To input your coordinates, please speciy an angle and a type
║        &&&&        ║   Here`s an example :
║    &&&&&&&&&&&&    ║   \033[92mcommand\033[91m@firing-console\033[97m> 1.2 Heavy
║  &&&&&&&&&&&&&&&&  ║   
║                    ║   Bear in mind the angle is relative to the velocity of our ship
╚════════════════════╝     helping tool : www.desmos.com/calculator/6ghiuav1rs
''')
    return input("\033[92mcommand\033[91m@firing-console\033[97m> ")




def OutOfAmmo(ammo_type):
    print(f'''  
╔════════════════════╗  
║                    ║   \x1B[1mLt Eremson\x1B[0m
║       &&&&&&       ║   \x1B[4mShip weapons and firing control specialist\x1B[0m
║     &&&&&&&&&&     ║   
║     &&&&&&&&&&     ║   Sir! We're out of {ammo_type} missiles!
║     &&&&&&&&&&     ║   
║     &&&&&&&&&&     ║   
║       &&&&&&       ║   
║        &&&&        ║   
║        &&&&        ║   
║    &&&&&&&&&&&&    ║   
║  &&&&&&&&&&&&&&&&  ║   
║                    ║   
╚════════════════════╝     
''')
    input(" enter to continue > ")


def OutOfEveryting():
    print(f'''  
╔════════════════════╗  
║                    ║   \x1B[1mLt Eremson\x1B[0m
║       &&&&&&       ║   \x1B[4mShip weapons and firing control specialist\x1B[0m
║     &&&&&&&&&&     ║   
║     &&&&&&&&&&     ║   Sir! We're out of every projectiles!
║     &&&&&&&&&&     ║   
║     &&&&&&&&&&     ║   
║       &&&&&&       ║   
║        &&&&        ║   
║        &&&&        ║   
║    &&&&&&&&&&&&    ║   
║  &&&&&&&&&&&&&&&&  ║   
║                    ║   
╚════════════════════╝     
''')
    input(" enter to continue > ")









def GameChoseStratShipPosition():

    clear_screen()

    default_presets = [
        [-1, 0.05, 35],
        [0, 0.05, 35],
        [-1, 0.05, 30],
        [0, 0.05, 30]
    ]


    inp = input("""
 please specify the starting values of your ship
 This part has no type checker, it can crash if values are not entered the right way
 please specify them in this order : speed on r, speed on theta, starting radius
 example : > 0 0.05 30   <= recommended starting configuration
 alternatively you can type 'default' to get access to a few preset values  
   vr vtheta r        
 > """)
    


    if inp == "default":
        print("===== Default available starting values =====\n\n")

        for i in range(len(default_presets)):
            print(f'.{i}) vr: {default_presets[i][0]}\t vt: {default_presets[i][1]}\t r: {default_presets[i][2]}')
        
        inp = int(input("\n\n > "))

        vr = default_presets[inp][0]
        vt = default_presets[inp][1]
        r = default_presets[inp][2]

        return vr, vt, r

    else:
        inp_split = inp.split(" ")
        vr = float(inp_split[0])
        vt = float(inp_split[1])
        r = float(inp_split[2])

        return vr, vt, r