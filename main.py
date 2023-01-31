import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import os
from PIL import ImageTk
import string
import sqlite3


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
        rating = [item.text for item in soup.find_all('div', {'class': 'rating-cinemagia'})]
        titles = [item.text for item in soup.find_all('h2')]
        rating_inc = 0


        for item in soup.find_all("ul", {'class': "cast"}):
            movie_cast = {"director": [], "actors": [], "movie_genre": [], "distributor": [], "image_url": [],
                          "rating": [], "score": 0}

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
            movie_cast['rating'].append(rating[rating_inc])
            rating_inc += 1
            movie_cast['score'] = MovieSQL.get_final_score(movie_cast)
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

        recommended_button = tk.Button(usable_frame, text="For You", command=lambda: self.recommended_button_command())
        recommended_button.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(usable_frame, text=f"Search movie:", anchor="e", bg="#666666", width=70,
                 fg="white").grid(row=0, column=1)

        self.textbox = tk.Entry(usable_frame, width=75)
        self.textbox.grid(row=0, column=2)

        search_button = tk.Button(usable_frame, text="Search", command=lambda: self.get_entry_text())
        search_button.grid(row=0, column=3, padx=10, pady=10)

    def filter_search_movies(self):
        searched_movie = {}
        for item in self.data:

            for k, v in item.items():
                if str.lower(self.searched_txt) in str.lower(k):
                    searched_movie[k] = v
        self.create_text_labels(searched_movie, True)



    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_text_labels(self, data, if_searched):
        global button_list, button_list_search

        bg_color = ["#E7D39C", "#CCB677"]
        bg_color_counter = 0
        for k, v in data.items():
            usable_frame = tk.Frame(self.second_frame)
            usable_frame.configure(bg=bg_color[bg_color_counter])
            usable_frame.grid(row=self.row_count)
            row = f"\n{k}\n\n"
            for k_1, v_1 in v.items():
                if k_1 == "score":
                    continue
                elif k_1 != "image_url":
                    row += f"{k_1}: {', '.join(v_1)}\n"
                else:
                    main_path = os.getcwd()
                    os.chdir("movie_images")
                    self.download_image(v_1[0], f"{self.row_count}_image.png")
                    movie_image = ImageTk.PhotoImage(file=f"{self.row_count}_image.png")
                    movie_photo = tk.Label(usable_frame, image=movie_image, bg=bg_color[bg_color_counter])
                    movie_photo.photo = movie_image
                    movie_photo.grid(column=0, row=1, padx=20, sticky=tk.W)
                    os.chdir(main_path)

            tk.Label(usable_frame, text=row, font=("Arial", 14), justify="left", bg=bg_color[bg_color_counter], anchor="w",
                     width=70).grid(column=1, row=1, padx=20, sticky=tk.W)
            if if_searched:
                button_list_search.append(tk.Button(usable_frame, text="LIKED", bg="#3AB14D", fg="white"
                                                    , font=("Arial", 14, 'bold'),
                                                    command=lambda t=(k, v): self.get_button(t)))
                button_list_search[-1].grid(column=2, row=1, sticky=tk.W, padx=20, )
            else:
                button_list.append(tk.Button(usable_frame, text="LIKED", bg="#3AB14D", fg="white",
                                             font=("Arial", 14, "bold"), command=lambda t=(k, v): self.get_button(t)))
                button_list[-1].grid(column=2, row=1, sticky=tk.W, padx=20, )

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
    def get_button(self, t):
        print(t, "pressed")
        movie = MovieSQL(t[0], t[1])
        movie.write_data_in_sql("movies", False)

    def recommended_button_command(self):
        global recommended_videos
        self.row_count = 2
        self.pg_count = 0
        self.searched_txt = self.textbox.get()
        self.second_frame.destroy()

        self.second_frame = tk.Frame(self.canvas)
        self.second_frame.configure(bg="#666666")
        self.canvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        self.title_frame()
        self.search_frame()

        self.create_text_labels(recommended_videos, True)
        self.row_count = 2
        self.pg_count = 0

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




class MovieSQL:
    def __init__(self, movie_name, movie_dict):

        self.movie_name = movie_name
        self.movie_name = self.movie_name.replace('\'', '\'\'')
        self.movie_director = ', '.join(movie_dict["director"]).replace('\'', '\'\'')
        self.movie_actors = ', '.join(movie_dict["actors"]).replace('\'', '\'\'')
        self.movie_genre = ', '.join(movie_dict["movie_genre"]).replace('\'', '\'\'')
        self.movie_distributor = ', '.join(movie_dict["distributor"]).replace('\'', '\'\'')
        self.movie_rating = ', '.join(movie_dict["rating"]).replace('\'', '\'\'')
        self.movie_score = movie_dict["score"]
        self.movie_url = ', '.join(movie_dict["image_url"]).replace('\'', '\'\'')

    def write_data_in_sql(self, table_name, delete):
        con = sqlite3.connect("Movie_data.db")
        cur = con.cursor()
        if delete:
            cur.execute("DROP TABLE IF EXISTS all_movies;")
        create_command = f"""CREATE TABLE IF NOT EXISTS {table_name}(
                            Name TEXT,
                            Director TEXT,
                            Actors TEXT,
                            Genre TEXT,
                            Distributor TEXT,
                            Rating REAL,
                            Score INTEGER,
                            Image_URL,
                            PRIMARY KEY(Name)
                            );"""

        cur.execute(create_command)
        try:
            insert_command = f"""INSERT INTO {table_name} VALUES('{self.movie_name}',
                                                       '{self.movie_director}',
                                                       '{self.movie_actors}',
                                                       '{self.movie_genre}',
                                                       '{self.movie_distributor}',
                                                       '{self.movie_rating}',
                                                       '{self.movie_score}',
                                                       '{self.movie_url}');"""
            cur.execute(insert_command)
        except sqlite3.Error:
            print(f"error: {self.movie_name} couldn't be added")
        con.commit()

        con.close()

    @staticmethod
    def create_movie_table():
        con = sqlite3.connect("Movie_data.db")
        cur = con.cursor()
        create_command = f"""CREATE TABLE IF NOT EXISTS movies(
                            Name TEXT,
                            Director TEXT,
                            Actors TEXT,
                            Genre TEXT,
                            Distributor TEXT,
                            Rating REAL,
                            Score INTEGER,
                            Image_URL,
                            PRIMARY KEY(Name)
                            );"""

        cur.execute(create_command)
        con.commit()
        con.close()

    @staticmethod
    def read_column(column, table_name):
        output = []
        con = sqlite3.connect("Movie_data.db")
        cur = con.cursor()

        actors = cur.execute(f"SELECT {column} FROM {table_name}")
        output_1 = actors.fetchall()
        con.commit()

        con.close()
        for item in output_1:
            output += item[0].split(", ")
        return output
    @staticmethod
    def get_points_for(column, object):
        point_multiplayer = {"Actors": 12, "Director": 15, "Genre": 9, 'Distributor': 2}
        actors_list = MovieSQL.read_column(column, "movies")
        actors_points = {item: actors_list.count(item) for item in set(actors_list)}

        try:
            actor_points = actors_points[object]
        except KeyError:
            actor_points = 0

        return actor_points * point_multiplayer[column]
    @staticmethod
    def read_movies(table_name):
        con = sqlite3.connect("Movie_data.db")
        cur = con.cursor()

        actors = cur.execute(f"SELECT Name FROM {table_name}")
        output_1 = actors.fetchall()
        con.commit()

        con.close()

        return [item[0] for item in output_1]

    @staticmethod
    def get_final_score(data_dict):
        score = 0
        try:
            for item in data_dict["director"]:
                score += MovieSQL.get_points_for("Director", item)
            for item in data_dict["actors"]:
                score += MovieSQL.get_points_for("Actors", item)
            for item in data_dict["movie_genre"]:
                score += MovieSQL.get_points_for("Genre", item)
            for item in data_dict["distributor"]:
                score += MovieSQL.get_points_for("Distributor", item)
        except sqlite3.OperationalError:
            score = 0
        return score


    @staticmethod

    def get_recommended_videos():
        output = {}
        con = sqlite3.connect("Movie_data.db")
        cur = con.cursor()

        actors = cur.execute(f"SELECT * FROM all_movies ORDER BY Score DESC, Rating DESC")
        output_1 = actors.fetchall()
        con.commit()

        con.close()

        print("merge")

        for item in output_1:
            if item[0] not in MovieSQL.read_movies("movies"):
                output[item[0]] = {"director": item[1].split(", "), "actors": item[2].split(", "),
                                         "movie_genre": item[3].split(", "), "distributor": item[4].split(", "),
                                         "image_url": [item[7]],
                                         "rating": [str(item[5])], "score": int(item[6])}
            if len(output) == 20:
                break
        print(output)
        return output




if __name__ == "__main__":
    MovieSQL.create_movie_table()
    button_list = []
    button_list_search = []
    update_table = True

    m_2022 = Movies('https://www.cinemagia.ro/filme-2022/nota/', 10)
    m_2021 = Movies('https://www.cinemagia.ro/filme-2021/nota/', 10)
    m_2020 = Movies('https://www.cinemagia.ro/filme-2020/nota/', 10)
    m_2019 = Movies('https://www.cinemagia.ro/filme-2019/nota/', 10)

    movie_list = m_2022.get_movies() + m_2021.get_movies() + m_2020.get_movies() + m_2019.get_movies()
    print(movie_list)

    for item in movie_list:
        for k, v in item.items():
            movie = MovieSQL(k, v)
            movie.write_data_in_sql("all_movies", update_table)
            update_table = False

    recommended_videos = MovieSQL.get_recommended_videos()

    Interface(movie_list)
    main_path = os.getcwd()
    os.chdir("movie_images")
    for item in os.listdir():
        os.remove(item)
    os.chdir(main_path)

