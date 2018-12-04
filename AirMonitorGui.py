import Tkinter
import argparse

from Engine import AirMonitorEngine
from ConfigReader import read_config
from Meters import create_smog_meter
from Metrics import get_aqi_color, get_2_5_color, get_10_color
from DataTargets import create_data_target


class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
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

    def initialize(self):
        self.grid()

        row_0 = 0
        row_1 = 1
        row_2 = 2
        column_0 = 0
        column_1 = 1
        column_2 = 2
        self.label7 = Tkinter.Label(self, anchor="center", bg="black")
        self.label7.grid(column=column_0, row=row_2, sticky='NESW')

        self.label8 = Tkinter.Label(self, anchor="center", bg="black")
        self.label8.grid(column=column_1, row=row_2, sticky='NESW')

        self.label9 = Tkinter.Label(self, anchor="center", bg="black")
        self.label9.grid(column=column_2, row=row_2, sticky='NESW')

        self.label = Tkinter.Label(self,anchor="center",bg="black")
        self.label.grid(column=column_0,row=row_0,sticky='NESW')

        self.label2 = Tkinter.Label(self,anchor="center",bg="black")
        self.label2.grid(column=column_1,row=row_0,sticky='NESW')

        self.label3 = Tkinter.Label(self,anchor="center",bg="black")
        self.label3.grid(column=column_2,row=row_0,sticky='NESW')

        self.label4 = Tkinter.Label(self,anchor="center",bg="black")
        self.label4.grid(column=column_0,row=row_1,sticky='NESW')

        self.label5 = Tkinter.Label(self,anchor="center",bg="black")
        self.label5.grid(column=column_1,row=row_1,sticky='NESW')

        self.label6 = Tkinter.Label(self,anchor="center",bg="black")
        self.label6.grid(column=column_2,row=row_1,sticky='NESW')

        self.grid_columnconfigure(column_0,weight=1)
        self.grid_columnconfigure(column_1,weight=1)
        self.grid_columnconfigure(column_2,weight=1)
        self.grid_rowconfigure(row_0,weight=1)
        self.grid_rowconfigure(row_1,weight=1)

    def update_result(self, smog_values):
        self.smog_values = smog_values

    def update_ui(self):
        self.engine.probe()
        result = self.smog_values
        if result is not None:
            color_2_5 = get_2_5_color(result.momentarily[0])
            color_10 = get_10_color(result.momentarily[1])
            aqi_color = get_aqi_color(result.momentarily[2])
            self.label.config(text="%.1f" % result.momentarily[0], fg=color_2_5)
            self.label2.config(text="%.1f" % result.momentarily[1], fg=color_10)
            self.label3.config(text="%.1f" % result.momentarily[2], fg=aqi_color)

            self.label7.config(text="PM 2.5", fg="white")
            self.label8.config(text="PM 10", fg="white")
            self.label9.config(text="AQI", fg="white")

            if result.average is not None:
                color_2_5_avg = get_2_5_color(result.average[0])
                color_10_avg = get_10_color(result.average[1])
                aqi_color_avg = get_aqi_color(result.average[2])
                self.label4.config(text="%.1f" % result.average[0], fg=color_2_5_avg)
                self.label5.config(text="%.1f" % result.average[1], fg=color_10_avg)
                self.label6.config(text="%.1f" % result.average[2], fg=aqi_color_avg)

        self.after(33, self.update_ui)


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title("Air Quality Monitor")
    app.after(33, app.update_ui)
    app.mainloop()
