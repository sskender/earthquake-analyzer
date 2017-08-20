from tkinter import *


class DisplayFrame():
    
    def __init__(self,window,position,size):
        self.window = window
        self.placeX = position[0]; self.placeY = position[1]
        self.sizeX  = size[0];     self.sizeY  = size[1]
        self.create_window()
        
    def create_window(self):
        """ main frame and location """
        self.display = Frame(self.window,relief=GROOVE,width=self.sizeX,height=self.sizeY,bd=1)
        self.display.place(x=self.placeX,y=self.placeY)

        """ canvas with frame for text and scrollbar """        
        self.canvas = Canvas(self.display)
        self.frameInDisplay = Frame(self.display)
        self.scroll = Scrollbar(self.display,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)

        """ place scrollbar and frame """        
        self.scroll.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.frameInDisplay,anchor="nw")

        """ call function to do actual scroll """
        self.frameInDisplay.bind("<Configure>",self.scroll_window)

    def scroll_window(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=self.sizeX,height=self.sizeY)