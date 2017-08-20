import tkinter
from src.gui_app import *


def main():
    root = tkinter.Tk()
    program = Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()