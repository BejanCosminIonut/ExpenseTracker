from tkinter import *
from setupWindow import SetupWindow

root = Tk()
root.geometry("600x400")
root.title("ExpenseTracker")
root.resizable(False, False)
window = SetupWindow(root)

def main():
    root.mainloop()

if __name__ == '__main__':
    main()