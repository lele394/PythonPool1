
from utilities import clear_screen



#
# ╔╗ ═  ╠ 
# ╚╝║

def GameBanner():
    clear_screen()
    print(
        """
╔═══════════════════════════════════════════════════╗
║  _   __    _         _   _ ___     __ ___      _  ║
║ |_  (_    |_   |\ | / \ |_) | |_| (_   |  /\  |_) ║
║ | o __) o |    | \| \_/ | \ | | | __)  | /--\ | \ ║
║        ~o   Story of a stranded crew   o~         ║
╠═══════════════════════════════════════════════════╣
║   Game made as a project in the CompuPhys Master  ║
║     UFR-ST Besancon ~ Léo BECHET ~ 2023/2024      ║
╚═══════════════════════════════════════════════════╝
"""
    )


GameBanner()



def GameIntroduction(skip=False):

    if not skip:
        print("blah blah")



    return












def GameWin(type: str, master_deltat):
    """
    LT : target collided with an light round

    TS : target collided with the ship

    """
    clear_screen()
    match type:
        case "LT":
            print("Sir, our calculations were correct! a light round destroyed the inhibitor")

        case 'TS':
            print("""
You madlad, you somewhow sent us directly into it! We've suffered minimal
damage and the gun crew was able to gun down the inhibitor in a heartbeat!""")

    print(f'You saved your crew in {round(master_deltat, 3)}')
    input("press enter to leave > ")
    quit()



    return

def GameLoss(type: str):
    """
    LS : ship collided with a light round

    OOB : ship went out of bound

    FIBH: ship fell in the blackhole
    """
    clear_screen()





    return




def ElasticCollision():
    return
