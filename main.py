# Granny`s Skirmish
# version 0.9.8

"""Импорт"""
import json
import platform
from tkinter import *
from tkinter import colorchooser as cc
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from pygame import mixer
from images import *
from objects import *
from music import *

"""Файл настроек"""
with open("data.json", 'r', encoding="utf-8") as file:  # Открываем файл с настройками
    settings = json.load(file)  # Записываем как словарь в переменную

"""Переменные"""
sysName = platform.uname().system
objectsVariable = VariableHeap()
musicPaths = MusicPathHeap()
soundPaths = SoundPathHeap()
run = True  # Флаг работы приложения
version = settings['version']  # Загрузка номера версии
if sysName == "Windows":
    windowSize = settings["windowsizewin"]  # Размер окна
else:
    windowSize = settings["windowsizelin"]
canvasSize = settings["canvassize"]  # Размер области рисования
aboutmessage = settings["aboutmessage"] % version  # Формирование сообщения об игре
authorsmessage = settings["authorsmessage"]  # Формирование сообщения об авторах
grannyWalkSpeedNormal = settings['grannyspeed']['normal']  # Нормальная скорость персонажа
grannyWalkSpeed = grannyWalkSpeedNormal  # Переменная скорость персонажа
grannyWalkSpeedFast = settings['grannyspeed']['fast']  # Быстрая скорость персонажа
grannyWalkSpeedSlow = settings['grannyspeed']['slow']  # Медленная скорость персонажа
savageSpeed = settings["savagespeed"]  # Скорость Дикаря
gravitySpeedNormal = settings['gravity']['normal']  # Нормальная скорость гравитации (да, не ускорение)
gravitySpeedInvert = settings['gravity']['inverted']  # Инвертированная скорость гравитации
gravitySpeed = gravitySpeedNormal  # Переменная скорость гравитации
effectduration = settings['effectduration']  # Длительность эффектов грибов
animationGrannyduration = settings['animationGrannyduration']  # Задержки анимации персонажа
animationSavageduration = settings['animationSavageduration']  # Задержки анимации Дикаря

backgroundcolor = settings["backgroung"]  # Цвет фона

lasteffecttime = time.time()  # Время последней активации эффекта
lastframetime = time.time()  # Последнее время кадра

isExitActive = False  # Доступен ли выход с уровня
avoidEffects = False  # Необходимо ли сбросить эффекты

antigrav = False  # Включена ли антигравитация
simpgrav = False  # Двигается ли персонаж под действием гравитации
wallside = "0"  # Сторона стенки в которую уперся персонаж

isMusicOn = False

keytime = time.time()  # Время последнего нажатия на клавиши
KeySpeed = 0  # Скорость нажатий за секунду
fps = 0  # Моментальная частота кадров
fpsGlobal = 0  # Частота кадров

limitedFlag = False  # Ограничен ли уровень по времени
limitedtime = 0  # Время включения ограничения

objectsVariable.lives = settings['livesnormal']  # Переменное количество жизней на уровне
objectsVariable.Globallives = objectsVariable.lives
level = 0  # Уровень

typeMusic = 0
volumeMusic = settings["musicvolume"]
volumeSound = settings["soundvolume"]

shouldReloadButtons = True

ladd = False
"""Построение окна"""
root = Tk()  # Создаем окно
root.title(settings['title'])  # Заголовок окна
root.configure(bg=backgroundcolor)  # Фон окна
root.geometry("%ix%i" % (windowSize[0], windowSize[1]))  # Размеры окна
root.resizable(0, 0)  # Запрет на изменение размеров окна
image = ImageHeap()
if sysName == "Windows":
    root.iconbitmap(image.iconPath)
"""Музыка"""
mixer.init()

def music_stop():
    global isMusicOn
    mixer.music.stop()
    isMusicOn = False

def music():
    global isMusicOn, typeMusic
    mixer.music.set_volume(volumeMusic / 100)
    mixer.Channel(0).set_volume(volumeSound / 100)
    mixer.Channel(1).set_volume(volumeSound / 100)
    mixer.Channel(2).set_volume(volumeSound / 100)
    mixer.Channel(3).set_volume(volumeSound / 100)
    mixer.Channel(4).set_volume(volumeSound / 100)
    if musicmode.get() is False:
        music_stop()
    if level == 0:
        if typeMusic == 1:
            isMusicOn = False
        typeMusic = 0
    else:
        if typeMusic == 0:
            isMusicOn = False
        typeMusic = 1

    if (musicmode.get() is True) & (typeMusic == 0) & (isMusicOn is False):
        music_stop()
        if sysName == "Windows":
            mixer.music.load(musicPaths.mainmenuWin)
        else:
            mixer.music.load(musicPaths.mainmenuLin)
        mixer.music.play(loops=200)
        isMusicOn = True

    if (musicmode.get() is True) & (typeMusic == 1) & (isMusicOn is False):
        music_stop()
        if sysName == "Windows":
            mixer.music.load(musicPaths.levelWin)
        else:
            mixer.music.load(usicPaths.levelLin)
        mixer.music.play(loops=1000)
        isMusicOn = True

"""Элементы окна"""
statusbar = Label(root, justify=LEFT, text="Готов", width=settings["statusbarwidth"], height=1,
                  bg=backgroundcolor, anchor=W)  # Статусбар
labelLevel = Label(root, justify=LEFT, text=" ", width=settings["hidwidth"], height=1, bg=backgroundcolor,
                   anchor=W)  # Отображение уровня
labelCats = Label(root, justify=LEFT, text=" ", width=settings["hidwidth"], height=1, bg=backgroundcolor,
                  anchor=W)  # Отображение количества котов на уровне
labelScore = Label(root, justify=LEFT, text=" ", width=settings["hidwidth"], height=1, bg=backgroundcolor,
                   anchor=W)  # Счет
labelLives = Label(root, justify=LEFT, text=" ", width=settings["hidwidth"], height=1, bg=backgroundcolor,
                   anchor=W)  # Отображение количества жизней
canvas = Canvas(root, width=canvasSize[0], height=canvasSize[1], bd=0, highlightthickness=0, bg=backgroundcolor)

# Отображние эффектов, их длительности, ограничений по времени
labelFast = Label(root, text="Fast", width=settings["effectwidth"], height=1, bg="PaleVioletRed1")
labelSlow = Label(root, text="Slow", width=settings["effectwidth"], height=1, bg="PaleGoldenrod")
labelGrav = Label(root, text="Grav", width=settings["effectwidth"], height=1, bg="turquoise1")
labelEffect = Label(root, text=" ", width=settings["effectwidth"], height=1, bg="MediumPurple1")
labelTime = Label(root, text="Time", width=settings["effectwidth"], height=1, bg="lightcoral")
labelTimer = Label(root, text="Timer", width=settings["timerwidth"], height=1, bg="lightcoral")

# Удаление кнопок с главного меню
def clearbutt():
    newgameButt.place_forget()
    exitgameButt.place_forget()

# Начало новой игры
def newgame():
    global level
    if level != 0:
        ask = mb.askyesno(title="Внимание", message="Вы действительно хотите начать новую игру?")
        if ask:
            objectsVariable.lives = settings['livesnormal']
            level = 0
            objectsVariable.Score = 0
            objectsVariable.GlobalScore = 0
            clearbutt()
            LevelAdd()
    else:
        objectsVariable.lives = settings['livesnormal']
        level = 0
        objectsVariable.Score = 0
        objectsVariable.GlobalScore = 0
        clearbutt()
        LevelAdd()

# Опрос закрытия программы
def on_closing():  # Опрос закрытия
    global run
    if mb.askokcancel("Выход", "Вы уже уходите?"):
        print("Выход")
        run = False
        root.destroy()

# Кнопки главного меню
newgameButt = Button(root, image = image.newgame,  command=newgame, borderwidth=0, bd=0)
exitgameButt = Button(root, image =image.quit, command=on_closing, borderwidth=0, bd=0)

"""Добавление элементов в окно"""
def loadScreen():
    labelLevel.grid(row=0, column=0)
    labelScore.grid(row=0, column=1)
    labelCats.grid(row=0, column=2)
    labelLives.grid(row=0, column=3)
    canvas.grid(row=1, column=0, columnspan=4)
    statusbar.place(x=0, y=500)

loadScreen()

# Переменная для режимов отладки и музыки
musicmode = BooleanVar()
musicmode.set(settings["musicswitch"])
soundmode = BooleanVar()
soundmode.set(settings["soundswitch"])
debugmode = IntVar()
scalevolumeMusic = IntVar()
scalevolumeMusic.set(volumeMusic)
scalevolumeSound = IntVar()
scalevolumeSound.set(volumeMusic)

"""Окно выбора громкости Музыки"""
def setvolumemusic():
    global volumeMusicWindow
    volumeMusicWindow = Toplevel()
    volumeMusicWindow.title("Громкость музыки")  # Заголовок окна
    volumeMusicWindow.configure(bg=backgroundcolor)  # Фон окна
    volumeMusicWindow.geometry("%ix%i" % (216, 130))  # Размеры окна
    volumeMusicWindow.resizable(0, 0)  # Запрет на изменение размеров окна
    if sysName == "Windows":
        volumeMusicWindow.iconbitmap(image.iconPath)
    Label(volumeMusicWindow, bg=backgroundcolor, text="Выберите подходящую громкость", font=("Arial", 10)).grid(
        row=0, column=0, columnspan=2)
    Label(volumeMusicWindow, bg=backgroundcolor, text="Текущая громкость: %s" % volumeMusic, font=("Arial", 10)).grid(
        row=1, column=0, columnspan=2)
    Scale(volumeMusicWindow, variable=scalevolumeMusic, bg=backgroundcolor, orient=HORIZONTAL, length=180, font=("Arial", 10)).grid(
        row=3, column=0, columnspan=2)
    Button(volumeMusicWindow, text="Сохранить", bg=backgroundcolor, command=savevolumemusic, font=("Arial", 10)).grid(
        row=4, column=0, pady=10)
    Button(volumeMusicWindow, text="Отменить", bg=backgroundcolor, command=undovolumemusic, font=("Arial", 10)).grid(
        row=4, column=1, pady=10)

def savevolumemusic():
    global volumeMusic
    volumeMusic = scalevolumeMusic.get()
    volumeMusicWindow.destroy()

def undovolumemusic():
    volumeMusicWindow.destroy()
    scalevolumeMusic.set(volumeMusic)

"""Окно выбора громкости Звуков"""
def setvolumesound():
    global volumeSoundWindow
    volumeSoundWindow = Toplevel()
    volumeSoundWindow.title("Громкость pderjd")  # Заголовок окна
    volumeSoundWindow.configure(bg=backgroundcolor)  # Фон окна
    volumeSoundWindow.geometry("%ix%i" % (216, 130))  # Размеры окна
    volumeSoundWindow.resizable(0, 0)  # Запрет на изменение размеров окна
    if sysName == "Windows":
        volumeSoundWindow.iconbitmap(image.iconPath)
    Label(volumeSoundWindow, bg=backgroundcolor, text="Выберите подходящую громкость", font=("Arial", 10)).grid(
        row=0, column=0, columnspan=2)
    Label(volumeSoundWindow, bg=backgroundcolor, text="Текущая громкость: %s" % volumeSound, font=("Arial", 10)).grid(
        row=1, column=0, columnspan=2)
    Scale(volumeSoundWindow, variable=scalevolumeSound, bg=backgroundcolor, orient=HORIZONTAL, length=180, font=("Arial", 10)).grid(
        row=3, column=0, columnspan=2)
    Button(volumeSoundWindow, text="Сохранить", bg=backgroundcolor, command=savevolumesound, font=("Arial", 10)).grid(
        row=4, column=0, pady=10)
    Button(volumeSoundWindow, text="Отменить", bg=backgroundcolor, command=undovolumesound, font=("Arial", 10)).grid(
        row=4, column=1, pady=10)

def savevolumesound():
    global volumeSound
    volumeSound = scalevolumeSound.get()
    volumeSoundWindow.destroy()

def undovolumesound():
    volumeSoundWindow.destroy()
    scalevolumeSound.set(volumeSound)
"""Функции окон"""
# Открытие главного меню
def mainmenu_open():  # Открытие главного меню
    global level, shouldReloadButtons
    level = 0
    objectsVariable.lives = settings['livesnormal']
    objectsVariable.Score = 0
    objectsVariable.GlobalScore = 0
    canvas.create_image(320, 240, image=image.mainmenuBackgroung, tag="mainmenu")
    labelLevel.config(text=" ")
    labelCats.config(text=" ")
    labelScore.config(text=" ")
    labelLives.config(text=" ")
    newgameButt.place(x=182, y=245)
    exitgameButt.place(x=182, y=335)
    labelFast.place_forget()
    labelSlow.place_forget()
    labelGrav.place_forget()
    labelEffect.place_forget()
    labelTime.place_forget()
    labelTimer.place_forget()
    shouldReloadButtons = True
    print("Запуск")

# Обновление статусбара
def status():
    CatStr = "%s из %s" % (objectsVariable.CatAmountReal, objectsVariable.CatAmountAll)
    if Hero.avaible:
        GrannyPos = str(Hero.coords())
    else:
        GrannyPos = "None"
    if alphaSavage.avaible:
        alphaPos = str(alphaSavage.coords())
    else:
        alphaPos = "None"
    if betaSavage.avaible:
        betaPos = str(betaSavage.coords())
    else:
        betaPos = "None"
    if gammaSavage.avaible:
        gammaPos = str(gammaSavage.coords())
    else:
        gammaPos = "None"
    if deltaSavage.avaible:
        deltaPos = str(deltaSavage.coords())
    else:
        deltaPos = "None"
    if level != 0:
        labelLevelText = "Уровень: %i" % level
        labelLevel.config(text=labelLevelText)
        labelCatsText = "Коты: %s" % CatStr
        labelCats.config(text=labelCatsText)
        labelScoreText = "Счет: %i" % (objectsVariable.Score + objectsVariable.GlobalScore)
        labelScore.config(text=labelScoreText)
        labelLivesText = "Жизни: %i" % objectsVariable.lives
        labelLives.config(text=labelLivesText)

    if debugmode.get() == 1:
        message = "Plat:%s; Head:%s; Ladd:%s; Barr:%s; Side:%s; GraHitSav:%s; SavHitGra:%s;" % (
            plat, head, ladd, barr, wallside, GraHitSav[0], SavHitGra)
        if level == 0:
            message = "Готов"
    elif debugmode.get() == 2:
        message = "Vent:%s; Flow:%s; Carr:%s; Fast:%s; Slow:%s; Grav:%s; ExitActive:%s;" % (
            vent, flow, carr, fast, slow, grav, isExitActive)
        if level == 0:
            message = "Готов"
    elif debugmode.get() == 3:
        message = "GrannyPos:%s; alphaPos:%s; betaPos:%s; gammaPos:%s; deltaPos:%s;" % (
            GrannyPos, alphaPos, betaPos, gammaPos, deltaPos)
        if level == 0:
            message = "Готов"
    elif debugmode.get() == 4:
        message = "System:%s, FPS:%i; Key:%i; Cheat:%s; Music:%s; MVol:%i; Sound:%s; SVol:%i" % (
            sysName, fpsGlobal, KeySpeed, settings["cheatmode"], musicmode.get(), volumeMusic,soundmode.get(), volumeSound)
        if level == 0:
            message = "Готов"
    elif level != 0:
        message = "Работаю"
    else:
        message = "Готов"
    statusbar.config(text=message)

# Очистка зоны рисования
def clearcanvas():
    canvas.delete("mainmenu")
    canvas.delete("ladder")
    canvas.delete("play")
    canvas.delete("platform")
    canvas.delete("cat")
    canvas.delete("wall")
    canvas.delete("bonus")
    canvas.delete("granny")
    canvas.delete("savage")
    canvas.delete("exit")

"""Объекты"""
# Персонаж
class Granny:  # Класс персонажа, которым мы управляем
    def __init__(self, spawncoords, canvas, image):
        self.image = image
        self.canvas = canvas
        self.id = self.canvas.create_image(spawncoords[0], spawncoords[1], image=self.image["image"], tag="granny")
        self.x = spawncoords[0]  # Координата Х
        self.y = spawncoords[1]  # Координата У
        self.avaible = True  # Существует ли объект
        self.action = ""  # Очередь действий
        # Обработка нажатий
        self.canvas.bind_all('<KeyPress-a>', self.turn_left)
        self.canvas.bind_all('<KeyPress-d>', self.turn_right)
        self.canvas.bind_all('<KeyPress-w>', self.turn_up)
        self.canvas.bind_all('<KeyPress-s>', self.turn_down)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
        self.canvas.bind_all('<KeyPress-Down>', self.turn_down)
        self.canvas.bind_all('<KeyPress-space>', self.hit_enemy)
        self.isWalkingLeft = False  # Идет ли персонаж влево
        self.isWalkingRight = False  # Идет ли персонаж вправо
        self.isClimbingUp = False  # Забирается ли персонаж
        self.isClimbingDown = False  # Спускается ли персонаж
        self.isHitEnemy = False  # Бьет ли персонаж
        self.lastanimation = "None"  # Переменная последней проигранной анимации
        self.lastWalkRightImage = 0  # Последнее использованное изображение для анимации шага вправо
        self.lastWalkLeftImage = 0  # Последнее использованное изображение для анимации шага влево
        self.lastClimbUpImage = 0  # Последнее использованное изображение для анимации забирания
        self.lastHitEnemyImage = 0  # Последнее использованное изображение для анимации удара
        self.lastanimationtime = time.time()  # Время последнего анимирования

    def coords(self):  # Массив с координатами
        return [self.x, self.y]

    def actionzone(self):  # Зона действий
        return [self.x - 25, self.x + 25, self.y - 30, self.y + 30]

    def action_queue(self):  # Сама очередь действий
        if self.action == "turn_left":  # Если нужно повернуть налево
            self.isWalkingLeft = True  # Ставим флаг, что поворачиваем (для анимации)
            if (self.x > 30) & (wallside != "R"):  # Если не у края и не уперлись в стену
                self.canvas.move(self.id, -grannyWalkSpeed, 0)  # Двигаемся влево на значение скорости
                self.x -= grannyWalkSpeed  # Обновляем координату
        if self.action == "turn_right":  # Если нужно повернуть направо
            self.isWalkingRight = True  # Ставим флаг, что поворачиваем
            if (self.x < 610) & (wallside != "L"):  # Если не у края и не уперлись в стену
                self.canvas.move(self.id, grannyWalkSpeed, 0)  # Двигаемся вправо на значение скорости
                self.x += grannyWalkSpeed  # Обновляем координату
        if self.action == "turn_up":  # Если нужно подняться наверх
            if not objectsVariable.isLadderTop:
                self.isClimbingUp = True  # Ставим флаг, что забираемся
                if (self.y > 30) & ladd:  # Если не у края и на лестнице
                    self.canvas.move(self.id, 0, -grannyWalkSpeed)  # Двигаемся вверх на значение скорости
                    self.y -= grannyWalkSpeed  # Обновляем координату
        if self.action == "turn_down":  # Если нужно стуститься вниз
            self.isClimbingDown = True  # Ставим флаг, что спускаемся
            if (plat is False) & (antigrav is False) & (simpgrav is False):
                self.canvas.move(self.id, 0, grannyWalkSpeed)  # Двигаемся вниз на значение скорости
                self.y += grannyWalkSpeed  # Обновляем координату
        if self.action == "hit_enemy":  # Если нужно ударить
            if soundmode.get():
                mixer.Channel(4).play(mixer.Sound(random.choice(soundPaths.grannyhit)))
            self.isHitEnemy = True  # Ставим флаг, что ударяем
            savageKill()  # Обьявляем всех Дикарей в зоне мертвыми
        self.action = ""  # Сбрасываем задачу

    def turn_left(self, event):  # Движение влево
        if objectsVariable.keyCounter <= settings["keyboardLimit"]:
            self.action = "turn_left"
        objectsVariable.keyCounter += 1

    def turn_right(self, event):  # Движение вправо
        if objectsVariable.keyCounter <= settings["keyboardLimit"]:
            self.action = "turn_right"
        objectsVariable.keyCounter += 1

    def turn_up(self, event):  # Движение вверх до потолка
        if objectsVariable.keyCounter <= settings["keyboardLimit"]:
            self.action = "turn_up"
        objectsVariable.keyCounter += 1

    def turn_down(self, event):  # Движение вниз
        if objectsVariable.keyCounter <= settings["keyboardLimit"]:
            self.action = "turn_down"
        objectsVariable.keyCounter += 1

    def hit_enemy(self, event):  # Удар
        if objectsVariable.keyCounter <= settings["keyboardLimit"]:
            self.action = "hit_enemy"
        objectsVariable.keyCounter += 1

    def touch_place(self):  # Массив точек касания нижней линии
        return [self.y + 30, self.x + 5, self.x - 5]

    def touch_head(self):  # Массив точек касания верхней линии
        return [self.y - 30, self.x + 5, self.x - 5]

    def hit_area(self):  # Массив зоны удара
        return [self.x - 60, self.x + 60, self.y - 30, self.y + 30]

    def gravitymove(self):  # Движение под действием гравитации
        if ((self.y > 30) & (head is False)) | (gravitySpeed > 0):  # Если не бьемся головой или нормальная гравитация
            self.canvas.move(self.id, 0, gravitySpeed)
            self.y += gravitySpeed

    def animate(self):  # Анимирование
        if (time.time() - self.lastanimationtime) > animationGrannyduration:  # Если прошла задержка
            # Анимации после движений
            if self.lastanimation == "WalkRight":
                self.canvas.itemconfig(self.id, image=self.image["grannyStandRight"])
            if self.lastanimation == "WalkLeft":
                self.canvas.itemconfig(self.id, image=self.image["grannyStandLeft"])
            if (self.lastanimation == "Stand") | (self.lastanimation == "Hit"):
                self.canvas.itemconfig(self.id, image=self.image["image"])
            if self.lastanimation == "Climbing":
                self.canvas.itemconfig(self.id, image=self.image["grannyClimbUp"][1])
                # Анимации во время движений
            if self.isWalkingRight:
                if self.lastWalkRightImage == 3:
                    self.lastWalkRightImage = 0
                self.canvas.itemconfig(self.id, image=self.image["grannyWalkRight"][self.lastWalkRightImage])
                self.lastWalkRightImage += 1
                self.isWalkingRight = False
                self.lastanimation = "WalkRight"
            if self.isWalkingLeft:
                if self.lastWalkLeftImage == 3:
                    self.lastWalkLeftImage = 0
                self.canvas.itemconfig(self.id, image=self.image["grannyWalkLeft"][self.lastWalkLeftImage])
                self.lastWalkLeftImage += 1
                self.isWalkingLeft = False
                self.lastanimation = "WalkLeft"
            if self.isHitEnemy:
                if self.lastHitEnemyImage == 2:
                    self.lastHitEnemyImage = 0
                self.canvas.itemconfig(self.id, image=self.image["grannyHit"][self.lastHitEnemyImage])
                self.lastHitEnemyImage += 1
                self.isHitEnemy = False
                self.lastanimation = "Hit"
            # Забирание и спуск по лестнице
            if objectsVariable.isLadderTop:
                self.canvas.itemconfig(self.id, image=self.image["image"])

            if (ladd is True) & (plat is False):
                if self.isClimbingUp:
                    if self.lastClimbUpImage == 3:
                        self.lastClimbUpImage = 0
                    self.canvas.itemconfig(self.id, image=self.image["grannyClimbUp"][self.lastClimbUpImage])
                    self.lastClimbUpImage += 1
                    self.isClimbingUp = False
                    self.lastanimation = "Climbing"
                    if (ladd is False) | (plat is True):
                        self.lastanimation = "Stand"

                if self.isClimbingDown:
                    self.canvas.itemconfig(self.id, image=self.image["grannyClimbDown"])
                    self.isClimbingDown = False
                    self.lastanimation = "Climbing"
                    if (ladd is False) | (plat is True):
                        self.lastanimation = "Stand"
                        # Падение
            if (plat is False) & (ladd is False):
                self.canvas.itemconfig(self.id, image=self.image["grannyFall"])
                self.isWalkingLeft = False
                self.isWalkingRight = False
                self.lastanimation = "Stand"
                # Обновляем таймер анимации
            self.lastanimationtime = time.time()

"""Уровни"""
# Инициальзация уровня по data.json
def LevelInit():
    clearbutt()
    clearcanvas()
    global shouldReloadButtons, limitedtime, avoidEffects, limitedFlag, Hero, Base, Exit, alphaPlatform, betaPlatform, gammaPlatform, deltaPlatform, epsilonPlatform, zetaPlatform, etaPlatform, thetaPlatform, iotaPlatform, alphaCat, betaCat, gammaCat, deltaCat, epsilonCat, zetaCat, alphaBonus, betaBonus, gammaBonus, deltaBonus, epsilonBonus, zetaBonus, alphaLadder, betaLadder, gammaLadder, deltaLadder, epsilonLadder, zetaLadder, alphaWall, betaWall, gammaWall, deltaWall, epsilonWall, zetaWall, alphaSavage, betaSavage, gammaSavage, deltaSavage, alphaFastroom, betaFastroom, alphaSlowroom, betaSlowroom, alphaGravroom, betaGravroom
    shouldReloadButtons = True
    limitedFlag = False
    avoidEffects = True
    limitedtime = 0
    canvas.create_image(320, 240, image=image.jungleBackgroung, tag="play")
    Base = PlatformBase(canvas=canvas, image=image.baseplatform)
    Exit = ExitFlower(settings['levels'][level]['exitCoords'], canvas=canvas, image=image.exitImage)
    objectsVariable.CatAmountAll = settings['levels'][level]['CatAmountAll']
    objectsVariable.CatAmountReal = settings['levels'][level]['CatAmountReal']
    """Платформы"""
    if settings['levels'][level]['alphaPlatformFlag']:
        alphaPlatform = PlatformSimple(settings['levels'][level]['alphaPlatformCoords'], canvas=canvas)
    else:
        alphaPlatform = Empty()
    if settings['levels'][level]['betaPlatformFlag']:
        betaPlatform = PlatformSimple(settings['levels'][level]['betaPlatformCoords'], canvas=canvas)
    else:
        betaPlatform = Empty()
    if settings['levels'][level]['gammaPlatformFlag']:
        gammaPlatform = PlatformSimple(settings['levels'][level]['gammaPlatformCoords'], canvas=canvas)
    else:
        gammaPlatform = Empty()
    if settings['levels'][level]['deltaPlatformFlag']:
        deltaPlatform = PlatformSimple(settings['levels'][level]['deltaPlatformCoords'], canvas=canvas)
    else:
        deltaPlatform = Empty()
    if settings['levels'][level]['epsilonPlatformFlag']:
        epsilonPlatform = PlatformSimple(settings['levels'][level]['epsilonPlatformCoords'], canvas=canvas)
    else:
        epsilonPlatform = Empty()
    if settings['levels'][level]['zetaPlatformFlag']:
        zetaPlatform = PlatformSimple(settings['levels'][level]['zetaPlatformCoords'], canvas=canvas)
    else:
        zetaPlatform = Empty()
    if settings['levels'][level]['etaPlatformFlag']:
        etaPlatform = PlatformSimple(settings['levels'][level]['etaPlatformCoords'], canvas=canvas)
    else:
        etaPlatform = Empty()
    if settings['levels'][level]['thetaPlatformFlag']:
        thetaPlatform = PlatformSimple(settings['levels'][level]['thetaPlatformCoords'], canvas=canvas)
    else:
        thetaPlatform = Empty()
    if settings['levels'][level]['iotaPlatformFlag']:
        iotaPlatform = PlatformSimple(settings['levels'][level]['iotaPlatformCoords'], canvas=canvas)
    else:
        iotaPlatform = Empty()

    """Лестницы"""
    if settings['levels'][level]['alphaLadderFlag']:
        alphaLadder = Ladder(settings['levels'][level]['alphaLadderCoords'], canvas=canvas, image=image.ladder)
    else:
        alphaLadder = Empty()
    if settings['levels'][level]['betaLadderFlag']:
        betaLadder = Ladder(settings['levels'][level]['betaLadderCoords'], canvas=canvas, image=image.ladder)
    else:
        betaLadder = Empty()
    if settings['levels'][level]['gammaLadderFlag']:
        gammaLadder = Ladder(settings['levels'][level]['gammaLadderCoords'], canvas=canvas, image=image.ladder)
    else:
        gammaLadder = Empty()
    if settings['levels'][level]['deltaLadderFlag']:
        deltaLadder = Ladder(settings['levels'][level]['deltaLadderCoords'], canvas=canvas, image=image.ladder)
    else:
        deltaLadder = Empty()
    if settings['levels'][level]['epsilonLadderFlag']:
        epsilonLadder = Ladder(settings['levels'][level]['epsilonLadderCoords'], canvas=canvas, image=image.ladder)
    else:
        epsilonLadder = Empty()
    if settings['levels'][level]['zetaLadderFlag']:
        zetaLadder = Ladder(settings['levels'][level]['zetaLadderCoords'], canvas=canvas, image=image.ladder)
    else:
        zetaLadder = Empty()

    """Стены"""
    if settings['levels'][level]['alphaWallFlag']:
        alphaWall = Wall(settings['levels'][level]['alphaWallCoords'], canvas=canvas, image=image.wallImage)
    else:
        alphaWall = Empty()
    if settings['levels'][level]['betaWallFlag']:
        betaWall = Wall(settings['levels'][level]['betaWallCoords'], canvas=canvas, image=image.wallImage)
    else:
        betaWall = Empty()
    if settings['levels'][level]['gammaWallFlag']:
        gammaWall = Wall(settings['levels'][level]['gammaWallCoords'], canvas=canvas, image=image.wallImage)
    else:
        gammaWall = Empty()
    if settings['levels'][level]['deltaWallFlag']:
        deltaWall = Wall(settings['levels'][level]['deltaWallCoords'], canvas=canvas, image=image.wallImage)
    else:
        deltaWall = Empty()
    if settings['levels'][level]['epsilonWallFlag']:
        epsilonWall = Wall(settings['levels'][level]['epsilonWallCoords'], canvas=canvas, image=image.wallImage)
    else:
        epsilonWall = Empty()
    if settings['levels'][level]['zetaWallFlag']:
        zetaWall = Wall(settings['levels'][level]['zetaWallCoords'], canvas=canvas, image=image.wallImage)
    else:
        zetaWall = Empty()

    """Коты"""
    if settings['levels'][level]['alphaCatFlag']:
        alphaCat = Cat(settings['levels'][level]['alphaCatCoords'], canvas=canvas, image=image.cats)
    else:
        alphaCat = Empty()
    if settings['levels'][level]['betaCatFlag']:
        betaCat = Cat(settings['levels'][level]['betaCatCoords'], canvas=canvas, image=image.cats)
    else:
        betaCat = Empty()
    if settings['levels'][level]['gammaCatFlag']:
        gammaCat = Cat(settings['levels'][level]['gammaCatCoords'], canvas=canvas, image=image.cats)
    else:
        gammaCat = Empty()
    if settings['levels'][level]['deltaCatFlag']:
        deltaCat = Cat(settings['levels'][level]['deltaCatCoords'], canvas=canvas, image=image.cats)
    else:
        deltaCat = Empty()
    if settings['levels'][level]['epsilonCatFlag']:
        epsilonCat = Cat(settings['levels'][level]['epsilonCatCoords'], canvas=canvas, image=image.cats)
    else:
        epsilonCat = Empty()
    if settings['levels'][level]['zetaCatFlag']:
        zetaCat = Cat(settings['levels'][level]['zetaCatCoords'], canvas=canvas, image=image.cats)
    else:
        zetaCat = Empty()

    """Цветочки"""
    if settings['levels'][level]['alphaBonusFlag']:
        alphaBonus = BonusFlower(settings['levels'][level]['alphaBonusCoords'], canvas=canvas,
                                 imagerise=random.choice(image.bonus), imageseed=image.bonusSeed)
    else:
        alphaBonus = Empty()
    if settings['levels'][level]['betaBonusFlag']:
        betaBonus = BonusFlower(settings['levels'][level]['betaBonusCoords'], canvas=canvas,
                                imagerise=random.choice(image.bonus), imageseed=image.bonusSeed)
    else:
        betaBonus = Empty()
    if settings['levels'][level]['gammaBonusFlag']:
        gammaBonus = BonusFlower(settings['levels'][level]['gammaBonusCoords'], canvas=canvas,
                                 imagerise=random.choice(image.bonus), imageseed=image.bonusSeed)
    else:
        gammaBonus = Empty()
    if settings['levels'][level]['deltaBonusFlag']:
        deltaBonus = BonusFlower(settings['levels'][level]['deltaBonusCoords'], canvas=canvas,
                                 imagerise=random.choice(image.bonus), imageseed=image.bonusSeed)
    else:
        deltaBonus = Empty()
    if settings['levels'][level]['epsilonBonusFlag']:
        epsilonBonus = BonusFlower(settings['levels'][level]['epsilonBonusCoords'], canvas=canvas,
                                   imagerise=random.choice(image.bonus), imageseed=image.bonusSeed)
    else:
        epsilonBonus = Empty()
    if settings['levels'][level]['zetaBonusFlag']:
        zetaBonus = BonusFlower(settings['levels'][level]['zetaBonusCoords'], canvas=canvas,
                                imagerise=random.choice(image.bonus), imageseed=image.bonusSeed)
    else:
        zetaBonus = Empty()

    """Туземец"""
    if settings['levels'][level]['alphaSavageFlag']:
        alphaSavage = Savage(settings['levels'][level]['alphaSavageCoords'], canvas=canvas, image=image.savage,
                             animationsavageduration=animationSavageduration, savagespeed=savageSpeed)
    else:
        alphaSavage = Empty()
    if settings['levels'][level]['betaSavageFlag']:
        betaSavage = Savage(settings['levels'][level]['betaSavageCoords'], canvas=canvas, image=image.savage,
                            animationsavageduration=animationSavageduration, savagespeed=savageSpeed)
    else:
        betaSavage = Empty()
    if settings['levels'][level]['gammaSavageFlag']:
        gammaSavage = Savage(settings['levels'][level]['gammaSavageCoords'], canvas=canvas, image=image.savage,
                             animationsavageduration=animationSavageduration, savagespeed=savageSpeed)
    else:
        gammaSavage = Empty()
    if settings['levels'][level]['deltaSavageFlag']:
        deltaSavage = Savage(settings['levels'][level]['deltaSavageCoords'], canvas=canvas, image=image.savage,
                             animationsavageduration=animationSavageduration, savagespeed=savageSpeed)
    else:
        deltaSavage = Empty()

    """Быстромор"""
    if settings['levels'][level]['alphaFastroomFlag']:
        alphaFastroom = Fastroom(settings['levels'][level]['alphaFastroomCoords'], canvas=canvas, image=image.mushroom)
    else:
        alphaFastroom = Empty()
    if settings['levels'][level]['betaFastroomFlag']:
        betaFastroom = Fastroom(settings['levels'][level]['betaFastroomCoords'], canvas=canvas, image=image.mushroom)
    else:
        betaFastroom = Empty()

    """Медлянка"""
    if settings['levels'][level]['alphaSlowroomFlag']:
        alphaSlowroom = Slowroom(settings['levels'][level]['alphaSlowroomCoords'], canvas=canvas, image=image.mushroom)
    else:
        alphaSlowroom = Empty()
    if settings['levels'][level]['betaSlowroomFlag']:
        betaSlowroom = Slowroom(settings['levels'][level]['betaSlowroomCoords'], canvas=canvas, image=image.mushroom)
    else:
        betaSlowroom = Empty()

    """Вверхшенка"""
    if settings['levels'][level]['alphaGravroomFlag']:
        alphaGravroom = Gravroom(settings['levels'][level]['alphaGravroomCoords'], canvas=canvas, image=image.mushroom)
    else:
        alphaGravroom = Empty()
    if settings['levels'][level]['betaGravroomFlag']:
        betaGravroom = Gravroom(settings['levels'][level]['betaGravroomCoords'], canvas=canvas, image=image.mushroom)
    else:
        betaGravroom = Empty()

    Hero = Granny(spawncoords=settings['levels'][level]['spawnCoords'], canvas=canvas, image=image.granny)

# Обработка выбора уровня
def LevelShoose():
    global level
    ask = sd.askinteger(title="Выбор уровня",
                        prompt="Введите номер уровня.\nМаксимальный уровень: %i" % settings["levelamount"], minvalue=1,
                        maxvalue=settings["levelamount"])
    if type(ask) == int:
        if (level == 0) | settings["cheatmode"]:
            level = ask
            LevelInit()

# Переход на следующий уровень или конец игры
def LevelAdd():  # Логика переключения
    global level, shouldReloadButtons
    objectsVariable.Globallives = objectsVariable.lives
    objectsVariable.GlobalScore += objectsVariable.Score
    objectsVariable.Score = 0
    if level < settings["levelamount"]:  # Если уровень не последний
        if (level != 0) & soundmode.get():
            mixer.Channel(0).play(mixer.Sound(soundPaths.exit))
        level += 1  # Добавляем уровень
        LevelInit()  # Загружаем уровень
    elif level == settings["levelamount"]:  # Если уровень последний
        mixer.Channel(0).play(mixer.Sound(soundPaths.win))
        endgame(win=True)  # Вывод сообшения о победе
    shouldReloadButtons = True

# Начать уровень заново
def LevelRestart():
    ask = mb.askyesno(title="Внимание", message="Вы действительно хотите начать уровень заново?")
    if ask:
        objectsVariable.lives = objectsVariable.Globallives
        objectsVariable.Score = 0
        LevelInit()

"""Доп. Функции"""
# Общая проверка по массивам
def action_check(playerzone, objectzone, index):  # Проверка выхода по массивам
    solution = False
    if (playerzone[0] + index >= objectzone[0]) & (playerzone[0] + index <= objectzone[1]):
        if (playerzone[2] >= objectzone[2]) & (playerzone[2] <= objectzone[3]):
            solution = True
        if (playerzone[3] >= objectzone[2]) & (playerzone[3] <= objectzone[3]):
            solution = True
    if (playerzone[1] - index >= objectzone[0]) & (playerzone[1] - index <= objectzone[1]):
        if (playerzone[2] >= objectzone[2]) & (playerzone[2] <= objectzone[3]):
            solution = True
        if (playerzone[3] >= objectzone[2]) & (playerzone[3] <= objectzone[3]):
            solution = True
    return solution

# Платформа
# Над платформой
def grannyoverplatform():  # Определение платформ на уровнях !!!Не забывать добавлять!!!
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    solutionEta = False
    solutionTheta = False
    solutionIota = False
    playertouch = Hero.touch_place()
    BaseTouch = Base.touch_place()
    solutionBase = ground_check(playertouch, BaseTouch)
    if alphaPlatform.avaible:
        AlphaTouch = alphaPlatform.touch_place()
        solutionAlpha = ground_check(playertouch, AlphaTouch)
    if betaPlatform.avaible:
        BetaTouch = betaPlatform.touch_place()
        solutionBeta = ground_check(playertouch, BetaTouch)
    if gammaPlatform.avaible:
        GammaTouch = gammaPlatform.touch_place()
        solutionGamma = ground_check(playertouch, GammaTouch)
    if deltaPlatform.avaible:
        DeltaTouch = deltaPlatform.touch_place()
        solutionDelta = ground_check(playertouch, DeltaTouch)
    if epsilonPlatform.avaible:
        EpsilonTouch = epsilonPlatform.touch_place()
        solutionEpsilon = ground_check(playertouch, EpsilonTouch)
    if zetaPlatform.avaible:
        ZetaTouch = zetaPlatform.touch_place()
        solutionZeta = ground_check(playertouch, ZetaTouch)
    if etaPlatform.avaible:
        EtaTouch = etaPlatform.touch_place()
        solutionEta = ground_check(playertouch, EtaTouch)
    if thetaPlatform.avaible:
        ThetaTouch = thetaPlatform.touch_place()
        solutionTheta = ground_check(playertouch, ThetaTouch)
    if iotaPlatform.avaible:
        IotaTouch = iotaPlatform.touch_place()
        solutionIota = ground_check(playertouch, IotaTouch)

    if (solutionBase is True) | (solutionAlpha is True) | (solutionBeta is True) | (solutionGamma is True) | (
            solutionDelta is True) | (solutionEpsilon is True) | (solutionZeta is True) | (solutionEta is True) | (
            solutionTheta is True) | (solutionIota is True):
        globalsolution = True
    return globalsolution

def ground_check(playertouch, platformtouch):  # Проверка земли под ногами по массивам
    solution = False
    if platformtouch[0] == playertouch[0]:
        if (playertouch[1] >= platformtouch[1]) & (playertouch[1] <= platformtouch[2]):
            solution = True
        if (playertouch[2] >= platformtouch[1]) & (playertouch[2] <= platformtouch[2]):
            solution = True
    return solution

# Под платформой
def grannyunderplatform():  # Определение платформ на уровнях !!!Не забывать добавлять!!!
    globalsolution = True
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    solutionEta = False
    solutionTheta = False
    solutionIota = False

    playertouch = Hero.touch_head()
    if alphaPlatform.avaible:
        AlphaTouch = alphaPlatform.touch_head()
        solutionAlpha = head_check(playertouch, AlphaTouch)
    if betaPlatform.avaible:
        BetaTouch = betaPlatform.touch_head()
        solutionBeta = head_check(playertouch, BetaTouch)
    if gammaPlatform.avaible:
        GammaTouch = gammaPlatform.touch_head()
        solutionGamma = head_check(playertouch, GammaTouch)
    if deltaPlatform.avaible:
        DeltaTouch = deltaPlatform.touch_head()
        solutionDelta = head_check(playertouch, DeltaTouch)
    if epsilonPlatform.avaible:
        EpsilonTouch = epsilonPlatform.touch_head()
        solutionEpsilon = head_check(playertouch, EpsilonTouch)
    if zetaPlatform.avaible:
        ZetaTouch = zetaPlatform.touch_head()
        solutionZeta = head_check(playertouch, ZetaTouch)
    if etaPlatform.avaible:
        EtaTouch = etaPlatform.touch_head()
        solutionEta = head_check(playertouch, EtaTouch)
    if thetaPlatform.avaible:
        ThetaTouch = thetaPlatform.touch_head()
        solutionTheta = head_check(playertouch, ThetaTouch)
    if iotaPlatform.avaible:
        IotaTouch = iotaPlatform.touch_head()
        solutionIota = head_check(playertouch, IotaTouch)

    if (solutionAlpha is False) & (solutionBeta is False) & (solutionGamma is False) & (solutionDelta is False) & (
            solutionEpsilon is False) & (solutionZeta is False) & (solutionEta is False) & (solutionTheta is False) & (
            solutionIota is False):
        globalsolution = False
    return globalsolution

def head_check(playertouch, platformtouch):  # Проверка земли над головой по массивам
    solution = False
    if platformtouch[0] == playertouch[0]:
        if (playertouch[1] >= platformtouch[1]) & (playertouch[1] <= platformtouch[2]):
            solution = True
        if (playertouch[2] >= platformtouch[1]) & (playertouch[2] <= platformtouch[2]):
            solution = True
    return solution

# Туземец и персонаж
def savagehitgranny():
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    playerzone = Hero.actionzone()
    if alphaSavage.avaible:
        Alphazone = alphaSavage.actionzone()
        solutionAlpha = action_check(playerzone, Alphazone, 24)
    if betaSavage.avaible:
        Betazone = betaSavage.actionzone()
        solutionBeta = action_check(playerzone, Betazone, 24)
    if gammaSavage.avaible:
        Gammazone = gammaSavage.actionzone()
        solutionGamma = action_check(playerzone, Gammazone, 24)
    if deltaSavage.avaible:
        Deltazone = deltaSavage.actionzone()
        solutionDelta = action_check(playerzone, Deltazone, 24)

    if (solutionAlpha is True) | (solutionBeta is True) | (solutionGamma is True) | (solutionDelta is True):
        globalsolution = True

    return globalsolution

def grannyhitsavage():
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    playerzone = Hero.hit_area()
    if alphaSavage.avaible:
        Alphazone = alphaSavage.actionzone()
        solutionAlpha = action_check(playerzone, Alphazone, 24)
    if betaSavage.avaible:
        Betazone = betaSavage.actionzone()
        solutionBeta = action_check(playerzone, Betazone, 24)
    if gammaSavage.avaible:
        Gammazone = gammaSavage.actionzone()
        solutionGamma = action_check(playerzone, Gammazone, 24)
    if deltaSavage.avaible:
        Deltazone = deltaSavage.actionzone()
        solutionDelta = action_check(playerzone, Deltazone, 24)

    if (solutionAlpha is True) | (solutionBeta is True) | (solutionGamma is True) | (solutionDelta is True):
        globalsolution = True

    return [globalsolution, solutionAlpha, solutionBeta, solutionGamma, solutionDelta]

# Лестница и персонаж
def topladder(theladder, theplayer):
    ladderaction = theladder.actionzone()
    playeraction = theplayer.actionzone()
    if ladderaction[2] >= playeraction[3]:
        theladder.isLadderTop = True
    else:
        theladder.isLadderTop = False

def grannyonladder():
    global ladd
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    playerzone = Hero.actionzone()
    if alphaLadder.avaible:
        Alphazone = alphaLadder.actionzone()
        solutionAlpha = action_check(playerzone, Alphazone, 15)
        topladder(alphaLadder, Hero)
    if betaLadder.avaible:
        Betazone = betaLadder.actionzone()
        solutionBeta = action_check(playerzone, Betazone, 15)
        topladder(betaLadder, Hero)
    if gammaLadder.avaible:
        Gammazone = gammaLadder.actionzone()
        solutionGamma = action_check(playerzone, Gammazone, 15)
        topladder(gammaLadder, Hero)
    if deltaLadder.avaible:
        Deltazone = deltaLadder.actionzone()
        solutionDelta = action_check(playerzone, Deltazone, 15)
        topladder(deltaLadder, Hero)
    if epsilonLadder.avaible:
        Epsilonzone = epsilonLadder.actionzone()
        solutionEpsilon = action_check(playerzone, Epsilonzone, 15)
        topladder(epsilonLadder, Hero)
    if zetaLadder.avaible:
        Zetazone = zetaLadder.actionzone()
        solutionZeta = action_check(playerzone, Zetazone, 15)
        topladder(zetaLadder, Hero)

    if (solutionAlpha is True) | (solutionBeta is True) | (solutionGamma is True) | (solutionDelta is True) | (
            solutionEpsilon is True) | (solutionZeta is True):
        globalsolution = True

    if ((alphaLadder.isLadderTop is True) | (betaLadder.isLadderTop is True) | (gammaLadder.isLadderTop is True) | (
        deltaLadder.isLadderTop is True) | (epsilonLadder.isLadderTop is True) | (zetaLadder.isLadderTop is True)) & (
        Hero.lastanimation == "Climbing"):
        objectsVariable.isLadderTop = True
    else:
        objectsVariable.isLadderTop = False

    if ladd is False:
        objectsVariable.isLadderTop = False

    return globalsolution

# Кот и персоныж
def grannycarrycat():  # Определение котов на уровне !!!Не забывать добавлять!!!
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    playerzone = Hero.actionzone()
    if alphaCat.avaible:
        Alphazone = alphaCat.actionzone()
        solutionAlpha = action_check(playerzone, Alphazone, 10)
        if solutionAlpha is True:
            alphaCat.collect()
            objectsVariable.Score += settings["ScoreAddCat"]  # Зачисляем очки
            objectsVariable.CatAmountReal += 1
    if betaCat.avaible:
        Betazone = betaCat.actionzone()
        solutionBeta = action_check(playerzone, Betazone, 10)
        if solutionBeta is True:
            betaCat.collect()
            objectsVariable.Score += settings["ScoreAddCat"]  # Зачисляем очки
            objectsVariable.CatAmountReal += 1
    if gammaCat.avaible:
        Gammazone = gammaCat.actionzone()
        solutionGamma = action_check(playerzone, Gammazone, 10)
        if solutionGamma is True:
            gammaCat.collect()
            objectsVariable.Score += settings["ScoreAddCat"]  # Зачисляем очки
            objectsVariable.CatAmountReal += 1
    if deltaCat.avaible:
        Deltazone = deltaCat.actionzone()
        solutionDelta = action_check(playerzone, Deltazone, 10)
        if solutionDelta is True:
            deltaCat.collect()
            objectsVariable.Score += settings["ScoreAddCat"]  # Зачисляем очки
            objectsVariable.CatAmountReal += 1
    if epsilonCat.avaible:
        Epsilonzone = epsilonCat.actionzone()
        solutionEpsilon = action_check(playerzone, Epsilonzone, 10)
        if solutionEpsilon is True:
            epsilonCat.collect()
            objectsVariable.Score += settings["ScoreAddCat"]  # Зачисляем очки
            objectsVariable.CatAmountReal += 1
    if zetaCat.avaible:
        Zetazone = zetaCat.actionzone()
        solutionZeta = action_check(playerzone, Zetazone, 10)
        if solutionZeta is True:
            zetaCat.collect()
            objectsVariable.Score += settings["ScoreAddCat"]  # Зачисляем очки
            objectsVariable.CatAmountReal += 1
    if (solutionAlpha is True) | (solutionBeta is True) | (solutionGamma is True) | (solutionDelta is True) | (
            solutionEpsilon is True) | (solutionZeta is True):
        if soundmode.get():
            mixer.Channel(3).play(mixer.Sound(random.choice(soundPaths.cat)))
        globalsolution = True

    return globalsolution

# Цветочек и персонаж
def grannygetbonus():  # Определение цветочков на уровне !!!Не забывать добавлять!!!
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    playerzone = Hero.actionzone()
    if alphaBonus.avaible:
        Alphazone = alphaBonus.actionzone()
        solutionAlpha = action_check(playerzone, Alphazone, 16)
        if solutionAlpha is True:
            objectsVariable.Score += settings["ScoreAddBonus"]
            alphaBonus.rise()
    if betaBonus.avaible:
        Betazone = betaBonus.actionzone()
        solutionBeta = action_check(playerzone, Betazone, 16)
        if solutionBeta is True:
            objectsVariable.Score += settings["ScoreAddBonus"]
            betaBonus.rise()
    if gammaBonus.avaible:
        Gammazone = gammaBonus.actionzone()
        solutionGamma = action_check(playerzone, Gammazone, 16)
        if solutionGamma is True:
            objectsVariable.Score += settings["ScoreAddBonus"]
            gammaBonus.rise()
    if deltaBonus.avaible:
        Deltazone = deltaBonus.actionzone()
        solutionDelta = action_check(playerzone, Deltazone, 16)
        if solutionDelta is True:
            objectsVariable.Score += settings["ScoreAddBonus"]
            deltaBonus.rise()
    if epsilonBonus.avaible:
        Epsilonzone = epsilonBonus.actionzone()
        solutionEpsilon = action_check(playerzone, Epsilonzone, 16)
        if solutionEpsilon is True:
            objectsVariable.Score += settings["ScoreAddBonus"]
            epsilonBonus.rise()
    if zetaBonus.avaible:
        Zetazone = zetaBonus.actionzone()
        solutionZeta = action_check(playerzone, Zetazone, 16)
        if solutionZeta is True:
            objectsVariable.Score += settings["ScoreAddBonus"]
            zetaBonus.rise()
    if (solutionAlpha is True) | (solutionBeta is True) | (solutionGamma is True) | (solutionDelta is True) | (
            solutionEpsilon is True) | (solutionZeta is True):
        globalsolution = True
        if soundmode.get():
            mixer.Channel(1).play(mixer.Sound(soundPaths.bonus))
    return globalsolution

# Грибочки и персонаж
def grannyfastroom():
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    playerzone = Hero.actionzone()
    if alphaFastroom.avaible:
        Alphazone = alphaFastroom.actionzone()
        solutionAlpha = action_check(playerzone, Alphazone, 15)
        if solutionAlpha is True:
            objectsVariable.isFastEffect = True
    if betaFastroom.avaible:
        Betazone = betaFastroom.actionzone()
        solutionBeta = action_check(playerzone, Betazone, 15)
        if solutionBeta is True:
            objectsVariable.isFastEffect = True
    if (solutionAlpha is True) | (solutionBeta is True):
        globalsolution = True
        if objectsVariable.isFastroomSoundPlayed is False:
            if soundmode.get():
                mixer.Channel(2).play(mixer.Sound(soundPaths.mushroom))
            objectsVariable.isFastroomSoundPlayed = True
    else:
        objectsVariable.isFastroomSoundPlayed = False

    return globalsolution

def grannyslowroom():
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    playerzone = Hero.actionzone()
    if alphaSlowroom.avaible:
        Alphazone = alphaSlowroom.actionzone()
        solutionAlpha = action_check(playerzone, Alphazone, 15)
        if solutionAlpha is True:
            objectsVariable.isSlowEffect = True
    if betaSlowroom.avaible:
        Betazone = betaSlowroom.actionzone()
        solutionBeta = action_check(playerzone, Betazone, 15)
        if solutionBeta is True:
            objectsVariable.isSlowEffect = True
    if (solutionAlpha is True) | (solutionBeta is True):
        globalsolution = True
        if objectsVariable.isSlowroomSoundPlayed is False:
            if soundmode.get():
                mixer.Channel(2).play(mixer.Sound(soundPaths.mushroom))
            objectsVariable.isSlowroomSoundPlayed = True
    else:
        objectsVariable.isSlowroomSoundPlayed = False

    return globalsolution

def grannygravroom():
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    playerzone = Hero.actionzone()
    if alphaGravroom.avaible:
        Alphazone = alphaGravroom.actionzone()
        solutionAlpha = action_check(playerzone, Alphazone, 15)
        if solutionAlpha is True:
            objectsVariable.isGravEffect = True
    if betaGravroom.avaible:
        Betazone = betaGravroom.actionzone()
        solutionBeta = action_check(playerzone, Betazone, 15)
        if solutionBeta is True:
            objectsVariable.isGravEffect = True
    if (solutionAlpha is True) | (solutionBeta is True):
        globalsolution = True
        if objectsVariable.isGravroomSoundPlayed is False:
            if soundmode.get():
                mixer.Channel(2).play(mixer.Sound(soundPaths.mushroom))
            objectsVariable.isGravroomSoundPlayed = True
    else:
        objectsVariable.isGravroomSoundPlayed = False

    return globalsolution

# Выход с уровня
def grannyinexit():  # Определение выхода на уровне
    globalsolution = False
    if level != 0:
        playerzone = Hero.actionzone()
        Exitzone = Exit.actionzone()
        globalsolution = action_check(playerzone, Exitzone, 30)
    return globalsolution

# Стены для персонажа и дикаря
def grannyandwall():
    global wallside
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    playerzone = Hero.actionzone()
    if alphaWall.avaible:
        Alphazone = alphaWall.actionzone()
        solutionAlpha = wall_check(playerzone, Alphazone, None)
    if betaWall.avaible:
        Betazone = betaWall.actionzone()
        solutionBeta = wall_check(playerzone, Betazone, None)
    if gammaWall.avaible:
        Gammazone = gammaWall.actionzone()
        solutionGamma = wall_check(playerzone, Gammazone, None)
    if deltaWall.avaible:
        Deltazone = deltaWall.actionzone()
        solutionDelta = wall_check(playerzone, Deltazone, None)
    if epsilonWall.avaible:
        Epsilonzone = epsilonWall.actionzone()
        solutionEpsilon = wall_check(playerzone, Epsilonzone, None)
    if zetaWall.avaible:
        Zetazone = zetaWall.actionzone()
        solutionZeta = wall_check(playerzone, Zetazone, None)
    if (solutionAlpha is True) | (solutionBeta is True) | (solutionGamma is True) | (solutionDelta is True) | (
            solutionEpsilon is True) | (solutionZeta is True):
        globalsolution = True

    if globalsolution is False:
        wallside = "0"

    return globalsolution

def wall_check(playerzone, wallzone, thesavage):  # Проверка стен по массивам
    global wallside
    solution = False
    if (playerzone[0] + 16 >= wallzone[0]) & (playerzone[0] + 16 <= wallzone[1]):
        if (playerzone[2] >= wallzone[2]) & (playerzone[2] <= wallzone[3]):
            solution = True
        if (playerzone[3] >= wallzone[2]) & (playerzone[3] <= wallzone[3]):
            if thesavage is None:
                wallside = "R"
            else:
                thesavage.wallside = "R"
            solution = True
    if (playerzone[1] - 16 >= wallzone[0]) & (playerzone[1] - 16 <= wallzone[1]):
        if (playerzone[2] >= wallzone[2]) & (playerzone[2] <= wallzone[3]):
            solution = True
        if (playerzone[3] >= wallzone[2]) & (playerzone[3] <= wallzone[3]):
            if thesavage is None:
                wallside = "L"
            else:
                thesavage.wallside = "L"
            solution = True
    return solution

def anysavageandwall(theobject): # Проверяет столкновение для одного любого Дикаря
    globalsolution = False
    solutionAlpha = False
    solutionBeta = False
    solutionGamma = False
    solutionDelta = False
    solutionEpsilon = False
    solutionZeta = False
    savagezone = theobject.actionzone()
    if alphaWall.avaible:
        Alphazone = alphaWall.actionzone()
        solutionAlpha = wall_check(savagezone, Alphazone, theobject)
    if betaWall.avaible:
        Betazone = betaWall.actionzone()
        solutionBeta = wall_check(savagezone, Betazone, theobject)
    if gammaWall.avaible:
        Gammazone = gammaWall.actionzone()
        solutionGamma = wall_check(savagezone, Gammazone, theobject)
    if deltaWall.avaible:
        Deltazone = deltaWall.actionzone()
        solutionDelta = wall_check(savagezone, Deltazone, theobject)
    if epsilonWall.avaible:
        Epsilonzone = epsilonWall.actionzone()
        solutionEpsilon = wall_check(savagezone, Epsilonzone, theobject)
    if zetaWall.avaible:
        Zetazone = zetaWall.actionzone()
        solutionZeta = wall_check(savagezone, Zetazone, theobject)
    if (solutionAlpha is True) | (solutionBeta is True) | (solutionGamma is True) | (solutionDelta is True) | (
            solutionEpsilon is True) | (solutionZeta is True):
        globalsolution = True

    if globalsolution is False:
        theobject.wallside = "0"

    return globalsolution

# Гравитация
def gravity():  # Если персонаж не на платформн и не на лестнице, на нее действует гравитация
    global simpgrav
    if ((plat is False) | (antigrav is True)) & (ladd is False):
        simpgrav = True
        Hero.gravitymove()
    else:
        simpgrav = False

# Эффекты грибов
def effects():
    global lasteffecttime, gravitySpeed, grannyWalkSpeed, antigrav, avoidEffects
    if objectsVariable.isFastEffect:
        grannyWalkSpeed = grannyWalkSpeedFast
        lasteffecttime = time.time()
        labelFast.place(x=500, y=475)
        labelEffect.place(x=450, y=475)
        labelSlow.place_forget()
        objectsVariable.isFastEffect = False
    if objectsVariable.isSlowEffect:
        grannyWalkSpeed = grannyWalkSpeedSlow
        lasteffecttime = time.time()
        labelSlow.place(x=545, y=475)
        labelEffect.place(x=450, y=475)
        labelFast.place_forget()
        objectsVariable.isSlowEffect = False
    if objectsVariable.isGravEffect:
        gravitySpeed = gravitySpeedInvert
        lasteffecttime = time.time()
        labelGrav.place(x=590, y=475)
        labelEffect.place(x=450, y=475)
        antigrav = True
        objectsVariable.isGravEffect = False
    if time.time() - lasteffecttime < effectduration:
        TimeStr = "%.2f с" % (effectduration - (time.time() - lasteffecttime))
        labelEffect.config(text=TimeStr)
    if ((objectsVariable.isFastEffect is False) & (objectsVariable.isSlowEffect is False) & (
            objectsVariable.isGravEffect == False) & (
                time.time() - lasteffecttime >= effectduration)) | avoidEffects:
        labelFast.place_forget()
        labelSlow.place_forget()
        labelGrav.place_forget()
        labelEffect.place_forget()
        avoidEffects = False
        antigrav = False
        grannyWalkSpeed = grannyWalkSpeedNormal
        gravitySpeed = gravitySpeedNormal

# Убийства
def savageKill():
    global alphaSavage, betaSavage, gammaSavage, deltaSavage
    if GraHitSav[0]:
        if alphaSavage.avaible & GraHitSav[1]:
            canvas.delete(alphaSavage.id)
            alphaSavage = Empty()
        if betaSavage.avaible & GraHitSav[2]:
            canvas.delete(betaSavage.id)
            betaSavage = Empty()
        if gammaSavage.avaible & GraHitSav[3]:
            canvas.delete(gammaSavage.id)
            gammaSavage = Empty()
        if deltaSavage.avaible & GraHitSav[4]:
            canvas.delete(deltaSavage.id)
            deltaSavage = Empty()

def grannyKill():
    global Hero
    if SavHitGra:
        if soundmode.get():
            mixer.Channel(1).play(mixer.Sound(random.choice(soundPaths.savagehit)))
        canvas.delete(Hero.id)
        objectsVariable.lives -= 1
        if objectsVariable.lives < 0:
            endgame(win=False)
        else:
            Hero = Granny(spawncoords=settings['levels'][level]['spawnCoords'], canvas=canvas, image=image.granny)

# Функции Дикаря
# Платформа по которой он ходит
def savagePlates(thesavage, homeplatform):
    if homeplatform == "base":
        thesavage.way = Base.border()
    if homeplatform == "alpha":
        if alphaPlatform.avaible:
            thesavage.way = alphaPlatform.border()
        else:
            thesavage.way = Base.border()
    if homeplatform == "beta":
        if betaPlatform.avaible:
            thesavage.way = betaPlatform.border()
        else:
            thesavage.way = Base.border()
    if homeplatform == "gamma":
        if gammaPlatform.avaible:
            thesavage.way = gammaPlatform.border()
        else:
            thesavage.way = Base.border()
    if homeplatform == "delta":
        if deltaPlatform.avaible:
            thesavage.way = deltaPlatform.border()
        else:
            thesavage.way = Base.border()
    if homeplatform == "epsilon":
        if epsilonPlatform.avaible:
            thesavage.way = epsilonPlatform.border()
        else:
            thesavage.way = Base.border()
    if homeplatform == "zeta":
        if zetaPlatform.avaible:
            thesavage.way = zetaPlatform.border()
        else:
            thesavage.way = Base.border()
    if homeplatform == "eta":
        if etaPlatform.avaible:
            thesavage.way = etaPlatform.border()
        else:
            thesavage.way = Base.border()
    if homeplatform == "theta":
        if thetaPlatform.avaible:
            thesavage.way = thetaPlatform.border()
        else:
            thesavage.way = Base.border()
    if homeplatform == "iota":
        if iotaPlatform.avaible:
            thesavage.way = iotaPlatform.border()
        else:
            thesavage.way = Base.border()

# Изменение направления при встрече с концом платформы
def savageDirection(thesavage):
    coords = thesavage.coords()
    way = thesavage.way
    if coords[0] <= way[0]:
        thesavage.changedirection()
    elif coords[0] >= way[1]:
        thesavage.changedirection()

# Установка платформ и направлений
def savageWalking():
    if alphaSavage.avaible:
        homeplatform = settings["levels"][level]["alphaSavagePlatform"]
        savagePlates(alphaSavage, homeplatform)
        if anysavageandwall(alphaSavage):
            alphaSavage.changedirection()
        else:
            savageDirection(alphaSavage)
    if betaSavage.avaible:
        homeplatform = settings["levels"][level]["betaSavagePlatform"]
        savagePlates(betaSavage, homeplatform)
        if anysavageandwall(betaSavage):
            betaSavage.changedirection()
        else:
            savageDirection(betaSavage)
    if gammaSavage.avaible:
        homeplatform = settings["levels"][level]["gammaSavagePlatform"]
        savagePlates(gammaSavage, homeplatform)
        if anysavageandwall(gammaSavage):
            gammaSavage.changedirection()
        else:
            savageDirection(gammaSavage)
    if deltaSavage.avaible:
        homeplatform = settings["levels"][level]["deltaSavagePlatform"]
        savagePlates(deltaSavage, homeplatform)
        if anysavageandwall(deltaSavage):
            deltaSavage.changedirection()
        else:
            savageDirection(deltaSavage)

# Организация движений
def savageMove(thesavage):
    if thesavage.direction == "right":
        thesavage.turn_right()
    else:
        thesavage.turn_left()

# Вызов очереди действий существующих дикарей
def savageActions():
    if alphaSavage.avaible:
        savageMove(alphaSavage)
        alphaSavage.action_queue()
    if betaSavage.avaible:
        savageMove(betaSavage)
        betaSavage.action_queue()
    if gammaSavage.avaible:
        savageMove(gammaSavage)
        gammaSavage.action_queue()
    if deltaSavage.avaible:
        savageMove(deltaSavage)
        deltaSavage.action_queue()

# Анимация существующих дикарей
def savageAnimate():
    if alphaSavage.avaible:
        alphaSavage.animate()
    if betaSavage.avaible:
        betaSavage.animate()
    if gammaSavage.avaible:
        gammaSavage.animate()
    if deltaSavage.avaible:
        deltaSavage.animate()

# Проверка на сбор котиков. Открытие цветка и выход с уровня
def recquecountertoexit():
    global isExitActive
    if objectsVariable.CatAmountReal == objectsVariable.CatAmountAll:
        isExitActive = True
        Exit.opening()
        if grannyinexit() is True:
            LevelAdd()
    else:
        isExitActive = False

# Организация временных ограничений уровней
def levelLimit():
    global limitedFlag, limitedtime
    if settings["levels"][level]["limited"]:
        if limitedFlag is False:
            limitedFlag = True
            limitedtime = time.time()
            labelTime.place(x=50, y=475)
            labelTimer.place(x=90, y=475)
        elif limitedFlag is True:
            if time.time() - limitedtime < settings["levels"][level]["time"]:
                TimeStr = "%.2f с" % (settings["levels"][level]["time"] - (time.time() - limitedtime))
                labelTimer.config(text=TimeStr)
            if (time.time() - limitedtime) > settings["levels"][level]["time"]:
                limitedFlag = False
                if settings["levels"][level]["limittype"] == "NEXT":
                    LevelAdd()
                elif settings["levels"][level]["limittype"] == "LOSE":
                    endgame(win=False)
    else:
        limitedFlag = False
        labelTime.place_forget()
        labelTimer.place_forget()

# Организация конца игры, вывод сообщений о выйгрыше/проигрыше
def endgame(win):
    if win:
        objectsVariable.GlobalScore += objectsVariable.Score
        message = "Поздравляем с победой! \nВы набрали %i из %i очков" % (
            objectsVariable.GlobalScore, settings["ScoreMax"])
        mb.showinfo(title="Победа", message=message)
        mainmenu_open()
    else:
        objectsVariable.GlobalScore += objectsVariable.Score
        message = "К сожалению, Вы проиграли. \nВы набрали %i из %i очков" % (
            objectsVariable.GlobalScore, settings["ScoreMax"])
        mb.showinfo(title="Проигрыш", message=message)
        mainmenu_open()

# Подсчет кликов и кадров
def timer():
    global  keytime, KeySpeed, fps, fpsGlobal
    if (time.time() - keytime) >= 1:
        KeySpeed = objectsVariable.keyCounter
        fpsGlobal = fps
        fps = 0
        objectsVariable.keyCounter = 0
        keytime = time.time()
    if KeySpeed > settings["keyboardLimit"]:
        message = "Скорость клавиатуры превышает допустимую. \n Допустимая: %i \n Текущая: %i \n" % (
            settings["keyboardLimit"], KeySpeed) + "Измените скорость в настройках компьютера на %i пунктов" % (
            settings["keyboardLimit"] - KeySpeed)
        mb.showwarning(title="Настройте клавиатуру", message=message)

# Выбор цвета фона
def color():
    global backgroundcolor
    newbackground = cc.askcolor()
    backgroundcolor = newbackground[1]
    reloadScreen()

# Включение и отключение кнопок меню сверху
def buttonstate():
    global shouldReloadButtons
    if shouldReloadButtons:
        if level == 0:
            gamemenu.entryconfig("Выход в меню", state="disabled")
            gamemenu.entryconfig("Начать уровень заново", state="disabled")
            gamemenu.entryconfig("Выбор уровня", state="normal")
        else:
            gamemenu.entryconfig("Выход в меню", state="normal")
            gamemenu.entryconfig("Начать уровень заново", state="normal")
            if not settings["cheatmode"]:
                gamemenu.entryconfig("Выбор уровня", state="disabled")

    shouldReloadButtons = False

# Опрос выхода в главное меню
def on_mainmenu():
    ask = mb.askyesno(title="Выход в меню", message="Вы действительно хотите выйти в меню?")
    if ask:
        mainmenu_open()

# Составление меню
def menu():  # Описание меню(сверху полоска)
    global gamemenu
    mainmenu = Menu(root)
    gamemenu = Menu(mainmenu, tearoff=0, bg=backgroundcolor)
    gamemenu.add_command(label="Новая игра", command=newgame)
    gamemenu.add_command(label="Начать уровень заново", command=LevelRestart)
    gamemenu.add_command(label="Выбор уровня", command=LevelShoose)
    gamemenu.add_separator()
    optionmenu = Menu(gamemenu, tearoff=1, bg=backgroundcolor)
    musicmenu = Menu(optionmenu, tearoff=1, bg=backgroundcolor)
    musicmenu.add_command(label="Громкость", command=setvolumemusic)
    musicmenu.add_radiobutton(label="Включена", value=True, variable=musicmode)
    musicmenu.add_radiobutton(label="Отключена", value=False, variable=musicmode)
    soundmenu = Menu(optionmenu, tearoff=1, bg=backgroundcolor)
    soundmenu.add_command(label="Громкость", command=setvolumesound)
    soundmenu.add_radiobutton(label="Включена", value=True, variable=soundmode)
    soundmenu.add_radiobutton(label="Отключена", value=False, variable=soundmode)
    debugmenu = Menu(optionmenu, tearoff=1, bg=backgroundcolor)
    debugmenu.add_radiobutton(label="Отключена", value=0, variable=debugmode)
    debugmenu.add_radiobutton(label="Флаги персонажа", value=1, variable=debugmode)
    debugmenu.add_radiobutton(label="Флаги обьектов", value=2, variable=debugmode)
    debugmenu.add_radiobutton(label="Положение", value=3, variable=debugmode)
    debugmenu.add_radiobutton(label="Системное", value=4, variable=debugmode)
    gamemenu.add_cascade(label="Настройки", menu=optionmenu)
    optionmenu.add_cascade(label="Музыка", menu=musicmenu)
    optionmenu.add_cascade(label="Звуки", menu=soundmenu)
    optionmenu.add_command(label="Выбрать цвет фона", command=color)
    optionmenu.add_cascade(label="Отладка", menu=debugmenu)
    gamemenu.add_separator()
    gamemenu.add_command(label="Выход в меню", command=on_mainmenu)
    gamemenu.add_command(label="Выход", command=on_closing)
    aboutmenu = Menu(mainmenu, tearoff=0, bg=backgroundcolor)
    aboutmenu.add_command(label="Авторы", command=lambda: mb.showinfo(title="Авторы", message=authorsmessage))
    aboutmenu.add_command(label="Об игре", command=lambda: mb.showinfo(title="Об игре", message=aboutmessage))
    mainmenu.add_cascade(label="Игра", menu=gamemenu)
    mainmenu.add_cascade(label="Справка", menu=aboutmenu)
    root.config(menu=mainmenu)

# Перезагрузка экрана
def reloadScreen():
    labelLevel.grid_forget()
    labelScore.grid_forget()
    labelCats.grid_forget()
    labelLives.grid_forget()
    statusbar.place_forget()
    labelLevel.config(bg=backgroundcolor)
    labelScore.config(bg=backgroundcolor)
    labelCats.config(bg=backgroundcolor)
    labelLives.config(bg=backgroundcolor)
    statusbar.config(bg=backgroundcolor)
    root.configure(bg=backgroundcolor)
    loadScreen()
    menu()

Hero = Empty()
menu()  # Создаем меню
mainmenu_open()  # Запускаем заглавный экран
root.protocol("WM_DELETE_WINDOW", on_closing)  # Обработка выхода при нажатии на крестик
# Главный цикл
while run:
    if (time.time() - lastframetime) >= settings["frametime"]:
        fps += 1
        music()
        if level != 0:  # Если игра идет
            plat = grannyoverplatform()  # Cтоит ли персонаж на платформе
            carr = grannycarrycat()  # Подбирает ли персонаж котенка
            vent = grannyinexit()  # Стоит ли персонаж у выходв
            barr = grannyandwall()  # Стоит ли персонаж у стены
            flow = grannygetbonus()  # Стоит ли персонаж у цветочка
            fast = grannyfastroom()  # Стоит ли персонаж у Быстромора
            grav = grannygravroom()  # Стоит ли персонаж у Вверхшенки
            slow = grannyslowroom()  # Стоит ли персонаж у Медлянки
            head = grannyunderplatform()  # Стоит ли персонаж под платформой
            SavHitGra = savagehitgranny()  # Может ли Дикарь убить персонажа
            GraHitSav = grannyhitsavage()  # Может ли персонаж убить Дикаря
            grannyKill()  # Проверка смерти персонажа
            effects()  # Применение эффектов от грибов
            levelLimit()  # Применение временных ограничений
            recquecountertoexit()  # Делаем проверку готовность выйти с уровня
            status()  # Обновляем статусбар и данные для пользователя
            savageWalking()  # Дикарь
            savageActions()
            savageAnimate()
            if Hero.avaible:  # Если герой есть, применяем к нему
                ladd = grannyonladder()  # Стоит ли персонаж на лестнице
                Hero.action_queue()  # Выполнение очереди действий
                gravity()  # Применяем к персонажу фактор графитации
                Hero.animate()  # Анимируем персонажа
        buttonstate()
        timer()
        root.update_idletasks()  # Обновляем объекты окна
        root.update()
        lastframetime = time.time()
