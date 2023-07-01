import random

import source.utils.config
from source import utils

game_events = {}
resources = ["water", "food", "energy", "technology", "minerals"]


class Deal:
    """
    Deal(offer={random.choice(resources):random.randint(0,1000)}, request={random.choice(resources):random.randint(0,1000)}
    """
    def __init__(self, offer, request, **kwargs):
        self.offer = offer
        self.request = request
        self.friendly = kwargs.get("friendly", None)

        self.create_friendly_offer()

    def make_deal(self):
        player = source.utils.Globals.app.player
        # add offer
        for key, value in self.offer.items():
            setattr(player, key, getattr(player, key) + value)

        # subtract request
        for key, value in self.request.items():
            setattr(player, key, getattr(player, key) - value)

    def create_friendly_offer_(self):
        """
        creates a friendly deal:
        it always offers what you have least of and requests what you have most
        """
        f = random.randint(0, 1)
        if f == 0:
            return
        player = None  # define player variable
        if source.utils.Globals.app:
            player = source.utils.Globals.app.player

            # extract "city" from dict
            d_raw = player.get_stock()
            d = {key: value for key, value in d_raw.items() if key != "city"}

            # offer

            offer_key = min(d, key=d.get)
            min_v = abs(d[offer_key])
            max_v = abs(d[offer_key] + random.randint(250, 450))
            try:
                offer_value = abs(random.randint(min_v,max_v ))
            except ValueError:
                print("create_friendly_offer error:",min_v,max_v )
                return

            self.offer = {offer_key: abs(offer_value)}

            # request
            request_key = max(d, key=d.get)
            request_value = getattr(player, request_key)
            request_value -= random.randint(25, 50 + abs(getattr(player, request_key)))
            self.request = {request_key: request_value}

    def create_friendly_offer___(self):
        player = None  # define player variable
        if source.utils.Globals.app:
            player = source.utils.Globals.app.player

            # extract "city" from dict
            d_raw = player.get_stock()
            d = {key: max(0, value) for key, value in d_raw.items() if key != "city"}

            # check if any value in the stock is less than 0
            if any(value < 0 for value in d.values()):
                # replace negative values with 0
                d = {key: max(0, value) for key, value in d.items()}

            # get lowest and highest keys
            # offer
            offer_key = min(d, key=d.get)
            request_key = max(d, key=d.get)

            # calculate offer value
            offer_value = max(d[offer_key] - random.randint(25, 250), 0) + random.randint(25, 250)
            self.offer = {}
            self.offer[offer_key] = offer_value

            # calculate request value
            request_value = getattr(player, request_key)
            request_value -= random.randint(25, 250)
            self.request = {}
            self.request[request_key] = request_value

    def create_friendly_offer_____(self):
        player = None  # define player variable
        if source.utils.Globals.app:
            player = source.utils.Globals.app.player

            # extract "city" from dict
            d_raw = player.get_stock()
            d = {key: max(0, value) for key, value in d_raw.items() if key != "city"}

            # check if any value in the stock is less than 0
            if any(value < 0 for value in d.values()):
                # replace negative values with 0
                d = {key: max(0, value) for key, value in d.items()}

            # get key with lowest value
            lowest_value_key = min(d, key=d.get)

            # calculate minimum value needed to set lowest value to 25
            min_value = max(25 - d[lowest_value_key], 0)

            # calculate offer value
            offer_value = min_value + random.randint(25, 250)
            self.offer = {}
            self.offer[lowest_value_key] = offer_value

            # calculate request value
            request_key = max(d, key=d.get)
            request_value = getattr(player, request_key)
            request_value -= random.randint(25, 250)
            self.request = {}
            self.request[request_key] = request_value

    def create_friendly_offer(self):
        player = None  # define player variable
        if source.utils.Globals.app:
            player = source.utils.Globals.app.player

            # extract "city" from dict
            d_raw = player.get_stock()
            d = {key: max(0, value) for key, value in d_raw.items() if key != "city"}

            # check if any value in the stock is less than 0
            if any(value < 0 for value in d.values()):
                # replace negative values with 0
                d = {key: max(0, value) for key, value in d.items()}

            # get key with lowest value
            lowest_value_key = min(d, key=d.get)

            # calculate minimum value needed to set lowest value to 25
            min_value = max(25 - d[lowest_value_key], 0)

            # calculate offer value
            offer_value = d[lowest_value_key] + min_value + random.randint(25, 250)
            self.offer = {}
            self.offer[lowest_value_key] = offer_value

            # calculate request value
            request_key = max(d, key=d.get)
            request_value = getattr(player, request_key)
            request_value -= random.randint(25, 250)
            self.request = {}
            self.request[request_key] = request_value
class GameEvent:
    def __init__(self, name, title, body, end_text, functions, **kwargs):
        self.name = name
        self.title = title
        self.body = body
        self.end_text = end_text
        self.functions = functions
        self.deal = kwargs.get("deal", None)
        self.event_id = len(game_events.keys())

        game_events[self.name] = self

    def set_body(self):
        # check for valid references, otherwise return
        if not utils.Globals.app:
            return

        # check for deal, otherwise don't change the body
        if not self.deal:
            return

        # get a random planet from the explored planets
        explored_planets = utils.Globals.app.explored_planets
        explored_planets_with_aliens = []

        # check if has some explored planets
        if len(explored_planets) > 0:
            explored_planets_with_aliens = [i for i in explored_planets if i.alien_population != 0]

        # check for planets with alien population, choose a random one
        if len(explored_planets_with_aliens) > 0:
            planet = random.choice(explored_planets_with_aliens)
        else:
            planet = None

        # generate text to display
        request_text = ""
        offer_text = ""

        for key, value in self.deal.request.items():
            request_text += str(value) + " " + key
        for key, value in self.deal.offer.items():
            offer_text += str(value) + " " + key

        # set body
        if planet:
            self.body = f"the alien population of the planet {planet.name} offers you a deal: they want {request_text} for {offer_text}."
        else:
            self.body = f"some aliens offer you a deal: they want {request_text} for {offer_text}"


# define GameEvents
start = GameEvent(
    name="start",
    title="Welcome !!!",
    body="... after 75000 years of darkness, you finally reached the the solar system " \
         "of 'Elbauz_gamma_epsilon5'.\nYou are the last survivors from PlanetEarth.Mankind is " \
         "counting on you, so don't mess it up!!!\nYour goal is to get at least 500 people " \
         "surviving ! ",
    end_text="GOOD LUCK !",
    functions=None,
    )

goal1 = GameEvent(
    name="goal1",
    title="Congratulation!",
    body="your population has reached 500 people.  ",
    end_text="",
    functions=None
    )

goal2 = GameEvent(
    name="goal2",
    title="Congratulation!",
    body="your population has reached 1000 people.\nYou are now able to build second level buildings like:\n\n" +
         str([key for key in source.utils.config.build_population_minimum if source.utils.config.build_population_minimum[key] == 1000]).split("[")[1].split("]")[0],
    end_text="go for it!",
    functions=None
    )

goal3 = GameEvent(
    name="goal3",
    title="Congratulation!",
    body="your population has reached 10000 people.\nYou are now able to build third level buildings like:\n\n" +
         str([key for key in source.utils.config.build_population_minimum if source.utils.config.build_population_minimum[key] == 10000]).split("[")[1].split("]")[0],
    end_text="go for it!",
    functions=None
    )

alien_deal_random = GameEvent(
    name="alien_deal_random",
    title="Deal Offer",
    body="the alien population of the planet (not set) offers you a deal: they want 200 food for 33 technology.",
    end_text="do you accept the offer?",
    deal= Deal(offer={random.choice(resources):random.randint(0,1000)}, request={random.choice(resources):random.randint(0,1000)}),
    functions={"yes": None, "no": None},
    )


friendly_trader =  GameEvent(
    name="friendly_trader",
    title="Deal Offer",
    body="the alien population of the planet (not set) offers you a deal: they want 200 food for 33 technology.",
    end_text="do you accept the offer?",
    deal= Deal(offer={random.choice(resources):random.randint(0,1000)}, request={random.choice(resources):random.randint(0,1000)}, friendly=True),
    functions={"yes": None, "no": None},
    friendly=True
    )