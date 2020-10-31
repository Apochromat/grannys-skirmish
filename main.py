"""Granny`s Skirmish"""
"""version 0.8"""
"""Импорт"""
import time, random, math, sys, os, json
from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageTk

"""Файл настроек"""
with open("gamedata.json", 'r', encoding="utf-8") as file:
    settings = json.load(file)
"""Переменные"""
run = True
version = settings['version']
windowSize = settings["windowsize"] # Размер окна
canvasSize = settings["canvassize"] # размер области рисования
aboutmessage = settings["aboutmessage"] % version
authorsmessage = settings["authorsmessage"]
grannyWalkSpeedNormal = settings['grannyspeed']['normal']         # Бабкина скорость
grannyWalkSpeed = grannyWalkSpeedNormal
grannyWalkSpeedFast = settings['grannyspeed']['fast']
grannyWalkSpeedSlow = settings['grannyspeed']['slow']
gravitySpeedNormal = settings['gravity']['normal']     # Скорость гравитации (да, не ускорение)
gravitySpeedInvert = settings['gravity']['inverted']
gravitySpeed = gravitySpeedNormal
effectduration = settings['effectduration']          # Длительность эффектов
animationduration = settings['animationduration']    # Задержки анимации
lastanimationtime = time.time() # Задаем счетчик кадра

lastanimation = "None"  # Переменная последней проигранной анимации
lastWalkRightImage = 0  # Последнее использованное изображение для анимации шага вправо(т.к. анимация в массиве)
lastWalkLeftImage = 0   # Последнее использованное изображение для анимации шага влево(т.к. анимация в массиве)
lastClimbUpImage = 0    # Последнее использованное изображение для анимации забирания (т.к. анимация в массиве)

isWalkingLeft = False   # Идет ли персонаж влево
isWalkingRight = False  # Идет ли персонаж вправо
isClimbingUp = False    # Забирается ли персонаж
isClimbingDown = False  # Спускается ли персонаж

lasteffecttime = time.time()

isFastEffect = False
isSlowEffect = False
isGravEffect = False
isExitActive = False    # Доступен ли выход с уровня

antigrav = False
wallside="0"

livesNormal = settings['livesnormal']
lives = livesNormal
level = 0                   # Уровень
Score = 0               # Счет
ScoreAddCat = settings["ScoreAddCat"]       # Очки за кота
ScoreAddBonus = settings["ScoreAddBonus"]   # Очки за цветки
ScoreMax = settings["ScoreMax"]        # Максимум очков
"""Построение окна"""
root = Tk()                                                     # Создаем окно
root.title(settings['title'])                                 # Заголовок окна
root.geometry("%ix%i" % (windowSize[0], windowSize[1]))         # Размеры окна
root.resizable(0, 0)                                            # Запрет на изменение размеров окна
"""Элементы окна"""
statusbar = Label(root, justify=LEFT, text="Готов", width=settings["statusbarwidth"], height=1, bg="thistle2", anchor=W)
labelLevel = Label(root, justify=LEFT, text=" ", width=settings["hidwidth"], height=1, bg="thistle2", anchor=W)
labelCats= Label(root, justify=LEFT, text=" ", width=settings["hidwidth"], height=1, bg="thistle2", anchor=W)
labelScore = Label(root, justify=LEFT, text=" ", width=settings["hidwidth"], height=1, bg="thistle2", anchor=W)
labelLives = Label(root, justify=LEFT, text=" ", width=settings["hidwidth"], height=1, bg="thistle2", anchor=W)
canvas = Canvas(root, width=canvasSize[0], height=canvasSize[1], bd=0, highlightthickness=0, bg="lavender")

labelFast = Label(root, text="Fast", width=settings["effectwidth"], height=1, bg="PaleVioletRed1")
labelSlow = Label(root, text="Slow", width=settings["effectwidth"], height=1, bg="PaleGoldenrod")
labelGrav = Label(root, text="Grav", width=settings["effectwidth"], height=1, bg="turquoise1")
labelEffect = Label(root, text=" ", width=settings["effectwidth"], height=1, bg="MediumPurple1")


def clearbutt():
    newgameButt.place_forget()
    exitgameButt.place_forget()

def newgame():
    global Score, level
    level = 0
    Score = 0
    clearbutt()
    Level1()

def on_closing():                                                                   # Опрос закрытия
    global run
    if mb.askokcancel("Выход", "Вы уже уходите?"):
        print("Выход")
        run = False
        root.destroy()

newgameButt = Button(root, text="Новая игра", bg="khaki", width=16, height=1, font=("Comic Sans MS", 20),
                         command=newgame)
exitgameButt = Button(root, text="Выход", bg="khaki", width=16, height=1, font=("Comic Sans MS", 20),
                          command=on_closing)

"""Добавление элементов в окно"""
labelLevel.grid(row=0, column=0)
labelScore.grid(row=0, column=1)
labelCats.grid(row=0, column=2)
labelLives.grid(row=0, column=3)
canvas.grid(row=1, column=0, columnspan = 4)
statusbar.grid(row=2, column=0, columnspan = 4)

debugmode = IntVar() # Переменная из Tkinter для режима отладки
"""Изображения"""
def imgload(path):   # Функция загрузки изображений
    img = Image.open(path)
    output = ImageTk.PhotoImage(img)
    return output

mainmenuBackgroung = imgload(os.path.join('assets', 'graphics', 'background', 'menu_background.jpg')) # Главное меню
jungleBackgroung = imgload(os.path.join('assets', 'graphics', 'background', 'jungle_background.jpg')) # Фон джунглей
baseplatform = imgload(os.path.join('assets', 'graphics', 'platformbase.png'))      # Базовая платформа
ladder1 = imgload(os.path.join('assets', 'graphics', 'moving', 'ladder.png'))       # Лестница
wallImage = imgload(os.path.join('assets', 'graphics', 'wall.png'))                 # Стена

cats = [imgload(os.path.join('assets', 'graphics', 'cat', 'cat1.png')),              # Массив с котами
        imgload(os.path.join('assets', 'graphics', 'cat', 'cat2.png')),
        imgload(os.path.join('assets', 'graphics', 'cat', 'cat3.png'))]

mushroom = [imgload(os.path.join('assets', 'graphics', 'mushroom', 'fastroom.png')),
            imgload(os.path.join('assets', 'graphics', 'mushroom', 'slowroom.png')),
            imgload(os.path.join('assets', 'graphics', 'mushroom', 'gravroom.png'))]

bonusSeed = imgload(os.path.join('assets', 'graphics', 'bonus', 'bonusSeed.png'))

bonus = [imgload(os.path.join('assets', 'graphics', 'bonus', 'bonus0.png')),
        imgload(os.path.join('assets', 'graphics', 'bonus', 'bonus1.png')),
        imgload(os.path.join('assets', 'graphics', 'bonus', 'bonus2.png'))]

exitImage = [imgload(os.path.join('assets', 'graphics', 'exitflower_inactive.png')),  # Массив с цветком-выходом
             imgload(os.path.join('assets', 'graphics', 'exitflower_active.png'))]

grannyImage = imgload(os.path.join('assets', 'graphics', 'granny', 'granny_stand_forward.png'))            # Персонаж стоя
grannyFall = imgload(os.path.join('assets', 'graphics', 'granny', 'granny_fall.png'))                      # Персонаж падая
grannyStandRight = imgload(os.path.join('assets', 'graphics', 'granny', 'granny_stand_right.png'))         # Персонаж стоя лицом вправо
grannyStandLeft = imgload(os.path.join('assets', 'graphics', 'granny', 'granny_stand_left.png'))           # Персонаж стоя лицом влево
grannyWalkLeft = [imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_left_1.png')),         # Массив анимаций походки
                  imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_left_2.png')),         #   налево для персонажа
                  imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_left_3.png'))]
grannyWalkRight = [imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_right_1.png')),       # Массив анимаций походки
                  imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_right_2.png')),        #   направо для персонажа
                  imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_right_3.png'))]
grannyClimbUp = [imgload(os.path.join('assets', 'graphics', 'granny', 'granny_climb_up_1.png')),           # Массив анимаций забирания
                imgload(os.path.join('assets', 'graphics', 'granny', 'granny_climb_up_2.png')),            #   для персонажа
                imgload(os.path.join('assets', 'graphics', 'granny', 'granny_climb_up_3.png'))]
grannyClimbDown = imgload(os.path.join('assets', 'graphics', 'granny', 'granny_climb_down.png'))           # Персонаж спускается

"""Функции окон"""
def mainmenu_open():                                                                # Открытие главного меню
    global  labelLevel, labelLives, labelCats, labelScore, level
    level = 0
    canvas.create_image(320, 240, image=mainmenuBackgroung, tag="mainmenu")
    labelLevelText = " "
    labelLevel.config(text=labelLevelText)
    labelCatsText = " "
    labelCats.config(text=labelCatsText)
    labelScoreText = " "
    labelScore.config(text=labelScoreText)
    labelLivesText = " "
    labelLives.config(text=labelLivesText)
    newgameButt.place(x=195, y=260)
    exitgameButt.place(x=195, y=350)
    labelFast.place_forget()
    labelSlow.place_forget()
    labelGrav.place_forget()
    labelEffect.place_forget()
    print("Запуск")

def status():                                                                       # Обновление статуса
    if fall == True:
        FallStr="True"
    else: FallStr="False"
    if ladd == True:
        LaddStr="True"
    else: LaddStr="False"
    if vent == True:
        VentStr="True"
    else: VentStr="False"
    if barr == True:
        BarrStr="True"
    else: BarrStr="False"
    if flow == True:
        FlowStr="True"
    else: FlowStr="False"
    if head == True:
        HeadStr="True"
    else: HeadStr="False"
    CatStr = "%s из %s" % (CatAmountReal, CatAmountAll)
    GrannyPos = str(Hero.coords())
    if level !=0:
        labelLevelText = "Уровень: %i" % level
        labelLevel.config(text=labelLevelText)
        labelCatsText = "Коты: %s" % CatStr
        labelCats.config(text=labelCatsText)
        labelScoreText = "Счет: %i" % Score
        labelScore.config(text=labelScoreText)
        labelLivesText = "Жизни: %i" % lives
        labelLives.config(text=labelLivesText)

    if debugmode.get()==1:                                                          # Режим отладки
        message = "Fall:%s; Head:%s; Ladd:%s; Vent:%s; Barr:%s; Side:%s; Flow:%s; GrannyPos:%s; LastAnim:%s;" % (
                FallStr, HeadStr, LaddStr, VentStr, BarrStr, wallside, FlowStr, GrannyPos, lastanimation)
        if level==0:
            message = "Готов"
    elif level != 0:
        message = "Работаю"
    else:
        message = "Готов"
    statusbar.config(text = message)

def clearcanvas():  # Очистка зоны рисования
    canvas.delete("mainmenu")
    canvas.delete("ladder")
    canvas.delete("play")
    canvas.delete("platform")
    canvas.delete("cat")
    canvas.delete("wall")
    canvas.delete("bonus")
    canvas.delete("granny")
    canvas.delete("exit")

"""Классы"""
class Granny():     # Класс персонажа, которым мы управляем
    def __init__(self, spawncoords):
        self.id = canvas.create_image(spawncoords[0], spawncoords[1], image=grannyImage, tag="granny")
        self.x = spawncoords[0]
        self.y = spawncoords[1]
            # Обработка нажатий
        canvas.bind_all('<KeyPress-a>', self.turn_left)
        canvas.bind_all('<KeyPress-d>', self.turn_right)
        canvas.bind_all('<KeyPress-w>', self.turn_up)
        canvas.bind_all('<KeyPress-s>', self.turn_down)
        canvas.bind_all('<KeyPress-Left>', self.turn_left)
        canvas.bind_all('<KeyPress-Right>', self.turn_right)
        canvas.bind_all('<KeyPress-Up>', self.turn_up)
        canvas.bind_all('<KeyPress-Down>', self.turn_down)

    def coords(self):   # Массив с координатами
        coordsArray = [self.x, self.y]
        return coordsArray

    def actionzone(self):   # Зона действий
        actionArray = [self.x-25, self.x+25, self.y-30, self.y+30]
        return actionArray

    def turn_left(self, event): # Движение влево
        global isWalkingLeft
        if level !=  0:
            isWalkingLeft = True
            if (self.x > 30) & (wallside!="R"):
                canvas.move(self.id, -grannyWalkSpeed, 0)
                self.x -= grannyWalkSpeed

    def turn_right(self, event): # Движение вправо
        global isWalkingRight
        if level != 0:
            isWalkingRight = True
            if (self.x < 610) & (wallside!="L"):
                canvas.move(self.id, grannyWalkSpeed, 0)
                self.x += grannyWalkSpeed

    def turn_up(self, event): # Движение вверх до потолка
        global  isClimbingUp
        if level != 0:
            isClimbingUp = True
            if (self.y > 30) & ladd:
                canvas.move(self.id, 0, -grannyWalkSpeed)
                self.y -= grannyWalkSpeed

    def turn_down(self, event): # Движение вниз
        global isClimbingDown
        if level != 0:
            isClimbingDown = True
            if fall:
                canvas.move(self.id, 0, grannyWalkSpeed)
                self.y += grannyWalkSpeed

    def touch_place(self): # Массив точек касания нижней линии
        touch = [self.y + 30, self.x+5, self.x-5]
        return touch

    def touch_head(self): # Массив точек касания верхней линии
        head = [self.y - 30, self.x+5, self.x-5]
        return head

    def gravitymove(self):  # Движение под действием гравитации
        if ((self.y>30)&(head == False))|(gravitySpeed>0):
            canvas.move(self.id, 0, gravitySpeed)
            self.y += gravitySpeed

    def animate(self):      # Анимирование
        global lastanimation, lastanimationtime, lastWalkLeftImage, lastWalkRightImage, lastClimbUpImage,\
            isWalkingRight, isWalkingLeft, isClimbingUp, isClimbingDown
        if (time.time()-lastanimationtime)>animationduration:   # Если прошла задержка
            # Анимации после движений
            if lastanimation == "WalkRight":
                canvas.itemconfig(self.id, image=grannyStandRight)
            if lastanimation == "WalkLeft":
                canvas.itemconfig(self.id, image=grannyStandLeft)
            if lastanimation == "Stand":
                canvas.itemconfig(self.id, image=grannyImage)
            if lastanimation == "Climbing":
                canvas.itemconfig(self.id, image=grannyClimbUp[1])
            # Анимации во время движений
            if isWalkingRight:
                if lastWalkRightImage == 3: lastWalkRightImage =0
                canvas.itemconfig(self.id, image=grannyWalkRight[lastWalkRightImage])
                lastWalkRightImage +=1
                isWalkingRight=False
                lastanimation = "WalkRight"
            if isWalkingLeft:
                if lastWalkLeftImage == 3: lastWalkLeftImage = 0
                canvas.itemconfig(self.id, image=grannyWalkLeft[lastWalkLeftImage])
                lastWalkLeftImage += 1
                isWalkingLeft=False
                lastanimation = "WalkLeft"
            if (ladd == True) & fall:
                if isClimbingUp:
                    if lastClimbUpImage == 3: lastClimbUpImage = 0
                    canvas.itemconfig(self.id, image=grannyClimbUp[lastClimbUpImage])
                    lastClimbUpImage += 1
                    isClimbingUp = False
                    lastanimation = "Climbing"
                    if (ladd == False)|(fall == False):
                        lastanimation ="Stand"

                if isClimbingDown:
                    canvas.itemconfig(self.id, image=grannyClimbDown)
                    isClimbingDown = False
                    lastanimation = "Climbing"
                    if (ladd == False)|(fall == False):
                        lastanimation ="Stand"
            # Падение
            if fall & (ladd == False):
                canvas.itemconfig(self.id, image=grannyFall)
                isWalkingLeft = False
                isWalkingRight = False
                lastanimation = "Stand"
            # Обновляем таймер кадра
            lastanimationtime = time.time()

class PlatformBase():   # Класс базовой платформы, которая присутствует на всех уровнях
    def __init__(self):
        self.avaible = True
        self.id = canvas.create_image(320, 465, image=baseplatform, tag="platform")

    def touch_place(self): # Массив точек касания верхней линии
        touch = [450, 0, 640]
        return touch

class PlatformSimple():     # Класс обычной платформы, масштабируется и изменяется для каждого уровня
    def __init__(self,coordsArray):
        self.coords = coordsArray
        self.avaible = True
        self.id = canvas.create_rectangle(self.coords[1], self.coords[0], self.coords[2], self.coords[0]+ 30,
                                          fill="#a2653e", tag="platform")

    def touch_place(self):  # Массив точек касания верхней линии
        touch=[self.coords[0], self.coords[1], self.coords[2]]
        return touch

    def touch_head(self):  # Массив точек касания нижней линии
        head=[self.coords[0]+30, self.coords[1], self.coords[2]]
        return head

class Wall():
    # Ширина 32, Высота 64
    def __init__(self, coordsArray):
        self.coords = coordsArray
        self.avaible = True
        self.centre = [self.coords[0] + 16, self.coords[1] + 32]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=wallImage, tag="wall")
    def actionzone(self):   # Зона активности (совершения действий)
        actionArray = [self.centre[0]-30, self.centre[0]+30, self.centre[1]-32, self.centre[1]+32]
        return actionArray

class Ladder():     # Класс лестницы, позволяет забираться на верх
    # Ширина 50, Высота 120
    def __init__(self, coordsArray): # ax by (Верхний левый угол)
        self.coords = coordsArray
        self.avaible = True
        self.centre = [self.coords[0]+25, self.coords[1]+60]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=ladder1, tag="ladder")
    def actionzone(self):   # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 10, self.centre[0]+10, self.centre[1] - 60, self.centre[1] + 60]
        return actionArray

class Cat():    # Класс котика, которых мы спасаем
    # Ширина 24, Высота 32
    def __init__(self, coordsArray):  # ax by (Верхний левый угол)
        self.coords = coordsArray
        self.centre = [self.coords[0] + 12, self.coords[1] + 16]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=random.choice(cats), tag="cat")
        self.avaible = True

    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 12, self.centre[0] + 12, self.centre[1] - 16, self.centre[1] + 16]
        return actionArray

    def collect(self):  # Собрать котика
        global Score
        self.avaible = False
        Score += ScoreAddCat  # Зачисляем очки
        canvas.delete(self.id)

class BonusFlower():
    # Ширина 32, Высота 36
    def __init__(self, coordsArray):  # ax by (Верхний левый угол)
        self.coords = coordsArray
        self.centre = [self.coords[0] + 16, self.coords[1] + 18]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=bonusSeed, tag="bonus")
        self.avaible = True
    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 25, self.centre[0] + 16, self.centre[1] - 18, self.centre[1] + 18]
        return actionArray
    def rise(self):
        global Score
        self.avaible = False
        Score += ScoreAddBonus
        canvas.itemconfig(self.id, image=random.choice(bonus))

class Fastroom():
    # Ширина 24, Высота 24
    def __init__(self, coordsArray):  # ax by (Верхний левый угол)
        self.coords = coordsArray
        self.centre = [self.coords[0] + 12, self.coords[1] + 12]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=mushroom[0], tag="mushroom")
        self.avaible = True
    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 12, self.centre[0] + 12, self.centre[1] - 12, self.centre[1] + 12]
        return actionArray
    def effect(self):
        global isFastEffect
        isFastEffect = True

class Slowroom():
    # Ширина 24, Высота 24
    def __init__(self, coordsArray):  # ax by (Верхний левый угол)
        self.coords = coordsArray
        self.centre = [self.coords[0] + 12, self.coords[1] + 12]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=mushroom[1], tag="mushroom")
        self.avaible = True

    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 12, self.centre[0] + 12, self.centre[1] - 12, self.centre[1] + 12]
        return actionArray

    def effect(self):
        global isSlowEffect
        isSlowEffect = True

class Gravroom():
    # Ширина 24, Высота 24
    def __init__(self, coordsArray):  # ax by (Верхний левый угол)
        self.coords = coordsArray
        self.centre = [self.coords[0] + 12, self.coords[1] + 12]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=mushroom[2], tag="mushroom")
        self.avaible = True

    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 12, self.centre[0] + 12, self.centre[1] - 12, self.centre[1] + 12]
        return actionArray

    def effect(self):
        global isGravEffect
        isGravEffect = True

class Savage():
    pass

class ExitFlower():     # Класс цветка-выхода
    # Ширина 60, Высота 60
    def __init__(self, coordsArray): # ax by (Верхний левый угол)
        self.coords = coordsArray
        self.avaible = True
        self.centre = [self.coords[0]+30, self.coords[1]+30]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=exitImage[0], tag="exit")
    def actionzone(self):   # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 30, self.centre[0] + 30, self.centre[1] - 30, self.centre[1] + 30]
        return actionArray
    def opening(self):      # Открытие цветка
        canvas.itemconfig(self.id, image=exitImage[1])

class Empty():
    def __init__(self):
        self.avaible = False

"""Уровни"""
def LevelInit():
    clearbutt()
    clearcanvas()
    global Hero, Base, Exit, CatAmountReal, CatAmountAll, alphaPlatform, betaPlatform, gammaPlatform, deltaPlatform, epsilonPlatform, zetaPlatform, etaPlatform, thetaPlatform, iotaPlatform, alphaCat, betaCat, gammaCat, deltaCat, epsilonCat, zetaCat, alphaBonus, betaBonus, gammaBonus, deltaBonus, epsilonBonus, zetaBonus, alphaLadder, betaLadder, gammaLadder, deltaLadder, epsilonLadder, zetaLadder, alphaWall, betaWall, gammaWall, deltaWall, epsilonWall, zetaWall, alphaSavage, betaSavage, gammaSavage, deltaSavage, alphaFastroom, betaFastroom, alphaSlowroom, betaSlowroom, alphaGravroom, betaGravroom
    canvas.create_image(320, 240, image=jungleBackgroung, tag="play")
    Base = PlatformBase()
    Exit = ExitFlower(settings['levels'][level]['exitCoords'])
    CatAmountAll = settings['levels'][level]['CatAmountAll']
    CatAmountReal = settings['levels'][level]['CatAmountReal']
    """Платформы"""
    if settings['levels'][level]['alphaPlatformFlag']:
        alphaPlatform = PlatformSimple(settings['levels'][level]['alphaPlatformCoords'])
    else: alphaPlatform = Empty()
    if settings['levels'][level]['betaPlatformFlag']:
        betaPlatform = PlatformSimple(settings['levels'][level]['betaPlatformCoords'])
    else:
        betaPlatform = Empty()
    if settings['levels'][level]['gammaPlatformFlag']:
        gammaPlatform = PlatformSimple(settings['levels'][level]['gammaPlatformCoords'])
    else:
        gammaPlatform = Empty()
    if settings['levels'][level]['deltaPlatformFlag']:
        deltaPlatform = PlatformSimple(settings['levels'][level]['deltaPlatformCoords'])
    else:
        deltaPlatform = Empty()
    if settings['levels'][level]['epsilonPlatformFlag']:
        epsilonPlatform = PlatformSimple(settings['levels'][level]['epsilonPlatformCoords'])
    else:
        epsilonPlatform = Empty()
    if settings['levels'][level]['zetaPlatformFlag']:
        zetaPlatform = PlatformSimple(settings['levels'][level]['zetaPlatformCoords'])
    else:
        zetaPlatform = Empty()
    if settings['levels'][level]['etaPlatformFlag']:
        etaPlatform = PlatformSimple(settings['levels'][level]['etaPlatformCoords'])
    else:
        etaPlatform = Empty()
    if settings['levels'][level]['thetaPlatformFlag']:
        thetaPlatform = PlatformSimple(settings['levels'][level]['thetaPlatformCoords'])
    else:
        thetaPlatform = Empty()
    if settings['levels'][level]['iotaPlatformFlag']:
        iotaPlatform = PlatformSimple(settings['levels'][level]['iotaPlatformCoords'])
    else:
        iotaPlatform = Empty()

    """Коты"""
    if settings['levels'][level]['alphaCatFlag']:
        alphaCat = Cat(settings['levels'][level]['alphaCatCoords'])
    else: alphaCat = Empty()
    if settings['levels'][level]['betaCatFlag']:
        betaCat = Cat(settings['levels'][level]['betaCatCoords'])
    else:
        betaCat = Empty()
    if settings['levels'][level]['gammaCatFlag']:
        gammaCat = Cat(settings['levels'][level]['gammaCatCoords'])
    else:
        gammaCat = Empty()
    if settings['levels'][level]['deltaCatFlag']:
        deltaCat = Cat(settings['levels'][level]['deltaCatCoords'])
    else:
        deltaCat = Empty()
    if settings['levels'][level]['epsilonCatFlag']:
        epsilonCat = Cat(settings['levels'][level]['epsilonCatCoords'])
    else:
        epsilonCat = Empty()
    if settings['levels'][level]['zetaCatFlag']:
        zetaCat = Cat(settings['levels'][level]['zetaCatCoords'])
    else:
        zetaCat = Empty()

    """Цветочки"""
    if settings['levels'][level]['alphaBonusFlag']:
        alphaBonus = BonusFlower(settings['levels'][level]['alphaBonusCoords'])
    else: alphaBonus = Empty()
    if settings['levels'][level]['betaBonusFlag']:
        betaBonus = BonusFlower(settings['levels'][level]['betaBonusCoords'])
    else:
        betaBonus = Empty()
    if settings['levels'][level]['gammaBonusFlag']:
        gammaBonus = BonusFlower(settings['levels'][level]['gammaBonusCoords'])
    else:
        gammaBonus = Empty()
    if settings['levels'][level]['deltaBonusFlag']:
        deltaBonus = BonusFlower(settings['levels'][level]['deltaBonusCoords'])
    else:
        deltaBonus = Empty()
    if settings['levels'][level]['epsilonBonusFlag']:
        epsilonBonus = BonusFlower(settings['levels'][level]['epsilonBonusCoords'])
    else:
        epsilonBonus = Empty()
    if settings['levels'][level]['zetaBonusFlag']:
        zetaBonus = BonusFlower(settings['levels'][level]['zetaBonusCoords'])
    else:
        zetaBonus = Empty()

    """Лестницы"""
    if settings['levels'][level]['alphaLadderFlag']:
        alphaLadder = Ladder(settings['levels'][level]['alphaLadderCoords'])
    else:
        alphaLadder = Empty()
    if settings['levels'][level]['betaLadderFlag']:
        betaLadder = Ladder(settings['levels'][level]['betaLadderCoords'])
    else:
        betaLadder = Empty()
    if settings['levels'][level]['gammaLadderFlag']:
        gammaLadder = Ladder(settings['levels'][level]['gammaLadderCoords'])
    else:
        gammaLadder = Empty()
    if settings['levels'][level]['deltaLadderFlag']:
        deltaLadder = Ladder(settings['levels'][level]['deltaLadderCoords'])
    else:
        deltaLadder = Empty()
    if settings['levels'][level]['epsilonLadderFlag']:
        epsilonLadder = Ladder(settings['levels'][level]['epsilonLadderCoords'])
    else:
        epsilonLadder = Empty()
    if settings['levels'][level]['zetaLadderFlag']:
        zetaLadder = Ladder(settings['levels'][level]['zetaLadderCoords'])
    else:
        zetaLadder = Empty()

    """Стены"""
    if settings['levels'][level]['alphaWallFlag']:
        alphaWall = Wall(settings['levels'][level]['alphaWallCoords'])
    else:
        alphaWall = Empty()
    if settings['levels'][level]['betaWallFlag']:
        betaWall = Wall(settings['levels'][level]['betaWallCoords'])
    else:
        betaWall = Empty()
    if settings['levels'][level]['gammaWallFlag']:
        gammaWall = Wall(settings['levels'][level]['gammaWallCoords'])
    else:
        gammaWall = Empty()
    if settings['levels'][level]['deltaWallFlag']:
        deltaWall = Wall(settings['levels'][level]['deltaWallCoords'])
    else:
        deltaWall = Empty()
    if settings['levels'][level]['epsilonWallFlag']:
        epsilonWall = Wall(settings['levels'][level]['epsilonWallCoords'])
    else:
        epsilonWall = Empty()
    if settings['levels'][level]['zetaWallFlag']:
        zetaWall = Wall(settings['levels'][level]['zetaWallCoords'])
    else:
        zetaWall = Empty()

    """Туземец"""
    if settings['levels'][level]['alphaSavageFlag']:
        alphaSavage = Savage(settings['levels'][level]['alphaSavageCoords'])
    else:
        alphaSavage = Empty()
    if settings['levels'][level]['betaSavageFlag']:
        betaSavage = Savage(settings['levels'][level]['betaSavageCoords'])
    else:
        betaSavage = Empty()
    if settings['levels'][level]['gammaSavageFlag']:
        gammaSavage = Savage(settings['levels'][level]['gammaSavageCoords'])
    else:
        gammaSavage = Empty()
    if settings['levels'][level]['deltaSavageFlag']:
        deltaSavage = Savage(settings['levels'][level]['deltaSavageCoords'])
    else:
        deltaSavage = Empty()

    """Быстромор"""
    if settings['levels'][level]['alphaFastroomFlag']:
        alphaFastroom = Fastroom(settings['levels'][level]['alphaFastroomCoords'])
    else:
        alphaFastroom = Empty()
    if settings['levels'][level]['betaFastroomFlag']:
        betaFastroom = Fastroom(settings['levels'][level]['betaFastroomCoords'])
    else:
        betaFastroom = Empty()

    """Медлянка"""
    if settings['levels'][level]['alphaSlowroomFlag']:
        alphaSlowroom = Slowroom(settings['levels'][level]['alphaSlowroomCoords'])
    else:
        alphaSlowroom = Empty()
    if settings['levels'][level]['betaSlowroomFlag']:
        betaSlowroom = Slowroom(settings['levels'][level]['betaSlowroomCoords'])
    else:
        betaSlowroom = Empty()

    """Вверхшенка"""
    if settings['levels'][level]['alphaGravroomFlag']:
        alphaGravroom = Gravroom(settings['levels'][level]['alphaGravroomCoords'])
    else:
        alphaGravroom = Empty()
    if settings['levels'][level]['betaGravroomFlag']:
        betaGravroom = Gravroom(settings['levels'][level]['betaGravroomCoords'])
    else:
        betaGravroom = Empty()

    Hero = Granny(spawncoords=settings['levels'][level]['spawnCoords'])

def Level1():   # Создаем объекты уровня
    global level
    level = 1
    LevelInit()

def Level2():   # Создаем объекты уровня
    global level
    level = 2
    LevelInit()

def Level3():  # Создаем объекты уровня
    pass

def Level4():  # Создаем объекты уровня
    pass

def Level5():  # Создаем объекты уровня
    pass

"""Доп. Функции"""
# Общая проверка по массивам
def action_check(Grannyzone, Actionzone, Index):   # Проверка выхода по массивам
    solution = False
    if (Grannyzone[0]+Index >= Actionzone[0]) & (Grannyzone[0]+Index <= Actionzone[1]):
        if (Grannyzone[2] >= Actionzone[2]) & (Grannyzone[2] <= Actionzone[3]):
            solution = True
        if (Grannyzone[3] >= Actionzone[2]) & (Grannyzone[3] <= Actionzone[3]):
            solution = True
    if (Grannyzone[1]-Index >= Actionzone[0]) & (Grannyzone[1]-Index <= Actionzone[1]):
        if (Grannyzone[2] >= Actionzone[2]) & (Grannyzone[2] <= Actionzone[3]):
            solution = True
        if (Grannyzone[3] >= Actionzone[2]) & (Grannyzone[3] <= Actionzone[3]):
            solution = True
    return solution

# Платформа
def grannyoverplatform():  # Определение платформ на уровнях !!!Не забывать добавлять!!!
    globalsolution = True
    solutionAlpha = True
    solutionBeta = True
    solutionGamma = True
    solutionDelta = True
    solutionEpsilon = True
    solutionZeta = True
    solutionEta = True
    solutionTheta = True
    solutionIota = True
    GrannyTouch = Hero.touch_place()
    BaseTouch = Base.touch_place()
    solutionBase = ground_check(GrannyTouch, BaseTouch)
    if alphaPlatform.avaible:
        AlphaTouch = alphaPlatform.touch_place()
        solutionAlpha = ground_check(GrannyTouch, AlphaTouch)
    if betaPlatform.avaible:
        BetaTouch = betaPlatform.touch_place()
        solutionBeta = ground_check(GrannyTouch, BetaTouch)
    if gammaPlatform.avaible:
        GammaTouch = gammaPlatform.touch_place()
        solutionGamma = ground_check(GrannyTouch, GammaTouch)
    if deltaPlatform.avaible:
        DeltaTouch = deltaPlatform.touch_place()
        solutionDelta = ground_check(GrannyTouch, DeltaTouch)
    if epsilonPlatform.avaible:
        EpsilonTouch = epsilonPlatform.touch_place()
        solutionEpsilon = ground_check(GrannyTouch, EpsilonTouch)
    if zetaPlatform.avaible:
        ZetaTouch = zetaPlatform.touch_place()
        solutionZeta = ground_check(GrannyTouch, ZetaTouch)
    if etaPlatform.avaible:
        EtaTouch = etaPlatform.touch_place()
        solutionEta = ground_check(GrannyTouch, EtaTouch)
    if thetaPlatform.avaible:
        ThetaTouch = thetaPlatform.touch_place()
        solutionTheta = ground_check(GrannyTouch, ThetaTouch)
    if iotaPlatform.avaible:
        IotaTouch = iotaPlatform.touch_place()
        solutionIota = ground_check(GrannyTouch, IotaTouch)

    if (solutionBase == False)|(solutionAlpha == False)|(solutionBeta == False)|(solutionGamma == False)|(solutionDelta== False)|(solutionEpsilon == False)|(solutionZeta == False)|(solutionEta == False)|(solutionTheta == False)|(solutionIota == False):
        globalsolution = False
    return globalsolution
def ground_check(GrannyTouch, PlatformTouch): # Проверка земли под ногами по массивам
    solution = True
    if PlatformTouch[0] == GrannyTouch[0]:
        if (GrannyTouch[1] >= PlatformTouch[1]) & (GrannyTouch[1] <= PlatformTouch[2]):
            solution = False
        if (GrannyTouch[2] >= PlatformTouch[1]) & (GrannyTouch[2] <= PlatformTouch[2]):
            solution = False
    return solution

def grannyunderplatform():  # Определение платформ на уровнях !!!Не забывать добавлять!!!
    globalsolution = True
    solutionAlpha = True
    solutionBeta = True
    solutionGamma = True
    solutionDelta = True
    solutionEpsilon = True
    solutionZeta = True
    solutionEta = True
    solutionTheta = True
    solutionIota = True
    GrannyTouch = Hero.touch_head()
    if alphaPlatform.avaible:
        AlphaTouch = alphaPlatform.touch_head()
        solutionAlpha = head_check(GrannyTouch, AlphaTouch)
    if betaPlatform.avaible:
        BetaTouch = betaPlatform.touch_head()
        solutionBeta = head_check(GrannyTouch, BetaTouch)
    if gammaPlatform.avaible:
        GammaTouch = gammaPlatform.touch_head()
        solutionGamma = head_check(GrannyTouch, GammaTouch)
    if deltaPlatform.avaible:
        DeltaTouch = deltaPlatform.touch_head()
        solutionDelta = head_check(GrannyTouch, DeltaTouch)
    if epsilonPlatform.avaible:
        EpsilonTouch = epsilonPlatform.touch_head()
        solutionEpsilon = head_check(GrannyTouch, EpsilonTouch)
    if zetaPlatform.avaible:
        ZetaTouch = zetaPlatform.touch_head()
        solutionZeta = head_check(GrannyTouch, ZetaTouch)
    if etaPlatform.avaible:
        EtaTouch = etaPlatform.touch_head()
        solutionEta = head_check(GrannyTouch, EtaTouch)
    if thetaPlatform.avaible:
        ThetaTouch = thetaPlatform.touch_head()
        solutionTheta = head_check(GrannyTouch, ThetaTouch)
    if iotaPlatform.avaible:
        IotaTouch = iotaPlatform.touch_head()
        solutionIota = head_check(GrannyTouch, IotaTouch)

    if (solutionAlpha == False)|(solutionBeta == False)|(solutionGamma == False)|(solutionDelta== False)|(solutionEpsilon == False)|(solutionZeta == False)|(solutionEta == False)|(solutionTheta == False)|(solutionIota == False):
        globalsolution = False
    return globalsolution
def head_check(GrannyTouch, PlatformTouch): # Проверка земли над головой по массивам
    solution = False
    if PlatformTouch[0] == GrannyTouch[0]:
        if (GrannyTouch[1] >= PlatformTouch[1]) & (GrannyTouch[1] <= PlatformTouch[2]):
            solution = True
        if (GrannyTouch[2] >= PlatformTouch[1]) & (GrannyTouch[2] <= PlatformTouch[2]):
            solution = True
    return solution

# Лестницы
def grannyonladder(): # Определение лестниц на уровне !!!Не забывать добавлять!!!
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    Grannyzone = Hero.actionzone()
    if alphaLadder.avaible:
        Alphazone = alphaLadder.actionzone()
        solutionAlpha = action_check(Grannyzone, Alphazone, 15)
    if betaLadder.avaible:
        Betazone = betaLadder.actionzone()
        solutionBeta = action_check(Grannyzone, Betazone, 15)
    if gammaLadder.avaible:
        Gammazone = gammaLadder.actionzone()
        solutionGamma = action_check(Grannyzone, Gammazone, 15)
    if deltaLadder.avaible:
        Deltazone = deltaLadder.actionzone()
        solutionDelta = action_check(Grannyzone, Deltazone, 15)
    if epsilonLadder.avaible:
        Epsilonzone = epsilonLadder.actionzone()
        solutionEpsilon = action_check(Grannyzone, Epsilonzone, 15)
    if zetaLadder.avaible:
        Zetazone = zetaLadder.actionzone()
        solutionZeta = action_check(Grannyzone, Zetazone, 15)

    if (solutionAlpha == True) | (solutionBeta == True) |(solutionGamma == True) |(solutionDelta == True) |(solutionEpsilon == True) |(solutionZeta == True):
        globalsolution = True

    return globalsolution

# Котики
def grannycarrycat(): # Определение котов на уровне !!!Не забывать добавлять!!!
    global CatAmountReal
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    Grannyzone = Hero.actionzone()
    if alphaCat.avaible:
        Alphazone = alphaCat.actionzone()
        solutionAlpha = action_check(Grannyzone, Alphazone, 10)
        if solutionAlpha == True:
            alphaCat.collect()
            CatAmountReal += 1
    if betaCat.avaible:
        Betazone = betaCat.actionzone()
        solutionBeta = action_check(Grannyzone, Betazone, 10)
        if solutionBeta == True:
            betaCat.collect()
            CatAmountReal += 1
    if gammaCat.avaible:
        Gammazone = gammaCat.actionzone()
        solutionGamma = action_check(Grannyzone, Gammazone, 10)
        if solutionGamma == True:
            gammaCat.collect()
            CatAmountReal += 1
    if deltaCat.avaible:
        Deltazone = deltaCat.actionzone()
        solutionDelta = action_check(Grannyzone, Deltazone, 10)
        if solutionDelta == True:
            deltaCat.collect()
            CatAmountReal += 1
    if epsilonCat.avaible:
        Epsilonzone = epsilonCat.actionzone()
        solutionEpsilon = action_check(Grannyzone, Epsilonzone, 10)
        if solutionEpsilon == True:
            epsilonCat.collect()
            CatAmountReal += 1
    if zetaCat.avaible:
        Zetazone = zetaCat.actionzone()
        solutionZeta = action_check(Grannyzone, Zetazone, 10)
        if solutionZeta == True:
            zetaCat.collect()
            CatAmountReal += 1
    if (solutionAlpha == True) | (solutionBeta == True) | (solutionGamma == True) | (solutionDelta == True) | (solutionEpsilon == True) | (solutionZeta == True):
        globalsolution = True

    return globalsolution
# Цветочки
def grannygetbonus(): # Определение цветочков на уровне !!!Не забывать добавлять!!!
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    Grannyzone = Hero.actionzone()
    if alphaBonus.avaible:
        Alphazone = alphaBonus.actionzone()
        solutionAlpha = action_check(Grannyzone, Alphazone, 16)
        if solutionAlpha == True:
            alphaBonus.rise()
    if betaBonus.avaible:
        Betazone = betaBonus.actionzone()
        solutionBeta = action_check(Grannyzone, Betazone, 16)
        if solutionBeta == True:
            betaBonus.rise()
    if gammaBonus.avaible:
        Gammazone = gammaBonus.actionzone()
        solutionGamma = action_check(Grannyzone, Gammazone, 16)
        if solutionGamma == True:
            gammaBonus.rise()
    if deltaBonus.avaible:
        Deltazone = deltaBonus.actionzone()
        solutionDelta = action_check(Grannyzone, Deltazone, 16)
        if solutionDelta == True:
            deltaBonus.rise()
    if epsilonBonus.avaible:
        Epsilonzone = epsilonBonus.actionzone()
        solutionEpsilon = action_check(Grannyzone, Epsilonzone, 16)
        if solutionEpsilon == True:
            epsilonBonus.rise()
    if zetaBonus.avaible:
        Zetazone = zetaBonus.actionzone()
        solutionZeta = action_check(Grannyzone, Zetazone, 16)
        if solutionZeta == True:
            zetaCat.rise()
    if (solutionAlpha == True) | (solutionBeta == True) | (solutionGamma == True) | (solutionDelta == True) | (solutionEpsilon == True) | (solutionZeta == True):
        globalsolution = True

    return globalsolution

# Грибочки
def grannyfastroom():
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    Grannyzone = Hero.actionzone()
    if alphaFastroom.avaible:
        Alphazone = alphaFastroom.actionzone()
        solutionAlpha = action_check(Grannyzone, Alphazone, 12)
        if solutionAlpha == True:
            alphaFastroom.effect()
    if betaFastroom.avaible:
        Betazone = betaFastroom.actionzone()
        solutionBeta = action_check(Grannyzone, Betazone, 12)
        if solutionBeta == True:
            betaFastroom.effect()
    if (solutionAlpha == True) | (solutionBeta == True):
        globalsolution = True

    return globalsolution

def grannyslowroom():
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    Grannyzone = Hero.actionzone()
    if alphaSlowroom.avaible:
        Alphazone = alphaSlowroom.actionzone()
        solutionAlpha = action_check(Grannyzone, Alphazone, 12)
        if solutionAlpha == True:
            alphaSlowroom.effect()
    if betaSlowroom.avaible:
        Betazone = betaSlowroom.actionzone()
        solutionBeta = action_check(Grannyzone, Betazone, 12)
        if solutionBeta == True:
            betaSlowroom.effect()
    if (solutionAlpha == True) | (solutionBeta == True):
        globalsolution = True

    return globalsolution

def grannygravroom():
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    Grannyzone = Hero.actionzone()
    if alphaGravroom.avaible:
        Alphazone = alphaGravroom.actionzone()
        solutionAlpha = action_check(Grannyzone, Alphazone, 12)
        if solutionAlpha == True:
            alphaGravroom.effect()
    if betaGravroom.avaible:
        Betazone = betaGravroom.actionzone()
        solutionBeta = action_check(Grannyzone, Betazone, 12)
        if solutionBeta == True:
            betaGravroom.effect()
    if (solutionAlpha == True) | (solutionBeta == True):
        globalsolution = True

    return globalsolution

# Выход
def grannyinexit(): # Определение выхода на уровне
    globalsolution = False
    if level != 0:
        Grannyzone = Hero.actionzone()
        Exitzone = Exit.actionzone()
        globalsolution = action_check(Grannyzone, Exitzone, 30)
    return globalsolution

# Стены
def grannyandwall(): # Определение стен на уровне !!!Не забывать добавлять!!!
    global wallside
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    Grannyzone = Hero.actionzone()
    if alphaWall.avaible:
        Alphazone = alphaWall.actionzone()
        solutionAlpha = wall_check(Grannyzone, Alphazone)
    if betaWall.avaible:
        Betazone = betaWall.actionzone()
        solutionBeta = wall_check(Grannyzone, Betazone)
    if gammaWall.avaible:
        Gammazone = gammaWall.actionzone()
        solutionGamma = wall_check(Grannyzone, Gammazone)
    if deltaWall.avaible:
        Deltazone = deltaWall.actionzone()
        solutionDelta = wall_check(Grannyzone, Deltazone)
    if epsilonWall.avaible:
        Epsilonzone = epsilonWall.actionzone()
        solutionEpsilon = wall_check(Grannyzone, Epsilonzone)
    if zetaWall.avaible:
        Zetazone = zetaWall.actionzone()
        solutionZeta = wall_check(Grannyzone, Zetazone)
    if (solutionAlpha == True) | (solutionBeta == True) | (solutionGamma == True) | (solutionDelta == True) | (solutionEpsilon == True) | (solutionZeta == True):
        globalsolution = True

    if globalsolution==False:
        wallside = "0"

    return globalsolution
def wall_check(Grannyzone, Wallzone):   # Проверка стен по массивам
    global wallside
    wallside="0"
    solution = False
    if (Grannyzone[0]+16 >= Wallzone[0]) & (Grannyzone[0]+16 <= Wallzone[1]):
        if (Grannyzone[2] >= Wallzone[2]) & (Grannyzone[2] <= Wallzone[3]):
            solution = True
        if (Grannyzone[3] >= Wallzone[2]) & (Grannyzone[3] <= Wallzone[3]):
            wallside="R"
            solution = True
    if (Grannyzone[1]-16 >= Wallzone[0]) & (Grannyzone[1]-16 <= Wallzone[1]):
        if (Grannyzone[2] >= Wallzone[2]) & (Grannyzone[2] <= Wallzone[3]):
            solution = True
        if (Grannyzone[3] >= Wallzone[2]) & (Grannyzone[3] <= Wallzone[3]):
            wallside="L"
            solution = True
    return solution

def gravity(): # Если персонаж не на платформн и не на лестнице, на нее действует гравитация
    if (fall & (ladd == False))|(antigrav == True):
        Hero.gravitymove()

def effects():
    global isFastEffect, isSlowEffect, isGravEffect, lasteffecttime, gravitySpeed, grannyWalkSpeed, antigrav
    if isFastEffect:
        grannyWalkSpeed = grannyWalkSpeedFast
        lasteffecttime = time.time()
        labelFast.place(x=500, y=475)
        labelEffect.place(x=460, y=475)
        labelSlow.place_forget()
        labelGrav.place_forget()
        isFastEffect = False
    if isSlowEffect:
        grannyWalkSpeed = grannyWalkSpeedSlow
        lasteffecttime = time.time()
        labelSlow.place(x=540, y=475)
        labelEffect.place(x=460, y=475)
        labelFast.place_forget()
        labelGrav.place_forget()
        isSlowEffect = False
    if isGravEffect:
        gravitySpeed = gravitySpeedInvert
        lasteffecttime = time.time()
        labelGrav.place(x=580, y=475)
        labelEffect.place(x=460, y=475)
        labelFast.place_forget()
        labelSlow.place_forget()
        antigrav = True
        isGravEffect = False
    if (time.time()-lasteffecttime<effectduration):
        TimeStr = "%.2f с" % (effectduration-(time.time()-lasteffecttime))
        labelEffect.config(text=TimeStr)
    if (isFastEffect==False)&(isSlowEffect==False)&(isGravEffect==False)&(time.time()-lasteffecttime>=effectduration):
        labelFast.place_forget()
        labelSlow.place_forget()
        labelGrav.place_forget()
        labelEffect.place_forget()
        antigrav = False
        grannyWalkSpeed = grannyWalkSpeedNormal
        gravitySpeed = gravitySpeedNormal

def LevelAdd(): # Логика переключения
    global level
    if level == 1:
        level = 2
        LevelInit()
    elif level == 2:
        endgame()

def recquecountertoexit():  # Проверка на сбор котиков. Открытие цветка и выход с уровня
    global isExitActive
    if CatAmountReal == CatAmountAll:
        isExitActive = True
        Exit.opening()
        if grannyinexit() == True:
            LevelAdd()
    else:
        isExitActive = False

def endgame():
    global level, Score
    if 1:
        level = 0
        message = "Поздравляем с победой! \nВы набрали %i из %i очков" % (Score, ScoreMax)
        mb.showinfo(title="Победа", message=message)
        Score = 0
        mainmenu_open()

# Главный цикл
def menu(): # Описание меню(сверху полоска)
    mainmenu = Menu(root)
    gamemenu = Menu(mainmenu, tearoff=0, bg="thistle2")
    gamemenu.add_command(label="Новая игра", command=newgame)
    levelmenu = Menu(gamemenu, tearoff=1, bg="thistle2")
    levelmenu.add_command(label="Уровень 1", command=Level1)
    levelmenu.add_command(label="Уровень 2", command=Level2)
    levelmenu.add_command(label="Уровень 3", command=Level3)
    levelmenu.add_command(label="Уровень 4", command=Level4)
    levelmenu.add_command(label="Уровень 5", command=Level5)
    gamemenu.add_cascade(label="Уровни", menu=levelmenu)
    gamemenu.add_separator()
    optionmenu = Menu(gamemenu, tearoff=1, bg="thistle2")
    optionmenu.add_checkbutton(label="Отладка",onvalue=1, offvalue=0, variable=debugmode)
    gamemenu.add_cascade(label="Настройки", menu=optionmenu)
    gamemenu.add_separator()
    gamemenu.add_command(label="Выход", command=on_closing)
    aboutmenu = Menu(mainmenu, tearoff=0, bg="thistle2")
    aboutmenu.add_command(label="Авторы", command=lambda: mb.showinfo(title="Авторы", message=authorsmessage))
    aboutmenu.add_command(label="Об игре", command=lambda: mb.showinfo(title="Авторы", message=aboutmessage))
    mainmenu.add_cascade(label="Игра", menu=gamemenu)
    mainmenu.add_cascade(label="Справка", menu=aboutmenu)
    root.config(menu=mainmenu)

menu()  # Создаем меню
mainmenu_open() # Запускаем заглавный экран
root.protocol("WM_DELETE_WINDOW", on_closing)   # Обработка выхода при нажатии на крестик
while run:
    if level != 0:
        fall = grannyoverplatform()    # Определяем основные переменные
        ladd = grannyonladder()
        carr = grannycarrycat()
        vent = grannyinexit()
        barr = grannyandwall()
        flow = grannygetbonus()
        fast = grannyfastroom()
        grav = grannygravroom()
        slow = grannyslowroom()
        head = grannyunderplatform()
        effects()
        recquecountertoexit()           # Делаем проверку готовность выйти с уровня
        gravity()                       # Применяем к персонажу фактор графитации
        status()                        # Обновляем статусбар и данные для пользователя
        Hero.animate()                  # Анимируем персонажа
    root.update_idletasks()             # Обновляем объекты и окно
    root.update()
    time.sleep(0.015)                   # Задержка
