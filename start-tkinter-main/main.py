#!/usr/bin/env python3

from os.path import basename, splitext
from os.path import exists
import tkinter as tk
import datetime

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if "textvariable" not in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Foo"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.btnQuit = tk.Button(self, text="Quit", command=self.quit)
        self.lblMain = tk.Label(self, text="Color mishma")
        self.lblMain.bind("<Button-1>", self.time_update_handler)
        self.time_update()

        self.frameR = tk.Frame(self)
        self.frameG = tk.Frame(self)
        self.frameB = tk.Frame(self)
        self.frameMem = tk.Frame(self)

        self.lblR = tk.Label(self.frameR, text= "R", width=2)
        self.lblG = tk.Label(self.frameG, text= "G", width=2)
        self.lblB = tk.Label(self.frameB, text= "B", width=2)
        self.varR = tk.IntVar()
        self.varR.trace_add("write", self.update_color)
        self.varG = tk.IntVar()
        self.varG.trace_add("write", self.update_color)
        self.varB = tk.IntVar()
        self.varB.trace_add("write", self.update_color)
        self.scaleR = tk.Scale(self.frameR, from_=0, to=255, orient=tk.HORIZONTAL, length=200, variable=self.varR)
        self.scaleG = tk.Scale(self.frameG,from_=0, to=255, orient=tk.HORIZONTAL, length=200, variable=self.varG)
        self.scaleB = tk.Scale(self.frameB,from_=0, to=255, orient=tk.HORIZONTAL, length=200, variable=self.varB)
        
        self.entryR = tk.Entry(self.frameR,textvariable=self.varR, width=3)
        self.entryG = tk.Entry(self.frameG,textvariable=self.varG, width=3)
        self.entryB = tk.Entry(self.frameB,textvariable=self.varB, width=3)
        

        self.canvas = tk.Canvas(self, background="#ff5588",width=350)
        self.canvas.bind("<Button-1>", self.clickHandler)



        self.lblMain.pack()
        self.btnQuit.pack()

        self.frameR.pack(side=tk.TOP)
        self.frameG.pack(side=tk.TOP)
        self.frameB.pack(side=tk.TOP)

        self.lblR.pack(side=tk.LEFT, anchor=tk.S)
        self.lblG.pack(side=tk.LEFT, anchor=tk.S)
        self.lblB.pack(side=tk.LEFT, anchor=tk.S)

        self.entryR.pack(side=tk.LEFT, anchor=tk.S)
        self.entryG.pack(side=tk.LEFT, anchor=tk.S)
        self.entryB.pack(side=tk.LEFT, anchor=tk.S)

        self.scaleR.pack(side=tk.LEFT, anchor=tk.S)
        self.scaleG.pack(side=tk.LEFT, anchor=tk.S)
        self.scaleB.pack(side=tk.LEFT, anchor=tk.S)

        self.canvas.pack(side=tk.TOP, fill="both")
        self.frameMem.pack(side=tk.TOP, fill="both")

        self.canvaslist = []
        for row in range(3):
            for col in range(7):
                canvas = tk.Canvas(self.frameMem, width=50, height=50, bg="#12abc3")
                canvas.bind("<Button-1>", self.clickHandler)
                canvas.grid(row=row, column=col)
                self.canvaslist.append(canvas)
        
        self.colorLoad()



    
    def clickHandler(self, event):
        if self.cget("cursor") != "pencil":
            self.config(cursor="pencil")
            self.copyColor = event.widget.cget("background")
        else:
            self.config(cursor="")
            if event.widget is self.canvas:
                r = int(self.copyColor[1:3], 16)
                g = int(self.copyColor[3:5], 16)
                b = int(self.copyColor[5:], 16)
                self.varR.set(r)
                self.varG.set(g)
                self.varB.set(b)
            event.widget.config(background = self.copyColor)

    def update_color(self, event=None, neco=None, dalsi=None):
        r = self.scaleR.get()
        g = self.scaleG.get()
        b = self.scaleB.get()
        self.canvas.config(background=f"#{r:02X}{g:02X}{b:02X}")

    def time_update(self):
        time = datetime.datetime.now().replace(microsecond=0)
        self.lblMain.configure(text = time)
        self.lblMain.after(1000, self.time_update)

    def time_update_handler(self, 
                            event):
        self.lblMain.after_cancel()

    def colorSave(self):
        with open("colors.txt", "w") as f:
            f.write(self.canvas.cget("background")+"\n")
            for c in self.canvaslist:
                f.write(c.cget("background")+"\n")
    
    def colorLoad(self):
        if not exists("colors.txt"):
            return
        with open("colors.txt", "r") as f:
            try:
                color = f.readline().strip()
                self.canvas.config(background=color)
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:], 16)
                self.varR.set(r)
                self.varG.set(g)
                self.varB.set(b)
                for canvas in self.canvaslist:
                    canvas.config(background=f.readline().strip())
            except (ValueError, tk.TclError):
                pass

    def about(self):
        window = About(self)
        window.grab_set()

    def quit(self, event=None):
        self.colorSave()
        super().quit()

    def destroy(self):
        super().destroy()


app = Application()
app.mainloop()