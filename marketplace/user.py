# Status: FINAL, dgaida2, 15.10.2024

# definiert die Klasse User.
# user ist ein Aktionär auf dem Online-Marktplatz. Kann sowohl Produkte kaufen als auch verkaufen.
# Ein user hat auch Freunde.
# ihm können deshalb auch Produkte/Auktionen vorgeschlagen werden. Beispielsweise solche,
# die seine Freunde interessieren.
# Ein Nutzer wird über seine ID identifiziert. Ein Nutzer hat ein Budget (balance), das sich verkleinert, wenn User
# etwas verkauft und das sich vergrößert, wenn User etwas verkauft.
# Nutzer wohnt an einer zufälligen GPS-Koordinate, für die der Wohnort als String zurückgegeben werden kann.
# (wird in drittes Praktikum benötigt)

# Nur für dritten Praktikumstermin:
# User erbt von der Klasse SetNode, SetNode ist ein Knoten in einer disjunkten Menge, definiert in Praktikumsgruppen,
# damit ist User ein Mitglied einer Praktikumsgruppe

import marketplace.praktikumsgruppen


class User(marketplace.praktikumsgruppen.SetNode):
    """
    """Repräsentiert einen Nutzer.

    Attribute:
        _id (str): Nutzer-ID
        _password (str): Passwort des Nutzers
        _name_first (str): Vorname
        _name_family (str): Familienname
        _friends (set): Menge der Freunde des Nutzers
        _balance (float): Kontostand des Nutzers in Euro
        _gps_coords (tuple): GPS-Koordinaten (Latitude, Longitude)
        _address (str): Adresse zum Wohnort
        _rating_stars (list): Liste der vergebenen Sternebewertungen
    """

    # *** CONSTRUCTORS ***
    def __init__(self, user_id: str, password: str, name_family: str, name_first: str, gps_coord, address):
        """

        :param user_id: GM‑ID des Studierenden / Nutzerkennung
        :param password: Passwort (Standardmäßig "abcde")
        :param name_family: Familienname
        :param name_first: Vorname
        :param gps_coord: Tupel mit (Latitude, Longitude) des Wohnorts
        :param address: Adresse (String) zum Wohnort
        """
        super().__init__()

        self._id = user_id
        self._password = password

        self._name_first = name_first
        self._name_family = name_family

        self._friends = set()              # Freunde des Nutzers

        self._balance = 500.0           # Kontostand des Nutzers in Euro

        # Tupel mit Längen- und Breitengrad des erfundenen Wohnorts des Users.
        self._gps_coords = gps_coord

        # Adresse, die zur GPS-Koordinate gehört
        self._address = address

        self._rating_stars = []

    # *** PUBLIC SET methods ***

    def decrease_balance(self, amount):
        """
        decrease balance by given amount. must be called when user purchases something
        :param amount: amount in Euros by which the balance is reduced
        """
        self._balance -= amount

    def increase_balance(self, amount):
        """
        increase balance by given amount. must be called when user sells something
        :param amount: amount in Euros by which the balance is increased
        """
        self._balance += amount

    # *** PUBLIC methods ***

    def password_valid(self, password):
        return password == self._password

    def friends_add_list(self, friend_ids):
        """
        add the given list of friend id's to the set _friends
        :param friend_ids: list of friend id's
        """
        for friend_id in friend_ids:
            self._friends.add(friend_id)

    def friends_add(self, friend_id):
        self._friends.add(friend_id)

    def friends_delete(self, friend_id):
        self._friends.remove(friend_id)

    def rate_user(self, stars: int):
        self._rating_stars.append(stars)

    # *** PUBLIC GET methods ***

    def pretty_print(self):
        return "ID: {0} Name: {1} Wohnort: {2}".format(self._id.ljust(15), self.name(),
                                                       self.address())

    @staticmethod
    def get_id_from_pretty_print(pretty_print_text: str):
        splits = pretty_print_text.split(" ")
        return splits[1]

    def is_friend(self, user_id):
        return user_id in self._friends

    def get_rating_stars_mean(self):
        mean = 0
        for star in self._rating_stars:
            mean = mean + star

        if len(self._rating_stars) >= 1:
            mean /= len(self._rating_stars)

        return mean

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    # *** PUBLIC methods to return class properties ***

    def balance(self):
        return self._balance

    def name(self):
        return f"{self._name_first} {self._name_family}"

    def id(self):
        return self._id

    def password(self):
        return self._password

    def friends(self):
        return self._friends

    def gps_coords(self):
        return self._gps_coords

    def address(self):
        return self._address

    # *** PRIVATE variables ***
