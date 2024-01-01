import pygame

from data.scripts.colors import *
from data.scripts.draw import *
from data.scripts.fonts import *
from data.scripts.init import *
from data.scripts.image import *
from data.scripts.join_jamos import *
from data.scripts.keyboard import *
from data.scripts.ui import *
from data.scripts.icon import *
from data.scripts.mouse import *

ScreenSize = GetScreenSize()
WindowSize = ScreenSize
WindowPos = (0, 0)
window, hwnd = init(WindowSize, WindowPos, "Creamy Window", pygame.NOFRAME|pygame.HIDDEN, "CREAM.png", True)
clock = pygame.time.Clock()
login = eval(open(".\\data\\login.json", "r", encoding='utf8').read())

def login():
    login = eval(open(".\\data\\login.json", "r", encoding='utf8').read())
    UserName = username.text
    Password = password.text

    for data in login:
        if (UserName == data.get("username", "") and Password == data.get("password", "")):
            minimize(hwnd)
            system.Hidden = True
            system.cleared = True
            username.text = ""
            password.text = ""
            return True
        
    return False

    

class system:
    cleared = True
    Hidden = True
    background:pygame.Surface=None
    InfoSize = 768, 480
    InfoPos = (ScreenSize[0]-InfoSize[0])//2, (ScreenSize[1]-InfoSize[1])//2
    InfoPlate = pygame.Surface(InfoSize, pygame.SRCALPHA)
    locked = LoadImage("locked.png")
    LoginCenter = ScreenSize[0]//2+InfoSize[0]//4, ScreenSize[1]//2

    def event(events:list[pygame.event.Event], KeyPressing) -> None:

        if (not system.Hidden): AlwaysOnTop(hwnd)

        if ("alt" in KeyPressing and '`' in KeyPressing and system.cleared and system.Hidden):

            system.Hidden = False
            system.cleared = False

            maximize(hwnd)
            system.background = pygame.transform.smoothscale(screenshot(10), ScreenSize)


        if ('alt' not in KeyPressing or '`' not in KeyPressing):
            system.cleared = True

        for event in events:
            if (event.type == pygame.QUIT):
                pass

        return

    def display(window:pygame.Surface=window, KeyPressed:list=[]) -> None:

        window.fill(Colors.Real.White)
        if (not system.Hidden and system.background):
            mouse = pygame.mouse.get_pos()

            window.blit(system.background, (0, 0))
            window.blit(system.InfoPlate, system.InfoPos)
            window.blit(system.locked, system.InfoPos)
            draw.text("Login To Unlock", font("Hancom Gothic Bold", 26), window, system.LoginCenter[0], system.LoginCenter[1]-65, color=Colors.Real.DarkGray,)


            for ui in UI.objects:
                ui.draw(
                    KeyPressed=KeyPressed,
                    mouse=mouse,
                    MouseState=MouseState
                )
    

draw.rrect(system.InfoPlate, [0, 0, system.InfoSize[0], system.InfoSize[1]], Colors.Real.LightGray, 0.1+0.001)
draw.rrect(system.InfoPlate, [1, 1, system.InfoSize[0]-2, system.InfoSize[1]-2], Colors.Real.White, 0.1)

username = UI.TextInput(surface=window,
                        rect=[system.LoginCenter[0]-150, system.LoginCenter[1]-35, 300, 50],
                        color=Colors.Real.White, border=Colors.Real.DarkGray, 
                        hint="Username", font=font("Hancom Gothic Regular", 14), HintColor=Colors.Real.Gray,
                        ActiveColor=Colors.Real.Purple)

password = UI.TextInput(window,
                        [system.LoginCenter[0]-150, system.LoginCenter[1]+25, 240, 50], 
                        Colors.Real.White, Colors.Real.DarkGray,
                        hint="Password", font=font("Hancom Gothic Regular", 14), HintColor=Colors.Real.Gray,
                        ActiveColor=Colors.Real.Purple,
                        password=True)

login = UI.Button(surface=window,
                  rect=[system.LoginCenter[0]+100, system.LoginCenter[1]+25, 50, 50],
                  color=Colors.Real.Purple, border=Colors.Real.DarkGray,
                  ActiveColor=rgb(50, 8, 117),
                  icon="arrow-right", IconColor=Colors.Real.White, IconThickness="m",
                  function=login)


while __name__ == "__main__":
    events = pygame.event.get()
    KeyPressing, KeyReleased, KeyPressed = keyboard.get_input()
    MouseState = mouse.state()

    system.event(events, KeyPressing)
    system.display(KeyPressed=KeyPressed)

    if (events):
        clock.tick(120)
    else:
        clock.tick(60)
    ##################### update #####################
    pygame.display.update()