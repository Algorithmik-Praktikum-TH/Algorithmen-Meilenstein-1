# Definiert die Klasse Trie. Die Struktur wird verwendet, um alle Wörter zu finden, die mit einem gegebenen Präfix beginnen.

class TrieNode:
    """Ein Knoten der Trie-Struktur.

   Attribute:
       children: Dictionary, die Zeichen auf `TrieNode`-Kinder abbildet.
       _is_end_of_word: Boolescher Wert, der angibt, ob der Knoten das Ende eines Wortes darstellt.
   """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """Initialisiert einen `TrieNode` mit leerer Kinder-Dictionary und End-of-Word-Flag False."""
        self.children = {}
        self._is_end_of_word = False

    # *** PUBLIC SET methods ***

    def set_is_end_of_word(self):
        """
        Setzt das Flag `_is_end_of_word` auf True.
        """
        self._is_end_of_word = True

    # *** PUBLIC methods to return class properties ***

    def is_end_of_word(self):
        return self._is_end_of_word


class Trie:
    """Trie-Datenstruktur zum Speichern von Zeichenketten.

    Attribute:
        _root (TrieNode): Die Wurzel des Trie.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """Initialisiert das `Trie` mit einer Wurzel-`TrieNode`."""
        self._root = TrieNode()

    # *** PUBLIC methods ***

    def insert(self, word):
        """Fügt ein Wort in das Trie ein. Für jedes Zeichen wird ein Kindknoten erzeugt, falls noch nicht vorhanden.
        Der Knoten des letzten Zeichens wird als Wortende markiert.

        :param word: Das einzufügende Wort
        """
        word = word.lower()
        node = self._root
        for char in word:           # for each character of the word
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.set_is_end_of_word()

    # *** PUBLIC GET methods ***

    def search(self, prefix):
        """Sucht alle Wörter, die mit dem gegebenen Präfix beginnen.

        :param prefix: Das Präfix, nach dem gesucht werden soll
        :return: Liste mit allen passenden Wörtern
        """
        prefix = prefix.lower()
        node = self._root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return Trie._find_words(node, prefix)

    # *** PRIVATE methods ***

    @staticmethod
    def _find_words(node, prefix):
        """Findet rekursiv alle Wörter, die von diesem Knoten aus gebildet werden können.

        :param node: Startknoten
        :param prefix: Aktuelles Präfix von der Wurzel bis zu diesem Knoten
        :return: Liste gefundener Wörter
        """
        words = []
        if node.is_end_of_word():
            words.append(prefix)
        for char, next_node in node.children.items():
            words.extend(Trie._find_words(next_node, prefix + char))
        return words
