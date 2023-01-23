import pandas as pd
import string
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk


class Movies:
    def __init__(self, url, page_nb):
        self.url = url
        self.pages = page_nb

    def get_movies(self):
        inc = 1
        while inc <= self.pages:
            payload = {'pn': inc}
            try:
                r = requests.get(self.url, params=payload)

                if r.ok:

                    soup = BeautifulSoup(r.content, 'html.parser')
                    movie_data = self.get_movie_cast(soup)
                    return movie_data


            except requests.exceptions.RequestException as e:
                print('exceptie')
                SystemExit(e)

            except AttributeError as e:
                print('exceptie')
                SystemExit(e)
            inc += 1


    @staticmethod
    def get_movie_cast(soup):
        output = []

        for item in soup.find_all("ul", {'class': "cast"}):
            movie_cast = {"director": [], "actors": [], "movie_genre": [], "distributor": []}

            for item_1 in item.find_all("li"):

                for actor in item_1.find_all("a"):
                    if "Actor" in actor["title"]:
                        movie_cast["actors"].append(actor["title"][actor["title"].find(" ") + 1::])
                    elif "Regizor" in actor["title"]:
                        movie_cast["director"].append(actor["title"][actor["title"].find(" ") + 1::])
                    elif "Filme distribuite de" in actor["title"]:
                        movie_cast["distributor"].append(actor["title"][21::])
                    elif "Filme" in actor["title"]:
                        movie_cast["movie_genre"].append(actor["title"][actor["title"].find(" ") + 1::])
            output.append(movie_cast)
        titles = [item.text for item in soup.find_all('h2')]
        return dict(zip(titles, output))


class Interface:
    def __init__(self, data):

        self.data = data

        self.root = tk.Tk()
        self.root.geometry("1000x1000")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scroll_bar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.second_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        self.create_text_labels()

        self.root.mainloop()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_text_labels(self):
        row_count = 1
        for k, v in self.data.items():
            row = f"\n{k}\n\n"
            for k_1, v_1 in v.items():
                row += f"{k_1}: {' '.join(v_1)}\n"
            print(row)
            tk.Label(self.second_frame, text=row, font=("Helvetica", 14), justify="left").\
                grid(column=0, row=row_count, padx=20, sticky=tk.W)
            tk.Button(self.second_frame, text="Watched").grid(column=1, row=row_count, sticky=tk.W)
            tk.Button(self.second_frame, text="Watched").grid(column=1, row=row_count, sticky=tk.W)
            row_count += 1

if __name__ == "__main__":
    m = Movies('https://www.cinemagia.ro/filme-2022/nota/', 1)
    Interface(m.get_movies())








