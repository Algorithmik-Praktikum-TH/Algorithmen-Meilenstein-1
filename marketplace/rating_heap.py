"""Ein einfacher Max-Heap für Benutzerbewertungen.

Dieses Modul verwendet eine "lazy"-Heap-Strategie: beim Aktualisieren eines Nutzers
wird ein neuer Eintrag in den Heap geschoben und die aktuelle Bewertung in einem
Dictionary gehalten. Beim Lesen der Top-Nutzer werden veraltete Einträge entfernt.

Die Vereinfachung vermeidet komplexe Index-Updates und ist ausreichend für die
Aufgabenstellung (Effizienz: push O(log n), get_top amortisiert O(log n)).
"""
import heapq


class RatingHeap:
    def __init__(self):
        # interne Min-Heap mit negierten Werten, damit wir ein Max-Verhalten erhalten
        self._heap = []  # list of tuples (-mean_stars, user_id)
        # Aktuelle mittlere Bewertung pro Nutzer (oder fehlt => Nutzer nicht vorhanden)
        self._means = {}

    def add_user(self, user_id, mean_stars: float):
        if user_id in self._means:
            return
        self._means[user_id] = mean_stars
        heapq.heappush(self._heap, (-mean_stars, user_id))

    def update_user(self, user_id, mean_stars: float):
        # lazy update: schreibe neue Bewertung ins Dictionary und push in Heap
        self._means[user_id] = mean_stars
        heapq.heappush(self._heap, (-mean_stars, user_id))

    def remove_user(self, user_id):
        if user_id in self._means:
            del self._means[user_id]

    def get_top_user(self):
        """Gibt das Tupel (mean_stars, user_id) des aktuell besten Nutzers zurück.

        Falls keine Nutzer vorhanden sind, wird None zurückgegeben.
        Alte/stale Heap-Einträge werden bei Bedarf entfernt.
        """
        while self._heap:
            neg_mean, uid = self._heap[0]
            current = self._means.get(uid)
            # falls Nutzer entfernt oder die Bewertung inzwischen anders ist,
            # entferne das veraltete Heap-Element
            if current is None:
                heapq.heappop(self._heap)
                continue
            if -neg_mean != current:
                heapq.heappop(self._heap)
                continue
            return (current, uid)
        return None
