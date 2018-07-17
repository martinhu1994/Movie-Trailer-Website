import media
import fresh_tomatoes


def create_movie_list():
    """ Creats six Movie instances and returns these instances as a list."""

    deadpool = media.Movie("Deadpoll", 
                           "https://m.media-amazon.com/images/M/MV5BYzE5MjY1ZDgtMTkyNC00MTMyLThhMjAtZGI5OTE1NzFlZGJjXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SY1000_CR0,0,666,1000_AL_.jpg", 
                           "https://youtu.be/ONHBaC-pfsk")

    inception = media.Movie("Inception", 
                            "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SY1000_CR0,0,675,1000_AL_.jpg",
                            "https://youtu.be/97CDCk2n-Nw")

    interstellar = media.Movie("Interstellar",
                               "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SY1000_SX675_AL_.jpg",
                               "https://youtu.be/8EdxTFS3fD0")

    matrix = media.Movie("The Matrix", 
                         "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SY1000_CR0,0,665,1000_AL_.jpg", 
                         "https://youtu.be/a94b1yZOBes")

    intouchables = media.Movie("The Intouchables", 
                               "https://m.media-amazon.com/images/M/MV5BMTYxNDA3MDQwNl5BMl5BanBnXkFtZTcwNTU4Mzc1Nw@@._V1_SY1000_CR0,0,674,1000_AL_.jpg", 
                               "https://youtu.be/ZLqqNNN9cgU")

    incredibles = media.Movie("Incredibles 2", 
                              "https://m.media-amazon.com/images/M/MV5BMTEzNzY0OTg0NTdeQTJeQWpwZ15BbWU4MDU3OTg3MjUz._V1_SY1000_CR0,0,674,1000_AL_.jpg", 
                              "https://youtu.be/i5qOzqD9Rms")

    movies = [deadpool, inception, interstellar, matrix, intouchables, incredibles]
    return movies


def main():
    movies = create_movie_list()
    fresh_tomatoes.open_movies_page(movies)


if __name__ == '__main__':
    main()
