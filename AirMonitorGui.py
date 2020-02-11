import tkinter
import argparse

from Engine import AirMonitorEngine
from ConfigReader import read_config
from SmogMeters import create_smog_meter
from Metrics import get_aqi_color, get_2_5_color, get_10_color
from DataTargets import create_data_target

class AirMonitorGui(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self._labels = []

        self.initialize()

        parser = argparse.ArgumentParser(description='Air Monitor')
        parser.add_argument("location")

        arguments = parser.parse_args()
        config = read_config(arguments.location)
        self.engine = AirMonitorEngine(create_smog_meter(config["meter"], config["com_port"]),
                                       create_data_target(config["target"], config["key"]),
                                       self.update_result,
                                       config["period_minutes"])
        self.smog_values = None

    def add_label(self, col, row, font):
        label = tkinter.Label(self, anchor="center", bg="black", font=font)
        label.grid(column=col, row=row, sticky='NESW')
        self._labels.append(label)

        return label

    def initialize(self):
        self.grid()

        row_0 = 0
        row_1 = 1
        row_2 = 2
        column_0 = 0
        column_1 = 1
        column_2 = 2
        text_font = ("Courier",50)

        self.label_aqi = self.add_label(0, 0, text_font)
        self.label_pm25 = self.add_label(1, 0, text_font)
        self.label_pm10 = self.add_label(2, 0, text_font)
        self.label_aqi_now = self.add_label(0, 1, text_font)
        self.label_pm25_now = self.add_label(1, 1, text_font)
        self.label_pm10_now = self.add_label(2, 1, text_font)
        self.label_aqi_avg = self.add_label(0, 2, text_font)
        self.label_pm25_avg = self.add_label(1, 2, text_font)
        self.label_pm10_avg = self.add_label(2, 2, text_font)

        self.grid_columnconfigure(column_0, weight=1)
        self.grid_columnconfigure(column_1, weight=1)
        self.grid_columnconfigure(column_2, weight=1)
        self.grid_rowconfigure(row_0, weight=1)
        self.grid_rowconfigure(row_1, weight=1)
        self.grid_rowconfigure(row_2, weight=1)

    def update_result(self, smog_values):
        self.smog_values = smog_values

    def update_ui(self):        
        parent = self._labels[0].master
        window_width = parent.winfo_width()
        window_height = parent.winfo_height()

        min_h = window_height // 5
        min_w = window_width // 15

        font_size = min(min_h - 10 , min_w - 10)
        font = ("Courier",max(50, font_size))

        self.engine.probe()
        result = self.smog_values
        if result is not None:
            color_2_5 = get_2_5_color(result.momentarily[0])
            color_10 = get_10_color(result.momentarily[1])
            aqi_color = get_aqi_color(result.momentarily[2])
            self.label_aqi_now.config(text="%d" % result.momentarily[2], fg=aqi_color, font=font)
            self.label_pm25_now.config(text="%.1f" % result.momentarily[0], fg=color_2_5, font=font)
            self.label_pm10_now.config(text="%.1f" % result.momentarily[1], fg=color_10, font=font)

            self.label_aqi.config(text=" AQI ", fg="white", font=font)
            self.label_pm25.config(text=" PM 2.5 ", fg="white", font=font)
            self.label_pm10.config(text=" PM 10 ", fg="white", font=font)

            if result.average is not None:
                color_2_5_avg = get_2_5_color(result.average[0])
                color_10_avg = get_10_color(result.average[1])
                aqi_color_avg = get_aqi_color(result.average[2])
                self.label_aqi_avg.config(text="%d" % result.average[2], fg=aqi_color_avg, font=font)
                self.label_pm25_avg.config(text="%.1f" % result.average[0], fg=color_2_5_avg, font=font)
                self.label_pm10_avg.config(text="%.1f" % result.average[1], fg=color_10_avg, font=font)

        self.after(33, self.update_ui)


if __name__ == "__main__":
    app = AirMonitorGui()
    app.title("Air Quality Monitor")
    app.after(33, app.update_ui)
    app.mainloop()
