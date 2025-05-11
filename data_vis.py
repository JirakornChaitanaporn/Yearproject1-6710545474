import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Datatk(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.root = parent
        self.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.orig_df = pd.read_csv('database.csv')
        self.table_df = pd.read_csv('time_taken.csv')
        
        self.create_widgets()
        self.data = None

    def create_widgets(self):
        self.header = ttk.Label(self, text="Game Statistics", font=("Arial", 20, "bold"))
        self.header.grid(row=0, column=0, pady=10)

        self.frame_dist = ttk.LabelFrame(self, text="Select Visualization")
        self.frame_dist.grid(row=1, column=0, sticky="NEWS", padx=10, pady=5)

        self.cb_dist = ttk.Combobox(self.frame_dist, state="readonly")
        self.cb_dist['values'] = (
            'Enemy survival time',
            'Enemy attack frequency',
            'Time Taken Data Table',
            'Damage taken each wave',
            'Distance traveled enemy'
        )

        self.cb_dist.bind('<<ComboboxSelected>>', self.update_dist)
        self.cb_dist.grid(row=0, column=0, padx=10, pady=10)

        self.btn_quit = ttk.Button(self, text="Quit", command=self.root.destroy)
        self.btn_quit.grid(row=2, column=0, pady=10)

        self.fig_hist = Figure(figsize=(8, 4))
        self.ax_hist = self.fig_hist.add_subplot()

        self.fig_canvas = FigureCanvasTkAgg(self.fig_hist, master=self)
        self.fig_canvas.get_tk_widget().grid(row=0, column=0, sticky="news", padx=10, pady=10)

    def update_dist(self, ev):
        dist = self.cb_dist.get()
        if dist == 'Enemy survival time':
            self.plot_survival_time()
        elif dist == 'Enemy attack frequency':
            self.plot_attack_frequency()
        elif dist == 'Time Taken Data Table':
            self.plot_time_table()
        elif dist == 'Damage taken each wave':
            self.plot_damage()
        elif dist == 'Distance traveled enemy':
            self.plot_distance()

    def plot_survival_time(self):
        self.ax_hist.clear()
        enemy_survival_times = self.orig_df[['Enemy_survival_time']].head(50)
        enemy_survival_times.index = range(1, 51)

        sns.barplot(x=enemy_survival_times.index, y='Enemy_survival_time', 
                    data=enemy_survival_times, ax=self.ax_hist)
        self.ax_hist.set_ylabel('Survival Time (seconds)')
        self.ax_hist.set_xlabel('Individual enemy')
        self.ax_hist.set_title('Enemy Survival Time')
        self.ax_hist.tick_params(axis='x', rotation=45)
        self.fig_canvas.draw()

    def plot_attack_frequency(self):
        self.ax_hist.clear()
        Enemy_attack_frequency = self.orig_df[['Enemy_attack_frequency']].head(51)
        
        self.ax_hist.plot(Enemy_attack_frequency.index, 
                         Enemy_attack_frequency['Enemy_attack_frequency'], 
                         marker='^', linestyle='-', color='b')
        
        self.ax_hist.set_yticks(range(0, 31, 1))
        self.ax_hist.set_ylabel('Attack Count')
        self.ax_hist.set_xticks(range(0, 51, 1))
        self.ax_hist.set_xlabel('Enemy Index')
        self.ax_hist.set_title('Enemy Successful Attack Frequency')
        self.ax_hist.grid(axis='y', linestyle='--')
        self.fig_canvas.draw()

    def plot_time_table(self):
        self.ax_hist.clear()
        self.ax_hist.axis('off')
        self.ax_hist.set_frame_on(False)

        overall_mean_wave3 = self.table_df['Time_taken_between_wave'].mean()

        table_data = [
            [1, self.table_df.iloc[0]['Time_taken_between_wave'], overall_mean_wave3],
            [2, self.table_df.iloc[1]['Time_taken_between_wave'], overall_mean_wave3],
            [3, self.table_df.iloc[2]['Time_taken_between_wave'], overall_mean_wave3]
        ]

        table = self.ax_hist.table(cellText=table_data, 
                                colLabels=['Wave Num', 'Mean of Time Taken Each Wave', 'Overall Mean'],
                                cellLoc='center', 
                                loc='center')

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        self.fig_canvas.draw()



    def plot_damage(self):
        self.ax_hist.clear()
        Damage_taken_each_wave = self.orig_df[['Damage_taken_each_wave']]
        
        sns.boxplot(y=Damage_taken_each_wave['Damage_taken_each_wave'], ax=self.ax_hist)
        
        self.ax_hist.set_yticks(range(0, 161, 20))
        self.ax_hist.set_ylabel('Damage taken')
        self.ax_hist.set_title('Damage taken each wave')
        self.fig_canvas.draw()

    def plot_distance(self):
        self.ax_hist.clear()
        Distance_traveled_enemy = self.orig_df[['Distance_traveled_enemy']].head(51)
        
        self.ax_hist.scatter(Distance_traveled_enemy.index, 
                           Distance_traveled_enemy['Distance_traveled_enemy'])
        
        self.ax_hist.set_xticks(range(0, 51, 1))
        self.ax_hist.set_yticks(range(0, 12001, 1000))
        self.ax_hist.set_ylabel('Distance')
        self.ax_hist.set_title('Distance traveled by enemy')
        self.fig_canvas.draw()
