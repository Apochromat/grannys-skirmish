import time
import random

class VariableHeap:
    def __init__(self):
        self.isFastEffect = False  # Устанавливается ли эффект быстроты
        self.isSlowEffect = False  # Устанавливается ли эффект медленности
        self.isGravEffect = False  # Устанавливается ли эффект антигравитации

        self.lives = 0
        self.GlobalLives = 0

        self.CatAmountReal = 0
        self.CatAmountAll = 0

        self.GlobalScore = 0  # Счет
        self.Score = 0  # Счет уровня

        self.isLadderTop = False

        self.keyCounter = 0

# Базовая платформа
class PlatformBase:  # Класс базовой платформы, которая присутствует на всех уровнях
    def __init__(self, canvas, image):
        self.canvas = canvas
        self.avaible = True
        self.id = self.canvas.create_image(320, 465, image=image, tag="platform")
        self.bord = [30, 610]
        self.touch = [450, 0, 640]

    def border(self):
        return self.bord

    def touch_place(self):  # Массив точек касания верхней линии
        return self.touch

# Платформа
class PlatformSimple:  # Класс обычной платформы, масштабируется и изменяется для каждого уровня
    def __init__(self, coordsarray, canvas):
        self.canvas = canvas
        self.coords = coordsarray
        self.avaible = True
        self.id = self.canvas.create_rectangle(self.coords[1], self.coords[0], self.coords[2], self.coords[0] + 30,
                                               fill="#a2653e", tag="platform")

    def border(self):
        bord = [self.coords[1] + 15, self.coords[2] - 15]
        return bord

    def touch_place(self):  # Массив точек касания верхней линии
        touch = [self.coords[0], self.coords[1], self.coords[2]]
        return touch

    def touch_head(self):  # Массив точек касания нижней линии
        head = [self.coords[0] + 30, self.coords[1], self.coords[2]]
        return head

# Стена
class Wall:
    # Ширина 32, Высота 64
    def __init__(self, coordsarray, canvas, image):
        self.canvas = canvas
        self.coords = coordsarray
        self.avaible = True
        self.centre = [self.coords[0] + 16, self.coords[1] + 32]
        self.id = canvas.create_image(self.centre[0], self.centre[1], image=image, tag="wall")

    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 30, self.centre[0] + 30, self.centre[1] - 32, self.centre[1] + 32]
        return actionArray

# Лестница
class Ladder:  # Класс лестницы, позволяет забираться на верх
    # Ширина 50, Высота 120
    def __init__(self, coordsarray, canvas, image):  # ax by (Верхний левый угол)
        self.canvas = canvas
        self.coords = coordsarray
        self.avaible = True
        self.centre = [self.coords[0] + 25, self.coords[1] + 60]
        self.id = self.canvas.create_image(self.centre[0], self.centre[1], image=image, tag="ladder")
        self.isLadderTop = False

    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 10, self.centre[0] + 10, self.centre[1] - 60, self.centre[1] + 60]
        return actionArray

# Бонусный цветок
class BonusFlower:
    # Ширина 32, Высота 36
    def __init__(self, coordsarray, canvas, imageseed, imagerise):  # ax by (Верхний левый угол)
        self.imagerise = imagerise
        self.canvas = canvas
        self.coords = coordsarray
        self.centre = [self.coords[0] + 16, self.coords[1] + 18]
        self.id = self.canvas.create_image(self.centre[0], self.centre[1], image=imageseed, tag="bonus")
        self.avaible = True

    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 16, self.centre[0] + 16, self.centre[1] - 18, self.centre[1] + 18]
        return actionArray

    def rise(self):
        self.avaible = False
        self.canvas.itemconfig(self.id, image=self.imagerise)

# Быстромор
class Fastroom:
    # Ширина 24, Высота 24
    def __init__(self, coordsarray, canvas, image):  # ax by (Верхний левый угол)
        self.canvas = canvas
        self.coords = coordsarray
        self.centre = [self.coords[0] + 12, self.coords[1] + 12]
        self.id = self.canvas.create_image(self.centre[0], self.centre[1], image=image[0], tag="mushroom")
        self.avaible = True

    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 12, self.centre[0] + 12, self.centre[1] - 12, self.centre[1] + 12]
        return actionArray

# Медлянка
class Slowroom:
    # Ширина 24, Высота 24
    def __init__(self, coordsarray, canvas, image):  # ax by (Верхний левый угол)
        self.canvas = canvas
        self.coords = coordsarray
        self.centre = [self.coords[0] + 12, self.coords[1] + 12]
        self.id = self.canvas.create_image(self.centre[0], self.centre[1], image=image[1], tag="mushroom")
        self.avaible = True

    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 12, self.centre[0] + 12, self.centre[1] - 12, self.centre[1] + 12]
        return actionArray

# Вверхшенка
class Gravroom:
    # Ширина 24, Высота 24
    def __init__(self, coordsarray, canvas, image):  # ax by (Верхний левый угол)
        self.canvas = canvas
        self.coords = coordsarray
        self.centre = [self.coords[0] + 12, self.coords[1] + 12]
        self.id = self.canvas.create_image(self.centre[0], self.centre[1], image=image[2], tag="mushroom")
        self.avaible = True

    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 12, self.centre[0] + 12, self.centre[1] - 12, self.centre[1] + 12]
        return actionArray

# Кот
class Cat:  # Класс котика, которых мы спасаем
    # Ширина 24, Высота 32
    def __init__(self, coordsarray, canvas, image):  # ax by (Верхний левый угол)
        self.canvas = canvas
        self.coords = coordsarray
        self.centre = [self.coords[0] + 12, self.coords[1] + 16]
        self.id = self.canvas.create_image(self.centre[0], self.centre[1], image=random.choice(image), tag="cat")
        self.avaible = True

    def actionzone(self):  # Зона активности (совершения действий)
        return [self.centre[0] - 12, self.centre[0] + 12, self.centre[1] - 16, self.centre[1] + 16]

    def collect(self):  # Собрать котика
        self.avaible = False
        self.canvas.delete(self.id)

# Дикарь
class Savage:
    # Ширина 48 Высота 64
    def __init__(self, spawncoords, canvas, image, animationsavageduration, savagespeed):
        self.animationSavageduration = animationsavageduration
        self.savageSpeed = savagespeed
        self.canvas = canvas
        self.image = image
        self.id = self.canvas.create_image(spawncoords[0], spawncoords[1], image=self.image["image"], tag="savage")
        self.x = spawncoords[0]
        self.y = spawncoords[1]
        self.avaible = True
        self.action = ""
        self.way = [0, 640]
        self.wallside = 0
        self.direction = random.choice(["left", "right"])
        self.lastWalkRightImage = 0
        self.lastWalkLeftImage = 0
        self.isWalkingLeft = False
        self.isWalkingRight = False
        self.lastSavageanimationtime = time.time()

    def coords(self):  # Массив с координатами
        return [self.x, self.y]

    def actionzone(self):  # Зона действий
        return [self.x - 30, self.x + 30, self.y - 32, self.y + 32]

    def changedirection(self):
        if self.direction == "right":
            self.direction = "left"
        else:
            self.direction = "right"

    def action_queue(self):
        if self.action == "turn_left":
            self.isWalkingLeft = True
            self.animate()
            if self.x > 30:
                self.canvas.move(self.id, -self.savageSpeed, 0)
                self.x -= self.savageSpeed
        if self.action == "turn_right":
            self.isWalkingRight = True
            self.animate()
            if self.x < 610:
                self.canvas.move(self.id, self.savageSpeed, 0)
                self.x += self.savageSpeed
        self.action = ""

    def turn_left(self):  # Движение влево
        self.action = "turn_left"

    def turn_right(self):  # Движение вправо
        self.action = "turn_right"

    def animate(self):  # Анимирование
        if (time.time() - self.lastSavageanimationtime) > self.animationSavageduration:  # Если прошла задержка
            # Анимации во время движений
            if self.isWalkingRight | (self.direction == "right"):
                if self.lastWalkRightImage == 7:
                    self.lastWalkRightImage = 0
                self.canvas.itemconfig(self.id, image=self.image["savageWalkRight"][self.lastWalkRightImage])
                self.lastWalkRightImage += 1
                self.isWalkingRight = False
            if self.isWalkingLeft | (self.direction == "left"):
                if self.lastWalkLeftImage == 7:
                    self.lastWalkLeftImage = 0
                self.canvas.itemconfig(self.id, image=self.image["savageWalkLeft"][self.lastWalkLeftImage])
                self.lastWalkLeftImage += 1
                self.isWalkingLeft = False
            # Обновляем таймер кадра
            self.lastSavageanimationtime = time.time()


# Выход
class ExitFlower:  # Класс цветка-выхода
    # Ширина 60, Высота 60
    def __init__(self, coordsarray, canvas, image):  # ax by (Верхний левый угол)
        self.image = image
        self.canvas = canvas
        self.coords = coordsarray
        self.avaible = True
        self.centre = [self.coords[0] + 30, self.coords[1] + 30]
        self.id = self.canvas.create_image(self.centre[0], self.centre[1], image=self.image[0], tag="exit")

    def actionzone(self):  # Зона активности (совершения действий)
        actionArray = [self.centre[0] - 30, self.centre[0] + 30, self.centre[1] - 30, self.centre[1] + 30]
        return actionArray

    def opening(self):  # Открытие цветка
        self.canvas.itemconfig(self.id, image=self.image[1])

# Пустой объект
class Empty:
    def __init__(self):
        self.avaible = False
        self.id = None
        self.isLadderTop = False

    def coords(self):
        pass

    def actionzone(self):
        pass

    def action_queue(self):
        pass

    def touch_place(self):
        pass

    def touch_head(self):
        pass

    def hit_area(self):
        pass

    def gravitymove(self):
        pass

    def animate(self):
        pass
