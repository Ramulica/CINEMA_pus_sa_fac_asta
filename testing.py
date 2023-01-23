import tkinter as tk
import os
from PIL import Image, ImageTk


root = tk.Tk()
root.geometry("1000x1000")

main_path = os.getcwd()
os.chdir("movie_images")
movie_image = ImageTk.PhotoImage(file=f"test.jpg")
tk.Label(root, image=movie_image).pack()


root.mainloop()
