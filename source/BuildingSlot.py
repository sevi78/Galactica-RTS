class BuildingSlot:
    def __init__(self):
        self.building_slot_amount = 3
        self.building_slot_upgrades = 0
        self.building_slot_upgrade_prices = {0: 500, 1: 750, 2: 1250, 3: 2500, 4: 5000, 5: 25000}
        self.building_slot_upgrade_energy_consumtion = {0: 0, 1: 2, 2: 3, 3: 5, 4: 10, 5: 15}
        self.building_slot_max_amount = self.building_slot_amount + len(self.building_slot_upgrade_prices)

    def set_tooltip(self, events):
        #for building_name, image_rect in self.button_images.items():
        #
        #     if image_rect.collidepoint(pygame.mouse.get_pos()):
        #         self.hover = True
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        print (self.__dict__)

#
# building_slot = BuildingSlot()
#
# print (building_slot.__dict__)