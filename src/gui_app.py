from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog

from gui_frame import DisplayFrame
from urls import *
import downloader
import quake_class as q



class Application():
    
    def __init__(self,window):
        self.window = window
        self.quakes_list = list()
      
        
        # <main window>
        self.window.option_add("*font",("verdana",10,"bold"))
        self.window.title("Earthquake Analyzer 1.0 BETA")
        self.window.geometry("1180x700")
        self.window.resizable(width=FALSE,height=FALSE)
        # </main window>
        

        # <main menu>
        self.mainMenu = Menu(self.window)
        self.window.config(menu=self.mainMenu)
        
        # file menu
        self.fileMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="Download Data",menu=self.fileMenu)
        # file menu options
        self.fileMenu.add_command(label="Past Hour",command=lambda: self.triggerDownload(URLS["hour"]))
        self.fileMenu.add_command(label="Past Day",command=lambda: self.triggerDownload(URLS["day"]))
        self.fileMenu.add_command(label="Past 7 Days",command=lambda: self.triggerDownload(URLS["7days"]))
        self.fileMenu.add_command(label="Past 30 Days",command=lambda: self.triggerDownload(URLS["30days"]))
        self.fileMenu.add_command(label="Exit",command=lambda: exit() )

        # view menu
        self.viewMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="View",menu=self.viewMenu)        
        # view menu options
        self.viewMenu.add_command(label="Basic info",command=lambda: self.viewBasic())
        self.viewMenu.add_command(label="People reported",command=lambda: self.viewFelt())
        self.viewMenu.add_command(label="Tsunami alert",command=lambda: self.viewTsunami())
        self.viewMenu.add_command(label="Color alert",command=lambda: self.viewColor())

        # filter menu
        self.filterMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="Filter",menu=self.filterMenu)
        # filter menu options
        self.filterMenu.add_command(label="Stronger than",command=lambda: self.filterMagnitude())
        self.filterMenu.add_command(label="Deeper than",command=lambda: self.filterDepth())
        self.filterMenu.add_command(label="Reported more than",command=lambda: self.filterFelt())
        self.filterMenu.add_command(label="Filter location",command=lambda: self.filterLocation())
        self.filterMenu.add_command(label="Triggered tsunami",command=lambda: self.filterTsunami())
        self.filterMenu.add_command(label="Strong (orange,red alert)",command=lambda: self.filterStrong())
        
        # help menu
        self.helpMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="Help",menu=self.helpMenu)
        # help menu options
        self.helpMenu.add_command(label="About",command=lambda: tkinter.messagebox.showinfo("About","Earthquake Analyzer\nVERSION: 1.0 BETA\n2016"))
        # </main menu>

        
        # <frames>
        Label(self.window,text="GENERAL INFO").place(x=20,y=5)
        self.basicFrame = DisplayFrame(self.window,(10,25),(650,630))
        
        Label(self.window,text="PEOPLE FELT").place(x=700,y=5)
        self.feltFrame = DisplayFrame(self.window,(700,25),(430,190))
        
        Label(self.window,text="TRIGGERED TSUNAMI").place(x=700,y=225)
        self.tsunamiFrame = DisplayFrame(self.window,(700,245),(430,190))        
        
        Label(self.window,text="ALERT COLOR").place(x=700,y=445)
        self.colorFrame = DisplayFrame(self.window,(700,465),(430,190))
        # </frames>


        # <footer>
        self.quakes_number_var = StringVar()
        self.quakes_number_var.set(str(len(self.quakes_list)))
        Label(self.window,text="TOTAL EARTHQUAKES: ").place(x=40,y=670)
        Label(self.window,textvariable=self.quakes_number_var).place(x=215,y=670)
        # </footer>
        
            
    # <get data>
    def triggerDownload(self,url):
        self.quakes_list[:] = []
        data_web  = downloader.getData(url)
        data_json = downloader.getJson(data_web)

        if data_json != None:
            for item in data_json["features"]:
                quake = q.Quake(item)
                self.quakes_list.append(quake)

        self.refreshFrames()
    # </get data>


    # <additional views>
    def refreshFrames(self):
        for widget in self.basicFrame.frameInDisplay.winfo_children():
            widget.destroy()
        for widget in self.feltFrame.frameInDisplay.winfo_children():
            widget.destroy()
        for widget in self.tsunamiFrame.frameInDisplay.winfo_children():
            widget.destroy()
        for widget in self.colorFrame.frameInDisplay.winfo_children():
            widget.destroy()
        self.quakes_number_var.set(str(len(self.quakes_list)))
        
    def viewBasic(self):
        space = "\n{}\n".format("- " * 52); y = 0
        for quake in self.quakes_list:
            temp1 = "LOCATION:\t{}".format(quake.place)
            temp2 = "MAGNITUDE:\t{}\t\tDepth:\t\t{} KM" .format(quake.magnitude,quake.depth)
            temp3 = "Longitude:\t{0:.5f}\tLatitude:\t\t{1:.5f}" .format(quake.longitude,quake.latitude)
            Label(self.basicFrame.frameInDisplay,text=temp1,fg="green").grid(row=y,column=0,sticky=W); y += 1
            Label(self.basicFrame.frameInDisplay,text=temp2,fg="red").grid(row=y,column=0,sticky=W);   y += 1
            Label(self.basicFrame.frameInDisplay,text=temp3,fg="blue").grid(row=y,column=0,sticky=W);  y += 1
            Label(self.basicFrame.frameInDisplay,text=space,fg="black").grid(row=y,column=0,sticky=W); y += 1                    
                    
    def viewFelt(self):
        y = 0
        for quake in self.quakes_list:
            if quake.felt != None and quake.felt != 0:
                Label(self.feltFrame.frameInDisplay,text="LOCATION:   {}".format(" ".join(quake.place.split(" ")[3:])),fg="green").grid(row=y,column=1,sticky=W); y+=1
                Label(self.feltFrame.frameInDisplay,text="REPORTED:   {}\n".format(quake.felt),fg="orange").grid(row=y,column=1,sticky=W);                        y+=1

    def viewTsunami(self):
        y = 0
        for quake in self.quakes_list:
            if quake.tsunami == 1:
                Label(self.tsunamiFrame.frameInDisplay,text=quake.place,fg="blue").grid(row=y,column=1,sticky=W)
                y+=1
        
    def viewColor(self):
        y = 0
        for quake in self.quakes_list:
            if quake.alert in ["green","yellow","orange","red"]:
                Label(self.colorFrame.frameInDisplay,text=quake.place,fg=quake.alert).grid(row=y,column=1,sticky=W)
                y+=1
    # </additional views>


    # <filter>
    def filterMagnitude(self):
        response = tkinter.simpledialog.askfloat("Filter", "Filter magnitude\nstronger than:")
        if response == None: return
        self.quakes_list = [item for item in self.quakes_list if item.magnitude != None and float(item.magnitude) > response]
        self.refreshFrames()

    def filterDepth(self):
        response = tkinter.simpledialog.askfloat("Filter", "Filter deeper than:")
        if response == None: return
        self.quakes_list = [item for item in self.quakes_list if item.depth != None and float(item.depth) > response]
        self.refreshFrames()
        
    def filterFelt(self):
        response = tkinter.simpledialog.askinteger("Filter", "Filter reported\nmore than n times:")
        if response == None: return
        self.quakes_list = [item for item in self.quakes_list if item.felt != None and item.felt > response]
        self.refreshFrames()

    def filterLocation(self):
        response = tkinter.simpledialog.askstring("Filter", "Filter location name:")
        if response == None: return
        self.quakes_list = [item for item in self.quakes_list if response in item.place]
        self.refreshFrames()

    def filterTsunami(self):
        self.quakes_list = [item for item in self.quakes_list if item.tsunami == 1]
        self.refreshFrames()

    def filterStrong(self):
        self.quakes_list = [item for item in self.quakes_list if item.alert == "orange" or item.alert == "red"]
        self.refreshFrames()
    # </filter>