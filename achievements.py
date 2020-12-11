import json

achievementsNames = {
    "pacifist": {
            "name": "Пацифист",
            "description": "Не убить за игру ни одного дикаря"
        },
    "nonbeliever": {
            "name": "Неверующий",
            "description": "Не умереть ни разу"
        },
    "florist": {
            "name": "Флорист",
            "description": "Полить все цветочки в игре"
        },
    "bloodmary": {
            "name": "Кровавая Мери",
            "description": "Убить всех дикарей в игре"
        },
    "maximalist": {
            "name": "Максималист",
            "description": "Собрать все очки"
        },
    "end": {
            "name": "Конец?",
            "description": "Пройти игру"
        }
}

emptydata = {
    "islevelcyclecompleted": False,
    "recordscore": 0,
    "achievements": {
        "pacifist": False,
        "nonbeliever": False,
        "florist": False,
        "bloodmary": False,
        "maximalist": False,
        "end": False
    },
    "killedsavages": 0,
    "wateredflowers": 0,
    "lastlevel": 1,
    "lastlives": 5,
    "lastscore": 0
}

class PlayerData:

    def __init__(self):
        try:
            self.file = open("player.json", "r", encoding="utf-8")
        except FileNotFoundError:
            self.file = open("player.json", "a+", encoding="utf-8")
        try:
            self.data = json.load(self.file)
        except json.decoder.JSONDecodeError:
            print("Create player.json")
            self.eraseData()

    def writeData(self):
        with open("player.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.data, indent=4, ensure_ascii=False))

    def loadData(self):
        self.file = open("player.json", "r", encoding="utf-8")
        self.data = json.load(self.file)

    def eraseData(self):
        with open("player.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(emptydata, indent=4, ensure_ascii=False))
        self.loadData()
