wuee, cool. grösseri Planete, gseet scho vell besser uus wenns di rechtig grössi händ.

Wechtig !!!! onbedengt beachte, dass alles dynamisch glade werd. das heisst d' date werded usem beld useglese:

Biispell:

# draw background planet icon

# name usem planet usehole: "zork" zom biispell...
name = self.parent.selected_planet.name

# denn endig hinzuefüege:
pic = name + "_150x150.png"

# abchecke obs beld ide lischte vode vorgladnige belder dren esch       
if pic in self.parent.images[pictures_path]["planets"].keys(): 
	self.planet_image = self.parent.images[pictures_path]["planets"][pic]

# sosch halt skaliere ( schlechti performance, ond schlechti qualität)
else:
        self.planet_image = pygame.transform.scale(self.parent.selected_planet.image.copy(), (150, 150))



wenn de name vom beld ned öberii stemmt, muessi alles vo hand umbenenne oder en wüeschte hack mache wo eigentli
nor fehler produziert :) 

drom: "beldname" + "_" + "100x100" + ".png"

--> zom biispel:  "super geiler planet_1000x1000.png"   

es dörf nor emmer ein "_" drenn haa, sosch gets chaoss ;)

Au wechtig, das er genau so heisst wie im game. Schoscht gets: Chaoss :)



