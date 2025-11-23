import threading
import random
import time
import marketplace.users


class Simulator:
    def __init__(self):
        self.stop_simulation = False

    def place_random_bids(self, auctions, current_user_id, num_auctions=10):
        if self.stop_simulation:
            return

        users = auctions.users()

        user_ids = [user_id for user_id in users.keys() if user_id != current_user_id]

        auctions._place_random_bids(num_auctions, user_ids, True, current_user_id)

    def create_random_auctions(self, auctions, current_user_id):
        if self.stop_simulation:
            return

        user_ids = [user_id for user_id in auctions.users().keys() if user_id != current_user_id]

        for _ in range(5):
            random_user = random.choice(user_ids)
            item_name = "Kartoffelschäler"
            description = ""
            value_min = 1
            auctions.add_new_auction(random_user, item_name, description, value_min)

    def randomly_rate_users(self, users: marketplace.users.Users, current_user_id):
        if self.stop_simulation:
            return

        user_ids = [user_id for user_id in users.keys() if user_id != current_user_id]

        for _ in range(35):
            random_user = random.choice(user_ids)
            stars = random.randint(1,5)
            # Verwende die Users.rate_user-Methode, damit intern die Heap-Struktur aktualisiert wird
            try:
                users.rate_user(random_user, stars)
            except Exception:
                # defensive: falls etwas schief geht, fange das ab und setze fort
                pass

    def stop(self):
        self.stop_simulation = True


