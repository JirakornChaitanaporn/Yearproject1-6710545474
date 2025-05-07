import csv
from enemies import enemies
from player import Player

class Data: #Singleton class

    __instance = None

    def __new__(cls, file_path):
        if cls.__instance is None:
            cls.__instance = super(Data, cls).__new__(cls)
        return cls.__instance

    def __init__(self, file_path): 
        self.file_path = file_path
        self.db = self.load_data()

    @classmethod
    def get_instance(cls):
        if Data.__instance is None:
            Data()
        return Data.__instance

    def load_data(self):
        self.db = {}

        with open("database.csv", "r") as fp:
            reader = csv.reader(fp)
            headers = next(reader)
            for header in headers:
                self.db[header] = []

            for row in reader:
                for i, value in enumerate(row):
                    if i < len(headers):
                        self.db[headers[i]].append(value)
        
        return self.db

    def save_data(self):
        self.db = {
            "Enemy_survival_time": enemies.get_survive_time(),#histogram
            "Enemy_attack_frequency": enemies.get_attack_count_list(),  #bar
            "Damage_taken_each_wave": Player.get_damage_taken(),#box
            "Distance_traveled_enemy": enemies.get_distance_travelled_list() #scatter
        }

        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.db.keys())
            max_length = max(len(v) for v in self.db.values())
            for i in range(max_length):
                row = []
                for key in self.db.keys():
                    row.append(str(self.db[key][i]) if i < len(self.db[key]) else "")
                writer.writerow(row)
