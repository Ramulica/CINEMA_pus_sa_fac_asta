import sqlite3


class MovieSQL:
    def __init__(self, movie_name, movie_dict):

        self.movie_name = movie_name
        self.movie_name = self.movie_name.replace('\'', '\'\'')
        self.movie_director = ', '.join(movie_dict["director"])
        self.movie_actors = ', '.join(movie_dict["actors"])
        self.movie_genre = ', '.join(movie_dict["movie_genre"])
        self.movie_distributor = ', '.join(movie_dict["distributor"])

    def write_data_in_sql(self):
        con = sqlite3.connect("Movie_data.db")

        cur = con.cursor()
        create_command = """CREATE TABLE IF NOT EXISTS movies(
                            movie_name TEXT,
                            movie_director TEXT,
                            movie_actors TEXT,
                            movie_genre TEXT,
                            movie_distributor TEXT,
                            PRIMARY KEY(movie_name)
                            );"""

        cur.execute(create_command)

        insert_command = f"""INSERT INTO movies VALUES('{self.movie_name}',
                                                   '{self.movie_director}',
                                                   '{self.movie_actors}',
                                                   '{self.movie_genre}',
                                                   '{self.movie_distributor}');"""
        cur.execute(insert_command)
        con.commit()

        con.close()

movie = [{"Top 'Gun Maverick":
        {'director': ['Joseph Kosinski'],
         'actors': ['Tom Cruise', 'Jennifer Connelly', 'Val Kilmer'],
         'movie_genre': ['Acţiune', 'Dramă'], 'distributor': ['Ro Image 2000'],
         'image_url': ['https://static.cinemagia.ro/img/resize/db/movie/62/49/95/top-gun-maverick-280903l-147x210-b-d41cde02.jpg']}}]

for item in movie:
    for k, v in item.items():
        movie_calss = MovieSQL(k, v)

        movie_calss.write_data_in_sql()
