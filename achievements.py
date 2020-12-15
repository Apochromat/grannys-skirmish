import json

achievementsNames = {
    "pacifist": {
            "name": "Пацифист",
            "description": "Не убить за игру ни одного дикаря"
        },
    "nonbeliever": {
            "name": "Неверующий",
            "description": "Не умереть за всю игру ни разу"
        },
    "florist": {
            "name": "Флорист",
            "description": "Полить все цветочки"
        },
    "bloodmary": {
            "name": "Кровавая Мери",
            "description": "Убить всех дикарей"
        },
    "masquer": {
            "name": "Масочный режим",
            "description": "Найти все маски"
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
        "masquer": False,
        "end": False
    },
    "masks": {
        "bless": False,
        "joy": False,
        "luck": False,
        "rage": False
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
            self.erase_data()

    def write_data(self):
        with open("player.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.data, indent=4, ensure_ascii=False))

    def load_data(self):
        self.file = open("player.json", "r", encoding="utf-8")
        self.data = json.load(self.file)

    def erase_data(self):
        with open("player.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(emptydata, indent=4, ensure_ascii=False))
        self.load_data()
