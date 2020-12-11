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
        self.iconPath = os.path.join('assets', 'graphics', 'ui', 'icon.ico')
        self.quit = imgload(os.path.join('assets', 'graphics', 'ui', 'quit.png'))
        self.newgame = imgload(os.path.join('assets', 'graphics', 'ui', 'newgame.png'))
        self.continuegame = imgload(os.path.join('assets', 'graphics', 'ui', 'continue.png'))
        self.mainmenuBackgroung = imgload(os.path.join('assets', 'graphics', 'background', 'menu_background.png'))
        self.jungleBackgroung = imgload(os.path.join('assets', 'graphics', 'background', 'jungle_background.jpg'))
        self.baseplatform = imgload(os.path.join('assets', 'graphics', 'platform', 'platformbase.png'))
        self.ladder = imgload(os.path.join('assets', 'graphics', 'ladder.png'))
        self.wallImage = imgload(os.path.join('assets', 'graphics', 'wall.png'))

        self.cats = [imgload(os.path.join('assets', 'graphics', 'cat', 'cat_1.png')),
                     imgload(os.path.join('assets', 'graphics', 'cat', 'cat_2.png')),
                     imgload(os.path.join('assets', 'graphics', 'cat', 'cat_3.png'))]

        self.mushroom = [imgload(os.path.join('assets', 'graphics', 'mushroom', 'fastroom.png')),
                         imgload(os.path.join('assets', 'graphics', 'mushroom', 'slowroom.png')),
                         imgload(os.path.join('assets', 'graphics', 'mushroom', 'gravroom.png'))]

        self.bonusSeed = imgload(os.path.join('assets', 'graphics', 'bonus', 'bonusSeed.png'))
        self.bonus = [imgload(os.path.join('assets', 'graphics', 'bonus', 'bonus_1.png')),
                      imgload(os.path.join('assets', 'graphics', 'bonus', 'bonus_2.png')),
                      imgload(os.path.join('assets', 'graphics', 'bonus', 'bonus_3.png'))]

        self.exitImage = [imgload(os.path.join('assets', 'graphics', 'exit', 'exitflower_inactive.png')),
                          imgload(os.path.join('assets', 'graphics', 'exit', 'exitflower_active_1.png')),
                          imgload(os.path.join('assets', 'graphics', 'exit', 'exitflower_active_2.png')),
                          imgload(os.path.join('assets', 'graphics', 'exit', 'exitflower_active_3.png')),
                          imgload(os.path.join('assets', 'graphics', 'exit', 'exitflower_active_4.png'))]

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

        self.platformparts = [imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_1.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_2.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_3.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_4.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_5.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_6.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_7.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_8.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_9.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_10.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_11.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_12.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_13.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_14.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_15.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_16.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_17.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_18.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_19.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_20.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_21.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_22.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_23.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_24.png')),
                              imgload(os.path.join('assets', 'graphics', 'platform', 'parts', 'part_25.png'))]

        self.ach_pacifist = [imgload(os.path.join('assets', 'graphics', 'achievements', 'pacifist_inactive.png')),
                             imgload(os.path.join('assets', 'graphics', 'achievements', 'pacifist_active.png'))]

        self.ach_bloodmary = [imgload(os.path.join('assets', 'graphics', 'achievements', 'bloodmary_inactive.png')),
                              imgload(os.path.join('assets', 'graphics', 'achievements', 'bloodmary_active.png'))]

        self.ach_florist = [imgload(os.path.join('assets', 'graphics', 'achievements', 'florist_inactive.png')),
                            imgload(os.path.join('assets', 'graphics', 'achievements', 'florist_active.png'))]

        self.ach_nonbeliever = [imgload(os.path.join('assets', 'graphics', 'achievements', 'nonbeliever_inactive.png')),
                                imgload(os.path.join('assets', 'graphics', 'achievements', 'nonbeliever_active.png'))]

        self.ach_maximalist = [imgload(os.path.join('assets', 'graphics', 'achievements', 'maximalist_inactive.png')),
                               imgload(os.path.join('assets', 'graphics', 'achievements', 'maximalist_active.png'))]

        self.ach_end = [imgload(os.path.join('assets', 'graphics', 'achievements', 'end_inactive.png')),
                        imgload(os.path.join('assets', 'graphics', 'achievements', 'end_active.png'))]