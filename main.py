# Granny`s Skirmish
version = "v0.0.5"

# Импорт
import time, random, math, sys, PIL
from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageTk

# Переменные
run = True
windowSize = [640, 540] # Размер окна
canvasSize = [640, 480] # размер области рисования
aboutmessage = '"Granny`s Skirmish" \nversion: %s\n\nСмысл игры состоит в собирании котиков и попытках не умереть. ' \
               '\nУправление: W/↑- наверх, S/↓ - вниз, A/← - влево, D/→ - вправо, Space - удар' % version
authorsmessage = "Игра разработана: \nУстименко Степаном \nЯрцевой Ульяной "
grannyWalkSpeed = 5     # Бабкина скорость
level = 0               # Уровень
gravitySpeed = 5        # Скорость гравитации (да, не ускорение)

animationduration = 0.15    # Задержки анимации
lastanimationtime = time.time() # Задаем счетчик кадра

lastanimation = "None"  # Переменная последней проигранной анимации
lastWalkRightImage = 0  # Последнее использованное изображение для анимации шага вправо(т.к. анимация в массиве)
lastWalkLeftImage = 0   # Последнее использованное изображение для анимации шага влево(т.к. анимация в массиве)
lastClimbUpImage = 0    # Последнее использованное изображение для анимации забирания (т.к. анимация в массиве)

isWalkingLeft = False   # Идет ли персонаж влево
isWalkingRight = False  # Идет ли персонаж вправо
isClimbingUp = False    # Забирается ли персонаж
isClimbingDown = False  # Спускается ли персонаж

isExitActive = False    # Доступен ли выход с уровня

Score = 0               # Счет
ScoreAddCat = 10        # Очки за кота
# Построение окна
root = Tk()                                                     # Создаем окно
root.title("Granny`s Skirmish")                                 # Заголовок окна
root.iconbitmap("assets\graphics\icon.ico")                     # Иконка окна
root.geometry("%ix%i" % (windowSize[0], windowSize[1]))         # Размеры окна
root.resizable(0, 0)                                            # Запрет на изменение размеров окна
            # Элементы окна
statusbar = Label(root, justify=LEFT, text="Готов", width=90, height=1, bg="thistle2", anchor=W)
labelLevel = Label(root, justify=LEFT, text=" ", width=22, height=1, bg="thistle2", anchor=W)
labelCats= Label(root, justify=LEFT, text=" ", width=22, height=1, bg="thistle2", anchor=W)
labelScore = Label(root, justify=LEFT, text=" ", width=22, height=1, bg="thistle2", anchor=W)
labelLives = Label(root, justify=LEFT, text=" ", width=22, height=1, bg="thistle2", anchor=W)
canvas = Canvas(root, width=canvasSize[0], height=canvasSize[1], bd=0, highlightthickness=0, bg="lavender")
            # Добавление элементов в окно
labelLevel.grid(row=0, column=0)
labelScore.grid(row=0, column=1)
labelCats.grid(row=0, column=2)
labelLives.grid(row=0, column=3)
canvas.grid(row=1, column=0, columnspan = 4)
statusbar.grid(row=2, column=0, columnspan = 4)

debugmode = IntVar() # Переменная из Tkinter для режима отладки
# Изображения
def imgload(path):   # Функция загрузки изображений
    img = Image.open(path)
    output = ImageTk.PhotoImage(img)
    return output

mainmenuBackgroung = imgload('assets\graphics\g_backgrounds\menu_background.jpg')   # Главное меню
jungleBackgroung = imgload('assets\graphics\g_backgrounds\jungle_background.jpg')   # Фон джунглей
baseplatform = imgload('assets\graphics\platformbase.png')                          # Базовая платформа
ladder1 = imgload('assets\graphics\moving\ladder_1.png')                            # Лестница

cats = [imgload('assets\graphics\cat\cat1.png'),                                    # Массив с котами
        imgload('assets\graphics\cat\cat2.png'),
        imgload('assets\graphics\cat\cat3.png')]

exitImage = [imgload('assets\graphics\exitflower_inactive.png'),                    # Массив с цветком-выходом
             imgload('assets\graphics\exitflower_active.png')]

grannyImage = imgload('assets\graphics\granny\granny_stand_forward.png')            # Персонаж стоя
grannyFall = imgload('assets\graphics\granny\granny_fall.png')                      # Персонаж падая
grannyStandRight = imgload('assets\graphics\granny\granny_stand_right.png')         # Персонаж стоя лицом вправо
grannyStandLeft = imgload('assets\graphics\granny\granny_stand_left.png')           # Персонаж стоя лицом влево
grannyWalkLeft = [imgload('assets\graphics\granny\granny_walk_left_1.png'),         # Массив анимаций походки
                  imgload('assets\graphics\granny\granny_walk_left_2.png'),         #   налево для персонажа
                  imgload('assets\graphics\granny\granny_walk_left_3.png')]
grannyWalkRight = [imgload('assets\graphics\granny\granny_walk_right_1.png'),       # Массив анимаций походки
                  imgload('assets\graphics\granny\granny_walk_right_2.png'),        #   направо для персонажа
                  imgload('assets\graphics\granny\granny_walk_right_3.png')]
grannyClimbUp = [imgload('assets\graphics\granny\granny_climb_up_1.png'),           # Массив анимаций забирания
                imgload('assets\graphics\granny\granny_climb_up_2.png'),            #   для персонажа
                imgload('assets\graphics\granny\granny_climb_up_3.png')]
grannyClimbDown = imgload('assets\graphics\granny\granny_climb_down.png')           # Персонаж спускается


# Функции окон
def mainmenu_open():                                                                # Открытие главного меню
    canvas.create_image(320, 240, image=mainmenuBackgroung, tag="mainmenu")
    print("Запуск")

def on_closing():                                                                   # Опрос закрытия
    global run
    if mb.askokcancel("Выход", "Вы уже уходите?"):
        print("Выход")
        run = False
        root.destroy()

def status():                                                                       # Обновление статуса
    if fall == True:
        FallStr="True"
    else: FallStr="False"
    if ladd == True:
        LaddStr="True"
    else: LaddStr="False"
    if carr == True:
        CarrStr="True"
    else: CarrStr="False"
    if vent == True:
        VentStr="True"
    else: VentStr="False"
    CatStr = "%s из %s" % (CatAmountReal, CatAmountAll)
    GrannyPos = str(Hero.coords())
    labelLevelText = "Уровень: %i" % level
    labelLevel.config(text=labelLevelText)
    labelCatsText = "Коты: %s" % CatStr
    labelCats.config(text=labelCatsText)
    labelScoreText = "Счет: %i" % Score
    labelScore.config(text=labelScoreText)

    if debugmode.get()==1:                                                          # Режим отладки
        message = "Fall:%s; Ladd:%s; Carr:%s; Vent:%s; GrannyPos:%s; LastAnim:%s;" % (
                FallStr, LaddStr, CarrStr, VentStr, GrannyPos, lastanimation)
    else:
        message = "Работаю"
    statusbar.config(text = message)

def clearcanvas():  # Очистка зоны рисования
    canvas.delete("mainmenu")
    canvas.delete("ladder")
    canvas.delete("play")
    canvas.delete("platform")
    canvas.delete("cat")
    canvas.delete("granny")
    canvas.delete("exit")
# Классы
class Granny():     # Класс персонажа, которым мы управляем
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_image(60, 400, image=grannyImage, tag="granny")
        self.x = 60
        self.y = 400
            # Обработка нажатий
        self.canvas.bind_all('<KeyPress-a>', self.turn_left)
        self.canvas.bind_all('<KeyPress-d>', self.turn_right)
        self.canvas.bind_all('<KeyPress-w>', self.turn_up)
        self.canvas.bind_all('<KeyPress-s>', self.turn_down)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
        self.canvas.bind_all('<KeyPress-Down>', self.turn_down)

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
            if self.x > 30:
                canvas.move(self.id, -grannyWalkSpeed, 0)
                self.x -= grannyWalkSpeed


    def turn_right(self, event): # Движение вправо
        global isWalkingRight
        if level != 0:
            isWalkingRight = True
            if self.x < 610:
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

    def gravitymove(self):  # Движение под действием гравитации
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
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_image(320, 465, image=baseplatform, tag="platform")

    def touch_place(self): # Массив точек касания верхней линии
        touch = [450, 0, 640]
        return touch

class PlatformSimple():     # Класс обычной платформы, масштабируется и изменяется для каждого уровня
    def __init__(self, canvas, coordsArray):
        self.coords = coordsArray
        self.canvas = canvas
        self.id = canvas.create_rectangle(self.coords[1], self.coords[0], self.coords[2], self.coords[0]+ 30,
                                          fill="Brown", tag="platform")

    def touch_place(self):  # Массив точек касания верхней линии
        touch=[self.coords[0], self.coords[1], self.coords[2]]
        return touch

class Ladder():     # Класс лестницы, позволяет забираться на верх
    # Ширина 50, Высота 120
    def __init__(self, canvas, coordsArray): # ax by (Верхний левый угол)
        self.coords = coordsArray
        self.canvas = canvas
        self.centre = [self.coords[0]+25, self.coords[1]+60]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=ladder1, tag="ladder")
    def actionzone(self):   # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 10, self.centre[0]+10, self.centre[1] - 60, self.centre[1] + 60]
        return actionArray

class Cat():    # Класс котика, которых мы спасаем
    # Ширина 24, Высота 32
    def __init__(self, canvas, coordsArray):  # ax by (Верхний левый угол)
        self.coords = coordsArray
        self.canvas = canvas
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

class ExitFlower():     # Класс цветка-выхода
    # Ширина 60, Высота 60
    def __init__(self, canvas, coordsArray): # ax by (Верхний левый угол)
        self.coords = coordsArray
        self.canvas = canvas
        self.centre = [self.coords[0]+30, self.coords[1]+30]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=exitImage[0], tag="exit")
    def actionzone(self):   # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 30, self.centre[0] + 30, self.centre[1] - 30, self.centre[1] + 30]
        return actionArray
    def opening(self):      # Открытие цветка
        canvas.itemconfig(self.id, image=exitImage[1])

# Уровни
def Level1():   # Создаем объекты уровня
    global Base, level, Hero, Exit, AlphaPlatform, AlphaCat, AlphaLadder, CatAmountReal, CatAmountAll
    clearcanvas()
    canvas.create_image(320, 240, image=jungleBackgroung, tag="play")
    Base = PlatformBase(canvas=canvas)
    AlphaPlatform = PlatformSimple(canvas=canvas, coordsArray=[330,150,350]) # Платформа(y,a,b)
    AlphaLadder = Ladder(canvas=canvas, coordsArray=[100, 330])
    CatAmountAll = 1
    CatAmountReal = 0
    AlphaCat = Cat(canvas=canvas, coordsArray=[250, 298])
    Exit = ExitFlower(canvas=canvas, coordsArray=[400, 390])
    Hero = Granny(canvas=canvas)
    level = 1

def Level2():   # Создаем объекты уровня
    global Base, level, Hero, Exit, AlphaPlatform, AlphaCat, BetaCat, AlphaLadder, CatAmountReal, CatAmountAll
    clearcanvas()
    canvas.create_image(320, 240, image=jungleBackgroung, tag="play")
    Base = PlatformBase(canvas=canvas)
    AlphaPlatform = PlatformSimple(canvas=canvas, coordsArray=[330, 350, 600])  # Платформа(y,a,b)
    AlphaLadder = Ladder(canvas=canvas, coordsArray=[300, 330])
    CatAmountAll = 2
    CatAmountReal = 0
    AlphaCat = Cat(canvas=canvas, coordsArray=[200, 418])
    BetaCat = Cat(canvas=canvas, coordsArray=[500, 298])
    Exit = ExitFlower(canvas=canvas, coordsArray=[400, 270])
    Hero = Granny(canvas=canvas)
    level = 2

def Level3():  # Создаем объекты уровня
    pass

def Level4():  # Создаем объекты уровня
    pass

def Level5():  # Создаем объекты уровня
    pass

# Доп. Функции
    # Платформа
def grannyunderplatform():  # Определение платформ на уровнях !!!Не забывать добавлять!!!
    globalsolution = True
    if level == 1:
        GrannyTouch = Hero.touch_place()
        BaseTouch = Base.touch_place()
        AlphaTouch = AlphaPlatform.touch_place()
        solutionBase = ground_check(GrannyTouch, BaseTouch)
        solutionAlpha = ground_check(GrannyTouch, AlphaTouch)
        if (solutionAlpha == False)|(solutionBase == False):
            globalsolution = False
    if level == 2:
        GrannyTouch = Hero.touch_place()
        BaseTouch = Base.touch_place()
        AlphaTouch = AlphaPlatform.touch_place()
        solutionBase = ground_check(GrannyTouch, BaseTouch)
        solutionAlpha = ground_check(GrannyTouch, AlphaTouch)
        if (solutionAlpha == False) | (solutionBase == False):
            globalsolution = False

    if level == 3:
        pass

    if level == 4:
        pass

    if level == 5:
        pass
    return globalsolution

def ground_check(GrannyTouch, PlatformTouch): # Проверка земли под ногами по массивам
    solution = True
    if PlatformTouch[0] == GrannyTouch[0]:
        if (GrannyTouch[1] >= PlatformTouch[1]) & (GrannyTouch[1] <= PlatformTouch[2]):
            solution = False
        if (GrannyTouch[2] >= PlatformTouch[1]) & (GrannyTouch[2] <= PlatformTouch[2]):
            solution = False
    return solution

    # Лестница
def grannyonladder(): # Определение лестниц на уровне !!!Не забывать добавлять!!!
    globalsolution = False
    if level == 1:
        Grannyzone = Hero.actionzone()
        Alphazone = AlphaLadder.actionzone()
        solutionAlpha = ladder_check(Grannyzone, Alphazone)
        if (solutionAlpha == True) | 0:
            globalsolution = True

    if level == 2:
        Grannyzone = Hero.actionzone()
        Alphazone = AlphaLadder.actionzone()
        solutionAlpha = ladder_check(Grannyzone, Alphazone)
        if (solutionAlpha == True) | 0:
            globalsolution = True

    if level == 3:
        pass

    if level == 4:
        pass

    if level == 5:
        pass
    return globalsolution

def ladder_check(Grannyzone, Ladderzone):   # Проверка лестниц под ногами по массивам
    solution = False
    if (Grannyzone[0] + 15 >= Ladderzone[0]) & (Grannyzone[0] + 15 <= Ladderzone[1]):
        if (Grannyzone[2] >= Ladderzone[2]) & (Grannyzone[2] <= Ladderzone[3]):
            solution = True
        if (Grannyzone[3] >= Ladderzone[2]) & (Grannyzone[3] <= Ladderzone[3]):
            solution = True
    if (Grannyzone[1] - 15 >= Ladderzone[0]) & (Grannyzone[1] - 15 <= Ladderzone[1]):
        if (Grannyzone[2] >= Ladderzone[2]) & (Grannyzone[2] <= Ladderzone[3]):
            solution = True
        if (Grannyzone[3] >= Ladderzone[2]) & (Grannyzone[3] <= Ladderzone[3]):
            solution = True
    return solution


# Котики
def grannycarrycat(): # Определение котов на уровне !!!Не забывать добавлять!!!
    global CatAmountReal
    globalsolution = False
    if level == 1:
        Grannyzone = Hero.actionzone()
        Alphazone = AlphaCat.actionzone()
        solutionAlpha = False
        if AlphaCat.avaible:
            solutionAlpha = cat_check(Grannyzone, Alphazone)
            if solutionAlpha == True:
                AlphaCat.collect()
                CatAmountReal += 1
        if (solutionAlpha == True) | 0:
            globalsolution = True

    if level == 2:
        Grannyzone = Hero.actionzone()
        Alphazone = AlphaCat.actionzone()
        Betazone = BetaCat.actionzone()
        solutionAlpha = False
        solutionBeta = False

        if AlphaCat.avaible:
            solutionAlpha = cat_check(Grannyzone, Alphazone)
            if solutionAlpha == True:
                AlphaCat.collect()
                CatAmountReal += 1
        if BetaCat.avaible:
            solutionBeta = cat_check(Grannyzone, Betazone)
            if solutionBeta == True:
                BetaCat.collect()
                CatAmountReal += 1

        if (solutionAlpha == True) | (solutionBeta == True):
            globalsolution = True

    if level == 3:
        pass

    if level == 4:
        pass

    if level == 5:
        pass
    return globalsolution

def cat_check(Grannyzone, Catzone):   # Проверка лестниц под ногами по массивам
    solution = False
    if (Grannyzone[0]+10 >= Catzone[0]) & (Grannyzone[0]+10 <= Catzone[1]):
        if (Grannyzone[2] >= Catzone[2]) & (Grannyzone[2] <= Catzone[3]):
            solution = True
        if (Grannyzone[3] >= Catzone[2]) & (Grannyzone[3] <= Catzone[3]):
            solution = True
    if (Grannyzone[1]-10 >= Catzone[0]) & (Grannyzone[1]-10 <= Catzone[1]):
        if (Grannyzone[2] >= Catzone[2]) & (Grannyzone[2] <= Catzone[3]):
            solution = True
        if (Grannyzone[3] >= Catzone[2]) & (Grannyzone[3] <= Catzone[3]):
            solution = True
    return solution

    # Выход
def grannyinexit(): # Определение выхода на уровне
    globalsolution = False
    if level != 0:
        Grannyzone = Hero.actionzone()
        Exitzone = Exit.actionzone()
        globalsolution = exit_check(Grannyzone, Exitzone)
    return globalsolution

def exit_check(Grannyzone, Exitzone):   # Проверка выхода по массивам
    solution = False
    if (Grannyzone[0]+30 >= Exitzone[0]) & (Grannyzone[0]+30 <= Exitzone[1]):
        if (Grannyzone[2] >= Exitzone[2]) & (Grannyzone[2] <= Exitzone[3]):
            solution = True
        if (Grannyzone[3] >= Exitzone[2]) & (Grannyzone[3] <= Exitzone[3]):
            solution = True
    if (Grannyzone[1]-30 >= Exitzone[0]) & (Grannyzone[1]-30 <= Exitzone[1]):
        if (Grannyzone[2] >= Exitzone[2]) & (Grannyzone[2] <= Exitzone[3]):
            solution = True
        if (Grannyzone[3] >= Exitzone[2]) & (Grannyzone[3] <= Exitzone[3]):
            solution = True
    return solution

    # Остальное
def gravity(): # Если персонаж не на платформн и не на лестнице, на нее действует гравитация
    if fall & (ladd == False):
        Hero.gravitymove()

def LevelAdd(): # Логика переключения уровней
    if level == 1:
        Level2()
    elif level == 2:
        Level1()

def recquecountertoexit():  # Проверка на сбор котиков. Открытие цветка и выход с уровня
    global isExitActive
    if CatAmountReal == CatAmountAll:
        isExitActive = True
        Exit.opening()
        if grannyinexit() == True:
            LevelAdd()
    else:
        isExitActive = False

def newgame():
    global Score, level
    level = 0
    Score = 0
    Level1()

# Главный цикл
def menu(): # Описание меню(сверху полоска)
    mainmenu = Menu(root)
    gamemenu = Menu(mainmenu, tearoff=0)
    gamemenu.add_command(label="Новая игра", command=newgame)
    levelmenu = Menu(gamemenu, tearoff=1)
    levelmenu.add_command(label="Уровень 1", command=Level1)
    levelmenu.add_command(label="Уровень 2", command=Level2)
    levelmenu.add_command(label="Уровень 3", command=Level3)
    levelmenu.add_command(label="Уровень 4", command=Level4)
    levelmenu.add_command(label="Уровень 5", command=Level5)
    gamemenu.add_cascade(label="Уровни", menu=levelmenu)
    gamemenu.add_separator()
    optionmenu = Menu(gamemenu, tearoff=1)
    optionmenu.add_checkbutton(label="Отладка",onvalue=1, offvalue=0, variable=debugmode)
    gamemenu.add_cascade(label="Настройки", menu=optionmenu)
    gamemenu.add_separator()
    gamemenu.add_command(label="Выход", command=on_closing)
    aboutmenu = Menu(mainmenu, tearoff=0)
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
        fall = grannyunderplatform()    # Определяем основные переменные
        ladd = grannyonladder()
        carr = grannycarrycat()
        vent = grannyinexit()
        recquecountertoexit()           # Делаем проверку готовность выйти с уровня
        gravity()                       # Применяем к персонажу фактор графитации
        status()                        # Обновляем статусбар и данные для пользователя
        Hero.animate()                  # Анимируем персонажа
    root.update_idletasks()             # Обновляем объекты и окно
    root.update()
    time.sleep(0.015)                   # Задержка

