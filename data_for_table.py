import csv
from player import Player

class Data_timetaken: #Singleton class

    __instance = None

    def __new__(cls, file_path):
        if cls.__instance is None:
            cls.__instance = super(Data_timetaken, cls).__new__(cls)
        return cls.__instance

    def __init__(self, file_path): 
        self.file_path = file_path
        self.db = self.load_data()

    @classmethod
    def get_instance(cls):
        if Data_timetaken.__instance is None:
            Data_timetaken()
        return Data_timetaken.__instance

    def load_data(self):
        self.db = {}

        with open("time_taken.csv", "r") as fp:
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
        wave = []
        for i in range(len(Player.get_time_taken_each_wave())//3):
            wave.append(1)
            wave.append(2)
            wave.append(3)

        self.db = {
            "wave": wave,
            "Time_taken_between_wave": Player.get_time_taken_each_wave(),
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
