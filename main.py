import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import os
from PIL import ImageTk
import string


class Movies:
    def __init__(self, url, page_nb):
        self.url = url
        self.pages = page_nb

    def get_movies(self):
        inc = 1
        movie_data = []
        while inc <= self.pages:
            payload = {'pn': inc}
            try:
                r = requests.get(self.url, params=payload)

                if r.ok:

                    soup = BeautifulSoup(r.content, 'html.parser')
                    movie_data += [self.get_movie_cast(soup)]

            except requests.exceptions.RequestException as e:
                print('exceptie')
                SystemExit(e)

            except AttributeError as e:
                print('exceptie')
                SystemExit(e)
            inc += 1

        return movie_data

    @staticmethod
    def get_movie_cast(soup):
        output = []

        for item in soup.find_all("ul", {'class': "cast"}):
            movie_cast = {"director": [], "actors": [], "movie_genre": [], "distributor": [], "image_url": []}

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

        all_links = []
        for movie in soup.find_all("li", {"class": "movie"}):
            links = []
            image_tags = movie.find_all('img')
            for image_tag in image_tags:
                links.append(image_tag['src'])
            all_links.append(links[0])

        for i, item in enumerate(output):
            item["image_url"].append(all_links[i])

        titles = [item.text for item in soup.find_all('h2')]

        return dict(zip(titles, output))


class Interface:
    def __init__(self, data):

        self.window_refresh_heck = 801
        self.data = data
        self.row_count = 2
        self.pg_count = 2
        self.searched_txt = ""

        self.root = tk.Tk()
        self.root.geometry("1130x800")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scroll_bar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scroll_bar.set, bg="#666666")
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.second_frame = tk.Frame(self.canvas)
        self.second_frame.configure(bg="#666666")
        self.canvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        self.title_frame()

        self.textbox = tk.Entry()
        self.search_frame()

        self.create_text_labels({**self.data[0], **self.data[1], **self.data[2]}, False)

        self.root.mainloop()

    def get_entry_text(self):
        self.row_count = 2
        self.pg_count = 0
        self.searched_txt = self.textbox.get()
        self.second_frame.destroy()

        self.second_frame = tk.Frame(self.canvas)
        self.second_frame.configure(bg="#666666")
        self.canvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        self.title_frame()
        self.search_frame()

        self.filter_search_movies()
        self.row_count = 2
        self.pg_count = 0

    def title_frame(self):

        title_frame = tk.Frame(self.second_frame)
        title_frame.configure(bg="#666666")
        title_frame.grid(row=0)
        tk.Label(title_frame, text="CINEMA pus sa fac asta", font=("Arial", 20, "bold"), bg="#666666", fg="white",
                 width=63).pack(fill=tk.X, ipadx=20, ipady=20)

    def search_frame(self):

        usable_frame = tk.Frame(self.second_frame)
        usable_frame.configure(bg="#666666")
        usable_frame.grid(row=1)
        tk.Label(usable_frame, text=f"Search movie:", anchor="e", bg="#666666", width=75,
                 fg="white").grid(row=0, column=0)

        self.textbox = tk.Entry(usable_frame, width=75)
        self.textbox.grid(row=0, column=1)

        search_button = tk.Button(usable_frame, text="Search", command=lambda: self.get_entry_text())
        search_button.grid(row=0, column=2, padx=10, pady=10)

    def filter_search_movies(self):
        searched_movie = {}
        for item in self.data:

            for k, v in item.items():
                if str.lower(self.searched_txt) in str.lower(k):
                    searched_movie[k] = v
        print(searched_movie)
        self.create_text_labels(searched_movie, True)


    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_text_labels(self, data, if_searched):

        bg_color = ["#E7D39C", "#CCB677"]
        bg_color_counter = 0
        for k, v in data.items():
            usable_frame = tk.Frame(self.second_frame)
            usable_frame.configure(bg=bg_color[bg_color_counter])
            usable_frame.grid(row=self.row_count)
            row = f"\n{k}\n\n"
            for k_1, v_1 in v.items():
                if k_1 != "image_url":
                    row += f"{k_1}: {', '.join(v_1)}\n"
                else:
                    main_path = os.getcwd()
                    os.chdir("movie_images")
                    self.download_image(v_1[0], f"{self.row_count}_image.png")
                    movie_image = ImageTk.PhotoImage(file=f"{self.row_count}_image.png")
                    movie_photo = tk.Label(usable_frame, image=movie_image, bg=bg_color[bg_color_counter])
                    movie_photo.photo = movie_image
                    movie_photo.grid(column=0, row=1, padx=20, sticky=tk.W, rowspan=2)
                    os.chdir(main_path)

            tk.Label(usable_frame, text=row, font=("Arial", 14), justify="left", bg=bg_color[bg_color_counter], anchor="w",
                     width=70).grid(column=1, row=1, padx=20, sticky=tk.W, rowspan=2)
            tk.Button(usable_frame, text="Watched").grid(column=2, row=1, sticky=tk.W, padx=20)
            tk.Button(usable_frame, text="Not Watched").grid(column=2, row=2, sticky=tk.W, padx=20)
            self.row_count += 2
            if bg_color_counter == 0:
                bg_color_counter = 1
            else:
                bg_color_counter = 0
        if self.window_refresh_heck == 801:
            self.window_refresh_heck += 1
        else:
            self.window_refresh_heck -= 1

        self.pg_count += 1

        final_frame = tk.Frame(self.second_frame)
        final_frame.configure(bg=bg_color[bg_color_counter])
        final_frame.grid(row=self.row_count)
        if if_searched:
            lode_more_button = tk.Button(final_frame, text="Go back", font=("Arial", 14),
                                         command=lambda: [final_frame.destroy(), self.create_text_labels({**self.data[0], **self.data[1], **self.data[2]}, False),
                                                          self.root.geometry(f"1130x{self.window_refresh_heck}")])
        else:
            lode_more_button = tk.Button(final_frame, text="Load more movies", font=("Arial", 14),
                                         command=lambda: [final_frame.destroy(), self.create_text_labels(self.data[self.pg_count], False),
                                                          self.root.geometry(f"1130x{self.window_refresh_heck}")])
        lode_more_button.pack()

    @staticmethod


    def download_image(url, file_name):

        # Send GET request
        response = requests.get(url)

        # Save the image
        if response.status_code == 200:

            with open(file_name, "wb") as f:
                f.write(response.content)

        else:
            print(response.status_code)


if __name__ == "__main__":
    m_2022 = Movies('https://www.cinemagia.ro/filme-2022/nota/', 10)
    m_2021 = Movies('https://www.cinemagia.ro/filme-2021/nota/', 10)
    m_2020 = Movies('https://www.cinemagia.ro/filme-2020/nota/', 10)
    m_2019 = Movies('https://www.cinemagia.ro/filme-2019/nota/', 10)
    Interface(m_2022.get_movies() + m_2021.get_movies() + m_2020.get_movies() + m_2019.get_movies())
    main_path = os.getcwd()
    os.chdir("movie_images")
    for item in os.listdir():
        os.remove(item)
    os.chdir(main_path)