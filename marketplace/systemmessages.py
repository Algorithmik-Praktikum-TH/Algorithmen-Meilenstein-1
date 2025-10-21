# Definiert die Klasse SystemMessages
# über die Methode push() können Nachrichten in der Warteschlange gespeichert werden.
# Nachrichten in der Warteschlange werden nacheinander in dem tk.Label _lbl_sysmessage
# für 5 Sekunden angezeigt, bis keine Nachrichten mehr in der Warteschlange existieren.
# in der GUI werden diese Nachrichten oben links angezeigt.

import tkinter as tk


class SystemMessages:
    # *** CONSTRUCTORS ***
    def __init__(self, label: tk.Label):
        self._queue = []
        self._lbl_sysmessage = label
        self._displaying = False

    # *** PUBLIC SET methods ***

    # *** PUBLIC methods ***

    def push(self, message):
        self._queue.append(message)
        if not self._displaying:
            self._display_next_message()

    # *** PUBLIC GET methods ***

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    def _display_next_message(self):
        if not self._queue:
            self._displaying = False
            self._lbl_sysmessage.config(text="-", bg='#d9d9d9')
            return

        self._displaying = True
        message = self._queue.pop(0)
        self._lbl_sysmessage.config(text=message, bg='yellow')

        if len(self._queue) == 0:
            display_time = 15  # 15 seconds for the last message
        else:
            display_time = 3  # 3 seconds for other messages

        # Schedule the next message display
        self._lbl_sysmessage.after(display_time * 1000, self._display_next_message)

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***
