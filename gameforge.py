""" Gameforge 1.3"""

import json
import sys
import webbrowser
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb

# Пустота
class Empty():
    def __init__(self):
        self.i = 0
    def protocol(self, u, i):
        pass

# Переменные
colors = ["wheat1", "aquamarine", "palegreen1", "plum1", "grey80", "lightblue"]
lev_colors = ["wheat1", "plum1", "lightblue", "pink2", "palegreen1", "lemonchiffon", "grey80", "mediumpurple1",
              "orchid2", "khaki1","paleturquoise2", "burlywood1"]
background_color = "lavender"
is_level_editing = False
Level = Empty()
levelinforge = 0
hint = "Персонаж/Выход: X [30; 610], Y [30; 430]\n" \
       "Остальное: X [0; 610], Y [0; 430]\n" \
       "X1 должен быть меньше X2\n"\
       "Дикарь (Платформа) значения:\n base, alpha, beta, gamma, delta,\n epsilon, zeta, eta, theta, iota\n"\
       "Тип маски: bless, joy, luck, rage"

# Функции
def openfile():
    global settings, filepath
    filepath = fd.askopenfilename()
    with open(filepath, 'r', encoding="utf-8") as file:
        try:
            settings = json.load(file)
            load_vars()
            master.common_information_show()
        except json.decoder.JSONDecodeError:
            mb.showinfo(title="Ошибка открытия", message="Файл должен иметь структуру JSON")

def load_vars():
    try:
        versionVar.set(settings["version"])
        livesVar.set(settings["livesnormal"])
        catscoreVar.set(settings["ScoreAddCat"])
        bonusscoreVar.set(settings["ScoreAddBonus"])
        maxscoreVar.set(settings["ScoreMax"])
        effectdurationVar.set(settings["effectduration"])
        levelsVar.set(settings["levelamount"])
        savagesVar.set(settings["savagesamount"])
        flowersVar.set(settings["flowersamount"])
        cheatVar.set(settings["cheatmode"])
        musicVar.set(settings["musicswitch"])
        soundVar.set(settings["soundswitch"])
    except KeyError:
        warning("Это не файл 'Granny`s Skirmish'")
        openfile()
        
def load_level_vars(level):
    # Переменные Уровня"""
    # Основное"""
    level_editVar.set(settings["levels"][level]["level"])
    limit_editVar.set(settings["levels"][level]["limited"])
    if settings["levels"][level]["limittype"] == "NEXT":
        limit_type_editVar.set(0)
    else:
        limit_type_editVar.set(1)
    limit_time_editVar.set(settings["levels"][level]["time"])
    player_x_editVar.set(settings["levels"][level]["spawnCoords"][0])
    player_y_editVar.set(settings["levels"][level]["spawnCoords"][1])
    exit_x_editVar.set(settings["levels"][level]["exitCoords"][0])
    exit_y_editVar.set(settings["levels"][level]["exitCoords"][1])
    cats_editVar.set(settings["levels"][level]["CatAmountAll"])

    # Маски
    mask_state_editVar.set(settings["levels"][level]["maskFlag"])
    mask_kind_editVar.set(settings["levels"][level]["maskKind"])
    mask_chance_editVar.set(settings["levels"][level]["maskChance"]*100)
    mask_x_editVar.set(settings["levels"][level]["maskCoords"][0])
    mask_y_editVar.set(settings["levels"][level]["maskCoords"][1])

    # Платформы
    alpha_platform_state_editVar.set(settings["levels"][level]["alphaPlatformFlag"])
    alpha_platform_y_editVar.set(settings["levels"][level]["alphaPlatformCoords"][0])
    alpha_platform_x1_editVar.set(settings["levels"][level]["alphaPlatformCoords"][1])
    alpha_platform_x2_editVar.set(settings["levels"][level]["alphaPlatformCoords"][2])
    beta_platform_state_editVar.set(settings["levels"][level]["betaPlatformFlag"])
    beta_platform_y_editVar.set(settings["levels"][level]["betaPlatformCoords"][0])
    beta_platform_x1_editVar.set(settings["levels"][level]["betaPlatformCoords"][1])
    beta_platform_x2_editVar.set(settings["levels"][level]["betaPlatformCoords"][2])
    gamma_platform_state_editVar.set(settings["levels"][level]["gammaPlatformFlag"])
    gamma_platform_y_editVar.set(settings["levels"][level]["gammaPlatformCoords"][0])
    gamma_platform_x1_editVar.set(settings["levels"][level]["gammaPlatformCoords"][1])
    gamma_platform_x2_editVar.set(settings["levels"][level]["gammaPlatformCoords"][2])
    delta_platform_state_editVar.set(settings["levels"][level]["deltaPlatformFlag"])
    delta_platform_y_editVar.set(settings["levels"][level]["deltaPlatformCoords"][0])
    delta_platform_x1_editVar.set(settings["levels"][level]["deltaPlatformCoords"][1])
    delta_platform_x2_editVar.set(settings["levels"][level]["deltaPlatformCoords"][2])
    epsilon_platform_state_editVar.set(settings["levels"][level]["epsilonPlatformFlag"])
    epsilon_platform_y_editVar.set(settings["levels"][level]["epsilonPlatformCoords"][0])
    epsilon_platform_x1_editVar.set(settings["levels"][level]["epsilonPlatformCoords"][1])
    epsilon_platform_x2_editVar.set(settings["levels"][level]["epsilonPlatformCoords"][2])
    zeta_platform_state_editVar.set(settings["levels"][level]["zetaPlatformFlag"])
    zeta_platform_y_editVar.set(settings["levels"][level]["zetaPlatformCoords"][0])
    zeta_platform_x1_editVar.set(settings["levels"][level]["zetaPlatformCoords"][1])
    zeta_platform_x2_editVar.set(settings["levels"][level]["zetaPlatformCoords"][2])
    eta_platform_state_editVar.set(settings["levels"][level]["etaPlatformFlag"])
    eta_platform_y_editVar.set(settings["levels"][level]["etaPlatformCoords"][0])
    eta_platform_x1_editVar.set(settings["levels"][level]["etaPlatformCoords"][1])
    eta_platform_x2_editVar.set(settings["levels"][level]["etaPlatformCoords"][2])
    theta_platform_state_editVar.set(settings["levels"][level]["thetaPlatformFlag"])
    theta_platform_y_editVar.set(settings["levels"][level]["thetaPlatformCoords"][0])
    theta_platform_x1_editVar.set(settings["levels"][level]["thetaPlatformCoords"][1])
    theta_platform_x2_editVar.set(settings["levels"][level]["thetaPlatformCoords"][2])
    iota_platform_state_editVar.set(settings["levels"][level]["iotaPlatformFlag"])
    iota_platform_y_editVar.set(settings["levels"][level]["iotaPlatformCoords"][0])
    iota_platform_x1_editVar.set(settings["levels"][level]["iotaPlatformCoords"][1])
    iota_platform_x2_editVar.set(settings["levels"][level]["iotaPlatformCoords"][2])

    # Коты
    alpha_cat_state_editVar.set(settings["levels"][level]["alphaCatFlag"])
    alpha_cat_x_editVar.set(settings["levels"][level]["alphaCatCoords"][0])
    alpha_cat_y_editVar.set(settings["levels"][level]["alphaCatCoords"][1])
    beta_cat_state_editVar.set(settings["levels"][level]["betaCatFlag"])
    beta_cat_x_editVar.set(settings["levels"][level]["betaCatCoords"][0])
    beta_cat_y_editVar.set(settings["levels"][level]["betaCatCoords"][1])
    gamma_cat_state_editVar.set(settings["levels"][level]["gammaCatFlag"])
    gamma_cat_x_editVar.set(settings["levels"][level]["gammaCatCoords"][0])
    gamma_cat_y_editVar.set(settings["levels"][level]["gammaCatCoords"][1])
    delta_cat_state_editVar.set(settings["levels"][level]["deltaCatFlag"])
    delta_cat_x_editVar.set(settings["levels"][level]["deltaCatCoords"][0])
    delta_cat_y_editVar.set(settings["levels"][level]["deltaCatCoords"][1])
    epsilon_cat_state_editVar.set(settings["levels"][level]["epsilonCatFlag"])
    epsilon_cat_x_editVar.set(settings["levels"][level]["epsilonCatCoords"][0])
    epsilon_cat_y_editVar.set(settings["levels"][level]["epsilonCatCoords"][1])
    zeta_cat_state_editVar.set(settings["levels"][level]["zetaCatFlag"])
    zeta_cat_x_editVar.set(settings["levels"][level]["zetaCatCoords"][0])
    zeta_cat_y_editVar.set(settings["levels"][level]["zetaCatCoords"][1])

    # Бонусы
    alpha_bonus_state_editVar.set(settings["levels"][level]["alphaBonusFlag"])
    alpha_bonus_x_editVar.set(settings["levels"][level]["alphaBonusCoords"][0])
    alpha_bonus_y_editVar.set(settings["levels"][level]["alphaBonusCoords"][1])
    beta_bonus_state_editVar.set(settings["levels"][level]["betaBonusFlag"])
    beta_bonus_x_editVar.set(settings["levels"][level]["betaBonusCoords"][0])
    beta_bonus_y_editVar.set(settings["levels"][level]["betaBonusCoords"][1])
    gamma_bonus_state_editVar.set(settings["levels"][level]["gammaBonusFlag"])
    gamma_bonus_x_editVar.set(settings["levels"][level]["gammaBonusCoords"][0])
    gamma_bonus_y_editVar.set(settings["levels"][level]["gammaBonusCoords"][1])
    delta_bonus_state_editVar.set(settings["levels"][level]["deltaBonusFlag"])
    delta_bonus_x_editVar.set(settings["levels"][level]["deltaBonusCoords"][0])
    delta_bonus_y_editVar.set(settings["levels"][level]["deltaBonusCoords"][1])
    epsilon_bonus_state_editVar.set(settings["levels"][level]["epsilonBonusFlag"])
    epsilon_bonus_x_editVar.set(settings["levels"][level]["epsilonBonusCoords"][0])
    epsilon_bonus_y_editVar.set(settings["levels"][level]["epsilonBonusCoords"][1])
    zeta_bonus_state_editVar.set(settings["levels"][level]["zetaBonusFlag"])
    zeta_bonus_x_editVar.set(settings["levels"][level]["zetaBonusCoords"][0])
    zeta_bonus_y_editVar.set(settings["levels"][level]["zetaBonusCoords"][1])

    # Лестницы
    alpha_ladder_state_editVar.set(settings["levels"][level]["alphaLadderFlag"])
    alpha_ladder_x_editVar.set(settings["levels"][level]["alphaLadderCoords"][0])
    alpha_ladder_y_editVar.set(settings["levels"][level]["alphaLadderCoords"][1])
    beta_ladder_state_editVar.set(settings["levels"][level]["betaLadderFlag"])
    beta_ladder_x_editVar.set(settings["levels"][level]["betaLadderCoords"][0])
    beta_ladder_y_editVar.set(settings["levels"][level]["betaLadderCoords"][1])
    gamma_ladder_state_editVar.set(settings["levels"][level]["gammaLadderFlag"])
    gamma_ladder_x_editVar.set(settings["levels"][level]["gammaLadderCoords"][0])
    gamma_ladder_y_editVar.set(settings["levels"][level]["gammaLadderCoords"][1])
    delta_ladder_state_editVar.set(settings["levels"][level]["deltaLadderFlag"])
    delta_ladder_x_editVar.set(settings["levels"][level]["deltaLadderCoords"][0])
    delta_ladder_y_editVar.set(settings["levels"][level]["deltaLadderCoords"][1])
    epsilon_ladder_state_editVar.set(settings["levels"][level]["epsilonLadderFlag"])
    epsilon_ladder_x_editVar.set(settings["levels"][level]["epsilonLadderCoords"][0])
    epsilon_ladder_y_editVar.set(settings["levels"][level]["epsilonLadderCoords"][1])
    zeta_ladder_state_editVar.set(settings["levels"][level]["zetaLadderFlag"])
    zeta_ladder_x_editVar.set(settings["levels"][level]["zetaLadderCoords"][0])
    zeta_ladder_y_editVar.set(settings["levels"][level]["zetaLadderCoords"][1])

    # Стены
    alpha_wall_state_editVar.set(settings["levels"][level]["alphaWallFlag"])
    alpha_wall_x_editVar.set(settings["levels"][level]["alphaWallCoords"][0])
    alpha_wall_y_editVar.set(settings["levels"][level]["alphaWallCoords"][1])
    beta_wall_state_editVar.set(settings["levels"][level]["betaWallFlag"])
    beta_wall_x_editVar.set(settings["levels"][level]["betaWallCoords"][0])
    beta_wall_y_editVar.set(settings["levels"][level]["betaWallCoords"][1])
    gamma_wall_state_editVar.set(settings["levels"][level]["gammaWallFlag"])
    gamma_wall_x_editVar.set(settings["levels"][level]["gammaWallCoords"][0])
    gamma_wall_y_editVar.set(settings["levels"][level]["gammaWallCoords"][1])
    delta_wall_state_editVar.set(settings["levels"][level]["deltaWallFlag"])
    delta_wall_x_editVar.set(settings["levels"][level]["deltaWallCoords"][0])
    delta_wall_y_editVar.set(settings["levels"][level]["deltaWallCoords"][1])
    epsilon_wall_state_editVar.set(settings["levels"][level]["epsilonWallFlag"])
    epsilon_wall_x_editVar.set(settings["levels"][level]["epsilonWallCoords"][0])
    epsilon_wall_y_editVar.set(settings["levels"][level]["epsilonWallCoords"][1])
    zeta_wall_state_editVar.set(settings["levels"][level]["zetaWallFlag"])
    zeta_wall_x_editVar.set(settings["levels"][level]["zetaWallCoords"][0])
    zeta_wall_y_editVar.set(settings["levels"][level]["zetaWallCoords"][1])

    # Дикари
    alpha_savage_state_editVar.set(settings["levels"][level]["alphaSavageFlag"])
    alpha_savage_x_editVar.set(settings["levels"][level]["alphaSavageCoords"][0])
    alpha_savage_y_editVar.set(settings["levels"][level]["alphaSavageCoords"][1])
    alpha_savage_home_editVar.set(settings["levels"][level]["alphaSavagePlatform"])
    beta_savage_state_editVar.set(settings["levels"][level]["betaSavageFlag"])
    beta_savage_x_editVar.set(settings["levels"][level]["betaSavageCoords"][0])
    beta_savage_y_editVar.set(settings["levels"][level]["betaSavageCoords"][1])
    beta_savage_home_editVar.set(settings["levels"][level]["betaSavagePlatform"])
    gamma_savage_state_editVar.set(settings["levels"][level]["gammaSavageFlag"])
    gamma_savage_x_editVar.set(settings["levels"][level]["gammaSavageCoords"][0])
    gamma_savage_y_editVar.set(settings["levels"][level]["gammaSavageCoords"][1])
    gamma_savage_home_editVar.set(settings["levels"][level]["gammaSavagePlatform"])
    delta_savage_state_editVar.set(settings["levels"][level]["deltaSavageFlag"])
    delta_savage_x_editVar.set(settings["levels"][level]["deltaSavageCoords"][0])
    delta_savage_y_editVar.set(settings["levels"][level]["deltaSavageCoords"][1])
    delta_savage_home_editVar.set(settings["levels"][level]["deltaSavagePlatform"])

    # Грибы
    alpha_fastroom_state_editVar.set(settings["levels"][level]["alphaFastroomFlag"])
    alpha_fastroom_x_editVar.set(settings["levels"][level]["alphaFastroomCoords"][0])
    alpha_fastroom_y_editVar.set(settings["levels"][level]["alphaFastroomCoords"][1])
    beta_fastroom_state_editVar.set(settings["levels"][level]["betaFastroomFlag"])
    beta_fastroom_x_editVar.set(settings["levels"][level]["betaFastroomCoords"][0])
    beta_fastroom_y_editVar.set(settings["levels"][level]["betaFastroomCoords"][1])
    alpha_slowroom_state_editVar.set(settings["levels"][level]["alphaSlowroomFlag"])
    alpha_slowroom_x_editVar.set(settings["levels"][level]["alphaSlowroomCoords"][0])
    alpha_slowroom_y_editVar.set(settings["levels"][level]["alphaSlowroomCoords"][1])
    beta_slowroom_state_editVar.set(settings["levels"][level]["betaSlowroomFlag"])
    beta_slowroom_x_editVar.set(settings["levels"][level]["betaSlowroomCoords"][0])
    beta_slowroom_y_editVar.set(settings["levels"][level]["betaSlowroomCoords"][1])
    alpha_gravroom_state_editVar.set(settings["levels"][level]["alphaGravroomFlag"])
    alpha_gravroom_x_editVar.set(settings["levels"][level]["alphaGravroomCoords"][0])
    alpha_gravroom_y_editVar.set(settings["levels"][level]["alphaGravroomCoords"][1])
    beta_gravroom_state_editVar.set(settings["levels"][level]["betaGravroomFlag"])
    beta_gravroom_x_editVar.set(settings["levels"][level]["betaGravroomCoords"][0])
    beta_gravroom_y_editVar.set(settings["levels"][level]["betaGravroomCoords"][1])

def warning(message):
    mb.showwarning(title="Ошибка", message=message)

def write_vars():
    with open(filepath, 'w', encoding="utf-8") as file:
        file.write(json.dumps(settings, indent=4, ensure_ascii=False))
    load_vars()
    mb.showinfo(title="Запись", message="Значения успешно записаны в файл.")
    master.common_information_show()

def send_vars():
    if is_level_editing is False:
        settings["version"] = versionVar.get()
        if type(livesVar.get()) == int:
            if livesVar.get() > 1:
                settings["livesnormal"] = livesVar.get()
            else:
                warning("Число жизней должно быть больше 1")
        else:
            warning("Жизни должны быть целым положительным числом")

        if type(catscoreVar.get()) == int:
            if catscoreVar.get() > 1:
                settings["ScoreAddCat"] = catscoreVar.get()
            else:
                warning("Число очков должно быть больше 1")
        else:
            warning("Очки должны быть целым положительным числом")

        if type(bonusscoreVar.get()) == int:
            if bonusscoreVar.get() > 1:
                settings["ScoreAddBonus"] = bonusscoreVar.get()
            else:
                warning("Число очков должно быть больше 1")
        else:
            warning("Очки должны быть целым положительным числом")

        if type(maxscoreVar.get()) == int:
            if maxscoreVar.get() > 1:
                settings["ScoreMax"] = maxscoreVar.get()
            else:
                warning("Число очков должно быть больше 1")
        else:
            warning("Очки должны быть целым положительным числом")

        if type(effectdurationVar.get()) == int:
            if effectdurationVar.get() > 1:
                settings["effectduration"] = effectdurationVar.get()
            else:
                warning("Длительность эффекта должна быть больше 1")
        else:
            warning("Длительность должна быть целым положительным числом")

        if type(levelsVar.get()) == int:
            if levelsVar.get() >= 1:
                settings["levelamount"] = levelsVar.get()
            else:
                warning("Уровней должно быть не меньше 1")
        else:
            warning("Уровни должны быть целым положительным числом")

        if type(savagesVar.get()) == int:
            settings["savagesamount"] = savagesVar.get()
        else:
            warning("Количество должно быть целым положительным числом")

        if type(flowersVar.get()) == int:
            settings["flowersamount"] = flowersVar.get()
        else:
            warning("Количество должно быть целым положительным числом")

        try:
            settings["cheatmode"]=cheatVar.get()
        except ValueError:
            warning("Значение переменной 'Читы' только 1 или 0")

        try:
            settings["musicswitch"]=musicVar.get()
        except ValueError:
            warning("Значение переменной 'Музыка' только 1 или 0")

        try:
            settings["soundswitch"]=soundVar.get()
        except ValueError:
            warning("Значение переменной 'Звук' только 1 или 0")

        while settings["levelamount"] > (len(settings["levels"])-1):
            settings["levels"].append(emptylevel)

        for i in range(1, (settings["levelamount"]+1)):
            settings["levels"][i]["level"]=i

        write_vars()
    else:
        warning("Завершите редактирование уровня")

def level_edit():
    global is_level_editing, Level, levelinforge
    if is_level_editing is False:
        is_level_editing = True
        levelinforge = editlevelVar.get()
        load_level_vars(levelinforge)
        Level = LevelEdit(mainwindow=master)
        Level.window.protocol("WM_DELETE_WINDOW", level_edit_close)
    else:
        warning("Завершите редактирование уровня")

def level_edit_close():
    global is_level_editing, Level, levelinforge
    if mb.askyesno(title="Выход", message="Вы хотите завешить редактирование?\nНесохрененные данные будут утеряны"):
        is_level_editing = False
        levelinforge = 0
        Level.window.destroy()
        Level = Empty()

def level_edit_save():
    # Основное
    settings["levels"][levelinforge]["level"] = level_editVar.get()
    settings["levels"][levelinforge]["limited"] = limit_editVar.get()
    if limit_type_editVar.get() == 0:
        settings["levels"][levelinforge]["limittype"] = "NEXT"
    else:
        settings["levels"][levelinforge]["limittype"] = "LOSE"
    settings["levels"][levelinforge]["time"] = limit_time_editVar.get()
    settings["levels"][levelinforge]["spawnCoords"] = [player_x_editVar.get(), player_y_editVar.get()]
    settings["levels"][levelinforge]["exitCoords"] = [exit_x_editVar.get(), exit_y_editVar.get()]
    settings["levels"][levelinforge]["CatAmountAll"] = cats_editVar.get()

    # Маски
    settings["levels"][levelinforge]["maskFlag"] = mask_state_editVar.get()
    settings["levels"][levelinforge]["maskCoords"] = [mask_x_editVar.get(),
                                                          mask_y_editVar.get()]
    settings["levels"][levelinforge]["maskKind"] = mask_kind_editVar.get()
    settings["levels"][levelinforge]["maskChance"] = mask_chance_editVar.get()/100

    # Платформы
    settings["levels"][levelinforge]["alphaPlatformFlag"] = alpha_platform_state_editVar.get()
    settings["levels"][levelinforge]["alphaPlatformCoords"] = [alpha_platform_y_editVar.get(),
                                                               alpha_platform_x1_editVar.get(),
                                                               alpha_platform_x2_editVar.get()]
    settings["levels"][levelinforge]["betaPlatformFlag"] = beta_platform_state_editVar.get()
    settings["levels"][levelinforge]["betaPlatformCoords"] = [beta_platform_y_editVar.get(),
                                                              beta_platform_x1_editVar.get(),
                                                              beta_platform_x2_editVar.get()]
    settings["levels"][levelinforge]["gammaPlatformFlag"] = gamma_platform_state_editVar.get()
    settings["levels"][levelinforge]["gammaPlatformCoords"] = [gamma_platform_y_editVar.get(),
                                                               gamma_platform_x1_editVar.get(),
                                                               gamma_platform_x2_editVar.get()]
    settings["levels"][levelinforge]["deltaPlatformFlag"] = delta_platform_state_editVar.get()
    settings["levels"][levelinforge]["deltaPlatformCoords"] = [delta_platform_y_editVar.get(),
                                                               delta_platform_x1_editVar.get(),
                                                               delta_platform_x2_editVar.get()]
    settings["levels"][levelinforge]["epsilonPlatformFlag"] = epsilon_platform_state_editVar.get()
    settings["levels"][levelinforge]["epsilonPlatformCoords"] = [epsilon_platform_y_editVar.get(),
                                                                epsilon_platform_x1_editVar.get(),
                                                                epsilon_platform_x2_editVar.get()]
    settings["levels"][levelinforge]["zetaPlatformFlag"]= zeta_platform_state_editVar.get()
    settings["levels"][levelinforge]["zetaPlatformCoords"] = [zeta_platform_y_editVar.get(),
                                                              zeta_platform_x1_editVar.get(),
                                                              zeta_platform_x2_editVar.get()]
    settings["levels"][levelinforge]["etaPlatformFlag"]  = eta_platform_state_editVar.get()
    settings["levels"][levelinforge]["etaPlatformCoords"] = [eta_platform_y_editVar.get(),
                                                             eta_platform_x1_editVar.get(),
                                                             eta_platform_x2_editVar.get()]
    settings["levels"][levelinforge]["thetaPlatformFlag"] = theta_platform_state_editVar.get()
    settings["levels"][levelinforge]["thetaPlatformCoords"] = [theta_platform_y_editVar.get(),
                                                               theta_platform_x1_editVar.get(),
                                                               theta_platform_x2_editVar.get()]
    settings["levels"][levelinforge]["iotaPlatformFlag"] = iota_platform_state_editVar.get()
    settings["levels"][levelinforge]["iotaPlatformCoords"] = [iota_platform_y_editVar.get(),
                                                              iota_platform_x1_editVar.get(),
                                                              iota_platform_x2_editVar.get()]

    # Коты
    settings["levels"][levelinforge]["alphaCatFlag"] = alpha_cat_state_editVar.get()
    settings["levels"][levelinforge]["alphaCatCoords"] = [alpha_cat_x_editVar.get(),
                                                          alpha_cat_y_editVar.get()]
    settings["levels"][levelinforge]["betaCatFlag"] = beta_cat_state_editVar.get()
    settings["levels"][levelinforge]["betaCatCoords"] = [beta_cat_x_editVar.get(),
                                                         beta_cat_y_editVar.get()]
    settings["levels"][levelinforge]["gammaCatFlag"] = gamma_cat_state_editVar.get()
    settings["levels"][levelinforge]["gammaCatCoords"] = [gamma_cat_x_editVar.get(),
                                                          gamma_cat_y_editVar.get()]
    settings["levels"][levelinforge]["deltaCatFlag"] = delta_cat_state_editVar.get()
    settings["levels"][levelinforge]["deltaCatCoords"] = [delta_cat_x_editVar.get(),
                                                          delta_cat_y_editVar.get()]
    settings["levels"][levelinforge]["epsilonCatFlag"] = epsilon_cat_state_editVar.get()
    settings["levels"][levelinforge]["epsilonCatCoords"] = [epsilon_cat_x_editVar.get(),
                                                            epsilon_cat_y_editVar.get()]
    settings["levels"][levelinforge]["zetaCatFlag"] = zeta_cat_state_editVar.get()
    settings["levels"][levelinforge]["zetaCatCoords"] = [zeta_cat_x_editVar.get(),
                                                         zeta_cat_y_editVar.get()]

    # Бонусы
    settings["levels"][levelinforge]["alphaBonusFlag"] = alpha_bonus_state_editVar.get()
    settings["levels"][levelinforge]["alphaBonusCoords"] = [alpha_bonus_x_editVar.get(),
                                                            alpha_bonus_y_editVar.get()]
    settings["levels"][levelinforge]["betaBonusFlag"] = beta_bonus_state_editVar.get()
    settings["levels"][levelinforge]["betaBonusCoords"] = [beta_bonus_x_editVar.get(),
                                                           beta_bonus_y_editVar.get()]
    settings["levels"][levelinforge]["gammaBonusFlag"] = gamma_bonus_state_editVar.get()
    settings["levels"][levelinforge]["gammaBonusCoords"] = [gamma_bonus_x_editVar.get(),
                                                            gamma_bonus_y_editVar.get()]
    settings["levels"][levelinforge]["deltaBonusFlag"] = delta_bonus_state_editVar.get()
    settings["levels"][levelinforge]["deltaBonusCoords"] = [delta_bonus_x_editVar.get(),
                                                            delta_bonus_y_editVar.get()]
    settings["levels"][levelinforge]["epsilonBonusFlag"] = epsilon_bonus_state_editVar.get()
    settings["levels"][levelinforge]["epsilonBonusCoords"] = [epsilon_bonus_x_editVar.get(),
                                                              epsilon_bonus_y_editVar.get()]
    settings["levels"][levelinforge]["zetaBonusFlag"] = zeta_bonus_state_editVar.get()
    settings["levels"][levelinforge]["zetaBonusCoords"] = [zeta_bonus_x_editVar.get(),
                                                           zeta_bonus_y_editVar.get()]

    # Лестницы
    settings["levels"][levelinforge]["alphaLadderFlag"] = alpha_ladder_state_editVar.get()
    settings["levels"][levelinforge]["alphaLadderCoords"] = [alpha_ladder_x_editVar.get(),
                                                             alpha_ladder_y_editVar.get()]
    settings["levels"][levelinforge]["betaLadderFlag"] = beta_ladder_state_editVar.get()
    settings["levels"][levelinforge]["betaLadderCoords"] = [beta_ladder_x_editVar.get(),
                                                            beta_ladder_y_editVar.get()]
    settings["levels"][levelinforge]["gammaLadderFlag"] = gamma_ladder_state_editVar.get()
    settings["levels"][levelinforge]["gammaLadderCoords"] = [gamma_ladder_x_editVar.get(),
                                                             gamma_ladder_y_editVar.get()]
    settings["levels"][levelinforge]["deltaLadderFlag"] = delta_ladder_state_editVar.get()
    settings["levels"][levelinforge]["deltaLadderCoords"] = [delta_ladder_x_editVar.get(),
                                                             delta_ladder_y_editVar.get()]
    settings["levels"][levelinforge]["epsilonLadderFlag"] = epsilon_ladder_state_editVar.get()
    settings["levels"][levelinforge]["epsilonLadderCoords"] = [epsilon_ladder_x_editVar.get(),
                                                               epsilon_ladder_y_editVar.get()]
    settings["levels"][levelinforge]["zetaLadderFlag"] = zeta_ladder_state_editVar.get()
    settings["levels"][levelinforge]["zetaLadderCoords"] = [zeta_ladder_x_editVar.get(),
                                                            zeta_ladder_y_editVar.get()]

    # Стены
    settings["levels"][levelinforge]["alphaWallFlag"] = alpha_wall_state_editVar.get()
    settings["levels"][levelinforge]["alphaWallCoords"] = [alpha_wall_x_editVar.get(),
                                                           alpha_wall_y_editVar.get()]
    settings["levels"][levelinforge]["betaWallFlag"] = beta_wall_state_editVar.get()
    settings["levels"][levelinforge]["betaWallCoords"] = [beta_wall_x_editVar.get(),
                                                          beta_wall_y_editVar.get()]
    settings["levels"][levelinforge]["gammaWallFlag"] = gamma_wall_state_editVar.get()
    settings["levels"][levelinforge]["gammaWallCoords"] = [gamma_wall_x_editVar.get(),
                                                           gamma_wall_y_editVar.get()]
    settings["levels"][levelinforge]["deltaWallFlag"] = delta_wall_state_editVar.get()
    settings["levels"][levelinforge]["deltaWallCoords"] = [delta_wall_x_editVar.get(),
                                                           delta_wall_y_editVar.get()]
    settings["levels"][levelinforge]["epsilonWallFlag"] = epsilon_wall_state_editVar.get()
    settings["levels"][levelinforge]["epsilonWallCoords"] = [epsilon_wall_x_editVar.get(),
                                                             epsilon_wall_y_editVar.get()]
    settings["levels"][levelinforge]["zetaWallFlag"] = zeta_wall_state_editVar.get()
    settings["levels"][levelinforge]["zetaWallCoords"] = [zeta_wall_x_editVar.get(),
                                                          zeta_wall_y_editVar.get()]

    # Дикари
    settings["levels"][levelinforge]["alphaSavageFlag"] = alpha_savage_state_editVar.get()
    settings["levels"][levelinforge]["alphaSavageCoords"] = [alpha_savage_x_editVar.get(),
                                                             alpha_savage_y_editVar.get()]
    settings["levels"][levelinforge]["alphaSavagePlatform"] = alpha_savage_home_editVar.get()
    settings["levels"][levelinforge]["betaSavageFlag"] = beta_savage_state_editVar.get()
    settings["levels"][levelinforge]["betaSavageCoords"] = [beta_savage_x_editVar.get(),
                                                            beta_savage_y_editVar.get()]
    settings["levels"][levelinforge]["betaSavagePlatform"] = beta_savage_home_editVar.get()
    settings["levels"][levelinforge]["gammaSavageFlag"] = gamma_savage_state_editVar.get()
    settings["levels"][levelinforge]["gammaSavageCoords"] = [gamma_savage_x_editVar.get(),
                                                             gamma_savage_y_editVar.get()]
    settings["levels"][levelinforge]["gammaSavagePlatform"] = gamma_savage_home_editVar.get()
    settings["levels"][levelinforge]["deltaSavageFlag"] = delta_savage_state_editVar.get()
    settings["levels"][levelinforge]["deltaSavageCoords"] = [delta_savage_x_editVar.get(),
                                                             delta_savage_y_editVar.get()]
    settings["levels"][levelinforge]["deltaSavagePlatform"] = delta_savage_home_editVar.get()

    # Грибы
    settings["levels"][levelinforge]["alphaFastroomFlag"] = alpha_fastroom_state_editVar.get()
    settings["levels"][levelinforge]["alphaFastroomCoords"] = [alpha_fastroom_x_editVar.get(),
                                                           alpha_fastroom_y_editVar.get()]
    settings["levels"][levelinforge]["betaFastroomFlag"] = beta_fastroom_state_editVar.get()
    settings["levels"][levelinforge]["betaFastroomCoords"] = [beta_fastroom_x_editVar.get(),
                                                          beta_fastroom_y_editVar.get()]

    settings["levels"][levelinforge]["alphaSlowroomFlag"] = alpha_slowroom_state_editVar.get()
    settings["levels"][levelinforge]["alphaSlowroomCoords"] = [alpha_slowroom_x_editVar.get(),
                                                           alpha_slowroom_y_editVar.get()]
    settings["levels"][levelinforge]["betaSlowroomFlag"] = beta_slowroom_state_editVar.get()
    settings["levels"][levelinforge]["betaSlowroomCoords"] = [beta_slowroom_x_editVar.get(),
                                                          beta_slowroom_y_editVar.get()]

    settings["levels"][levelinforge]["alphaGravroomFlag"] = alpha_gravroom_state_editVar.get()
    settings["levels"][levelinforge]["alphaGravroomCoords"] = [alpha_gravroom_x_editVar.get(),
                                                           alpha_gravroom_y_editVar.get()]
    settings["levels"][levelinforge]["betaGravroomFlag"] = beta_gravroom_state_editVar.get()
    settings["levels"][levelinforge]["betaGravroomCoords"] = [beta_gravroom_x_editVar.get(),
                                                          beta_gravroom_y_editVar.get()]

    mb.showinfo(title="Запись", message="Значения сохранены. Не забудьте сохранить файл.")

def exit():
    if is_level_editing is False:
        if mb.askyesno(title="Выход", message="Вы действительно хотите выйти?\nНесохраненные данные будут утеряны"):
            master.destroy()
            sys.exit()
    else:
        warning("Завершите редактирование уровня")

"""Окна"""
class Root(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("480x420")
        self.title("Game Forge")
        self.resizable(0, 0)
        self.configure(bg=background_color)

        self.menu = Menu(self)
        self.filemenu = Menu(self.menu, tearoff=0, bg=background_color)
        self.filemenu.add_command(label="Открыть файл", command=openfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Выход", command=exit)
        self.menu.add_cascade(label="Файл", menu=self.filemenu)
        self.configure(menu=self.menu)

        self.common_frame=Frame(self, bg=background_color)
        self.common_frame.grid(row=1, column=0, columnspan=5)


    def common_entry(self, frame, row, column, var, text, color):
        Label(frame, text=text, font=("Arial", 12), bg=colors[color], anchor=E,
              width =12).grid(row=row, column=column, padx=0, pady=10)
        Entry(frame, font=("Arial", 10), bg=colors[color], textvariable=var,
              width =14).grid(row=row, column=column+1, padx=10, pady=10)

    def common_checkbutton(self, frame, row, column, var, text, color):
        Label(frame, text=text, font=("Arial", 12), bg=lev_colors[color], anchor=E,
              width =12).grid(row=row, column=column, padx=0, pady=10)
        Checkbutton(frame, bg=lev_colors[color], variable=var,
                    onvalue=1, offvalue=0).grid(row=row, column=column+1, padx=10, pady=10)


    def common_information_show(self, begin = False):
        Label(self, text="Общая информация", font=("Arial", 12),bg=background_color).grid(row=0, column=2,
                                                                                          padx=5, pady=0)

        self.common_entry(row=1, column=0, var=versionVar, text="Версия", color=0,
                          frame=self.common_frame)

        self.common_entry(row=2, column=0, var=livesVar, text="Жизни", color=0,
                          frame=self.common_frame)

        self.common_entry(row=3, column=0, var=catscoreVar, text="Очки (кот)", color=2,
                          frame=self.common_frame)

        self.common_entry(row=4, column=0, var=bonusscoreVar, text="Очки (цветок)", color=2,
                          frame=self.common_frame)

        self.common_entry(row=5, column=0, var=maxscoreVar, text="Очки (макс)", color=2,
                          frame=self.common_frame)

        self.common_entry(row=6, column=0, var=effectdurationVar, text="Эффект", color=1,
                          frame=self.common_frame)

        self.common_entry(row=1, column=3, var=levelsVar, text="Уровни", color=3,
                          frame=self.common_frame)


        self.common_entry(row=2, column=3, var=savagesVar, text="Дикари", color=3,
                          frame=self.common_frame)

        self.common_entry(row=3, column=3, var=flowersVar, text="Цветы", color=3,
                          frame=self.common_frame)

        self.common_checkbutton(row=4, column=3, var=cheatVar, text="Читы", color=3, frame=self.common_frame)

        self.common_checkbutton(row=5, column=3, var=musicVar, text="Музыка", color=5, frame=self.common_frame)

        self.common_checkbutton(row=6, column=3, var=soundVar, text="Звуки", color=5, frame=self.common_frame)

        if begin is False:
            Label(self, text="Редактировать уровень", font=("Arial", 12), bg="mistyrose",
                                         anchor=E, width =20).place(x=40, y=300)
            Spinbox(self, font=("Arial", 10), bg="mistyrose", textvariable=editlevelVar, from_=1,
                                           to=(len(settings["levels"])-1), width=20).place(x=250, y=300)

            Button(self, text="Редактировать", bg="mistyrose", font=("Arial", 12),
                   command=level_edit).place(x=165, y=330)
            Button(self, text="Сохранить изменения", bg="palegreen", font=("Arial", 12),
                   command=send_vars).place(x=40, y=380)

        Button(self, text="Закрыть", bg="pink2", font=("Arial", 12),
               command=exit, width=19).place(x=250, y=380)

class LevelEdit():
    def __init__(self, mainwindow):
        self.window = Toplevel(mainwindow)
        self.window.configure(bg=background_color)
        self.window.resizable(0, 0)
        self.window.title("Level Forge")
        self.data = emptylevel
        self.basics = LabelFrame(self.window, bg=lev_colors[0], text="Основное")
        self.hints = LabelFrame(self.window, bg=lev_colors[1], text="Подсказка")
        self.fastrooms = LabelFrame(self.window, bg=lev_colors[8], text="Быстроморы")
        self.slowrooms = LabelFrame(self.window, bg=lev_colors[9], text="Медлянки")
        self.gravrooms = LabelFrame(self.window, bg=lev_colors[10], text="Вверхшенки")
        self.masks = LabelFrame(self.window, bg=lev_colors[11], text="Маски")
        self.platforms = LabelFrame(self.window, bg=lev_colors[2], text="Платформы")
        self.cats = LabelFrame(self.window, bg=lev_colors[3], text="Коты")
        self.bonuses = LabelFrame(self.window, bg=lev_colors[4], text="Цветочки")
        self.ladders = LabelFrame(self.window, bg=lev_colors[5], text="Лестницы")
        self.walls = LabelFrame(self.window, bg=lev_colors[6], text="Стены")
        self.savages = LabelFrame(self.window, bg=lev_colors[7], text="Дикари")
        self.info = Label(self.window, text="Редактирование уровня", font=("Arial", 10), bg=background_color)
        self.info.grid(row=0, column=0, columnspan=8)
        self.basics.grid(row=1, column=0, columnspan=2, sticky=E)
        self.fastrooms.grid(row=1, column=2, sticky=E)
        self.slowrooms.grid(row=1, column=3, sticky=E)
        self.gravrooms.grid(row=1, column=4, sticky=E)
        self.masks.grid(row=1, column=5, sticky=E)
        self.hints.grid(row=1, column=6, sticky=NW)
        self.platforms.grid(row=2, column=0, columnspan=2, sticky=N)
        self.cats.grid(row=2, column=2, sticky=N)
        self.bonuses.grid(row=2, column=3, sticky=N)
        self.ladders.grid(row=2, column=4, sticky=N)
        self.walls.grid(row=2, column=5, sticky=N)
        self.savages.grid(row=2, column=6, sticky=N)
        self.show_all()

    def show_all(self):
        self.show_basics()
        self.show_platforms()
        self.show_cats()
        self.show_bonuses()
        self.show_ladders()
        self.show_walls()
        self.show_savages()
        self.show_mushrooms()
        self.show_mask()
        Label(self.hints, text=hint, bg=lev_colors[1], font=("Arial", 8), anchor=W).grid(sticky=W)
        self.level_save_butt = Button(self.window, bg="palegreen", text="Сохранить", command=level_edit_save,
                                      font=("Arial", 12))
        self.level_close_butt = Button(self.window, bg="pink3", text="Выход",command=level_edit_close,
                                       font=("Arial", 12))
        self.level_save_butt.grid(row=3, column=0, columnspan=3, sticky=E)
        self.level_close_butt.grid(row=3, column=4, columnspan=3, sticky=W)
        self.link = Label(self.hints, text="Wiki по объектам", fg="blue", cursor="hand2")
        self.link.grid(sticky=NW)
        self.link.bind("<Button-1>", lambda e: webbrowser.open_new(
            "https://github.com/Apochromat/grannys-skirmish/wiki/Objects"))

    def show_basics(self):
        self.create_spinbox(frame=self.basics, row=0, column=0, var= level_editVar, text="Уровень:",
                            color=0, beg=1, end=999, len=10, state = DISABLED)

        self.create_checkbutton(frame=self.basics, row=1, column=0, var=limit_editVar, text="Ограниченность:",
                                color=0)

        self.create_radiobutton(frame=self.basics, row=2, column=0, var=limit_type_editVar, text="Следующий:",
                                color=0, value=0)

        self.create_radiobutton(frame=self.basics, row=3, column=0, var=limit_type_editVar, text="Проигрыш:",
                                color=0, value=1)

        self.create_spinbox(frame=self.basics, row=4, column=0, var=limit_time_editVar, text="Время:",
                            color=0, beg=1, end=999, len=10)

        self.create_spinbox(frame=self.basics, row=0, column=2, var=player_x_editVar, text="Персонаж Х:",
                            color=0, beg=30, end=610, len=12)

        self.create_spinbox(frame=self.basics, row=1, column=2, var=player_y_editVar, text="Персонаж Y:",
                            color=0, beg=30, end=430, len=12)

        self.create_spinbox(frame=self.basics, row=2,  column=2, var=exit_x_editVar, text="Выход Х:",
                            color=0, beg=30, end=610, len=12)

        self.create_spinbox(frame=self.basics, row=3, column=2, var=exit_y_editVar, text="Выход Y:",
                            color=0, beg=30, end=430, len=12)

        self.create_spinbox(frame=self.basics, row=4, column=2, var=cats_editVar, text="Коты:",
                            color=0, beg=0, end=6, len=12)

    def show_platforms(self):
        """ALPHA"""
        self.create_checkbutton(frame=self.platforms, row=0,
                                column=0, var=alpha_platform_state_editVar, text="Alpha platform:", color=2)
        self.create_spinbox(frame=self.platforms, row=1,
                            column=0, var=alpha_platform_y_editVar, text="Y:", color=2, beg=0, end=430, len=10)
        self.create_spinbox(frame=self.platforms, row=2,
                            column=0, var=alpha_platform_x1_editVar, text="X1:", color=2, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.platforms, row=3,
                            column=0, var=alpha_platform_x2_editVar, text="X2:", color=2, beg=0, end=610, len=10)
        
        """BETA"""
        self.create_checkbutton(frame=self.platforms, row=4,
                                column=0, var=beta_platform_state_editVar, text="Beta platform:", color=2)
        self.create_spinbox(frame=self.platforms, row=5,
                            column=0, var=beta_platform_y_editVar, text="Y:", color=2, beg=0, end=430, len=10)
        self.create_spinbox(frame=self.platforms, row=6,
                            column=0, var=beta_platform_x1_editVar, text="X1:", color=2, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.platforms, row=7,
                            column=0, var=beta_platform_x2_editVar, text="X2:", color=2, beg=0, end=610, len=10)

        """GAMMA"""
        self.create_checkbutton(frame=self.platforms, row=8,
                                column=0, var=gamma_platform_state_editVar, text="Gamma platform:", color=2)
        self.create_spinbox(frame=self.platforms, row=9,
                            column=0, var=gamma_platform_y_editVar, text="Y:", color=2, beg=0, end=430, len=10)
        self.create_spinbox(frame=self.platforms, row=10,
                            column=0, var=gamma_platform_x1_editVar, text="X1:", color=2, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.platforms, row=11,
                            column=0, var=gamma_platform_x2_editVar, text="X2:", color=2, beg=0, end=610, len=10)

        """DELTA"""
        self.create_checkbutton(frame=self.platforms, row=12,
                                column=0, var=delta_platform_state_editVar, text="Delta platform:", color=2)
        self.create_spinbox(frame=self.platforms, row=13,
                            column=0, var=delta_platform_y_editVar, text="Y:", color=2, beg=0, end=430, len=10)
        self.create_spinbox(frame=self.platforms, row=14,
                            column=0, var=delta_platform_x1_editVar, text="X1:", color=2, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.platforms, row=15,
                            column=0, var=delta_platform_x2_editVar, text="X2:", color=2, beg=0, end=610, len=10)

        """EPSILON"""
        self.create_checkbutton(frame=self.platforms, row=16,
                                column=0, var=epsilon_platform_state_editVar, text="Epsilon platform:", color=2)
        self.create_spinbox(frame=self.platforms, row=17,
                            column=0, var=epsilon_platform_y_editVar, text="Y:", color=2, beg=0, end=430, len=10)
        self.create_spinbox(frame=self.platforms, row=18,
                            column=0, var=epsilon_platform_x1_editVar, text="X1:", color=2, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.platforms, row=19,
                            column=0, var=epsilon_platform_x2_editVar, text="X2:", color=2, beg=0, end=610, len=10)

        """ZETA"""
        self.create_checkbutton(frame=self.platforms, row=0,
                                column=2, var=zeta_platform_state_editVar, text="Zeta platform:", color=2)
        self.create_spinbox(frame=self.platforms, row=1,
                            column=2, var=zeta_platform_y_editVar, text="Y:", color=2, beg=0, end=430, len=10)
        self.create_spinbox(frame=self.platforms, row=2,
                            column=2, var=zeta_platform_x1_editVar, text="X1:", color=2, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.platforms, row=3,
                            column=2, var=zeta_platform_x2_editVar, text="X2:", color=2, beg=0, end=610, len=10)

        """ETA"""
        self.create_checkbutton(frame=self.platforms, row=4,
                                column=2, var=eta_platform_state_editVar, text="Eta platform:", color=2)
        self.create_spinbox(frame=self.platforms, row=5,
                            column=2, var=eta_platform_y_editVar, text="Y:", color=2, beg=0, end=430, len=10)
        self.create_spinbox(frame=self.platforms, row=6,
                            column=2, var=eta_platform_x1_editVar, text="X1:", color=2, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.platforms, row=7,
                            column=2, var=eta_platform_x2_editVar, text="X2:", color=2, beg=0, end=610, len=10)

        """THETA"""
        self.create_checkbutton(frame=self.platforms, row=8,
                                column=2, var=theta_platform_state_editVar, text="Theta platform:", color=2)
        self.create_spinbox(frame=self.platforms, row=9,
                            column=2, var=theta_platform_y_editVar, text="Y:", color=2, beg=0, end=430, len=10)
        self.create_spinbox(frame=self.platforms, row=10,
                            column=2, var=theta_platform_x1_editVar, text="X1:", color=2, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.platforms, row=11,
                            column=2, var=theta_platform_x2_editVar, text="X2:", color=2, beg=0, end=610, len=10)

        """IOTA"""
        self.create_checkbutton(frame=self.platforms, row=12,
                                column=2, var=iota_platform_state_editVar, text="Iota platform:", color=2)
        self.create_spinbox(frame=self.platforms, row=13,
                            column=2, var=iota_platform_y_editVar, text="Y:", color=2, beg=0, end=430, len=10)
        self.create_spinbox(frame=self.platforms, row=14,
                            column=2, var=iota_platform_x1_editVar, text="X1:", color=2, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.platforms, row=15,
                            column=2, var=iota_platform_x2_editVar, text="X2:", color=2, beg=0, end=610, len=10)
        
    def show_cats(self):
        """ALPHA"""
        self.create_checkbutton(frame=self.cats, row=0,
                                column=0, var=alpha_cat_state_editVar, text="Alpha cat:", color=3)
        self.create_spinbox(frame=self.cats, row=1,
                            column=0, var=alpha_cat_x_editVar, text="X:", color=3, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.cats, row=2,
                            column=0, var=alpha_cat_y_editVar, text="Y:", color=3, beg=0, end=430, len=10)

        """BETA"""
        self.create_checkbutton(frame=self.cats, row=3,
                                column=0, var=beta_cat_state_editVar, text="Beta cat:", color=3)
        self.create_spinbox(frame=self.cats, row=4,
                            column=0, var=beta_cat_x_editVar, text="X:", color=3, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.cats, row=5,
                            column=0, var=beta_cat_y_editVar, text="Y:", color=3, beg=0, end=430, len=10)

        """GAMMA"""
        self.create_checkbutton(frame=self.cats, row=6,
                                column=0, var=gamma_cat_state_editVar, text="Gamma cat:", color=3)
        self.create_spinbox(frame=self.cats, row=7,
                            column=0, var=gamma_cat_x_editVar, text="X:", color=3, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.cats, row=8,
                            column=0, var=gamma_cat_y_editVar, text="Y:", color=3, beg=0, end=430, len=10)

        """DELTA"""
        self.create_checkbutton(frame=self.cats, row=9,
                                column=0, var=delta_cat_state_editVar, text="Delta cat:", color=3)
        self.create_spinbox(frame=self.cats, row=10,
                            column=0, var=delta_cat_x_editVar, text="X:", color=3, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.cats, row=11,
                            column=0, var=delta_cat_y_editVar, text="Y:", color=3, beg=0, end=430, len=10)

        """EPSILON"""
        self.create_checkbutton(frame=self.cats, row=12,
                                column=0, var=epsilon_cat_state_editVar, text="Epsilon cat:", color=3)
        self.create_spinbox(frame=self.cats, row=13,
                            column=0, var=epsilon_cat_x_editVar, text="X:", color=3, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.cats, row=14,
                            column=0, var=epsilon_cat_y_editVar, text="Y:", color=3, beg=0, end=430, len=10)

        """ZETA"""
        self.create_checkbutton(frame=self.cats, row=15,
                                column=0, var=zeta_cat_state_editVar, text="Zeta cat:", color=3)
        self.create_spinbox(frame=self.cats, row=16,
                            column=0, var=zeta_cat_x_editVar, text="X:", color=3, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.cats, row=17,
                            column=0, var=zeta_cat_y_editVar, text="Y:", color=3, beg=0, end=430, len=10)

    def show_bonuses(self):
        """ALPHA"""
        self.create_checkbutton(frame=self.bonuses, row=0,
                                column=0, var=alpha_bonus_state_editVar, text="Alpha bonus:", color=4)
        self.create_spinbox(frame=self.bonuses, row=1,
                            column=0, var=alpha_bonus_x_editVar, text="X:", color=4, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.bonuses, row=2,
                            column=0, var=alpha_bonus_y_editVar, text="Y:", color=4, beg=0, end=430, len=10)

        """BETA"""
        self.create_checkbutton(frame=self.bonuses, row=3,
                                column=0, var=beta_bonus_state_editVar, text="Beta bonus:", color=4)
        self.create_spinbox(frame=self.bonuses, row=4,
                            column=0, var=beta_bonus_x_editVar, text="X:", color=4, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.bonuses, row=5,
                            column=0, var=beta_bonus_y_editVar, text="Y:", color=4, beg=0, end=430, len=10)

        """GAMMA"""
        self.create_checkbutton(frame=self.bonuses, row=6,
                                column=0, var=gamma_bonus_state_editVar, text="Gamma bonus:", color=4)
        self.create_spinbox(frame=self.bonuses, row=7,
                            column=0, var=gamma_bonus_x_editVar, text="X:", color=4, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.bonuses, row=8,
                            column=0, var=gamma_bonus_y_editVar, text="Y:", color=4, beg=0, end=430, len=10)

        """DELTA"""
        self.create_checkbutton(frame=self.bonuses, row=9,
                                column=0, var=delta_bonus_state_editVar, text="Delta bonus:", color=4)
        self.create_spinbox(frame=self.bonuses, row=10,
                            column=0, var=delta_bonus_x_editVar, text="X:", color=4, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.bonuses, row=11,
                            column=0, var=delta_bonus_y_editVar, text="Y:", color=4, beg=0, end=430, len=10)

        """EPSILON"""
        self.create_checkbutton(frame=self.bonuses, row=12,
                                column=0, var=epsilon_bonus_state_editVar, text="Epsilon bonus:", color=4)
        self.create_spinbox(frame=self.bonuses, row=13,
                            column=0, var=epsilon_bonus_x_editVar, text="X:", color=4, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.bonuses, row=14,
                            column=0, var=epsilon_bonus_y_editVar, text="Y:", color=4, beg=0, end=430, len=10)

        """ZETA"""
        self.create_checkbutton(frame=self.bonuses, row=15,
                                column=0, var=zeta_bonus_state_editVar, text="Zeta bonus:", color=4)
        self.create_spinbox(frame=self.bonuses, row=16,
                            column=0, var=zeta_bonus_x_editVar, text="X:", color=4, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.bonuses, row=17,
                            column=0, var=zeta_bonus_y_editVar, text="Y:", color=4, beg=0, end=430, len=10)

    def show_ladders(self):
        """ALPHA"""
        self.create_checkbutton(frame=self.ladders, row=0,
                                column=0, var=alpha_ladder_state_editVar, text="Alpha ladder:", color=5)
        self.create_spinbox(frame=self.ladders, row=1,
                            column=0, var=alpha_ladder_x_editVar, text="X:", color=5, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.ladders, row=2,
                            column=0, var=alpha_ladder_y_editVar, text="Y:", color=5, beg=0, end=430, len=10)

        """BETA"""
        self.create_checkbutton(frame=self.ladders, row=3,
                                column=0, var=beta_ladder_state_editVar, text="Beta ladder:", color=5)
        self.create_spinbox(frame=self.ladders, row=4,
                            column=0, var=beta_ladder_x_editVar, text="X:", color=5, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.ladders, row=5,
                            column=0, var=beta_ladder_y_editVar, text="Y:", color=5, beg=0, end=430, len=10)

        """GAMMA"""
        self.create_checkbutton(frame=self.ladders, row=6,
                                column=0, var=gamma_ladder_state_editVar, text="Gamma ladder:", color=5)
        self.create_spinbox(frame=self.ladders, row=7,
                            column=0, var=gamma_ladder_x_editVar, text="X:", color=5, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.ladders, row=8,
                            column=0, var=gamma_ladder_y_editVar, text="Y:", color=5, beg=0, end=430, len=10)

        """DELTA"""
        self.create_checkbutton(frame=self.ladders, row=9,
                                column=0, var=delta_ladder_state_editVar, text="Delta ladder:", color=5)
        self.create_spinbox(frame=self.ladders, row=10,
                            column=0, var=delta_ladder_x_editVar, text="X:", color=5, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.ladders, row=11,
                            column=0, var=delta_ladder_y_editVar, text="Y:", color=5, beg=0, end=430, len=10)

        """EPSILON"""
        self.create_checkbutton(frame=self.ladders, row=12,
                                column=0, var=epsilon_ladder_state_editVar, text="Epsilon ladder:", color=5)
        self.create_spinbox(frame=self.ladders, row=13,
                            column=0, var=epsilon_ladder_x_editVar, text="X:", color=5, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.ladders, row=14,
                            column=0, var=epsilon_ladder_y_editVar, text="Y:", color=5, beg=0, end=430, len=10)

        """ZETA"""
        self.create_checkbutton(frame=self.ladders, row=15,
                                column=0, var=zeta_ladder_state_editVar, text="Zeta ladder:", color=5)
        self.create_spinbox(frame=self.ladders, row=16,
                            column=0, var=zeta_ladder_x_editVar, text="X:", color=5, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.ladders, row=17,
                            column=0, var=zeta_ladder_y_editVar, text="Y:", color=5, beg=0, end=430, len=10)

    def show_walls(self):
            """ALPHA"""
            self.create_checkbutton(frame=self.walls, row=0,
                                    column=0, var=alpha_wall_state_editVar, text="Alpha wall:", color=6)
            self.create_spinbox(frame=self.walls, row=1,
                                column=0, var=alpha_wall_x_editVar, text="X:", color=6, beg=0, end=610, len=10)
            self.create_spinbox(frame=self.walls, row=2,
                                column=0, var=alpha_wall_y_editVar, text="Y:", color=6, beg=0, end=430, len=10)

            """BETA"""
            self.create_checkbutton(frame=self.walls, row=3,
                                    column=0, var=beta_wall_state_editVar, text="Beta wall:", color=6)
            self.create_spinbox(frame=self.walls, row=4,
                                column=0, var=beta_wall_x_editVar, text="X:", color=6, beg=0, end=610, len=10)
            self.create_spinbox(frame=self.walls, row=5,
                                column=0, var=beta_wall_y_editVar, text="Y:", color=6, beg=0, end=430, len=10)

            """GAMMA"""
            self.create_checkbutton(frame=self.walls, row=6,
                                    column=0, var=gamma_wall_state_editVar, text="Gamma wall:", color=6)
            self.create_spinbox(frame=self.walls, row=7,
                                column=0, var=gamma_wall_x_editVar, text="X:", color=6, beg=0, end=610, len=10)
            self.create_spinbox(frame=self.walls, row=8,
                                column=0, var=gamma_wall_y_editVar, text="Y:", color=6, beg=0, end=430, len=10)

            """DELTA"""
            self.create_checkbutton(frame=self.walls, row=9,
                                    column=0, var=delta_wall_state_editVar, text="Delta wall:", color=6)
            self.create_spinbox(frame=self.walls, row=10,
                                column=0, var=delta_wall_x_editVar, text="X:", color=6, beg=0, end=610, len=10)
            self.create_spinbox(frame=self.walls, row=11,
                                column=0, var=delta_wall_y_editVar, text="Y:", color=6, beg=0, end=430, len=10)

            """EPSILON"""
            self.create_checkbutton(frame=self.walls, row=12,
                                    column=0, var=epsilon_wall_state_editVar, text="Epsilon wall:", color=6)
            self.create_spinbox(frame=self.walls, row=13,
                                column=0, var=epsilon_wall_x_editVar, text="X:", color=6, beg=0, end=610, len=10)
            self.create_spinbox(frame=self.walls, row=14,
                                column=0, var=epsilon_wall_y_editVar, text="Y:", color=6, beg=0, end=430, len=10)

            """ZETA"""
            self.create_checkbutton(frame=self.walls, row=15,
                                    column=0, var=zeta_wall_state_editVar, text="Zeta wall:", color=6)
            self.create_spinbox(frame=self.walls, row=16,
                                column=0, var=zeta_wall_x_editVar, text="X:", color=6, beg=0, end=610, len=10)
            self.create_spinbox(frame=self.walls, row=17,
                                column=0, var=zeta_wall_y_editVar, text="Y:", color=6, beg=0, end=430, len=10)

    def show_savages(self):
            """ALPHA"""

            self.create_checkbutton(frame=self.savages, row=0,
                                    column=0, var=alpha_savage_state_editVar, text="Alpha savage:", color=7)
            self.create_spinbox(frame=self.savages, row=1,
                                column=0, var=alpha_savage_x_editVar, text="X:", color=7, beg=0, end=610, len=10)
            self.create_spinbox(frame=self.savages, row=2,
                                column=0, var=alpha_savage_y_editVar, text="Y:", color=7, beg=0, end=430, len=10)
            self.create_entry(frame=self.savages, row=3,
                              column=0, var=alpha_savage_home_editVar, text="Платформа:", color=7)

            """BETA"""
            self.create_checkbutton(frame=self.savages, row=4,
                                    column=0, var=beta_savage_state_editVar, text="Beta savage:", color=7)
            self.create_spinbox(frame=self.savages, row=5,
                                column=0, var=beta_savage_x_editVar, text="X:", color=7, beg=0, end=610, len=10)
            self.create_spinbox(frame=self.savages, row=6,
                                column=0, var=beta_savage_y_editVar, text="Y:", color=7, beg=0, end=430, len=10)
            self.create_entry(frame=self.savages, row=7,
                              column=0, var=beta_savage_home_editVar, text="Платформа:", color=7)

            """GAMMA"""
            self.create_checkbutton(frame=self.savages, row=8,
                                    column=0, var=gamma_savage_state_editVar, text="Gamma savage:", color=7)
            self.create_spinbox(frame=self.savages, row=9,
                                column=0, var=gamma_savage_x_editVar, text="X:", color=7, beg=0, end=610, len=10)
            self.create_spinbox(frame=self.savages, row=10,
                                column=0, var=gamma_savage_y_editVar, text="Y:", color=7, beg=0, end=430, len=10)
            self.create_entry(frame=self.savages, row=11,
                              column=0, var=gamma_savage_home_editVar, text="Платформа:", color=7)

            """DELTA"""
            self.create_checkbutton(frame=self.savages, row=12,
                                    column=0, var=delta_savage_state_editVar, text="Delta savage:", color=7)
            self.create_spinbox(frame=self.savages, row=13,
                                column=0, var=delta_savage_x_editVar, text="X:", color=7, beg=0, end=610, len=10)
            self.create_spinbox(frame=self.savages, row=14,
                                column=0, var=delta_savage_y_editVar, text="Y:", color=7, beg=0, end=430, len=10)
            self.create_entry(frame=self.savages, row=15,
                              column=0, var=delta_savage_home_editVar, text="Платформа:", color=7)
        
    def show_mushrooms(self):
        """ALPHA FAST"""
        self.create_checkbutton(frame=self.fastrooms, row=0,
                                column=0, var=alpha_fastroom_state_editVar, text="Alpha fastroom:", color=8)
        self.create_spinbox(frame=self.fastrooms, row=1,
                            column=0, var=alpha_fastroom_x_editVar, text="X:", color=8, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.fastrooms, row=2,
                            column=0, var=alpha_fastroom_y_editVar, text="Y:", color=8, beg=0, end=430, len=10)

        """BETA FAST"""
        self.create_checkbutton(frame=self.fastrooms, row=3,
                                column=0, var=beta_fastroom_state_editVar, text="Beta fastroom:", color=8)
        self.create_spinbox(frame=self.fastrooms, row=4,
                            column=0, var=beta_fastroom_x_editVar, text="X:", color=8, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.fastrooms, row=5,
                            column=0, var=beta_fastroom_y_editVar, text="Y:", color=8, beg=0, end=430, len=10)

        """ALPHA SLOW"""
        self.create_checkbutton(frame=self.slowrooms, row=0,
                                column=0, var=alpha_slowroom_state_editVar, text="Alpha slowroom:", color=9)
        self.create_spinbox(frame=self.slowrooms, row=1,
                            column=0, var=alpha_slowroom_x_editVar, text="X:", color=9, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.slowrooms, row=2,
                            column=0, var=alpha_slowroom_y_editVar, text="Y:", color=9, beg=0, end=430, len=10)

        """BETA SLOW"""
        self.create_checkbutton(frame=self.slowrooms, row=3,
                                column=0, var=beta_slowroom_state_editVar, text="Beta slowroom:", color=9)
        self.create_spinbox(frame=self.slowrooms, row=4,
                            column=0, var=beta_slowroom_x_editVar, text="X:", color=9, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.slowrooms, row=5,
                            column=0, var=beta_slowroom_y_editVar, text="Y:", color=9, beg=0, end=430, len=10)

        """ALPHA GRAV"""
        self.create_checkbutton(frame=self.gravrooms, row=0,
                                column=0, var=alpha_gravroom_state_editVar, text="Alpha gravroom:", color=10)
        self.create_spinbox(frame=self.gravrooms, row=1,
                            column=0, var=alpha_gravroom_x_editVar, text="X:", color=10, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.gravrooms, row=2,
                            column=0, var=alpha_gravroom_y_editVar, text="Y:", color=10, beg=0, end=430, len=10)

        """BETA GRAV"""
        self.create_checkbutton(frame=self.gravrooms, row=3,
                                column=0, var=beta_gravroom_state_editVar, text="Beta gravroom:", color=10)
        self.create_spinbox(frame=self.gravrooms, row=4,
                            column=0, var=beta_gravroom_x_editVar, text="X:", color=10, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.gravrooms, row=5,
                            column=0, var=beta_gravroom_y_editVar, text="Y:", color=10, beg=0, end=430, len=10)

    def show_mask(self):
        self.create_checkbutton(frame=self.masks, row=0,
                                column=0, var=mask_state_editVar, text="Mask :", color=11)
        self.create_spinbox(frame=self.masks, row=1,
                            column=0, var=mask_chance_editVar, text="Шанс (%):", color=11, beg=0, end=100, len=10)
        self.create_entry(frame=self.masks, row=2,
                          column=0, var=mask_kind_editVar, text="Тип:", color=11)
        self.create_spinbox(frame=self.masks, row=3,
                            column=0, var=mask_x_editVar, text="X:", color=11, beg=0, end=610, len=10)
        self.create_spinbox(frame=self.masks, row=4,
                            column=0, var=mask_y_editVar, text="Y:", color=11, beg=0, end=430, len=10)



    def create_spinbox(self, frame, row, column, var, text, color, beg, end, len, state=NORMAL):
        Label(frame, text=text, font=("Arial", 8), bg=lev_colors[color], anchor=E,
              width = len).grid(row=row, column=column, padx=0, pady=0)
        Spinbox(frame, font=("Arial", 8), bg=lev_colors[color], textvariable=var, from_=beg, to=end,
                       width=len, state=state).grid(row=row, column=column+1, padx=5, pady=0)

    def create_entry(self, frame, row, column, var, text, color):
        Label(frame, text=text, font=("Arial", 8), bg=lev_colors[color], anchor=E,
              width =10).grid(row=row, column=column, padx=0, pady=0)
        Entry(frame, font=("Arial", 8), bg=lev_colors[color], textvariable=var,
              width =12).grid(row=row, column=column+1, padx=5, pady=0)

    def create_radiobutton(self, frame, row, column, var, text, color, value):
        Label(frame, text=text, font=("Arial", 8), bg=lev_colors[color], anchor=E,
              width =14).grid(row=row, column=column, padx=0, pady=0)
        Radiobutton(frame, bg=lev_colors[color], variable=var,
                    value=value).grid(row=row, column=column+1, padx=5, pady=0)


    def create_checkbutton(self, frame, row, column, var, text, color):
        Label(frame, text=text, font=("Arial", 8), bg=lev_colors[color], anchor=E,
              width =14).grid(row=row, column=column, padx=0, pady=0)
        Checkbutton(frame, bg=lev_colors[color], variable=var,
                    onvalue=1, offvalue=0).grid(row=row, column=column+1, padx=5, pady=0)


master = Root()
# Переменные Общей информации
versionVar = StringVar()
livesVar = IntVar()
catscoreVar = IntVar()
bonusscoreVar = IntVar()
maxscoreVar = IntVar()
effectdurationVar = IntVar()
levelsVar = IntVar()
savagesVar = IntVar()
flowersVar = IntVar()
cheatVar = BooleanVar()
musicVar = BooleanVar()
soundVar = BooleanVar()
editlevelVar = IntVar()

# Переменные Уровня
# Основное
level_editVar = IntVar()
limit_editVar = BooleanVar()
limit_type_editVar = BooleanVar()
limit_time_editVar = IntVar()
player_x_editVar = IntVar()
player_y_editVar = IntVar()
exit_x_editVar = IntVar()
exit_y_editVar = IntVar()
cats_editVar = IntVar()

# Маски
mask_state_editVar = BooleanVar()
mask_kind_editVar = StringVar()
mask_chance_editVar = IntVar()
mask_x_editVar = IntVar()
mask_y_editVar = IntVar()

# Платформы
alpha_platform_state_editVar = BooleanVar()
alpha_platform_y_editVar = IntVar()
alpha_platform_x1_editVar = IntVar()
alpha_platform_x2_editVar = IntVar()
beta_platform_state_editVar = BooleanVar()
beta_platform_y_editVar = IntVar()
beta_platform_x1_editVar = IntVar()
beta_platform_x2_editVar = IntVar()
gamma_platform_state_editVar = BooleanVar()
gamma_platform_y_editVar = IntVar()
gamma_platform_x1_editVar = IntVar()
gamma_platform_x2_editVar = IntVar()
delta_platform_state_editVar = BooleanVar()
delta_platform_y_editVar = IntVar()
delta_platform_x1_editVar = IntVar()
delta_platform_x2_editVar = IntVar()
epsilon_platform_state_editVar = BooleanVar()
epsilon_platform_y_editVar = IntVar()
epsilon_platform_x1_editVar = IntVar()
epsilon_platform_x2_editVar = IntVar()
zeta_platform_state_editVar = BooleanVar()
zeta_platform_y_editVar = IntVar()
zeta_platform_x1_editVar = IntVar()
zeta_platform_x2_editVar = IntVar()
eta_platform_state_editVar = BooleanVar()
eta_platform_y_editVar = IntVar()
eta_platform_x1_editVar = IntVar()
eta_platform_x2_editVar = IntVar()
theta_platform_state_editVar = BooleanVar()
theta_platform_y_editVar = IntVar()
theta_platform_x1_editVar = IntVar()
theta_platform_x2_editVar = IntVar()
iota_platform_state_editVar = BooleanVar()
iota_platform_y_editVar = IntVar()
iota_platform_x1_editVar = IntVar()
iota_platform_x2_editVar = IntVar()

# Коты
alpha_cat_state_editVar = BooleanVar()
alpha_cat_x_editVar = IntVar()
alpha_cat_y_editVar = IntVar()
beta_cat_state_editVar = BooleanVar()
beta_cat_x_editVar = IntVar()
beta_cat_y_editVar = IntVar()
gamma_cat_state_editVar = BooleanVar()
gamma_cat_x_editVar = IntVar()
gamma_cat_y_editVar = IntVar()
delta_cat_state_editVar = BooleanVar()
delta_cat_x_editVar = IntVar()
delta_cat_y_editVar = IntVar()
epsilon_cat_state_editVar = BooleanVar()
epsilon_cat_x_editVar = IntVar()
epsilon_cat_y_editVar = IntVar()
zeta_cat_state_editVar = BooleanVar()
zeta_cat_x_editVar = IntVar()
zeta_cat_y_editVar = IntVar()

# Бонусы
alpha_bonus_state_editVar = BooleanVar()
alpha_bonus_x_editVar = IntVar()
alpha_bonus_y_editVar = IntVar()
beta_bonus_state_editVar = BooleanVar()
beta_bonus_x_editVar = IntVar()
beta_bonus_y_editVar = IntVar()
gamma_bonus_state_editVar = BooleanVar()
gamma_bonus_x_editVar = IntVar()
gamma_bonus_y_editVar = IntVar()
delta_bonus_state_editVar = BooleanVar()
delta_bonus_x_editVar = IntVar()
delta_bonus_y_editVar = IntVar()
epsilon_bonus_state_editVar = BooleanVar()
epsilon_bonus_x_editVar = IntVar()
epsilon_bonus_y_editVar = IntVar()
zeta_bonus_state_editVar = BooleanVar()
zeta_bonus_x_editVar = IntVar()
zeta_bonus_y_editVar = IntVar()

# Лестницы
alpha_ladder_state_editVar = BooleanVar()
alpha_ladder_x_editVar = IntVar()
alpha_ladder_y_editVar = IntVar()
beta_ladder_state_editVar = BooleanVar()
beta_ladder_x_editVar = IntVar()
beta_ladder_y_editVar = IntVar()
gamma_ladder_state_editVar = BooleanVar()
gamma_ladder_x_editVar = IntVar()
gamma_ladder_y_editVar = IntVar()
delta_ladder_state_editVar = BooleanVar()
delta_ladder_x_editVar = IntVar()
delta_ladder_y_editVar = IntVar()
epsilon_ladder_state_editVar = BooleanVar()
epsilon_ladder_x_editVar = IntVar()
epsilon_ladder_y_editVar = IntVar()
zeta_ladder_state_editVar = BooleanVar()
zeta_ladder_x_editVar = IntVar()
zeta_ladder_y_editVar = IntVar()

# Стены
alpha_wall_state_editVar = BooleanVar()
alpha_wall_x_editVar = IntVar()
alpha_wall_y_editVar = IntVar()
beta_wall_state_editVar = BooleanVar()
beta_wall_x_editVar = IntVar()
beta_wall_y_editVar = IntVar()
gamma_wall_state_editVar = BooleanVar()
gamma_wall_x_editVar = IntVar()
gamma_wall_y_editVar = IntVar()
delta_wall_state_editVar = BooleanVar()
delta_wall_x_editVar = IntVar()
delta_wall_y_editVar = IntVar()
epsilon_wall_state_editVar = BooleanVar()
epsilon_wall_x_editVar = IntVar()
epsilon_wall_y_editVar = IntVar()
zeta_wall_state_editVar = BooleanVar()
zeta_wall_x_editVar = IntVar()
zeta_wall_y_editVar = IntVar()

# Дикари
alpha_savage_state_editVar = BooleanVar()
alpha_savage_x_editVar = IntVar()
alpha_savage_y_editVar = IntVar()
alpha_savage_home_editVar = StringVar()
beta_savage_state_editVar = BooleanVar()
beta_savage_x_editVar = IntVar()
beta_savage_y_editVar = IntVar()
beta_savage_home_editVar = StringVar()
gamma_savage_state_editVar = BooleanVar()
gamma_savage_x_editVar = IntVar()
gamma_savage_y_editVar = IntVar()
gamma_savage_home_editVar = StringVar()
delta_savage_state_editVar = BooleanVar()
delta_savage_x_editVar = IntVar()
delta_savage_y_editVar = IntVar()
delta_savage_home_editVar = StringVar()

# Грибы
alpha_fastroom_state_editVar = BooleanVar()
alpha_fastroom_x_editVar = IntVar()
alpha_fastroom_y_editVar = IntVar()
beta_fastroom_state_editVar = BooleanVar()
beta_fastroom_x_editVar = IntVar()
beta_fastroom_y_editVar = IntVar()
alpha_slowroom_state_editVar = BooleanVar()
alpha_slowroom_x_editVar = IntVar()
alpha_slowroom_y_editVar = IntVar()
beta_slowroom_state_editVar = BooleanVar()
beta_slowroom_x_editVar = IntVar()
beta_slowroom_y_editVar = IntVar()
alpha_gravroom_state_editVar = BooleanVar()
alpha_gravroom_x_editVar = IntVar()
alpha_gravroom_y_editVar = IntVar()
beta_gravroom_state_editVar = BooleanVar()
beta_gravroom_x_editVar = IntVar()
beta_gravroom_y_editVar = IntVar()

# Шаблон уровня
emptylevel = data = {
            "level": 0,

			"limited" : False,
			"limittype" : "NEXT",
			"time" :0,

			"exitCoords": [0,0],
			"spawnCoords": [60, 400],

			"CatAmountAll": 0,

            "maskFlag": False,
            "maskKind": "bless",
            "maskChance": 0.3,
            "maskCoords": [0, 0],

            "alphaPlatformFlag": False,
			"alphaPlatformCoords": [0,0,0],
			"betaPlatformFlag": False,
			"betaPlatformCoords": [0,0,0],
			"gammaPlatformFlag": False,
			"gammaPlatformCoords": [0,0,0],
			"deltaPlatformFlag": False,
			"deltaPlatformCoords": [0,0,0],
			"epsilonPlatformFlag": False,
			"epsilonPlatformCoords": [0,0,0],
			"zetaPlatformFlag": False,
			"zetaPlatformCoords": [0,0,0],
			"etaPlatformFlag": False,
			"etaPlatformCoords": [0,0,0],
			"thetaPlatformFlag": False,
			"thetaPlatformCoords": [0,0,0],
			"iotaPlatformFlag": False,
			"iotaPlatformCoords": [0,0,0],

			"alphaCatFlag": False,
			"alphaCatCoords": [0,0],
			"betaCatFlag": False,
			"betaCatCoords": [0,0],
			"gammaCatFlag": False,
			"gammaCatCoords": [0,0],
			"deltaCatFlag": False,
			"deltaCatCoords": [0,0],
			"epsilonCatFlag": False,
			"epsilonCatCoords": [0,0],
			"zetaCatFlag": False,
			"zetaCatCoords": [0,0],

			"alphaBonusFlag": False,
			"alphaBonusCoords": [0,0],
			"betaBonusFlag": False,
			"betaBonusCoords": [0,0],
			"gammaBonusFlag": False,
			"gammaBonusCoords": [0,0],
			"deltaBonusFlag": False,
			"deltaBonusCoords": [0,0],
			"epsilonBonusFlag": False,
			"epsilonBonusCoords": [0,0],
			"zetaBonusFlag": False,
			"zetaBonusCoords": [0,0],

			"alphaLadderFlag": False,
			"alphaLadderCoords": [0,0],
			"betaLadderFlag": False,
			"betaLadderCoords": [0,0],
			"gammaLadderFlag": False,
			"gammaLadderCoords": [0,0],
			"deltaLadderFlag": False,
			"deltaLadderCoords": [0,0],
			"epsilonLadderFlag": False,
			"epsilonLadderCoords": [0,0],
			"zetaLadderFlag": False,
			"zetaLadderCoords": [0,0],

			"alphaWallFlag": False,
			"alphaWallCoords": [0,0],
			"betaWallFlag": False,
			"betaWallCoords": [0,0],
			"gammaWallFlag": False,
			"gammaWallCoords": [0,0],
			"deltaWallFlag": False,
			"deltaWallCoords": [0,0],
			"epsilonWallFlag": False,
			"epsilonWallCoords": [0,0],
			"zetaWallFlag": False,
			"zetaWallCoords": [0,0],

			"alphaSavageFlag": False,
			"alphaSavageCoords": [0,0],
			"alphaSavagePlatform": "base",
			"betaSavageFlag": False,
			"betaSavageCoords": [0,0],
			"betaSavagePlatform": "base",
			"gammaSavageFlag": False,
			"gammaSavageCoords": [0,0],
			"gammaSavagePlatform": "base",
			"deltaSavageFlag": False,
			"deltaSavageCoords": [0,0],
			"deltaSavagePlatform": "base",

			"alphaFastroomFlag": False,
			"alphaFastroomCoords": [0,0],
			"betaFastroomFlag": False,
			"betaFastroomCoords": [0,0],

			"alphaSlowroomFlag": False,
			"alphaSlowroomCoords": [0,0],
			"betaSlowroomFlag": False,
			"betaSlowroomCoords": [0,0],

			"alphaGravroomFlag": False,
			"alphaGravroomCoords": [0,0],
			"betaGravroomFlag": False,
			"betaGravroomCoords": [0,0]
        }

master.common_information_show(begin=True)
master.mainloop()
