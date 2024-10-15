import random
import json  # Assurez-vous d'importer json en haut du fichier

class Action:
    def __init__(self, name):
        self.name = name


class Character:
    def __init__(self, name, is_alive, current_room=None):  # Ajout d'un paramètre pour la pièce actuelle
        self.name = name
        self.is_alive = is_alive
        self.current_room = current_room  # Initialise la pièce actuelle
    
    def place_character(self, room):
        self.current_room = room
        
    def take_action(self): # after moving to another room
        pass


    def move_to_room(self, new_room=None):  # Ajout d'une méthode pour déplacer le personnage
        if not self.current_room.adjacent_rooms:
            raise ValueError("Aucune pièce adjacente pour un mouvement aléatoire.")  # Gère le cas où il n'y a pas de pièces adjacentes
            
        if not new_room:  # Si le mouvement aléatoire est demandé
            new_room = random.choice(self.current_room.adjacent_rooms + [self.current_room])  # Choisi une pièce adjacente au hasard
        self.current_room = new_room  # Met à jour la pièce actuelle


    def examine_object(self, object_id=None, random=False):  # Ajoute une méthode pour examiner un objet
        if random:  # Si l'examen aléatoire est demandé
            if self.current_room.objects:  # Vérifie si il y a des objets dans la pièce actuelle
                object = random.choice(self.current_room.objects)  # Choisi un objet au hasard
                print(f"Vous utilisez {object.name}.")
                object.use_object()
            else:
                raise ValueError("Aucun objet dans la pièce actuelle pour un examen aléatoire.")  # Gère le cas où il n'y a pas d'objets dans la pièce actuelle
        elif object_id:  # Si un nom d'objet spécifique est donné
            for obj in self.current_room.objects:  # Parcourt les objets de la pièce actuelle
                if obj.identifier() == object_id:  # Vérifie si l'objet correspond au nom donné
                    print(f"Vous examinez {obj.name}. {obj.description}")
                    return  # Sortie de la fonction après avoir trouvé et examiné l'objet
            raise ValueError("L'objet spécifié n'est pas trouvé dans la pièce actuelle.")  # Gère le cas où l'objet spécifié n'est pas trouvé
        else:
            raise ValueError("Aucun objet spécifié ou pas d'objets dans la pièce actuelle.")  # Gère le cas où aucun objet n'est spécifié ou qu'il n'y a pas d'objets dans la pièce actuelle

class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character  # Le personnage que le joueur contrôle

class Object:
    def __init__(self, identifier, name, description, states=None, current_state=None):
        self.identifier = identifier  # Ajout d'un identifiant pour l'objet
        self.name = name
        self.description = description
        self.states = states if states is not None else []
        self.current_state = current_state
        self.actions = {}
        
    def render_all_possible_action_from_object(self, body_found=False): # actions suggested are not the same before or after the body is revealed.
        return self.actions[body_found][self.current_state] # to develop.
        
    def use_object(self):
        print("You're using ", self.name)


class Time:
    def __init__(self, hour, minute=0):
        if not (0 <= hour <= 16):  # Vérifie que l'heure est entre 1 et 16
            raise ValueError("L'heure doit être comprise entre 1 et 16.")
        self.hour = hour
        self.minute = minute

class Room:
    def __init__(self, name, short_name, description=None, possible_adjacent_rooms_short_name=None, objects=None):
        self.name = name
        self.short_name = short_name
        self.description = description
        self.possible_adjacent_rooms_short_name = possible_adjacent_rooms_short_name if possible_adjacent_rooms_short_name is not None else []
        self.adjacent_rooms = []
        self.objects = objects if objects is not None else [] 
        
    def add_adjacent_room(self, room):
        if room not in self.adjacent_rooms:
            self.adjacent_rooms.append(room)
            room.add_adjacent_room(self)  # Assure la bidirectionnalité

    def add_object(self, obj):
        if obj.identifier not in [o.identifier for o in self.objects]:
            self.objects.append(obj)  # Ajoute l'objet à la liste des objets de la pièce

    def render_all_objects_in_room(self):
        return self.objects
    

    def generate_room(self, short_name):
        import json
        with open('rooms.json', 'r') as file:
            all_rooms = json.load(file)  # Charge les données des pièces depuis le fichier JSON
        for room_data in all_rooms:
            if room_data['short_name'] == short_name:
                return Room(room_data['name'], room_data['short_name'], room_data['description'], room_data['possible_adjacent_room'], room_data['possible_objects'])  # Crée et retourne une instance de Room
        raise ValueError("Aucune pièce trouvée avec le short_name donné.")  # Gère le cas où le short_name n'existe pas

    def generate_objects(self):
        import json
        with open('objects.json', 'r') as file:
            all_objects = json.load(file)  # Charge les données des objets depuis le fichier JSON
        for obj_data in all_objects:
            if obj_data['room'] == self.short_name:
                self.add_object(Object(obj_data['identifier'], obj_data['name'], obj_data['description']))  # Ajoute l'objet à la pièce

    def generate_adjacent_rooms(self, rooms):
        for room in rooms:
            if room.short_name in self.possible_adjacent_rooms_short_name:
                self.add_adjacent_room(room)


class PastAction:
    def __init__(self, description, action_type):
        self.description = description
        self.action_type = action_type  # 'alibi' ou 'crime'


class Game:
    def __init__(self, test=False):
        self.house = None
        self.characters = []  # Liste des personnages
        self.current_time = 0  # Initialisation du temps à 00:00
        self.test=test
        self.init_game()  # Appel de la méthode d'initialisation du jeu

    def init_game(self):
        self.house = House("First House")
        if self.test:
            self.house.generate_rooms()
            self.create_characters()

        else:
            self.house.ask_for_room_count()
            self.create_characters()
        self.place_all_characters()
        
        
    def start_game(self):
        while self.current_time < 8:
            for character in self.characters:
                if character.is_alive:
                    character.move_to_room()
            self.current_time += 1
            print(self.describe_characters() + "\n" + self.describe_nb_character_per_room())
            
    def create_characters(self, num_characters=None):
        with open('characters.json', 'r') as file:  # Charge les personnages depuis le fichier JSON
            all_characters = json.load(file)["personnages"]  # Accède à la liste des personnages
        
        if not num_characters:
            num_characters = int(input("Combien de personnages voulez-vous ? "))  # Demande le nombre de personnages
        selected_characters = random.sample(all_characters, num_characters)  # Sélectionne des personnages aléatoires, moins un pour le professeur
        
        # # Ajoute le professeur (la victime) qui n'est pas en vie
        # professor = next((char for char in all_characters if char["nom"] == "Jean Dupont"), None)  # Trouve le professeur
        # if professor:
        #     self.add_character(Character(professor["nom"], False))  # Ajoute le professeur comme personnage non vivant
        
        for character_data in selected_characters:
            character_name = character_data["nom"]  # Utilise le nom du personnage du JSON
            # if character_name != "Jean Dupont":
            self.add_character(Character(character_name, True))  # Ajoute le joueur

    def place_all_characters(self, first_place_short_name = "dining room"):
        first_place = None
        for room in self.house.rooms:
            if room.short_name == first_place_short_name:
                first_place = room
        for character in self.characters:
            character.place_character(first_place)

    def add_character(self, character):
        self.characters.append(character)  # Ajoute un joueur à la liste

    def describe_characters(self):
        description = f"Personnages at time {self.current_time}:\n"
        for character in self.characters:
            state = "vivant" if character.is_alive else "mort"
            description += f"{character.name} est dans {character.current_room.name} et est {state}.\n"
        return description
    
    def describe_nb_character_per_room(self):
        description = "In each room: \n"
        for room in self.house.rooms:
            description += " - " + room.name +": " + str(len([c for c in self.characters if c.current_room == room])) + " characters"+"\n"
        return description

    def describe_game_state(self):  # Ajout de la méthode pour décrire l'état du jeu
        description = self.house.describe_house() + "\n" + self.describe_characters() + "\n" + self.describe_nb_character_per_room()
        return description

class House:
    def __init__(self, name):
        self.name = name
        self.rooms = []  # Liste des pièces dans la maison
    def add_room(self, room):
        if room not in self.rooms:
            self.rooms.append(room)  # Ajoute une pièce à la maison
    def get_rooms(self):
        return self.rooms  # Retourne la liste des pièces de la maison
    def generate_house(self, num_house):
        self.generate_rooms()

    def generate_rooms(self, num_rooms=None):
        import json
        
        with open('rooms.json', 'r') as file:
            all_rooms = json.load(file)  # Charge les données des pièces depuis le fichier JSON
        
        # Assurez-vous que les pièces essentielles sont présentes
        essential_rooms = ["dining room", "living room", "kitchen", "office", "bedroom"]
        selected_rooms = [room for room in all_rooms if room['short_name'] in essential_rooms]  # Inclut les pièces essentielles
        
        if num_rooms:
            additional_rooms = [room for room in all_rooms if room['short_name'] not in essential_rooms]
            selected_rooms += random.sample(additional_rooms, num_rooms - len(selected_rooms))  # Ajoute des pièces aléatoires si nécessaire
        
        for room_data in selected_rooms:
            room = Room(room_data['name'], room_data['short_name'], room_data['description'], room_data['possible_adjacent_room'])  # Crée une instance de Room
            self.add_room(room)  # Ajoute la pièce à la maison
            
        for room in self.rooms:
            room.generate_objects()
            room.generate_adjacent_rooms(self.rooms)

    def ask_for_room_count(self):
        while True:
            try:
                num_rooms = int(input("Entrez un nombre de pièces entre 5 et 12 : "))
                if 5 <= num_rooms <= 12:
                    self.generate_rooms(num_rooms)  # Génère les pièces
                    break
                else:
                    print("Veuillez entrer un nombre valide.")
            except ValueError:
                print("Veuillez entrer un nombre entier.")

    def describe_house(self):
        description = f"Maison: {self.name}\n"
        for room in self.rooms:
            description += f"Pièce: {room.name}\n"
            description += f"Description: {room.description}\n"
            description += "Objets dans la pièce: " + ", ".join(obj.name for obj in room.objects) + "\n"
            description += "Pièces adjacentes: " + ", ".join(adj_room.name for adj_room in room.adjacent_rooms) + "\n"
            description += "\n"  # Ajoute une ligne vide entre les pièces
        return description
    
if __name__ == "__main__":  # Vérifie si le fichier est exécuté directement
    game = Game(test=True)  # Crée une instance de GameState
    print(game.describe_game_state())  # Affiche la description de la maison
    game.start_game()
