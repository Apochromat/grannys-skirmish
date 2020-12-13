# Granny`s Skirmish
# version 0.9.11

"""Импорт"""
import platform
from tkinter import *
from tkinter import colorchooser as cc
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from pygame import mixer
from images import *
from objects import *
from music import *
from achievements import *

"""Файл настроек"""
with open("data.json", 'r', encoding="utf-8") as file:  # Открываем файл с настройками
    settings = json.load(file)  # Записываем как словарь в переменную

"""Данные игрока"""
playerData = PlayerData()
playerData.data["lastlives"] = settings["livesnormal"]
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
last_frame_time = time.time()  # Последнее время кадра

isExitActive = False  # Доступен ли выход с уровня
avoidEffects = False  # Необходимо ли сбросить эффекты

antigrav = False  # Включена ли антигравитация
simpgrav = False  # Двигается ли персонаж под действием гравитации
wall_side = "0"  # Сторона стенки в которую уперся персонаж

isMusicOn = False

keytime = time.time()  # Время последнего нажатия на клавиши
KeySpeed = 0  # Скорость нажатий за секунду
fps = 0  # Моментальная частота кадров
fpsGlobal = 0  # Частота кадров

limitedFlag = False  # Ограничен ли уровень по времени
limitedtime = 0  # Время включения ограничения

objectsVariable.lives = settings['livesnormal']  # Переменное количество жизней на уровне
objectsVariable.GlobalLives = objectsVariable.lives
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
    if music_mode.get() is False:
        music_stop()
    if level == 0:
        if typeMusic == 1:
            isMusicOn = False
        typeMusic = 0
    else:
        if typeMusic == 0:
            isMusicOn = False
        typeMusic = 1

    if (music_mode.get() is True) & (typeMusic == 0) & (isMusicOn is False):
        music_stop()
        if sysName == "Windows":
            mixer.music.load(musicPaths.mainmenuWin)
        else:
            mixer.music.load(musicPaths.mainmenuLin)
        mixer.music.play(loops=200)
        isMusicOn = True

    if (music_mode.get() is True) & (typeMusic == 1) & (isMusicOn is False):
        music_stop()
        if sysName == "Windows":
            mixer.music.load(musicPaths.levelWin)
        else:
            mixer.music.load(musicPaths.levelLin)
        mixer.music.play(loops=1000)
        isMusicOn = True


"""Элементы окна"""
status_bar = Label(root, justify=LEFT, text="Готов", width=settings["statusbarwidth"], height=1,
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
def button_clear():
    newgameButt.place_forget()
    continueButt.place_forget()
    exitgameButt.place_forget()


# Начало новой игры
def new_game():
    global level
    if (level != 0) | (playerData.data["lastlevel"] != 1) | playerData.data["achievements"]["end"]:
        ask = mb.askyesno(title="Внимание", message="Вы действительно хотите начать новую игру? \n"
                                                    "Ваш прогресс бедет утерян.")
        if ask:
            objectsVariable.lives = settings['livesnormal']
            level = 0
            playerData.erase_data()
            objectsVariable.Score = 0
            objectsVariable.GlobalScore = 0
            button_clear()
            level_adding()
    else:
        objectsVariable.lives = settings['livesnormal']
        level = 0
        playerData.erase_data()
        objectsVariable.Score = 0
        objectsVariable.GlobalScore = 0
        button_clear()
        level_adding()


def continuegame():
    global level
    if (playerData.data["achievements"]["end"] is True) & (playerData.data["islevelcyclecompleted"] is True):
        mb.showinfo(title="Новая игра+", message="Вы закончили основную игру."
                                                 "\nНачинается новая игра+, достижения и рекорды сохранятся.")
        playerData.data["islevelcyclecompleted"] = False
        playerData.data["killedsavages"] = 0
        playerData.data["wateredflowers"] = 0
        objectsVariable.lives = settings["livesnormal"]
        objectsVariable.Score = 0
        objectsVariable.GlobalScore = 0
        button_clear()
        level_adding()
    else:
        objectsVariable.lives = playerData.data["lastlives"]
        level = playerData.data["lastlevel"]
        objectsVariable.Score = 0
        objectsVariable.GlobalScore = playerData.data["lastscore"]
        button_clear()
        level_initialization()


# Опрос закрытия программы
def on_closing():  # Опрос закрытия
    global run
    if mb.askokcancel("Выход", "Вы уже уходите?"):
        print("Выход")
        run = False
        root.destroy()


# Кнопки главного меню
newgameButt = Button(root, image=image.newgame, command=new_game, borderwidth=0, bd=0)
continueButt = Button(root, image=image.continuegame, command=continuegame, borderwidth=0, bd=0)
exitgameButt = Button(root, image=image.quit, command=on_closing, borderwidth=0, bd=0)


# Добавление элементов в окно
def load_screen():
    labelLevel.grid(row=0, column=0)
    labelScore.grid(row=0, column=1)
    labelCats.grid(row=0, column=2)
    labelLives.grid(row=0, column=3)
    canvas.grid(row=1, column=0, columnspan=4)
    status_bar.place(x=0, y=500)


load_screen()

# Переменная для режимов отладки и музыки
music_mode = BooleanVar()
music_mode.set(settings["musicswitch"])
sound_mode = BooleanVar()
sound_mode.set(settings["soundswitch"])
debug_mode = IntVar()
scale_volume_music = IntVar()
scale_volume_music.set(volumeMusic)
scale_volume_sound = IntVar()
scale_volume_sound.set(volumeMusic)

"""Окно выбора громкости Музыки"""


def set_music_volume():
    global volume_music_window
    volume_music_window = Toplevel()
    volume_music_window.title("Громкость музыки")  # Заголовок окна
    volume_music_window.configure(bg=backgroundcolor)  # Фон окна
    volume_music_window.geometry("%ix%i" % (216, 130))  # Размеры окна
    volume_music_window.resizable(0, 0)  # Запрет на изменение размеров окна
    if sysName == "Windows":
        volume_music_window.iconbitmap(image.iconPath)
    Label(volume_music_window, bg=backgroundcolor, text="Выберите подходящую громкость", font=("Arial", 10)).grid(
        row=0, column=0, columnspan=2)
    Label(volume_music_window, bg=backgroundcolor, text="Текущая громкость: %s" % volumeMusic, font=("Arial", 10)).grid(
        row=1, column=0, columnspan=2)
    Scale(volume_music_window, variable=scale_volume_music, bg=backgroundcolor, orient=HORIZONTAL, length=180,
          font=("Arial", 10)).grid(row=3, column=0, columnspan=2)
    Button(volume_music_window, text="Сохранить", bg=backgroundcolor, command=save_music_volume,
           font=("Arial", 10)).grid(row=4, column=0, pady=10)
    Button(volume_music_window, text="Отменить", bg=backgroundcolor, command=undo_music_volume,
           font=("Arial", 10)).grid(row=4, column=1, pady=10)


def save_music_volume():
    global volumeMusic
    volumeMusic = scale_volume_music.get()
    volume_music_window.destroy()


def undo_music_volume():
    volume_music_window.destroy()
    scale_volume_music.set(volumeMusic)


# Окно выбора громкости Звуков
def set_sound_volume():
    global volume_sound_window
    volume_sound_window = Toplevel()
    volume_sound_window.title("Громкость pderjd")  # Заголовок окна
    volume_sound_window.configure(bg=backgroundcolor)  # Фон окна
    volume_sound_window.geometry("%ix%i" % (216, 130))  # Размеры окна
    volume_sound_window.resizable(0, 0)  # Запрет на изменение размеров окна
    if sysName == "Windows":
        volume_sound_window.iconbitmap(image.iconPath)
    Label(volume_sound_window, bg=backgroundcolor, text="Выберите подходящую громкость", font=("Arial", 10)).grid(
        row=0, column=0, columnspan=2)
    Label(volume_sound_window, bg=backgroundcolor, text="Текущая громкость: %s" % volumeSound, font=("Arial", 10)).grid(
        row=1, column=0, columnspan=2)
    Scale(volume_sound_window, variable=scale_volume_sound, bg=backgroundcolor, orient=HORIZONTAL, length=180,
          font=("Arial", 10)).grid(
        row=3, column=0, columnspan=2)
    Button(volume_sound_window, text="Сохранить", bg=backgroundcolor, command=save_sound_volume,
           font=("Arial", 10)).grid(row=4, column=0, pady=10)
    Button(volume_sound_window, text="Отменить", bg=backgroundcolor, command=undo_sound_volume,
           font=("Arial", 10)).grid(row=4, column=1, pady=10)


def save_sound_volume():
    global volumeSound
    volumeSound = scale_volume_sound.get()
    volume_sound_window.destroy()


def undo_sound_volume():
    volume_sound_window.destroy()
    scale_volume_sound.set(volumeSound)


# Функции окон
# Открытие главного меню
def main_menu_open():  # Открытие главного меню
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
    newgameButt.place(x=182, y=280)
    continueButt.place(x=182, y=345)
    exitgameButt.place(x=182, y=410)
    if playerData.data["lastlevel"] != 1:
        continueButt.configure(state="normal")
    elif ((playerData.data["lastlevel"] == 1) & (playerData.data["islevelcyclecompleted"] is True)) | (
            playerData.data["achievements"]["end"] is False):
        continueButt.configure(state="disabled")
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
    cat_str = "%s из %s" % (objectsVariable.CatAmountReal, objectsVariable.CatAmountAll)
    if Hero.avaible:
        granny_pos = str(Hero.coords())
    else:
        granny_pos = "None"
    if alphaSavage.avaible:
        alpha_pos = str(alphaSavage.coords())
    else:
        alpha_pos = "None"
    if betaSavage.avaible:
        beta_pos = str(betaSavage.coords())
    else:
        beta_pos = "None"
    if gammaSavage.avaible:
        gamma_pos = str(gammaSavage.coords())
    else:
        gamma_pos = "None"
    if deltaSavage.avaible:
        delta_pos = str(deltaSavage.coords())
    else:
        delta_pos = "None"
    if level != 0:
        label_level_text = "Уровень: %i" % level
        labelLevel.config(text=label_level_text)
        label_cats_text = "Коты: %s" % cat_str
        labelCats.config(text=label_cats_text)
        label_score_text = "Счет: %i" % (objectsVariable.Score + objectsVariable.GlobalScore)
        labelScore.config(text=label_score_text)
        label_lives_text = "Жизни: %i" % objectsVariable.lives
        labelLives.config(text=label_lives_text)

    if debug_mode.get() == 1:
        message = "Plat:%s; Head:%s; Ladd:%s; Barr:%s; Side:%s; GraHitSav:%s; SavHitGra:%s;" % (
            plat, head, ladd, barr, wall_side, GraHitSav[0], SavHitGra)
        if level == 0:
            message = "Готов"
    elif debug_mode.get() == 2:
        message = "Vent:%s; Flow:%s; Fast:%s; Slow:%s; Grav:%s; ExitActive:%s;" % (
            vent, flow, fast, slow, grav, isExitActive)
        if level == 0:
            message = "Готов"
    elif debug_mode.get() == 3:
        message = "granny_pos:%s; alpha_pos:%s; beta_pos:%s; gamma_pos:%s; delta_pos:%s;" % (
            granny_pos, alpha_pos, beta_pos, gamma_pos, delta_pos)
        if level == 0:
            message = "Готов"
    elif debug_mode.get() == 4:
        message = "System:%s, FPS:%i; Key:%i; Cheat:%s; Music:%s; MVol:%i; Sound:%s; SVol:%i" % (
            sysName, fpsGlobal, KeySpeed, settings["cheatmode"], music_mode.get(), volumeMusic, sound_mode.get(),
            volumeSound)
        if level == 0:
            message = "Готов"
    elif level != 0:
        message = "Работаю"
    else:
        message = "Готов"
    status_bar.config(text=message)


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
    def __init__(self, spawncoords, the_canvas, the_image):
        self.image = the_image
        self.canvas = the_canvas
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
        self.isFallPlayed = False  # Проигран ли звук падения
        self.isLandPlayed = True  # Проигран ли звук приземления
        self.lastLadderSound = 0

    def coords(self):  # Массив с координатами
        return [self.x, self.y]

    def actionzone(self):  # Зона действий
        return [self.x - 25, self.x + 25, self.y - 30, self.y + 30]

    def action_queue(self):  # Сама очередь действий
        if self.action == "turn_left":  # Если нужно повернуть налево
            self.isWalkingLeft = True  # Ставим флаг, что поворачиваем (для анимации)
            if (self.x > 30) & (wall_side != "R"):  # Если не у края и не уперлись в стену
                self.canvas.move(self.id, -grannyWalkSpeed, 0)  # Двигаемся влево на значение скорости
                self.x -= grannyWalkSpeed  # Обновляем координату
        if self.action == "turn_right":  # Если нужно повернуть направо
            self.isWalkingRight = True  # Ставим флаг, что поворачиваем
            if (self.x < 610) & (wall_side != "L"):  # Если не у края и не уперлись в стену
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
            if sound_mode.get():
                mixer.Channel(4).play(mixer.Sound(random.choice(soundPaths.grannyhit)))
            self.isHitEnemy = True  # Ставим флаг, что ударяем
            savage_kill()  # Обьявляем всех Дикарей в зоне мертвыми
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

    def gravity_move(self):  # Движение под действием гравитации
        if ((self.y > 30) & (head is False)) | (gravitySpeed > 0):  # Если не бьемся головой или нормальная гравитация
            self.canvas.move(self.id, 0, gravitySpeed)
            self.y += gravitySpeed

    def ladder_sound(self, kind="up"):
        if kind == "up":
            if self.lastLadderSound == 4:
                self.lastLadderSound = 0
            mixer.Channel(4).play(mixer.Sound(soundPaths.ladder[self.lastLadderSound]))
            self.lastLadderSound += 1
        else:
            mixer.Channel(4).play(mixer.Sound(soundPaths.ladder[0]))

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
                    self.ladder_sound()
                    self.canvas.itemconfig(self.id, image=self.image["grannyClimbUp"][self.lastClimbUpImage])
                    self.lastClimbUpImage += 1
                    self.isClimbingUp = False
                    self.lastanimation = "Climbing"
                    if (ladd is False) | (plat is True):
                        self.lastanimation = "Stand"

                if self.isClimbingDown:
                    self.ladder_sound("down")
                    self.canvas.itemconfig(self.id, image=self.image["grannyClimbDown"])
                    self.isClimbingDown = False
                    self.lastanimation = "Climbing"
                    if (ladd is False) | (plat is True):
                        self.lastanimation = "Stand"

            if (plat is False) & (ladd is False):
                self.canvas.itemconfig(self.id, image=self.image["grannyFall"])
                if (self.isFallPlayed is False) & (antigrav is False):
                    mixer.Channel(4).play(mixer.Sound(soundPaths.fall))
                    self.isFallPlayed = True
                    self.isLandPlayed = False
                self.isWalkingLeft = False
                self.isWalkingRight = False
                self.lastanimation = "Stand"
            if ((plat is True) | (ladd is True)) & (self.isLandPlayed is False) & (antigrav is False):
                mixer.Channel(4).play(mixer.Sound(soundPaths.land))
                self.isLandPlayed = True
                self.isFallPlayed = False
            if antigrav is True:
                self.isFallPlayed = False
                # Обновляем таймер анимации
            self.lastanimationtime = time.time()


"""Уровни"""


# Инициальзация уровня по data.json
def level_initialization():
    playerData.data["lastlevel"] = level
    playerData.data["lastscore"] = objectsVariable.GlobalScore
    playerData.data["lastlives"] = objectsVariable.GlobalLives
    button_clear()
    clearcanvas()
    global shouldReloadButtons, limitedtime, avoidEffects, limitedFlag, Hero, Base, Exit, alphaPlatform, betaPlatform, gammaPlatform, deltaPlatform, epsilonPlatform, zetaPlatform, etaPlatform, thetaPlatform, iotaPlatform, alphaCat, betaCat, gammaCat, deltaCat, epsilonCat, zetaCat, alphaBonus, betaBonus, gammaBonus, deltaBonus, epsilonBonus, zetaBonus, alphaLadder, betaLadder, gammaLadder, deltaLadder, epsilonLadder, zetaLadder, alphaWall, betaWall, gammaWall, deltaWall, epsilonWall, zetaWall, alphaSavage, betaSavage, gammaSavage, deltaSavage, alphaFastroom, betaFastroom, alphaSlowroom, betaSlowroom, alphaGravroom, betaGravroom
    shouldReloadButtons = True
    limitedFlag = False
    avoidEffects = True
    limitedtime = 0
    canvas.create_image(320, 240, image=image.jungleBackgroung, tag="play")
    Base = PlatformBase(canvas=canvas, image=image.baseplatform)
    Exit = ExitFlower(settings['levels'][level]['exitCoords'], canvas=canvas, image=image.exitImage,
                      animationexitduration=settings["animationExitduration"])
    objectsVariable.CatAmountAll = settings['levels'][level]['CatAmountAll']
    objectsVariable.CatAmountReal = 0
    """Платформы"""
    if settings['levels'][level]['alphaPlatformFlag']:
        alphaPlatform = PlatformSimple(settings['levels'][level]['alphaPlatformCoords'], canvas=canvas,
                                       image=image.platformparts)
    else:
        alphaPlatform = Empty()
    if settings['levels'][level]['betaPlatformFlag']:
        betaPlatform = PlatformSimple(settings['levels'][level]['betaPlatformCoords'], canvas=canvas,
                                      image=image.platformparts)
    else:
        betaPlatform = Empty()
    if settings['levels'][level]['gammaPlatformFlag']:
        gammaPlatform = PlatformSimple(settings['levels'][level]['gammaPlatformCoords'], canvas=canvas,
                                       image=image.platformparts)
    else:
        gammaPlatform = Empty()
    if settings['levels'][level]['deltaPlatformFlag']:
        deltaPlatform = PlatformSimple(settings['levels'][level]['deltaPlatformCoords'], canvas=canvas,
                                       image=image.platformparts)
    else:
        deltaPlatform = Empty()
    if settings['levels'][level]['epsilonPlatformFlag']:
        epsilonPlatform = PlatformSimple(settings['levels'][level]['epsilonPlatformCoords'], canvas=canvas,
                                         image=image.platformparts)
    else:
        epsilonPlatform = Empty()
    if settings['levels'][level]['zetaPlatformFlag']:
        zetaPlatform = PlatformSimple(settings['levels'][level]['zetaPlatformCoords'], canvas=canvas,
                                      image=image.platformparts)
    else:
        zetaPlatform = Empty()
    if settings['levels'][level]['etaPlatformFlag']:
        etaPlatform = PlatformSimple(settings['levels'][level]['etaPlatformCoords'], canvas=canvas,
                                     image=image.platformparts)
    else:
        etaPlatform = Empty()
    if settings['levels'][level]['thetaPlatformFlag']:
        thetaPlatform = PlatformSimple(settings['levels'][level]['thetaPlatformCoords'], canvas=canvas,
                                       image=image.platformparts)
    else:
        thetaPlatform = Empty()
    if settings['levels'][level]['iotaPlatformFlag']:
        iotaPlatform = PlatformSimple(settings['levels'][level]['iotaPlatformCoords'], canvas=canvas,
                                      image=image.platformparts)
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

    Hero = Granny(spawncoords=settings['levels'][level]['spawnCoords'], the_canvas=canvas, the_image=image.granny)


# Обработка выбора уровня
def level_selection():
    global level
    ask = sd.askinteger(title="Выбор уровня",
                        prompt="Введите номер уровня.\nМаксимальный уровень: %i" % settings["levelamount"], minvalue=1,
                        maxvalue=settings["levelamount"])
    if type(ask) == int:
        if (level == 0) | settings["cheatmode"]:
            level = ask
            level_initialization()


# Переход на следующий уровень или конец игры
def level_adding():  # Логика переключения
    global level, shouldReloadButtons
    objectsVariable.GlobalLives = objectsVariable.lives
    objectsVariable.GlobalScore += objectsVariable.Score
    objectsVariable.Score = 0
    if level < settings["levelamount"]:  # Если уровень не последний
        if (level != 0) & sound_mode.get():
            mixer.Channel(0).play(mixer.Sound(soundPaths.exit))
        level += 1  # Добавляем уровень
        level_initialization()  # Загружаем уровень
    elif level == settings["levelamount"]:  # Если уровень последний
        endgame(win=True)  # Вывод сообшения о победе
    shouldReloadButtons = True


# Начать уровень заново
def level_restart():
    ask = mb.askyesno(title="Внимание", message="Вы действительно хотите начать уровень заново?")
    if ask:
        objectsVariable.lives = objectsVariable.GlobalLives
        objectsVariable.Score = 0
        level_initialization()


"""Доп. Функции"""


# Общая проверка по массивам
def action_check(playerzone, objectzone, index):  # Проверка выхода по массивам
    solution = False
    if (playerzone[0] + index >= objectzone[0]) & (playerzone[0] + index <= objectzone[1]):
        if (playerzone[2] >= objectzone[2]) & (playerzone[2] <= objectzone[3]):
            solution = True
        if (playerzone[3] >= objectzone[2]) & (playerzone[3] <= objectzone[3]):
            solution = True
        if (playerzone[2] <= objectzone[2]) & (playerzone[3] >= objectzone[3]):
            solution = True
    if (playerzone[1] - index >= objectzone[0]) & (playerzone[1] - index <= objectzone[1]):
        if (playerzone[2] >= objectzone[2]) & (playerzone[2] <= objectzone[3]):
            solution = True
        if (playerzone[3] >= objectzone[2]) & (playerzone[3] <= objectzone[3]):
            solution = True
        if (playerzone[2] <= objectzone[2]) & (playerzone[3] >= objectzone[3]):
            solution = True
    return solution


# Платформа
# Над платформой
def grannyoverplatform():  # Определение платформ на уровнях !!!Не забывать добавлять!!!
    globalsolution = False
    solution_alpha = False
    solution_beta = False
    solution_gamma = False
    solution_delta = False
    solution_epsilon = False
    solution_zeta = False
    solution_eta = False
    solution_theta = False
    solution_iota = False
    solution_base = ground_check(Hero, Base)
    if alphaPlatform.avaible:
        solution_alpha = ground_check(Hero, alphaPlatform)
    if betaPlatform.avaible:
        solution_beta = ground_check(Hero, betaPlatform)
    if gammaPlatform.avaible:
        solution_gamma = ground_check(Hero, gammaPlatform)
    if deltaPlatform.avaible:
        solution_delta = ground_check(Hero, deltaPlatform)
    if epsilonPlatform.avaible:
        solution_epsilon = ground_check(Hero, epsilonPlatform)
    if zetaPlatform.avaible:
        solution_zeta = ground_check(Hero, zetaPlatform)
    if etaPlatform.avaible:
        solution_eta = ground_check(Hero, etaPlatform)
    if thetaPlatform.avaible:
        solution_theta = ground_check(Hero, thetaPlatform)
    if iotaPlatform.avaible:
        solution_iota = ground_check(Hero, iotaPlatform)

    if (solution_base is True) | (solution_alpha is True) | (solution_beta is True) | (solution_gamma is True) | (
            solution_delta is True) | (solution_epsilon is True) | (solution_zeta is True) | (solution_eta is True) | (
            solution_theta is True) | (solution_iota is True):
        globalsolution = True
    return globalsolution


def ground_check(player, theplatform):  # Проверка земли под ногами по массивам
    solution = False
    platformtouch = theplatform.touch_place()
    playertouch = player.touch_place()
    if platformtouch[0] == playertouch[0]:
        if (playertouch[1] >= platformtouch[1]) & (playertouch[1] <= platformtouch[2]):
            solution = True
        if (playertouch[2] >= platformtouch[1]) & (playertouch[2] <= platformtouch[2]):
            solution = True
    return solution


# Под платформой
def grannyunderplatform():  # Определение платформ на уровнях !!!Не забывать добавлять!!!
    globalsolution = True
    solution_alpha = False
    solution_beta = False
    solution_gamma = False
    solution_delta = False
    solution_epsilon = False
    solution_zeta = False
    solution_eta = False
    solution_theta = False
    solution_iota = False
    if alphaPlatform.avaible:
        solution_alpha = head_check(Hero, alphaPlatform)
    if betaPlatform.avaible:
        solution_beta = head_check(Hero, betaPlatform)
    if gammaPlatform.avaible:
        solution_gamma = head_check(Hero, gammaPlatform)
    if deltaPlatform.avaible:
        solution_delta = head_check(Hero, deltaPlatform)
    if epsilonPlatform.avaible:
        solution_epsilon = head_check(Hero, epsilonPlatform)
    if zetaPlatform.avaible:
        solution_zeta = head_check(Hero, zetaPlatform)
    if etaPlatform.avaible:
        solution_eta = head_check(Hero, etaPlatform)
    if thetaPlatform.avaible:
        solution_theta = head_check(Hero, thetaPlatform)
    if iotaPlatform.avaible:
        solution_iota = head_check(Hero, iotaPlatform)

    if (solution_alpha is False) & (solution_beta is False) & (solution_gamma is False) & (solution_delta is False) & (
            solution_epsilon is False) & (solution_zeta is False) & (solution_eta is False) & (
            solution_theta is False) & (solution_iota is False):
        globalsolution = False
    return globalsolution


def head_check(player, theplatform):  # Проверка земли над головой по массивам
    solution = False
    platformtouch = theplatform.touch_head()
    playertouch = player.touch_head()
    if platformtouch[0] == playertouch[0]:
        if (playertouch[1] >= platformtouch[1]) & (playertouch[1] <= platformtouch[2]):
            solution = True
        if (playertouch[2] >= platformtouch[1]) & (playertouch[2] <= platformtouch[2]):
            solution = True
    return solution


# Туземец и персонаж
def savagehitgranny():
    globalsolution = False
    solution_alpha = False
    solution_beta = False
    solution_gamma = False
    solution_delta = False
    if alphaSavage.avaible:
        solution_alpha = action_check(Hero.actionzone(), alphaSavage.actionzone(), 24)
    if betaSavage.avaible:
        solution_beta = action_check(Hero.actionzone(), betaSavage.actionzone(), 24)
    if gammaSavage.avaible:
        solution_gamma = action_check(Hero.actionzone(), gammaSavage.actionzone(), 24)
    if deltaSavage.avaible:
        solution_delta = action_check(Hero.actionzone(), deltaSavage.actionzone(), 24)

    if (solution_alpha is True) | (solution_beta is True) | (solution_gamma is True) | (solution_delta is True):
        globalsolution = True

    return globalsolution


def grannyhitsavage():
    globalsolution = False
    solution_alpha = False
    solution_beta = False
    solution_gamma = False
    solution_delta = False
    if alphaSavage.avaible:
        solution_alpha = action_check(Hero.hit_area(), alphaSavage.actionzone(), 24)
    if betaSavage.avaible:
        solution_beta = action_check(Hero.hit_area(), betaSavage.actionzone(), 24)
    if gammaSavage.avaible:
        solution_gamma = action_check(Hero.hit_area(), gammaSavage.actionzone(), 24)
    if deltaSavage.avaible:
        solution_delta = action_check(Hero.hit_area(), deltaSavage.actionzone(), 24)

    if (solution_alpha is True) | (solution_beta is True) | (solution_gamma is True) | (solution_delta is True):
        globalsolution = True

    return [globalsolution, solution_alpha, solution_beta, solution_gamma, solution_delta]


# Лестница и персонаж
def topladder(theladder, theplayer):
    ladderaction = theladder.actionzone()
    playeraction = theplayer.actionzone()
    if ladderaction[2] == playeraction[3]:
        theladder.isLadderTop = True
    else:
        theladder.isLadderTop = False


def checkladder(theladder):
    topladder(theladder, Hero)
    return action_check(Hero.actionzone(), theladder.actionzone(), 15)


def grannyonladder():
    global ladd
    solution = False
    solution_alpha = False
    solution_beta = False
    solution_gamma = False
    solution_delta = False
    solution_epsilon = False
    solution_zeta = False
    if alphaLadder.avaible:
        solution_alpha = checkladder(alphaLadder)
    if betaLadder.avaible:
        solution_beta = checkladder(betaLadder)
    if gammaLadder.avaible:
        solution_gamma = checkladder(gammaLadder)
    if deltaLadder.avaible:
        solution_delta = checkladder(deltaLadder)
    if epsilonLadder.avaible:
        solution_epsilon = checkladder(epsilonLadder)
    if zetaLadder.avaible:
        solution_zeta = checkladder(zetaLadder)

    if (solution_alpha is True) | (solution_beta is True) | (solution_gamma is True) | (solution_delta is True) | (
            solution_epsilon is True) | (solution_zeta is True):
        solution = True

    if ((alphaLadder.isLadderTop is True) | (betaLadder.isLadderTop is True) | (gammaLadder.isLadderTop is True) | (
            deltaLadder.isLadderTop is True) | (epsilonLadder.isLadderTop is True) | (
                zetaLadder.isLadderTop is True)) & (
            Hero.lastanimation == "Climbing"):
        objectsVariable.isLadderTop = True
    else:
        objectsVariable.isLadderTop = False

    if ladd is False:
        objectsVariable.isLadderTop = False

    return solution


# Кот и персоныж
def checkcat(thecat):
    solution = action_check(Hero.actionzone(), thecat.actionzone(), 10)
    if solution is True:
        thecat.collect()
        mixer.Channel(3).play(mixer.Sound(random.choice(soundPaths.cat)))
        objectsVariable.Score += settings["ScoreAddCat"]  # Зачисляем очки
        objectsVariable.CatAmountReal += 1


def grannycarrycat():
    if alphaCat.avaible:
        checkcat(alphaCat)
    if betaCat.avaible:
        checkcat(betaCat)
    if gammaCat.avaible:
        checkcat(gammaCat)
    if deltaCat.avaible:
        checkcat(deltaCat)
    if epsilonCat.avaible:
        checkcat(epsilonCat)
    if zetaCat.avaible:
        checkcat(zetaCat)


# Цветочек и персонаж
def check_bonus(the_bonus, the_player):
    solution = action_check(the_player.actionzone(), the_bonus.actionzone(), 16)
    if solution is True:
        objectsVariable.Score += settings["ScoreAddBonus"]
        the_bonus.rise()
        flower_water_add_score()
    return solution


def granny_get_bonus():  # Определение цветочков на уровне !!!Не забывать добавлять!!!
    solution = False
    solution_alpha = False
    solution_beta = False
    solution_gamma = False
    solution_delta = False
    solution_epsilon = False
    solution_zeta = False
    if alphaBonus.avaible:
        solution_alpha = check_bonus(alphaBonus, Hero)
    if betaBonus.avaible:
        solution_beta = check_bonus(betaBonus, Hero)
    if gammaBonus.avaible:
        solution_gamma = check_bonus(gammaBonus, Hero)
    if deltaBonus.avaible:
        solution_delta = check_bonus(deltaBonus, Hero)
    if epsilonBonus.avaible:
        solution_epsilon = check_bonus(epsilonBonus, Hero)
    if zetaBonus.avaible:
        solution_zeta = check_bonus(zetaBonus, Hero)
    if (solution_alpha is True) | (solution_beta is True) | (solution_gamma is True) | (solution_delta is True) | (
            solution_epsilon is True) | (solution_zeta is True):
        solution = True
        if sound_mode.get():
            mixer.Channel(1).play(mixer.Sound(soundPaths.bonus))
    return solution


# Грибочки и персонаж
def check_mushroom(mushroom, kind):
    solution = action_check(Hero.actionzone(), mushroom.actionzone(), 15)
    if solution is True:
        if kind == "fast":
            objectsVariable.isFastEffect = True
        if kind == "slow":
            objectsVariable.isSlowEffect = True
        if kind == "grav":
            objectsVariable.isGravEffect = True
    return solution


def granny_and_fast():
    solution = False
    solution_alpha = False
    solution_beta = False
    if alphaFastroom.avaible:
        solution_alpha = check_mushroom(alphaFastroom, kind="fast")
    if betaFastroom.avaible:
        solution_beta = check_mushroom(betaFastroom, kind="fast")
    if (solution_alpha is True) | (solution_beta is True):
        solution = True
        if objectsVariable.isFastroomSoundPlayed is False:
            if sound_mode.get():
                mixer.Channel(2).play(mixer.Sound(soundPaths.mushroom))
            objectsVariable.isFastroomSoundPlayed = True
    else:
        objectsVariable.isFastroomSoundPlayed = False

    return solution


def granny_and_slow():
    solution = False
    solution_alpha = False
    solution_beta = False
    if alphaSlowroom.avaible:
        solution_alpha = check_mushroom(alphaSlowroom, kind="slow")
    if betaSlowroom.avaible:
        solution_beta = check_mushroom(betaSlowroom, kind="slow")
    if (solution_alpha is True) | (solution_beta is True):
        solution = True
        if objectsVariable.isSlowroomSoundPlayed is False:
            if sound_mode.get():
                mixer.Channel(2).play(mixer.Sound(soundPaths.mushroom))
            objectsVariable.isSlowroomSoundPlayed = True
    else:
        objectsVariable.isSlowroomSoundPlayed = False

    return solution


def granny_and_grav():
    solution = False
    solution_alpha = False
    solution_beta = False
    if alphaGravroom.avaible:
        solution_alpha = check_mushroom(alphaGravroom, kind="grav")
    if betaGravroom.avaible:
        solution_beta = check_mushroom(betaGravroom, kind="grav")
    if (solution_alpha is True) | (solution_beta is True):
        solution = True
        if objectsVariable.isGravroomSoundPlayed is False:
            if sound_mode.get():
                mixer.Channel(2).play(mixer.Sound(soundPaths.mushroom))
            objectsVariable.isGravroomSoundPlayed = True
    else:
        objectsVariable.isGravroomSoundPlayed = False

    return solution


# Выход с уровня
def granny_in_exit():
    return action_check(Hero.actionzone(), Exit.actionzone(), 30)


# Стены для персонажа и дикаря
def granny_and_wall():
    global wall_side
    solution = False
    solution_alpha = False
    solution_beta = False
    solution_gamma = False
    solution_delta = False
    solution_epsilon = False
    solution_zeta = False
    if alphaWall.avaible:
        solution_alpha = wall_check(Hero.actionzone(), alphaWall.actionzone(), None)
    if betaWall.avaible:
        solution_beta = wall_check(Hero.actionzone(), betaWall.actionzone(), None)
    if gammaWall.avaible:
        solution_gamma = wall_check(Hero.actionzone(), gammaWall.actionzone(), None)
    if deltaWall.avaible:
        solution_delta = wall_check(Hero.actionzone(), deltaWall.actionzone(), None)
    if epsilonWall.avaible:
        solution_epsilon = wall_check(Hero.actionzone(), epsilonWall.actionzone(), None)
    if zetaWall.avaible:
        solution_zeta = wall_check(Hero.actionzone(), zetaWall.actionzone(), None)
    if (solution_alpha is True) | (solution_beta is True) | (solution_gamma is True) | (solution_delta is True) | (
            solution_epsilon is True) | (solution_zeta is True):
        solution = True

    if solution is False:
        wall_side = "0"

    return solution


def wall_check(player_zone, wall_zone, the_savage):  # Проверка стен по массивам
    global wall_side
    solution = False
    if (player_zone[0] + 16 >= wall_zone[0]) & (player_zone[0] + 16 <= wall_zone[1]):
        if (player_zone[2] >= wall_zone[2]) & (player_zone[2] <= wall_zone[3]):
            solution = True
        if (player_zone[3] >= wall_zone[2]) & (player_zone[3] <= wall_zone[3]):
            if the_savage is None:
                wall_side = "R"
            else:
                the_savage.wall_side = "R"
            solution = True
    if (player_zone[1] - 16 >= wall_zone[0]) & (player_zone[1] - 16 <= wall_zone[1]):
        if (player_zone[2] >= wall_zone[2]) & (player_zone[2] <= wall_zone[3]):
            solution = True
        if (player_zone[3] >= wall_zone[2]) & (player_zone[3] <= wall_zone[3]):
            if the_savage is None:
                wall_side = "L"
            else:
                the_savage.wall_side = "L"
            solution = True
    return solution


def any_savage_and_wall(the_object):  # Проверяет столкновение для одного любого Дикаря
    solution = False
    solution_alpha = False
    solution_beta = False
    solution_gamma = False
    solution_delta = False
    solution_epsilon = False
    solution_zeta = False
    if alphaWall.avaible:
        solution_alpha = wall_check(the_object.actionzone(), alphaWall.actionzone(), the_object)
    if betaWall.avaible:
        solution_beta = wall_check(the_object.actionzone(), betaWall.actionzone(), the_object)
    if gammaWall.avaible:
        solution_gamma = wall_check(the_object.actionzone(), gammaWall.actionzone(), the_object)
    if deltaWall.avaible:
        solution_delta = wall_check(the_object.actionzone(), deltaWall.actionzone(), the_object)
    if epsilonWall.avaible:
        solution_epsilon = wall_check(the_object.actionzone(), epsilonWall.actionzone(), the_object)
    if zetaWall.avaible:
        solution_zeta = wall_check(the_object.actionzone(), zetaWall.actionzone(), the_object)
    if (solution_alpha is True) | (solution_beta is True) | (solution_gamma is True) | (solution_delta is True) | (
            solution_epsilon is True) | (solution_zeta is True):
        solution = True

    if solution is False:
        the_object.wall_side = "0"

    return solution


# Гравитация
def gravity():  # Если персонаж не на платформн и не на лестнице, на нее действует гравитация
    global simpgrav
    if ((plat is False) | (antigrav is True)) & (ladd is False):
        simpgrav = True
        Hero.gravity_move()
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
            objectsVariable.isGravEffect is False) & (
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
def savage_death(the_savage):
    canvas.delete(the_savage.id)
    savage_kill_add_score()


def savage_kill():
    global alphaSavage, betaSavage, gammaSavage, deltaSavage
    if GraHitSav[0]:
        if alphaSavage.avaible & GraHitSav[1]:
            savage_death(alphaSavage)
            alphaSavage = Empty()
        if betaSavage.avaible & GraHitSav[2]:
            savage_death(betaSavage)
            betaSavage = Empty()
        if gammaSavage.avaible & GraHitSav[3]:
            savage_death(gammaSavage)
            gammaSavage = Empty()
        if deltaSavage.avaible & GraHitSav[4]:
            savage_death(deltaSavage)
            deltaSavage = Empty()


def granny_kill():
    global Hero, avoidEffects
    if SavHitGra:
        if sound_mode.get():
            mixer.Channel(1).play(mixer.Sound(random.choice(soundPaths.savagehit)))
        canvas.delete(Hero.id)
        objectsVariable.lives -= 1
        if objectsVariable.lives < 0:
            endgame(win=False)
        else:
            avoidEffects = True
            Hero = Granny(spawncoords=settings['levels'][level]['spawnCoords'], the_canvas=canvas,
                          the_image=image.granny)


# Функции Дикаря
# Платформа по которой он ходит
def select_way_plate(the_savage, the_platform):
    if the_platform.avaible:
        the_savage.way = the_platform.border()
    else:
        the_savage.way = Base.border()


def savage_plates(the_savage, home_platform):
    if home_platform == "base":
        the_savage.way = Base.border()
    if home_platform == "alpha":
        select_way_plate(the_savage, alphaPlatform)
    if home_platform == "beta":
        select_way_plate(the_savage, betaPlatform)
    if home_platform == "gamma":
        select_way_plate(the_savage, gammaPlatform)
    if home_platform == "delta":
        select_way_plate(the_savage, deltaPlatform)
    if home_platform == "epsilon":
        select_way_plate(the_savage, epsilonPlatform)
    if home_platform == "zeta":
        select_way_plate(the_savage, zetaPlatform)
    if home_platform == "eta":
        select_way_plate(the_savage, etaPlatform)
    if home_platform == "theta":
        select_way_plate(the_savage, thetaPlatform)
    if home_platform == "iota":
        select_way_plate(the_savage, iotaPlatform)


# Изменение направления при встрече с концом платформы
def savage_direction(the_savage):
    coords = the_savage.coords()
    way = the_savage.way
    if coords[0] <= way[0]:
        the_savage.changedirection()
    elif coords[0] >= way[1]:
        the_savage.changedirection()


# Установка платформ и направлений
def savage_walking():
    if alphaSavage.avaible:
        savage_plates(alphaSavage, settings["levels"][level]["alphaSavagePlatform"])
        if any_savage_and_wall(alphaSavage):
            alphaSavage.changedirection()
        else:
            savage_direction(alphaSavage)
    if betaSavage.avaible:
        savage_plates(betaSavage, settings["levels"][level]["betaSavagePlatform"])
        if any_savage_and_wall(betaSavage):
            betaSavage.changedirection()
        else:
            savage_direction(betaSavage)
    if gammaSavage.avaible:
        savage_plates(gammaSavage, settings["levels"][level]["gammaSavagePlatform"])
        if any_savage_and_wall(gammaSavage):
            gammaSavage.changedirection()
        else:
            savage_direction(gammaSavage)
    if deltaSavage.avaible:
        savage_plates(deltaSavage, settings["levels"][level]["deltaSavagePlatform"])
        if any_savage_and_wall(deltaSavage):
            deltaSavage.changedirection()
        else:
            savage_direction(deltaSavage)


# Организация движений
def savage_moving(the_savage):
    if the_savage.direction == "right":
        the_savage.turn_right()
    else:
        the_savage.turn_left()


# Вызов очереди действий существующих дикарей
def savage_actions():
    if alphaSavage.avaible:
        savage_moving(alphaSavage)
        alphaSavage.action_queue()
        alphaSavage.animate()
    if betaSavage.avaible:
        savage_moving(betaSavage)
        betaSavage.action_queue()
        betaSavage.animate()
    if gammaSavage.avaible:
        savage_moving(gammaSavage)
        gammaSavage.action_queue()
        gammaSavage.animate()
    if deltaSavage.avaible:
        savage_moving(deltaSavage)
        deltaSavage.action_queue()
        deltaSavage.animate()


# Проверка на сбор котиков. Открытие цветка и выход с уровня
def cat_counter_for_exit():
    global isExitActive
    if objectsVariable.CatAmountReal >= objectsVariable.CatAmountAll:
        isExitActive = True
        Exit.opening()
        if granny_in_exit() is True:
            level_adding()
    else:
        isExitActive = False


# Организация временных ограничений уровней
def level_limits():
    global limitedFlag, limitedtime
    if settings["levels"][level]["limited"]:
        if limitedFlag is False:
            limitedFlag = True
            limitedtime = time.time()
            labelTime.place(x=50, y=475)
            labelTimer.place(x=90, y=475)
        elif limitedFlag is True:
            if time.time() - limitedtime < settings["levels"][level]["time"]:
                time_str = "%.2f с" % (settings["levels"][level]["time"] - (time.time() - limitedtime))
                labelTimer.config(text=time_str)
            if (time.time() - limitedtime) > settings["levels"][level]["time"]:
                limitedFlag = False
                if settings["levels"][level]["limittype"] == "NEXT":
                    level_adding()
                elif settings["levels"][level]["limittype"] == "LOSE":
                    endgame(win=False)
    else:
        limitedFlag = False
        labelTime.place_forget()
        labelTimer.place_forget()


# Организация конца игры, вывод сообщений о выйгрыше/проигрыше
def endgame(win):
    if win:
        mixer.Channel(0).play(mixer.Sound(soundPaths.win))
        objectsVariable.GlobalScore += objectsVariable.Score
        message = "Поздравляем с победой! \nВы набрали %i из %i очков" % (
            objectsVariable.GlobalScore, settings["ScoreMax"])
        achievements_give()
        if objectsVariable.GlobalScore > playerData.data["recordscore"]:
            playerData.data["recordscore"] = objectsVariable.GlobalScore
        playerData.data["achievements"]["end"] = True
        playerData.data["islevelcyclecompleted"] = True
        mb.showinfo(title="Победа", message=message)
        main_menu_open()
    else:
        mixer.Channel(0).play(mixer.Sound(soundPaths.lose))
        objectsVariable.GlobalScore += objectsVariable.Score
        message = "К сожалению, Вы проиграли. \nВы набрали %i из %i очков" % (
            objectsVariable.GlobalScore, settings["ScoreMax"])
        playerData.data["lastlevel"] = emptydata["lastlevel"]
        playerData.data["lastscore"] = emptydata["lastscore"]
        playerData.data["lastlives"] = settings["livesnormal"]
        mb.showinfo(title="Проигрыш", message=message)
        main_menu_open()


# Подсчет кликов и кадров
def timer():
    global keytime, KeySpeed, fps, fpsGlobal
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
    reload_screen()


# Получение достижений
def achievements_give():
    if playerData.data["killedsavages"] == 0:
        playerData.data["achievements"]["pacifist"] = True
    if objectsVariable.lives == settings["livesnormal"]:
        playerData.data["achievements"]["nonbeliever"] = True
    if playerData.data["wateredflowers"] == settings["flowersamount"]:
        playerData.data["achievements"]["florist"] = True
    if playerData.data["killedsavages"] == settings["savagesamount"]:
        playerData.data["achievements"]["bloodmary"] = True
    if objectsVariable.GlobalScore == settings["ScoreMax"]:
        playerData.data["achievements"]["maximalist"] = True


# Окно достижений
def achievements_window():
    global achWindow, pacifistFrame
    achWindow = Toplevel(root)
    achWindow.title("Достижения")  # Заголовок окна
    achWindow.configure(bg=backgroundcolor)  # Фон окна
    achWindow.resizable(0, 0)  # Запрет на изменение размеров окна
    if sysName == "Windows":
        achWindow.iconbitmap(image.iconPath)
    create_achievement_card(frame=achWindow, images=image.ach_pacifist, achname="pacifist",
                            state=playerData.data["achievements"]["pacifist"], row=0, column=0)
    create_achievement_card(frame=achWindow, images=image.ach_bloodmary, achname="bloodmary",
                            state=playerData.data["achievements"]["bloodmary"], row=2, column=0)
    create_achievement_card(frame=achWindow, images=image.ach_florist, achname="florist",
                            state=playerData.data["achievements"]["florist"], row=0, column=2)
    create_achievement_card(frame=achWindow, images=image.ach_nonbeliever, achname="nonbeliever",
                            state=playerData.data["achievements"]["nonbeliever"], row=2, column=2)
    create_achievement_card(frame=achWindow, images=image.ach_maximalist, achname="maximalist",
                            state=playerData.data["achievements"]["maximalist"], row=4, column=0)
    create_achievement_card(frame=achWindow, images=image.ach_end, achname="end",
                            state=playerData.data["achievements"]["end"], row=4, column=2)


def create_achievement_card(frame, images, achname, state, row, column):
    Label(frame, image=images[int(state)], bg=backgroundcolor).grid(row=row, column=column, rowspan=2, padx=5, pady=5)
    Label(frame, font=("Arial", 14), text=achievementsNames[achname]["name"], anchor=W,
          bg=backgroundcolor).grid(row=row, column=column + 1, sticky=W)
    Label(frame, font=("Arial", 12), text=achievementsNames[achname]["description"], anchor=W,
          bg=backgroundcolor).grid(row=row + 1, column=column + 1, sticky=NW)


# Включение и отключение кнопок меню сверху
def buttonstate():
    global shouldReloadButtons
    if shouldReloadButtons:
        if level == 0:
            game_menu.entryconfig("Выход в меню", state="disabled")
            game_menu.entryconfig("Начать уровень заново", state="disabled")
            game_menu.entryconfig("Выбор уровня", state="normal")
        else:
            game_menu.entryconfig("Выход в меню", state="normal")
            game_menu.entryconfig("Начать уровень заново", state="normal")
            if not settings["cheatmode"]:
                game_menu.entryconfig("Выбор уровня", state="disabled")

    shouldReloadButtons = False


# Опрос выхода в главное меню
def exit_in_main_menu():
    ask = mb.askyesno(title="Выход в меню", message="Вы действительно хотите выйти в меню?")
    if ask:
        main_menu_open()


# Составление меню
def menu():  # Описание меню(сверху полоска)
    global game_menu
    main_menu = Menu(root)
    game_menu = Menu(main_menu, tearoff=0, bg=backgroundcolor)
    game_menu.add_command(label="Новая игра", command=new_game)
    game_menu.add_command(label="Начать уровень заново", command=level_restart)
    game_menu.add_command(label="Выбор уровня", command=level_selection)
    game_menu.add_separator()
    game_menu.add_command(label="Выход в меню", command=exit_in_main_menu)
    game_menu.add_command(label="Выход", command=on_closing)
    option_menu = Menu(main_menu, tearoff=1, bg=backgroundcolor)
    music_menu = Menu(option_menu, tearoff=1, bg=backgroundcolor)
    music_menu.add_command(label="Громкость", command=set_music_volume)
    music_menu.add_radiobutton(label="Включена", value=True, variable=music_mode)
    music_menu.add_radiobutton(label="Отключена", value=False, variable=music_mode)
    sound_menu = Menu(option_menu, tearoff=1, bg=backgroundcolor)
    sound_menu.add_command(label="Громкость", command=set_sound_volume)
    sound_menu.add_radiobutton(label="Включена", value=True, variable=sound_mode)
    sound_menu.add_radiobutton(label="Отключена", value=False, variable=sound_mode)
    debug_menu = Menu(option_menu, tearoff=1, bg=backgroundcolor)
    debug_menu.add_radiobutton(label="Отключена", value=0, variable=debug_mode)
    debug_menu.add_radiobutton(label="Флаги персонажа", value=1, variable=debug_mode)
    debug_menu.add_radiobutton(label="Флаги обьектов", value=2, variable=debug_mode)
    debug_menu.add_radiobutton(label="Положение", value=3, variable=debug_mode)
    debug_menu.add_radiobutton(label="Системное", value=4, variable=debug_mode)
    option_menu.add_cascade(label="Музыка", menu=music_menu)
    option_menu.add_cascade(label="Звуки", menu=sound_menu)
    option_menu.add_command(label="Выбрать цвет фона", command=color)
    option_menu.add_cascade(label="Отладка", menu=debug_menu)
    about_menu = Menu(main_menu, tearoff=0, bg=backgroundcolor)
    about_menu.add_command(label="Авторы", command=lambda: mb.showinfo(title="Авторы", message=authorsmessage))
    about_menu.add_command(label="Об игре", command=lambda: mb.showinfo(title="Об игре", message=aboutmessage))
    progress_menu = Menu(main_menu, tearoff=0, bg=backgroundcolor)
    progress_menu.add_command(label="Достижения", command=achievements_window)
    progress_menu.add_command(label="Сбростить прогресс", command=clear_progress)
    main_menu.add_cascade(label="Игра", menu=game_menu)
    main_menu.add_cascade(label="Достижения", menu=progress_menu)
    main_menu.add_cascade(label="Опции", menu=option_menu)
    main_menu.add_cascade(label="Справка", menu=about_menu)
    root.config(menu=main_menu)


# Перезагрузка экрана
def reload_screen():
    labelLevel.grid_forget()
    labelScore.grid_forget()
    labelCats.grid_forget()
    labelLives.grid_forget()
    status_bar.place_forget()
    labelLevel.config(bg=backgroundcolor)
    labelScore.config(bg=backgroundcolor)
    labelCats.config(bg=backgroundcolor)
    labelLives.config(bg=backgroundcolor)
    status_bar.config(bg=backgroundcolor)
    root.configure(bg=backgroundcolor)
    root.geometry("%ix%i" % (windowSize[0], windowSize[1]))
    load_screen()
    menu()


# Добавляем +1 к убитым Дикарям
def savage_kill_add_score():
    playerData.data["killedsavages"] += 1


# Добавляем +1 к политым цветам
def flower_water_add_score():
    playerData.data["wateredflowers"] += 1


def clear_progress():
    if mb.askyesno(title="Сброс", message="Вы уверены, что хотите сбросить прогресс?"):
        playerData.erase_data()
        main_menu_open()


Hero = Empty()
Exit = Empty()
menu()  # Создаем меню
main_menu_open()  # Запускаем заглавный экран
root.protocol("WM_DELETE_WINDOW", on_closing)  # Обработка выхода при нажатии на крестик
# Главный цикл
while run:
    if (time.time() - last_frame_time) >= settings["frametime"]:
        fps += 1
        music()
        if level != 0:  # Если игра идет
            plat = grannyoverplatform()  # Стоит ли персонаж на платформе
            grannycarrycat()  # Подбирает ли персонаж котенка
            vent = granny_in_exit()  # Стоит ли персонаж у выходв
            barr = granny_and_wall()  # Стоит ли персонаж у стены
            flow = granny_get_bonus()  # Стоит ли персонаж у цветочка
            fast = granny_and_fast()  # Стоит ли персонаж у Быстромора
            grav = granny_and_grav()  # Стоит ли персонаж у Вверхшенки
            slow = granny_and_slow()  # Стоит ли персонаж у Медлянки
            head = grannyunderplatform()  # Стоит ли персонаж под платформой
            SavHitGra = savagehitgranny()  # Может ли Дикарь убить персонажа
            GraHitSav = grannyhitsavage()  # Может ли персонаж убить Дикаря
            granny_kill()  # Проверка смерти персонажа
            effects()  # Применение эффектов от грибов
            level_limits()  # Применение временных ограничений
            cat_counter_for_exit()  # Делаем проверку готовность выйти с уровня
            status()  # Обновляем статусбар и данные для пользователя
            savage_walking()  # Дикарь
            savage_actions()
            if Hero.avaible:  # Если герой есть, применяем к нему
                ladd = grannyonladder()  # Стоит ли персонаж на лестнице
                Hero.action_queue()  # Выполнение очереди действий
                gravity()  # Применяем к персонажу фактор графитации
                Hero.animate()  # Анимируем персонажа
            if Exit.avaible:  # Если герой есть, применяем к нему
                Exit.animate()  # Анимируем персонажа
            playerData.write_data()
        buttonstate()
        timer()
        root.update_idletasks()  # Обновляем объекты окна
        root.update()
        last_frame_time = time.time()
