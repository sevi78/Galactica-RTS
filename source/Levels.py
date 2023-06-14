level_dict = {1: {'P0101': {'x': '600',
                                        'y': '450',
                                        'position': ('600', '450'),
                                        'image_name': 'P0101_50x50.png',
                                        'name': 'P0101',
                                        'building_slot_amount': 3,
                                        'population': 0,
                                        'alien_population': 0,
                                        'specials': None,
                                        'type': '',
                                        "possible_resources": ["energy", "minerals", "city"]
                                        },

                  'GIN V.S.X.O.': {'x': '250',
                                   'y': '400',
                                   'position': ('250', '400'),
                                   'image_name': 'GIN V.S.X.O._80x80.png',
                                   'name': 'GIN V.S.X.O.',
                                   'building_slot_amount': 3,
                                   'population': 0,
                                   'alien_population': 0,
                                   'specials': None,
                                   'type': '',
                                   "possible_resources": ["water", "food", "minerals"]
                                   },

                  'Helios 12': {'x': '350',
                                'y': '300',
                                'position': ('350', '300'),
                                'image_name': 'Helios 12_70x70.png',
                                'name': 'Helios 12',
                                'building_slot_amount': 3,
                                'population': 0,
                                'alien_population': 0,
                                'specials': None,
                                'type': '',
                                "possible_resources": ["energy", "city"]
                                },

                  'Kepler-22b': {'x': '350',
                                 'y': '100',
                                 'position': ('350', '100'),
                                 'image_name': 'Kepler-22b_50x50.png',
                                 'name': 'Kepler-22b',
                                 'building_slot_amount': 3,
                                 'population': 0,
                                 'alien_population': 0,
                                 'specials': None,
                                 'type': '',
                                 "possible_resources": ["water", "energy", "food", "minerals", "city", "technology"]
                                 },

                  'ur-anus': {'x': '500',
                              'y': '130',
                              'position': ('500', '30'),
                              'image_name': 'ur-anus_60x60.png',
                              'name': 'ur-anus',
                              'building_slot_amount': 3,
                              'population': 0,
                              'alien_population': 0,
                              'specials': None,
                              'type': '',
                              "possible_resources": ["water", "energy", "minerals"]
                              },

                  'XKGPRZ 7931': {'x': '180',
                                  'y': '500',
                                  'position': ('180', '500'),
                                  'image_name': 'XKGPRZ 7931_50x50.png',
                                  'name': 'XKGPRZ 7931',
                                  'building_slot_amount': 3,
                                  'population': 0,
                                  'alien_population': 0,
                                  'specials': None,
                                  'type': '',
                                  "possible_resources": ["food", "minerals", "city", "technology"]
                                  },

                  'Zeta Bentauri': {'x': '960',
                                    'y': '340',
                                    'position': ('960', '340'),
                                    'image_name': 'Zeta Bentauri_60x60.png',
                                    'name': 'Zeta Bentauri',
                                    'building_slot_amount': 3,
                                    'population': 0,
                                    'alien_population': 0,
                                    'specials': None,
                                    'type': '',
                                    "possible_resources": ["water", "energy", "food", "minerals", "city", "technology"]
                                    },

                  'zork': {'x': '750',
                           'y': '120',
                           'position': ('750', '120'),
                           'image_name': 'zork_50x50.png',
                           'name': 'zork',
                           'building_slot_amount': 3,
                           'population': 0,
                           'alien_population': 0,
                           'specials': None,
                           'type': '',
                           "possible_resources": ["water", "food", "minerals", "technology"]
                           },

                  'Sun': {'x': '900',
                          'y': '450',
                          'position': ('900', '450'),
                          'image_name': 'sonnecomic_110x110.png',
                          'name': 'Sun',
                          'building_slot_amount': 0,
                          'population': 0,
                          'alien_population': 0,
                          'specials': None,
                          'type': '',
                          "possible_resources": ["energy"]
                          },
                  }
              }

level_dict_new = {}


def ramsch():
    pass

    # levels = {1:
    #                {"positions":{ '600_450': 'P0101_40x40.png', '250_400': 'GIN V.S.X.O._70x70.png', '350_300': 'Helios 12_60x60.png',
    #                               '350_100': 'Kepler-22b_40x40.png', '500_30': 'ur-anus_60x60.png', '180_500': 'XKGPRZ 7931_40x40.png',
    #                               '960_340': 'Zeta Bentauri_60x60.png', '750_120': 'zork_50x50.png'},
    #                 "building_slot_amounts":
    # }}

    # level1  = {'600_450': 'P0101_40x40.png', '250_400': 'GIN V.S.X.O._70x70.png', '350_300': 'Helios 12_60x60.png',
    #      '350_100': 'Kepler-22b_40x40.png', '500_30': 'ur-anus_60x60.png', '180_500': 'XKGPRZ 7931_40x40.png',
    #      '960_340': 'Zeta Bentauri_60x60.png', '750_120': 'zork_50x50.png'}

    # level_image_names = []
    # level_pos = []
    # for key, value in level1.items():
    #      level_image_names.append(value)
    #      level_pos.append(key)
    #
    # levels ={1:[PlanetParams(x= level_pos[i].split("_")[0],
    #                          y= level_pos[i].split("_")[1],
    #                          image_name = level_image_names[i]) for i in range(len(level_image_names))]
    #
    # }
    #
    # level = 1
    # levels_dict = {}
    # # print (levels[level])
    #
    # levels_dict[level] = {}
    # for pp in levels[level]:
    #      # print (pp.name)
    #      levels_dict[level][pp.name] = {}
    #      for key,value in pp.__dict__.items():
    #
    #
    #           # print (key,value)
    #           levels_dict[level][pp.name][key] = value
    #      #
    #      # levels_dict[pp.name]["image"] = pp.image_name
    #      # levels_dict[pp.name]["position"] = pp.position
    #      # levels_dict[pp.name]["building_slot_amount"] = pp.building_slot_amount
    #      #
    #
    # print (levels_dict)
    #
    #      # for kay, value  in levels[level][list]:
    #      #      levels_dict[l][list][key] = value
    #      # print (i[0][0].name)
    # # levels = {1:{"positions": level1,
    # #              "image_names":level_image_names,
    # #              "building_slot_amount":[]}}
    #
    #
    # level1_building_slots = {}

    # class PlanetParams:
    #     def __init__(self, x, y, image_name):
    #         self.x = x
    #         self.y = y
    #         self.position = (x, y)
    #         self.image_name = image_name
    #         self.name = image_name.split("_")[0]
    #         self.building_slot_amount = 3
    #         self.population = 0
    #         self.alien_population = 0
    #         self.specials = None
    #         self.type = ""
    #
