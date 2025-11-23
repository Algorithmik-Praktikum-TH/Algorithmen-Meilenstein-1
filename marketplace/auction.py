# Definiert die Klasse Auction.
# In einer Auktion wird ein Item, das von einem User versteigert wird (seller_id), an einen anderen User versteigert
# (purchaser_id). Es können mehrere User bei einer Auktion bieten, diese werden im Heap _users_bidding gespeichert

import heapq
import marketplace.user
import marketplace.item
import marketplace.stack
import random
from datetime import datetime, timedelta


class Auction:
    """
    Repräsentiert eine Auktion.

    Attribute:
        _id (str): Auktions-ID
        _item (marketplace.item.Item): Artikel, der in dieser Auktion verkauft wird
        _seller_id (str): Verkäufer-ID
        _purchaser_id (str): Käufer-ID (None zu Beginn; nach Auktionsende ggf. eine ID)
        _auction_ends (datetime): Zeitpunkt, wann die Auktion endet
        _recommended2users (set): Menge von Nutzer‑IDs, denen diese Auktion empfohlen wird
        _users_bidding (heap): Min-Heap der Gebote; das höchste Gebot liegt an der Wurzel (negativer Betrag)
        _bids_ordered (stack): Gebote in chronologischer Reihenfolge (Stack)
    """

    # *** CONSTRUCTORS ***
    def __init__(self, auction_id: str, user_id: str, item: marketplace.item.Item) -> None:
        """

        :param auction_id: id of auction
        :param user_id: id of seller in this auction
        :param item: das item, das in der Auktion verkauft wird
        """
        self._id = auction_id

        self._item = item

        self._seller_id = user_id
        self._purchaser_id = None       # noch hat niemand das Produkt gekauft

        # Uhrzeit inklusive datum, wann Auktion ausläuft.
        self._auction_ends = datetime.now() + timedelta(seconds=random.randint(45, 1200))

        # Menge von Nutzern, denen diese Auktion empfohlen wird.
        # Empfohlen wird z.B., weil Freunde Interesse zeigen oder der Nutzer ähnliche Artikel gekauft/geboten hat.
        self._recommended2users = set()

        # Verwende einen Heap, um neue Gebote effizient zu verwalten (min-Heap).
        self._users_bidding = []

        # Gebote aller Nutzer in der Reihenfolge, in der sie abgegeben wurden; das letzte Gebot liegt oben auf dem Stack.
        self._bids_ordered = marketplace.stack.Stack()

    # *** PUBLIC SET methods ***

    def set_purchaser_id(self):
        """
        Sets _purchaser_id to id of purchaser or to "Kein Bieter" but only if auction is expired
        :return:
        """
        if self.expired():
            self._purchaser_id = self.get_highest_bidder()
        else:
            raise ValueError("set_purchaser_id() darf noch nicht aufgerufen werden, da Auktion noch nicht zu Ende ist!")

        return self._purchaser_id

    def recommend2user(self, user_id):
        self._recommended2users.add(user_id)

    # *** PUBLIC methods ***

    def bid(self, user: marketplace.user.User, bid_amount, users_map=None):
        """
        Lets the given user bid on this auction with the amount bid_amount.

        :param user: Nutzer, der bieten möchte
        :param bid_amount: Gebotsbetrag in €
        :param users_map: Optionales Mapping aller Nutzer (Benutzer-ID -> User-Objekt). Wird benötigt,
                  um bei Bedarf das Porto anhand der GPS-Koordinaten zu berechnen.
        :return: True, falls das Gebot erfolgreich platziert wurde, sonst False
        """
        if bid_amount > user.balance():         # has user enough money?
            return False

        if bid_amount < self._item.value_min():     # is bid_amount above the minimum bid?
            return False

        user_id = user.id()

        portofee = self.calculate_portofee(buyer=user, users_map=users_map)

        # check whether user already bid before. If yes then check if new bid is higher than previous one.
        # if higher, then decrease balance only by the difference between both bids
        # muss dann auch in _bids_ordered den entsprechenden eintrag löschen und in _users_bidding auch oder dort den
        # betrag und den heap aktualisieren

        old_bid = self.get_bid_of_user(user_id)

        if old_bid is None or old_bid < bid_amount:

            if old_bid is not None:     # dann gibt es schon ein Gebot von user_id

                # Porto wurde schon im ersten Gebot abgezogen, deshalb muss es nicht nochmal abgezogen werden
                portofee = 0

                for item in self._bids_ordered:
                    if item[0] == user_id:
                        self._bids_ordered.remove(item)

            else:
                old_bid = 0     # setze old_bid von None auf 0, um unten damit rechnen zu können

            heapq.heappush(self._users_bidding, (-bid_amount, user_id))

            self._bids_ordered.push((user_id, bid_amount))

            user.decrease_balance(bid_amount + portofee - old_bid)

            # eine auktion, die user empfohlen wurde, muss jetzt nicht mehr empfohlen werden, da user
            # ja jetzt bietet
            if self.is_recommended2user(user_id):
                self._recommended2users.remove(user_id)

            return True
        else:
            return False
        
    def calculate_portofee(self, buyer=None, users_map=None):
        """
        Berechnet Porto für die Lieferung der Bestellung. Porto ist abhängig von Distanz zwischen Käufer
        und Verkäufer
        :return: Porto in Euro
        """
        # Wenn `buyer` und `users_map` übergeben werden, berechne das Porto anhand
        # der Distanz zwischen Käufer und Verkäufer (Haversine-Formel). Diese
        # Implementierung dient als praktikable Näherung (Teilprojekt 3).
        # Fallback: Pauschalbetrag für einfache Übungszwecke.
        if buyer is not None and users_map is not None and self._seller_id in users_map:
            try:
                seller = users_map[self._seller_id]
                # both buyer and seller have gps_coords() -> (lat, lon)
                b_coords = buyer.gps_coords()
                s_coords = seller.gps_coords()

                if b_coords is None or s_coords is None:
                    return 0.0

                # Haversine formula to compute distance in kilometers
                from math import radians, sin, cos, sqrt, atan2

                lat1, lon1 = b_coords
                lat2, lon2 = s_coords

                R = 6371.0  # Earth radius in km
                dlat = radians(lat2 - lat1)
                dlon = radians(lon2 - lon1)
                a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance_km = R * c

                # Preis: 0,1 € pro 5 km (wie in der Aufgabenstellung angegeben)
                fee = 0.1 * (distance_km / 5.0)
                # Auf Cent runden
                return round(fee, 2)
            except Exception:
                return 0.0

        # Basic fallback
        return 2.0
    # *** PUBLIC GET methods ***

    def sold(self):
        """

        :return: True, falls die Auktion abgelaufen ist UND eine Käufer-ID gesetzt wurde
             (bei keinem Käufer ist `_purchaser_id == "Kein Bieter"`).
        """
        return self._purchaser_id is not None

    def sold_success(self):
        """

        :return: True, falls die Auktion abgelaufen ist und eine Käufer-ID gesetzt wurde
        """
        return self._purchaser_id is not None and self._purchaser_id != "Kein Bieter"

    def expired(self):
        """

        :return: True, falls die Auktion abgelaufen ist, sonst False
        """
        return datetime.now() >= self._auction_ends

    def pretty_print(self, with_sold_by=True, user_id=None):
        if with_sold_by:
            return "ID: {0} Name: {1} Mindestgebot: {2} € \tHöchstes Gebot: {3} € \tAuktionsende: {4} \tVerkäufer: {5}".format(
                self._id.ljust(15), self._item.name().ljust(30), self._item.value_min(),
                self.get_highest_bid(),
                marketplace.auction.Auction.format_datetime(self._auction_ends), self._seller_id.ljust(10))
        elif user_id is not None:
            return "ID: {0} Name: {1} Mindestgebot: {2} € \tHöchstes Gebot: {3} € \tIhr Gebot: {4} € \tAuktionsende: {5}".format(
                self._id.ljust(15), self._item.name().ljust(30), self._item.value_min(),
                self.get_highest_bid(), self.get_bid_of_user(user_id),
                marketplace.auction.Auction.format_datetime(self._auction_ends))
        else:
            return "ID: {0} Name: {1} Mindestgebot: {2} € \tHöchstes Gebot: {3} € \tAuktionsende: {4}".format(
                self._id.ljust(15), self._item.name().ljust(30), self._item.value_min(),
                self.get_highest_bid(),
                marketplace.auction.Auction.format_datetime(self._auction_ends))

    def get_highest_bid(self):
        """

        :return: Höchstes Gebot in dieser Auktion in Euro
        """
        if not self._users_bidding:
            return 0.0
        return -self._users_bidding[0][0]  # Negativ, weil wir einen min-Heap verwenden

    def get_highest_bidder(self) -> str:
        """

        :return: Nutzer-ID des höchsten Bieters dieser Auktion
        """
        if not self._users_bidding:
            return "Kein Bieter"
        return self._users_bidding[0][1]

    def get_item_name(self):
        return self._item.name()

    def get_item_value_min(self):
        return self._item.value_min()

    def get_item_description(self):
        return self._item.description()

    def get_time_left(self):
        return (self._auction_ends - datetime.now()).total_seconds()

    def is_user_bidding(self, user_id):
        return any(id_bidder == user_id for _, id_bidder in self._users_bidding)

    def is_any_bidder(self):
        return bool(self._users_bidding)

    def get_bid_of_user(self, user_id):
        """

        :param user_id: Nutzer-ID
        :return: Gebotswert, den der angegebene Nutzer abgegeben hat; falls kein Gebot vorhanden ist, wird `None` zurückgegeben
        """
        # minuszeichen wegen min-heap
        return next((-value for value, id_bidder in self._users_bidding if id_bidder == user_id), None)

    def is_recommended2user(self, user_id):
        if self.is_user_bidding(user_id) and user_id in self._recommended2users:
            self._recommended2users.remove(user_id)
        # auction soll nur empfohlen werden, wenn user_id nicht schon auf Auktion bietet
        return user_id in self._recommended2users  # and not self.is_user_bidding(user_id)

    def get_last_bid(self):
        return self._bids_ordered.peek()

    # *** PUBLIC STATIC methods ***

    @staticmethod
    def get_id_from_pretty_print(printed_auction):
        printed_auction = printed_auction.split("Name: ")
        return printed_auction[0][4:].rstrip()

    @staticmethod
    def format_datetime(dt):
        now = datetime.now()
        today = now.date()
        tomorrow = today + timedelta(days=1)
        dt_date = dt.date()

        if dt_date == today:
            return dt.strftime("heute, %H:%M Uhr")
        elif dt_date == tomorrow:
            return dt.strftime("morgen, %H:%M Uhr")
        else:
            delta = (dt_date - today).days
            return dt.strftime(f"in {delta} Tagen, %H:%M Uhr")

    # *** PRIVATE methods ***

    # *** PUBLIC methods to return class properties ***

    def id(self):
        return self._id

    def seller_id(self):
        return self._seller_id

    def purchaser_id(self):
        return self._purchaser_id

    def auction_ends(self):
        return self._auction_ends

    def item(self):
        return self._item

    def users_bidding(self):
        return self._users_bidding

    def recommended2users(self):
        return self._recommended2users

    def bid_count(self):
        return len(self._users_bidding)

    # *** PRIVATE variables ***
