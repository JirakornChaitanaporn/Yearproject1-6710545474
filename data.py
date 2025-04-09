import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as py
import seaborn as sns

class Data: #Singleton class
    def __new__(cls):
        pass

    def __init__(self):
        self.dict_data = self.load_data()
        self.instance = Data()

    @classmethod
    def get_instance(cls):
        pass

    def load_data(self):
        pass

    def save_data(self):
        pass