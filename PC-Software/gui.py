from tkinter import *


class ReadingMeter:
    def __init__(self, x, y, name,unit):
        self.reading = DoubleVar()
        var_name = Label( text = name,font =("consolas", 13, "bold"))
        var_unit = Label( text = unit,font =("consolas", 13, "bold"))
        self.display = Label(textvariable=self.reading, relief = "solid", borderwidth = 0.5, font = "Times 13")  # we need this Label as a variable
        self.display.place(x=x+85, y=y, width = 100)
        var_name.place(x=x, y=y)
        var_unit.place(x = x+200, y = y )

class DateTime:
    def __init__(self, x, y, name):
        self.reading = DoubleVar()
        var_name = Label( text = name,font =("consolas", 13, "bold"))
        self.display = Label(textvariable=self.reading, font =("consolas", 13, "bold"))  # we need this Label as a variable
        self.display.place(x=x+60, y=y, width = 100)
        var_name.place(x=x, y=y)