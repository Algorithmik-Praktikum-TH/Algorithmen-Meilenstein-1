**Kurzfassung der wichtigen Änderungen**
- **`marketplace/rating_heap.py`**: Neue Hilfsklasse `RatingHeap` eingeführt, um Top-bewertete Nutzer effizient abzufragen (lazy max-heap).
- **`marketplace/users.py`**: Integration des `RatingHeap` bei Initialisierung; neue Methoden `rate_user(user_id, stars)` und `get_top_rated_user()` zentralisieren Bewertungsvorgänge und halten Heap synchron. Außerdem: Friend-suggestion- und Connectivity-Methoden implementiert bzw. erweitert.
- **`marketplace/simulator.py`**: Simulator so angepasst, dass er `users.rate_user(...)` verwendet (aktualisiert damit intern den Rating-Heap).
- **`marketplace/auctions.py`**: `get_top_rated_user()` delegiert an `Users.get_top_rated_user()`; `bid_in_auction()` leitet `users_map` an `Auction.bid()` weiter (Porto-Berechnung möglich).
- **`marketplace/auction.py`**: Porto-Berechnung `calculate_portofee(...)` implementiert (Haversine-Annäherung: 0,1 € pro 5 km) mit einem pauschalen Fallback.
- **`marketplace/max_heap.py`**: Entfernen der künstlichen NotImplemented-Barriere; Heap-Operationen gepflegt und getestet.
- **`marketplace/praktikumsgruppen.py`**: Union-Find Helfer (`_praktikumsgruppe`, `find_root()`, `union_with()`) implementiert und `create_groups()`/`get_groupmembers()` erweitert.
- **`auctionapp_init.py`**: Trie-Initialisierung ergänzt, um auch `user_id`s in die Autocomplete-Struktur einzufügen.

**Begründung der Änderungen**
- Rating-Heap (`RatingHeap`):
  - Ziel: effizienten Zugriff auf den aktuell besten Nutzer ermöglichen (Aufgabenstellung verlangt Top-rated-User-Abfrage).
  - Entscheidung: Lazy-Heap-Strategie (push-on-update + map) — einfacher und robust für die erwartete Datengröße.

- Integration in `Users`:
  - Zentralisierung der Bewertungslogik durch `Users.rate_user()` verhindert Inkonsistenzen und hält die Heap-Struktur synchron.

- Porto-Berechnung in `Auction`:
  - Anforderungen: Porto proportional zur Distanz (0,1 € pro 5 km).
  - Entscheidung: Haversine-Approximation statt Road-Distance (z. B. `osmnx`) um zusätzliche Abhängigkeiten und Netzwerkanforderungen zu vermeiden.

- Max-Heap:
  - Aufgabe verlangte die Anzeige der aktivsten Auktion; die frühere Blockade (NotImplementedError) wurde entfernt, damit die Klasse instanziierbar und testbar ist.

- Union-Find (`praktikumsgruppen`):
  - Ziel: zuverlässiges Management von Praktikumsgruppen als disjunkte Mengen; Implementierung orientiert sich an Standard-Union-Find-Prinzipien.

**Konkrete Änderungen (Datei-für-Datei, kurz)**
- `marketplace/rating_heap.py` (neu): `RatingHeap` mit `add_user`, `update_user`, `remove_user`, `get_top_user`.
- `marketplace/users.py` (modifiziert): `_rating_heap` initialisiert, `rate_user()` und `get_top_rated_user()` hinzugefügt, Friend-suggestion und BFS-Connectivity implementiert/ergänzt.
- `marketplace/simulator.py` (modifiziert): Simulator verwendet `users.rate_user()` zur Aktualisierung der Ratings.
- `marketplace/auctions.py` (modifiziert): Delegation von `get_top_rated_user()` an `Users`; `bid_in_auction()` übergibt `users_map` an `Auction.bid()`.
- `marketplace/auction.py` (modifiziert): Implementierung von `calculate_portofee()` (Haversine) und optionale Nutzung beim Bieten.
- `marketplace/max_heap.py` (modifiziert): Entfernen des initialen NotImplemented-Blocks; Implementierung der Heap-Methoden belassen und kleinere Korrekturen vorgenommen.
- `marketplace/praktikumsgruppen.py` (modifiziert): Union-Find-Helfer ergänzt.
- `auctionapp_init.py` (modifiziert): Trie befüllt jetzt zusätzlich mit `user_id`s.
