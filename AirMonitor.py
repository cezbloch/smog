from Metrics import get_2_5_color, get_10_color
import win32api
import win32con
import time
import ConfigParser
import argparse
from array import array
from Tkinter import *

from Engine import AirMonitorEngine
from ConfigReader import read_config
from SmogMeters import create_smog_meter
from DataTargets import create_data_target


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


class TextLabel(Frame):
    def __init__(self, master, width=0, height=0, **kwargs):
        self.width = width
        self.height = height

        Frame.__init__(self, master, width=self.width, height=self.height)
        self.text_widget = Label(self, **kwargs)
        self.text_widget.pack(expand=YES, fill=BOTH)
        self.grid_propagate(False)
        self.pack_propagate(False)
        self.pack()

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

    def grid(self, *args, **kwargs):
        Frame.grid(self, *args, **kwargs)
        self.grid_propagate(False)


class WindowDraggable:
    def __init__(self, label):
        self.label = label
        label.bind('<ButtonPress-1>', self.StartMove)
        label.bind('<ButtonRelease-1>', self.StopMove)
        label.bind('<B1-Motion>', self.OnMotion)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        x = (event.x_root - self.x - self.label.winfo_rootx() + self.label.winfo_rootx())
        y = (event.y_root - self.y - self.label.winfo_rooty() + self.label.winfo_rooty())
        self.label.winfo_toplevel().geometry("+%s+%s" % (x, y))


class AirMonitorApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        parser = argparse.ArgumentParser(description='Air Monitor')
        parser.add_argument("location")

        arguments = parser.parse_args()
        config = read_config(arguments.location)
        self.engine = AirMonitorEngine(create_smog_meter(config["meter"], config["com_port"]),
                                       create_data_target(config["target"], config["key"]),
                                       self.update_result,
                                       config["period_minutes"])
        self.smog_values = None

        self.configFileName = 'AirMonitor.ini'
        self.appConfig = ConfigParser.ConfigParser()
        if not ('Meter' in self.appConfig.sections()):
            self.appConfig.add_section('Meter')
        self.appConfig.set('Meter','sensorX', 0)
        self.appConfig.set('Meter','sensorY', 0)
        self.appConfig.set('Meter','windowX', 0)
        self.appConfig.set('Meter','windowY', 0)
        self.appConfig.read(self.configFileName)

        self.overrideredirect(True)
        self.wm_attributes("-topmost", 1)

        mainFrame = Frame(self)

        mainFrame.columnconfigure(0, pad=3)
        mainFrame.columnconfigure(1, pad=3)
        mainFrame.columnconfigure(2, pad=3)
        mainFrame.columnconfigure(3, pad=3)

        mainFrame.rowconfigure(0, pad=3)
        mainFrame.rowconfigure(1, pad=3)
        #mainFrame.rowconfigure(2, pad=3)
        #mainFrame.rowconfigure(3, pad=3)
        #mainFrame.rowconfigure(4, pad=3)
        #mainFrame.rowconfigure(5, pad=3)

        titleLabel = Label(mainFrame, text='Air Monitor', anchor=W, bg="blue", fg="white")
        closeButton = Button(titleLabel, text="X",  bg="blue", fg="white", command=self.close)
        titleLabel.grid(row = 0, column = 0, columnspan = 4, sticky=W+E+S+N)
        closeButton.pack(side=RIGHT)

        WindowDraggable(titleLabel)

        self.canvas = Canvas(mainFrame, height=150, width=250)
        #self.canvas.grid(row = 1, column = 0, columnspan = 2, sticky=W+E)
        self.rect = self.canvas.create_rectangle(0, 0, 150, 250, fill = "black")

        self.pm2_5Label = TextLabel(mainFrame,  width=400, height=100, text='00 PM2.5', anchor=W, bd=1, justify=CENTER, font=("Helvetica", 50), bg="black" ,fg="green" )
        self.pm2_5Label.grid(row = 1, column = 0, columnspan = 2, sticky=W+E+S+N)
        self.pm2_5_average_label = TextLabel(mainFrame,  width=400, height=100, text='Avg -', anchor=W, bd=1, justify=CENTER, font=("Helvetica", 50), bg="black" ,fg="green" )
        self.pm2_5_average_label.grid(row = 1, column = 2, columnspan = 2, sticky=W+E+S+N)
        self.pm10Label = TextLabel(mainFrame,  width=400, height=100, text='00 PM10', anchor=W, bd=1, justify=CENTER, font=("Helvetica", 50), bg="black" ,fg="green" )
        self.pm10Label.grid(row = 2, column = 0, columnspan = 2, sticky=W+E+S+N)
        self.pm10_average_label = TextLabel(mainFrame,  width=400, height=100, text='Avg -', anchor=W, bd=1, justify=CENTER, font=("Helvetica", 50), bg="black" ,fg="green" )
        self.pm10_average_label.grid(row = 2, column = 2, columnspan = 2, sticky=W+E+S+N)


        mainFrame.pack()

        windowX = self.appConfig.getint('Meter', 'windowX')
        windowY = self.appConfig.getint('Meter', 'windowY')
        if windowX == 0 and windowY == 0:
            self.centerWindow()
        else:
            self.setWindowPosition(windowX, windowY)

        self.do_blink = False
        self.maxX = self.appConfig.getint('Meter', 'sensorX')
        self.maxY = self.appConfig.getint('Meter', 'sensorY')
        self.maxSample = 0
        self.r = array('h')

    def close(self):
        (x, y, w, h) = self.getWindowPosition()
        self.appConfig.set('Meter','windowX', x)
        self.appConfig.set('Meter','windowY', y)
        self.appConfig.set('Meter','sensorX', self.maxX)
        self.appConfig.set('Meter','sensorY', self.maxY)

        configfile = open(self.configFileName, 'w')
        self.appConfig.write(configfile)

        self.destroy()

    def setWindowPosition(self, x, y):
        self.update_idletasks()
        rootsize = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        self.geometry("%dx%d+%d+%d" % (rootsize + (x, y)))

    def getWindowPosition(self):
        g = re.split('x|\+', self.geometry())
        w = int(g[0])
        h = int(g[1])
        x = int(g[2])
        y = int(g[3])
        return (x, y, w, h)

    def centerWindow(self):
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        rootsize = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = w/2 - rootsize[0]/2
        y = h/2 - rootsize[1]/2
        self.setWindowPosition(x, y)

    def moveMouse(self, startX, startY, stopX, stopY, steps = 0):
        if steps == 0:
            steps = min(abs(startX-stopX), abs(startY-stopY))

        for i in range(steps):
            y = (startY + (i+1)*(stopY-startY)/float(steps))
            x = (startX + (i+1)*(stopX-startX)/float(steps))
            win32api.SetCursorPos((int(x), int(y)))
            time.sleep(0.005)

    def update_result(self, smog_values):
        self.smog_values = smog_values

    def update_ui(self):
        self.engine.probe()
        result = self.smog_values
        if result is not None:
            color_2_5 = get_2_5_color(result.momentarily[0])
            color_10 = get_10_color(result.momentarily[1])
            self.pm2_5Label.text_widget.config(text="%.1f PM 2.5" % result.momentarily[0], fg=color_2_5)
            self.pm10Label.text_widget.config(text="%.1f PM 10" % result.momentarily[1], fg=color_10)

            if result.average is not None:
                color_2_5_avg = get_2_5_color(result.average[0])
                color_10_avg = get_10_color(result.average[1])
                self.pm2_5_average_label.text_widget.config(text="Avg %.1f" % result.average[0], fg=color_2_5_avg)
                self.pm10_average_label.text_widget.config(text="Avg %.1f" % result.average[1], fg=color_10_avg)

        self.after(33, self.update_ui)


def main():
    root = AirMonitorApp()
    root.after(33, root.update_ui)
    mainloop()


if __name__ == "__main__":
    main()

