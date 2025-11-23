# Status: FINAL, dgaida2, 15.10.2024

# definiert die Klasse Users.
# Users ist eine Menge von disjunkten Mengen (nur für drittes Praktikum) von der Klasse User,
# damit man Users in Praktikumsgruppen einsortieren kann. Für das erste und zweite Praktikum ist die Klasse
# Praktikumsgruppe lediglich ein Dictionary
# in der Klasse werden die csv-Dateien user.csv und friends.csv gelesen.

import csv
import marketplace.user
import marketplace.praktikumsgruppen
from marketplace.rating_heap import RatingHeap


class Users(marketplace.praktikumsgruppen.Praktikumsgruppen):
    # *** CONSTRUCTORS ***
    def __init__(self, csvfile, *args):
        super().__init__()

        self._read_users_from_csvfile(csvfile)

        self._read_friends_csv('friends.csv')

        # erstelle Praktikumsgruppen als Menge disjunkter Mengen bzw. als dictionary (1. und 2. Praktikum)
        super().create_groups(list(self.keys()), self._groupnumbers)

        # Erstelle und fülle die Bewertungs-Heap-Struktur zur schnellen Abfrage des Top-bewerteten Users
        self._rating_heap = RatingHeap()
        for uid in list(self.keys()):
            mean = self[uid].get_rating_stars_mean()
            self._rating_heap.add_user(uid, mean)

    # *** PUBLIC SET methods ***

    # *** PUBLIC methods ***

    def add(self, user_id, password, name_family="", name_first="", gps_coord=(None, None), address=""):
        """
        Fügt einen Benutzer mit `user_id` in die von `Praktikumsgruppen` geerbte Struktur ein.
        :param user_id: GM-ID des Benutzers
        :param password: Passwort des Benutzers
        :param name_family: Familienname
        :param name_first: Vorname
        :param gps_coord: Tupel mit Längen- und Breitengrad des erfundenen Wohnorts
        :param address: Adresse, die zur GPS-Koordinate gehört
        """
        self[user_id] = marketplace.user.User(user_id, password, name_family, name_first, gps_coord, address)

    def calc_distance_between_users(self, user_id1, user_id2):
        # TODO für Studierende: Berechne die Distanz zwischen den GPS-Koordinaten von user1 und user2
        #  anhand eines Karten-/Graphen-Algorithmus (kürzeste Fahrstrecke im Straßennetz).

        user1 = self[user_id1]
        user2 = self[user_id2]

        # TODO für Studierende: Ersetze diese naive Manhattan-Näherung durch eine Distanz aus einem Graph-Algorithmus
        #  (z. B. Road-Distance / Routing).
        distance = sum(abs(a - b) for a, b in zip(user1.gps_coords(), user2.gps_coords()))

        return distance

    # *** PUBLIC GET methods ***

    def get_name_of_user(self, user_id):
        node = self[user_id]
        return node.name()

    def num_users(self):
        return len(self.keys())

    def password_valid(self, user_id, password):
        return self[user_id].password_valid(password)

    def get_user_pretty_print_for_list(self, user_id):
        return (self[user_id].pretty_print() + "\t in Praktikumsgruppe repräsentiert durch: " +
                self.find_byid(user_id, True))

    def get_friends_andgroupmembers_pretty_print(self, user_id):
        """
        Liefert die Anzeige-Strings (pretty_print) für Freunde und Gruppenmitglieder des gegebenen `user_id`,
        wie sie in der GUI dargestellt werden sollen.

        :param user_id: normalerweise die aktuelle Nutzer-ID
        :return: Liste von Anzeige-Strings
        """
        friends = self[user_id].friends()

        friend_names = [self.get_user_pretty_print_for_list(friend) for friend in friends]

        group_members = self.get_groupmembers(user_id)
        
        if group_members is None:
            return friend_names

        # entferne mich selbst aus der Gruppe, da ich ja weiß, dass ich (user_id) in der Gruppe bin
        group_members.remove(user_id)

        group_members_pp = [self.get_user_pretty_print_for_list(member) for member in group_members]

        return friend_names + group_members_pp

    def get_mutual_friends(self, user_id):
        """
        Ermittelt Freunde-von-Freunden (Zweiten-Grades) für `user_id` und zählt, wie oft jeder Kandidat
        mit Freunden von `user_id` verknüpft ist.

        :param user_id: in der Regel die aktuelle Nutzer-ID
        :return: Dictionary {user_id: anzahl_gemeinsamer_freunde}
        """
        friends = self[user_id].friends()
        mutual_friends_count = {}

        for friend in friends:
            friend_friends = self[friend].friends()
            for mutual_friend in friend_friends:
                if mutual_friend != user_id and mutual_friend not in friends:
                    if mutual_friend in mutual_friends_count:
                        mutual_friends_count[mutual_friend] += 1
                    else:
                        mutual_friends_count[mutual_friend] = 1

        return mutual_friends_count

    def suggest_friends(self, user_id, num_common_friends=2, distance_threshold=0.1, pretty_print=True):
        """Schlägt für `user_id` andere Nutzer als Freunde vor.

        Zwei Kriterien werden kombiniert:
        1. Nutzer, die mindestens `num_common_friends` gemeinsame Freunde mit `user_id` haben.
        2. Nutzer, die über das Freundesnetzwerk in bis zu 3 Graden verbunden sind und die
           räumlich näher als `distance_threshold` liegen (Distanz-Metrik: derzeit Manhattan/vereinfachte).

        Rückgabe:
            Liste von Nutzer-IDs (oder deren `pretty_print()`-Darstellung, falls `pretty_print=True`).
            Zuerst erscheinen Kandidaten mit vielen gemeinsamen Freunden, danach nahe Kandidaten.
        """
        mutual_friends_count = self.get_mutual_friends(user_id)

        suggested_friends = []

        # Teil 1: Kandidaten mit mindestens num_common_friends gemeinsamen Freunden, absteigend sortiert
        common_candidates = [uid for uid, cnt in mutual_friends_count.items() if cnt >= num_common_friends]
        common_candidates.sort(key=lambda uid: mutual_friends_count[uid], reverse=True)

        # Teil 2: Nutzer, die innerhalb des Freundesgraphen (bis Grad 3) verbunden sind und nahe wohnen
        nearby_candidates = []
        for other_id in self.keys():
            if other_id == user_id:
                continue
            if other_id in self[user_id].friends():
                continue
            # consider only users connected within 3 degrees
            if self.are_users_connected(user_id, other_id, degree=3):
                dist = self.calc_distance_between_users(user_id, other_id)
                if dist <= distance_threshold:
                    nearby_candidates.append((other_id, dist))

        nearby_candidates.sort(key=lambda x: x[1])
        nearby_ids = [uid for uid, _ in nearby_candidates]

        # Kombiniere die Ergebnisse: zuerst gemeinsame Freunde, danach nahe Kandidaten ohne Duplikate
        combined = common_candidates + [uid for uid in nearby_ids if uid not in common_candidates]

        if pretty_print:
            return [self[uid].pretty_print() for uid in combined]

        return combined

    def rate_user(self, user_id: str, stars: int):
        """Bewerte `user_id` mit `stars` und aktualisiere die Top-Rated-DS.

        Diese Methode sollte anstelle von direktem Aufruf von `users[user_id].rate_user()`
        verwendet werden, damit die interne Bewertungs-Heap-Struktur aktuell bleibt.
        """
        if user_id not in self:
            raise KeyError("User not found")
        # delegiere an das User-Objekt
        self[user_id].rate_user(stars)
        # aktualisiere Heap mit neuer Mittelbewertung
        new_mean = self[user_id].get_rating_stars_mean()
        self._rating_heap.update_user(user_id, new_mean)

    def get_top_rated_user(self, with_num_stars=False):
        """Gibt den Top-bewerteten Nutzer zurück (unter Verwendung der Heap-Struktur).

        Falls mit `with_num_stars=True`, wird ein Tupel (mean_stars, user_id) zurückgegeben.
        """
        top = self._rating_heap.get_top_user()
        if not top:
            return None
        mean, uid = top
        if with_num_stars:
            return [mean, uid]
        return uid

    def are_users_connected(self, user_id1, user_id2, degree=3):
        """Überprüft, ob zwei Nutzer über das Freundesnetzwerk innerhalb einer
        maximalen Verbindungsdistanz `degree` verbunden sind.

        Implementierung: Breitensuche (BFS) im Freundesgraphen bis zur Tiefe `degree`.
        Rückgabe: `True`, falls `user_id2` innerhalb von `degree`-Kanten von `user_id1` erreichbar ist.
        """
        if user_id1 not in self or user_id2 not in self:
            return False

        if user_id1 == user_id2:
            return True

        # BFS bis zur vorgegebenen Tiefe (degree)
        from collections import deque

        visited = set([user_id1])
        queue = deque()
        queue.append((user_id1, 0))

        while queue:
            current, dist = queue.popleft()
            if dist >= degree:
                continue
            for friend in self[current].friends():
                if friend == user_id2:
                    return True
                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, dist + 1))

        return False

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    def _read_users_from_csvfile(self, csvfile):
        """
        Liest die angegebene CSV-Datei ein, die alle Studierenden dieses Semesters enthält
        (GM-ID, Namen, Praktikumsgruppennummer, GPS-Koordinaten, Adresse).

        :param csvfile: Pfad zur CSV-Datei mit den Studierendendaten
        """
        with open(csvfile, newline='', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            # Überspringe die Header-Zeile
            next(csvreader)

            # private member variable mit den Praktikumsgruppennummern der Studierenden
            # in der Reihenfolge, in der die Datensätze aus der CSV-Datei gelesen werden
            self._groupnumbers = []

            for row in csvreader:
                user_id, name_family, name_first, password, groupnum, gps_coords, address = row
                # macht aus String wieder das Tuple mit long und lat Koordinaten
                gps_coords = eval(gps_coords)
                self.add(user_id, password, name_family, name_first, gps_coords, address)
                self._groupnumbers.append(groupnum)

    def _read_friends_csv(self, file_path):
        """
        Liest die `friends.csv` ein und fügt Freundschaftsbeziehungen zu den User-Objekten hinzu.

        :param file_path: Pfad zur `friends.csv`-Datei
        """
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Überspringe die Header-Zeile
            for row in csvreader:
                user_id = row[0]
                friends = row[1].split(', ')
                self[user_id].friends_add_list(friends)
                for friend in friends:  # gehe alle Freunde durch und füge user_id ebenfalls als Freund hinzu
                    self[friend].friends_add(user_id)

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***
