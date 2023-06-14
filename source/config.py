import source.SaveLoad
from source.SaveLoad import *

prices = {
    "solar panel": {
        "water": 1,
        "energy": 10,
        "food": 0,
        "minerals": 25
        },
    "wind mill": {
        "water": 2,
        "energy": 10,
        "food": 0,
        "minerals": 25
        },
    "power plant": {
        "water": 5,
        "energy": 10,
        "food": 0,
        "minerals": 25
        },
    "spring": {
        "water": 0,
        "energy": 5,
        "food": 0,
        "minerals": 5
        },
    "water treatment": {
        "water": 0,
        "energy": 10,
        "food": 0,
        "minerals": 10
        },
    "terra former": {
        "water": 5,
        "energy": 15,
        "food": 0,
        "minerals": 25
        },
    "farm": {
        "water": 5,
        "energy": 10,
        "food": 5,
        "minerals": 3
        },
    "ranch": {
        "water": 10,
        "energy": 10,
        "food": 10,
        "minerals": 10
        },
    "agriculture complex": {
        "water": 25,
        "energy": 15,
        "food": 13,
        "minerals": 15
        },
    "mine": {
        "water": 5,
        "energy": 10,
        "food": 5,
        "minerals": 10
        },
    "open pit": {
        "water": 5,
        "energy": 10,
        "food": 10,
        "minerals": 15
        },
    "mineral complex": {
        "water": 15,
        "energy": 30,
        "food": 12,
        "minerals": 25
        },
    "town": {
        "water": 5,
        "energy": 5,
        "food": 5,
        "minerals": 5
        },
    "city": {
        "water": 5,
        "energy": 10,
        "food": 6,
        "minerals": 7
        },
    "metropole": {
        "water": 15,
        "energy": 30,
        "food": 10,
        "minerals": 25
        },
    "university": {
        "water": 1,
        "energy": 1,
        "food": 3,
        "minerals": 2
        },
    "space harbor": {
        "water": 5,
        "energy": 10,
        "food": 15,
        "minerals": 25
        },
    "particle accelerator": {
        "water": 15,
        "energy": 12,
        "food": 20,
        "minerals": 50
        },
    }
build_population_minimum = {'solar panel': 0,
                            'wind mill': 1000,
                            'power plant': 10000,
                            'spring': 0,
                            'water treatment': 1000,
                            'terra former': 10000,
                            'farm': 0,
                            'ranch': 1000,
                            'agriculture complex': 10000,
                            'mine': 0,
                            'open pit': 1000,
                            'mineral complex': 10000,
                            'town': 0,
                            'city': 0,
                            'metropole': 0,
                            'university': 0,
                            'space harbor': 1000,
                            'particle accelerator': 10000
                            }
building_production_time_scale = 5

building_production_time = {
    'solar panel': 3 * building_production_time_scale,
    'wind mill': 5 * building_production_time_scale,
    'power plant': 7 * building_production_time_scale,
    'spring': 1 * building_production_time_scale,
    'water treatment': 3 * building_production_time_scale,
    'terra former': 15 * building_production_time_scale,
    'farm': 3 * building_production_time_scale,
    'ranch': 7 * building_production_time_scale,
    'agriculture complex': 12 * building_production_time_scale,
    'mine': 5 * building_production_time_scale,
    'open pit': 15 * building_production_time_scale,
    'mineral complex': 23 * building_production_time_scale,
    'town': 1 * building_production_time_scale,
    'city': 3 * building_production_time_scale,
    'metropole': 5 * building_production_time_scale,
    'university': 2 * building_production_time_scale,
    'space harbor': 6 * building_production_time_scale,
    'particle accelerator': 13 * building_production_time_scale
    }
production = {
    "solar panel": {
        "water": 0,
        "energy": 1,
        "food": 0,
        "minerals": 0,
        "technology": 0,
        "city": 0

        },
    "wind mill": {
        "water": 0,
        "energy": 3,
        "food": 0,
        "minerals": 0,
        "technology": 0,
        "city": 0
        },
    "power plant": {
        "water": -1,
        "energy": 5,
        "food": -1,
        "minerals": -1,
        "technology": 0,
        "city": 0
        },
    "spring": {
        "water": 1,
        "energy": 0,
        "food": 0,
        "minerals": 0,
        "technology": 0,
        "city": 0
        },
    "water treatment": {
        "water": 3,
        "energy": -1,
        "food": -1,
        "minerals": 0,
        "technology": 0,
        "city": 0
        },
    "terra former": {
        "water": 5,
        "energy": -2,
        "food": -1,
        "minerals": 0,
        "technology": 0,
        "city": 0
        },
    "farm": {
        "water": 0,
        "energy": 0,
        "food": 1,
        "minerals": 0,
        "technology": 0,
        "city": 0
        },
    "ranch": {
        "water": 0,
        "energy": -1,
        "food": 3,
        "minerals": 0,
        "technology": 0,
        "city": 0
        },
    "agriculture complex": {
        "water": 1,
        "energy": -3,
        "food": 7,
        "minerals": -1,
        "technology": 0,
        "city": 0
        },
    "mine": {
        "water": -1,
        "energy": -2,
        "food": -1,
        "minerals": 1,
        "technology": 0,
        "city": 0
        },
    "open pit": {
        "water": -5,
        "energy": -10,
        "food": -3,
        "minerals": 3,
        "technology": 0,
        "city": 0
        },
    "mineral complex": {
        "water": -15,
        "energy": -15,
        "food": -10,
        "minerals": 7,
        "technology": 0,
        "city": 0
        },
    "town": {
        "water": -1,
        "energy": -1,
        "food": -1,
        "minerals": -1,
        "technology": 0,
        "city": 0
        },
    "city": {
        "water": -2,
        "energy": -2,
        "food": -2,
        "minerals": -2,
        "technology": 0,
        "city": 0
        },
    "metropole": {
        "water": -10,
        "energy": -5,
        "food": -10,
        "minerals": -1,
        "technology": 0,
        "city": 0
        },
    "university": {
        "water": -1,
        "energy": -1,
        "food": -1,
        "minerals": 5,
        "technology": 0,
        "city": 0
        },
    "space harbor": {
        "water": -3,
        "energy": -5,
        "food": 0,
        "minerals": 10,
        "technology": 0,
        "city": 0
        },
    "particle accelerator": {
        "water": -5,
        "energy": -10,
        "food": 0,
        "minerals": 25,
        "technology": 0,
        "city": 0
        }
    }


def load_settings():
    global key, name
    # production
    # load values from file
    production_file = load_file("buildings_production.json")
    # set values
    for key, value in production_file.items():
        if len(key.split(".")) == 2:
            name = key.split(".")[0]
            key_ = key.split(".")[1]
            production[name][key_] = value
            # print(production[name][key_], value)
    # print (production)
    # price
    # load values from file
    price_file = load_file("buildings_prices.json")
    # set values
    for key, value in price_file.items():
        if len(key.split(".")) == 2:
            # print(key, value)
            name = key.split(".")[0]
            key_ = key.split(".")[1]

            if key_ == "minimum population":
                build_population_minimum[name] = value
            elif key_ == "building_production_time":
                building_production_time[name] = value
            else:
                prices[name][key_] = value


load_settings()


# price_production = {}
# for name, res in prices.items():
#     price_production[name]["price"]=[res]
# print (price_production)
# for name, res in production.items():
#     price_production[name]["production"]=[res]
# def merge_building_dicts(*dicts):
#     price_production = {}
#     for d in dicts:
#         for building_name, building_info in d.items():
#             if building_name not in price_production:
#                 price_production[building_name] = {}
#             for info_type, info in building_info.items():
#                 if info_type not in price_production[building_name]:
#                     price_production[building_name][info_type] = {}
#                 price_production[building_name][info_type] = info
#     return price_production
#     return merged_dict
# print (merge_building_dicts(prices, production))

# build restrictions
# build_restrictions_population =  {}
# for key,value in production.items():
#     build_restrictions_population[key] = 0
#
# print (build_restrictions_population)


def create_info_panel_building_text():
    building_panel_info_text = {}
    text = ""
    for building, dict in prices.items():

        text = building + ":" + "\n"
        text += "\n" + "prices:" + "\n\n"
        for resource, value in dict.items():
            text += resource + ": " + str(value) + "\n"
        text += "\n" + "production: " + "\n"
        text += "\n"
        for r, v in production[building].items():
            text += r + ": " + str(v) + "\n"

        building_panel_info_text[building] = text

    return building_panel_info_text


# building_text = {}
#
# for key, value in production.items():
#     building_text[key] =
#
# print (building_production_time)
# print (production)

# building_production_time = {}
#
# for key, value  in production.items():
#     building_production_time[key] = 5
#
# print (building_production_time)


# planet_positions = {
#     'P0101': (513, 932),
#     'GIN V.S.X.O.': (1788, 742),
#     'Helios 12': (89, 410),
#     'Kepler-22b': (214, 173),
#     'ur-anus': (613, 258),
#     'XKGPRZ 7931': (1316, 531),
#     'Zeta Bentauri': (1495, 121),
#     'zork': (1132, 122),
#     'Sun': (925, 458),
#     "asteroids": (123, 321)
#     }

planet_positions = {'P0101': (1274.8285714285494, -162.97142857144792), 'GIN V.S.X.O.': (
1242.8285714285917, 435.02857142868413), 'Helios 12': (-254.17142857141616, -80.9714285714216), 'Kepler-22b': (
314.82857142856915, 154.02857142855405), 'ur-anus': (1089.8285714285769, -876.9714285713771), 'XKGPRZ 7931': (
42.8285714285698, -651.9714285713837), 'Zeta Bentauri': (1639.828571428568, -614.9714285714012), 'zork': (
130.82857142858333, -951.9714285713397), 'Sun': (581.8285714282565, -357.97142857146946), 'asteroids': (123, 321)
 }

population_grow_factor = 0.1
