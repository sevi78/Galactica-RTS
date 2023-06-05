import source.config


class EventText:
    def __init__(self):
        self.title = " Welcome !!!"
        self.body = None
        self.functions = []
        space = " "

        self.text = {"start": {"title": " Welcome !!!",
                               "body": """... after 75000 years of darkness, you finally reached the the solar system of 'Elbauz_gamma_epsilon5'.                   You are the last survivors from PlanetEarth. Mankind is counting on you, so don't mess it up!!!                               Your goal is to get at least 500 people surviving !                                                                                                                          GOOD LUCK !""", "functions": None
                               },
                     "end": {"title": " Welcome !!!",
                             "body": "... after 75000 years of darkness,\n you finally reached the the solar system of\n" \
                                     "'Elbauz_gamma_epsilon5'.\n You are the last survivors from PlanetEarth. \n" \
                                     "Mankind is counting on you, so don't mess it up!!! \n, ",
                             "functions": None
                             },
                     "goal1": {"title": "Congratulation!",
                               "body": "your population has reached 500 people.  ",
                               "functions": None
                               },
                     "goal2": {"title": "Congratulation!",
                               "body": "your population has reached 1000 people. You are now able to build second level buildings like:"
                                       + str([key for key in source.config.build_population_minimum if
                                              source.config.build_population_minimum[key] == 1000]).split("[")[
                                           1].split("]")[
                                           0] + "                                                              go for it!",
                               "functions": None
                               },
                     "goal3": {"title": "Congratulation!",
                               "body": "your population has reached 10000 people. You are now able to build second level buildings like:"
                                       + str([key for key in source.config.build_population_minimum if
                                              source.config.build_population_minimum[key] == 10000]).split("[")[
                                           1].split("]")[
                                           0] + "                                                              go for it!",
                               "functions": None
                               },
                     }

    def end(self):
        self.title = " Game Over !!!.\n"
        self.body = "...  mess it up better next time ...\n"
        self.functions = ["restart"]
