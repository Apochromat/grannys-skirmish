import os
from PIL import Image, ImageTk

"""Изображения"""


# Функция загрузки изображений
def imgload(path):  # Функция загрузки изображений
    img = Image.open(path)
    output = ImageTk.PhotoImage(img)
    return output


# Загрузка изображений
class ImageHeap:
    def __init__(self):
        self.mainmenuBackgroung = imgload(os.path.join('assets', 'graphics', 'background', 'menu_background.jpg'))
        self.jungleBackgroung = imgload(os.path.join('assets', 'graphics', 'background', 'jungle_background.jpg'))
        self.baseplatform = imgload(os.path.join('assets', 'graphics', 'platformbase.png'))
        self.ladder = imgload(os.path.join('assets', 'graphics', 'ladder.png'))
        self.wallImage = imgload(os.path.join('assets', 'graphics', 'wall.png'))

        self.cats = [imgload(os.path.join('assets', 'graphics', 'cat', 'cat1.png')),
                     imgload(os.path.join('assets', 'graphics', 'cat', 'cat2.png')),
                     imgload(os.path.join('assets', 'graphics', 'cat', 'cat3.png'))]

        self.mushroom = [imgload(os.path.join('assets', 'graphics', 'mushroom', 'fastroom.png')),
                         imgload(os.path.join('assets', 'graphics', 'mushroom', 'slowroom.png')),
                         imgload(os.path.join('assets', 'graphics', 'mushroom', 'gravroom.png'))]

        self.bonusSeed = imgload(os.path.join('assets', 'graphics', 'bonus', 'bonusSeed.png'))
        self.bonus = [imgload(os.path.join('assets', 'graphics', 'bonus', 'bonus0.png')),
                      imgload(os.path.join('assets', 'graphics', 'bonus', 'bonus1.png')),
                      imgload(os.path.join('assets', 'graphics', 'bonus', 'bonus2.png'))]

        self.exitImage = [imgload(os.path.join('assets', 'graphics', 'exitflower_inactive.png')),
                          imgload(os.path.join('assets', 'graphics', 'exitflower_active.png'))]

        self.savage = {
            "image": imgload(os.path.join('assets', 'graphics', 'savage', 'savage_stand.png')),
            "savageWalkLeft": [imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_left_1.png')),
                               imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_left_2.png')),
                               imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_left_3.png')),
                               imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_left_4.png')),
                               imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_left_5.png')),
                               imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_left_6.png')),
                               imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_left_7.png'))],
            "savageWalkRight": [imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_right_1.png')),
                                imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_right_2.png')),
                                imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_right_3.png')),
                                imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_right_4.png')),
                                imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_right_5.png')),
                                imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_right_6.png')),
                                imgload(os.path.join('assets', 'graphics', 'savage', 'savage_walk_right_7.png'))]
        }

        self.granny = {"image": imgload(os.path.join('assets', 'graphics', 'granny', 'granny_stand_forward.png')),
                       "grannyFall": imgload(os.path.join('assets', 'graphics', 'granny', 'granny_fall.png')),
                       "grannyStandRight": imgload(
                           os.path.join('assets', 'graphics', 'granny', 'granny_stand_right.png')),
                       "grannyStandLeft": imgload(
                           os.path.join('assets', 'graphics', 'granny', 'granny_stand_left.png')),
                       "grannyWalkLeft": [
                           imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_left_1.png')),
                           imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_left_2.png')),
                           imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_left_3.png'))],
                       "grannyWalkRight": [
                           imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_right_1.png')),
                           imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_right_2.png')),
                           imgload(os.path.join('assets', 'graphics', 'granny', 'granny_walk_right_3.png'))],
                       "grannyClimbUp": [
                           imgload(os.path.join('assets', 'graphics', 'granny', 'granny_climb_up_1.png')),
                           imgload(os.path.join('assets', 'graphics', 'granny', 'granny_climb_up_2.png')),
                           imgload(os.path.join('assets', 'graphics', 'granny', 'granny_climb_up_3.png'))],
                       "grannyClimbDown": imgload(
                           os.path.join('assets', 'graphics', 'granny', 'granny_climb_down.png')),
                       "grannyHit": [imgload(os.path.join('assets', 'graphics', 'granny', 'granny_hit_1.png')),
                                     imgload(os.path.join('assets', 'graphics', 'granny', 'granny_hit_2.png'))]
                       }
