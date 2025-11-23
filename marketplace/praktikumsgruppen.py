# Definiert die Klassen Praktikumsgruppen und SetNode, implementiert als Dictionary


class SetNode:
    """
    Knoten für die Implementierung einer disjunkten Mengenstruktur (Union-Find).

    Hinweis: Die Klasse `user.User` erbt in Praktikum 3 von `SetNode`. Für Praktikum 1
    und 2 ist dies nicht zwingend erforderlich, wird hier aber vorbereitet.

    Attribute:
        _parent (SetNode): Elternknoten in der Union-Find-Struktur (Standard: sich selbst).
        _weight (int): Gewicht / Größe des (Teil-)Baums, der in diesem Knoten verwurzelt ist.
        _praktikumsgruppe: Optionaler Bezeichner der Praktikumsgruppe (kann verwendet werden).
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """
        Initializes a new SetNode.
        """
        # TODO: werden nur für Praktikum 3 benötigt
        self._parent = self  # parent Knoten des SetNode Objekts. self bedeutet, dass der Knoten ein Wurzelknoten ist
        self._weight = 1  # Gewicht (Anzahl Knoten) des (Teil-)Baumes, der in dem SetNode Objekt verwurzelt ist
        # Praktikumsgruppe id (optional, can be used to store assigned group number)
        self._praktikumsgruppe = None

    def find_root(self):
        """Gibt die Wurzel dieses SetNode zurück und führt dabei Pfadkompression durch.

        Rückgabe: Das Wurzel-`SetNode`-Objekt der aktuellen Menge.
        """
        if self._parent is not self:
            self._parent = self._parent.find_root()
        return self._parent

    def union_with(self, other):
        """Vereint die Menge dieses Knotens mit der Menge eines anderen Knotens.

        Es wird weighted union verwendet (das größere Teilbaum bleibt Wurzel),
        damit die Baumhöhe gering gehalten wird.

        Rückgabe: Die neue Wurzel der vereinigten Menge.
        """
        root1 = self.find_root()
        root2 = other.find_root()
        if root1 is root2:
            return root1
        # attach smaller tree to larger
        if root1._weight >= root2._weight:
            root2._parent = root1
            root1._weight += root2._weight
            return root1
        else:
            root1._parent = root2
            root2._weight += root1._weight
            return root2

    def weight(self):
        """Gibt das Gewicht (Anzahl Knoten) des aktuellen Wurzelknotens zurück."""
        return self._weight

    # *** PUBLIC SET methods ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden

    # *** PUBLIC methods to return class properties ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden


class Praktikumsgruppen(dict):
    """
    In Praktikum 1 und 2: Dictionary mit allen Studierenden. Die Klasse `users.Users` erbt von dieser Klasse.
    In Praktikum 3: Repräsentiert eine Sammlung disjunkter Mengen zur Gruppierung von Nutzern in Praktikumsgruppen.

    Methodenhinweis:
        find(node): Liefert die Wurzel der Menge, die den Knoten enthält (mit Pfadkompression).
        find_byid(user_id, return_id=False): Sucht die Wurzel der Menge des Nutzers anhand der ID.
        union(user_id1, user_id2): Vereinigt die Mengen der beiden Nutzer.
        create_groups(user_ids, groupnumbers): Erstellt Gruppen anhand gegebener Nutzer-IDs und Gruppennummern.
        get_groupmembers(user_id): Liefert die Mitglieder der Gruppe des angegebenen Nutzers.
        print_ds(): Gibt die Disjoint-Set-Struktur aus.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """
        Initialisiert ein neues `Praktikumsgruppen`-Objekt.
        """
        super().__init__()
        self._group_map = {}  # user_id -> groupnumber*
        self._groups = {}     # groupnumber -> set(user_id)*

    # Disjoint-set methods for Praktikum 3
    def find(self, node):
        """Finde die Wurzel des gegebenen `SetNode`-Objekts.

        Diese Methode dient als Wrapper für `SetNode.find_root`.
        """
        return node.find_root()

    # *** PUBLIC methods ***

    # TODO in Praktikum 3: implement find(node), find_byid(user_id, return_id=False) and
    #  union(user_id1, user_id2)

    # die Methode existiert nur aus Kompatibilitätsgründen und wird im 3. Praktikum implementiert
    def find_byid(self, user_id, return_id=False):
        """
        Ermittelt die Wurzel der Menge (Praktikumsgruppe), in der der Nutzer mit `user_id` enthalten ist.

        :param user_id: Nutzer-ID
        :param return_id: Wenn True, wird die ID der Wurzel zurückgegeben, sonst das `SetNode`-Objekt
        :return: `SetNode` oder die Wurzel-ID (abhängig von `return_id`)
        """

        # Wenn der Nutzer nicht existiert, None zurückgeben
        if user_id not in self:
            return None
        node = self[user_id]
        root = node.find_root()
        if return_id:
            # Versuche die ID der Wurzel zurückzugeben (sofern die Klasse eine id()-Methode hat)
            try:
                return root.id()
            except Exception:
                return None
        else:
            return root

    def create_groups(self, user_ids, groupnumbers):
        """
        Erstellt Gruppen aus den gegebenen Nutzer-IDs und Gruppennummern.

        :param user_ids: Liste von Nutzer-IDs
        :param groupnumbers: Liste mit Gruppennummern entsprechend den Nutzer-IDs
        """
        # Erstellt die Zuordnung Benutzer -> Gruppennummer (_group_map) und die
        # Umkehrabbildung Gruppennummer -> Benutzermenge (_groups). Zusätzlich
        # werden benachbarte Benutzer mit gleicher Gruppennummer im Union-Find
        # miteinander vereinigt, sofern die Benutzerobjekte die SetNode-API
        # unterstützen.
        self._group_map = {}
        self._groups = {}

        for uid, gnr in zip(user_ids, groupnumbers):
            self._group_map[uid] = gnr
            if gnr not in self._groups:
                self._groups[gnr] = set()
            self._groups[gnr].add(uid)

        # Repräsentant pro Gruppe wählen und alle weiteren Mitglieder mit ihm unionieren
        reps = {}
        for uid, gnr in zip(user_ids, groupnumbers):
            if gnr not in reps:
                reps[gnr] = uid
            else:
                try:
                    self[reps[gnr]].union_with(self[uid])
                except Exception:
                    # Falls die Einträge keine SetNode-Methoden bieten, wird die Union übersprungen
                    pass
        

    # *** PUBLIC GET methods ***

    def get_groupmembers(self, user_id):
        """
        Gets the members of the group containing the user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of user IDs in the same group.
        """
        # Bestimme die Gruppenmitglieder. Falls Union-Find vorhanden ist, nutze
        # die Wurzel-ID zur Bestimmung aller Mitglieder, ansonsten greife auf die
        # einfache Mapping-Implementierung zurück.
        if user_id not in self:
            return []

        try:
            root_id = self.find_byid(user_id, True)
            members = [uid for uid in self.keys() if self.find_byid(uid, True) == root_id]
            return members
        except Exception:
            gnr = self._group_map.get(user_id)
            if gnr is None:
                return []
            return list(self._groups[gnr])
        

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***
