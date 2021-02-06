import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path

def main():
    root = tk.Tk()
    window = tk.Frame(root)
    window.pack()

    button = tk.Button(root, text="Click for file dialog", 
                      command=lambda :fdialog(root))
    button.pack()

    root.mainloop()

def fdialog(root):
    filepath = fd.askopenfilename(title="test", initialdir=Path.home(), 
                                  filetypes=(("all files", "*.*"),))


    return None

if __name__ == "__main__":
    main()