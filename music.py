import os

# Загрузка Музыки
class MusicPathHeap:
    def __init__(self):
        self.mainmenuWin = os.path.join('assets', 'music', 'mainmenu.mid')
        self.mainmenuLin = os.path.join('assets', 'music', 'mainmenu.mp3')
        self.levelWin = os.path.join('assets', 'music', 'level.mid')
        self.levelLin = os.path.join('assets', 'music', 'level.mp3')

# Загрузка Звуков
class SoundPathHeap:
    def __init__(self):
        self.exit = os.path.join('assets', 'sound', 'exit.ogg')
        self.bonus = os.path.join('assets', 'sound', 'bonus.ogg')
        self.mushroom = os.path.join('assets', 'sound', 'mushroom.ogg')
        self.win = os.path.join('assets', 'sound', 'win.ogg')
        self.cat = [os.path.join('assets', 'sound', 'cat1.ogg'),
                    os.path.join('assets', 'sound', 'cat2.ogg')]
        self.savagehit = [os.path.join('assets', 'sound', 'savagehit1.ogg'),
                          os.path.join('assets', 'sound', 'savagehit2.ogg')]
        self.grannyhit = [os.path.join('assets', 'sound', 'grannyhit1.ogg'),
                          os.path.join('assets', 'sound', 'grannyhit2.ogg')]
