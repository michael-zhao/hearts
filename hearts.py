from random import *
import pyfiglet
import tabulate

class Deck:
    """Creates a deck of cards 2,3,4,5,6,7,8,9,10,J,K,Q,A with suits Spades, Clubs, Hearts, & Diamonds."""
    ranks = [str(x) for x in range(2, 11)] + list('JQKA')
    suits = ['spades', 'clubs', 'hearts', 'diamonds']
    def __init__(self):
        """Initializes a deck."""
        super().__init__()
        self.cards = [(x, y) for x in Deck.ranks for y in Deck.suits]

class Player:
    """Creates a player with a hand of cards."""
    def __init__(self):
        """Initializes a player with an empty hand and a score."""
        super().__init__()
        self.hand = set()
        self.score = 0

class Game:
    """Records the Hearts game state."""
    def __init__(self):
        """Creates a deck of cards, 4 players, and turn count."""
        super().__init__()
        self.deck = Deck()
        self.p1 = Player() # player-controlled
        self.p2 = Player()
        self.p3 = Player()
        self.p4 = Player()
        self.players = [self.p1, self.p2, self.p3, self.p4]
        self.turn = 0 # starts turn (trick/round) 0
    
    def deal(self):
        """Deals 13 random cards to each of the 4 players."""
        for player in self.players:
            while len(player.hand) < 13:
                player.hand.add(self.deck.cards[randint(0,51)])

    def player_discard(self, cards: list, direction: str): 
        """Discards (passes) 3 cards in the desired direction."""
        # print(cards)
        # print(self.p1.hand)
        for card in cards:
            # print("inner loop")
            self.p1.hand.remove(card)
            if direction == "left":
                self.p2.hand.add(card)
            if direction == "right":
                self.p4.hand.add(card)
            if direction == "top":
                self.p3.hand.add(card)
            else:
                pass
    
    def player_add(self, cards: list, direction: str):
        """
        Receives 3 cards from the player in the opposite direction 
        (e.g. direction=left comes from the right).
        """
        pass

    def round(self):
        """Progresses through a round, ends when each player's hand is empty (len(hand)=0)."""
        score_table = [["Player 1", self.p1.score], ["Player 2", self.p2.score], ["Player 3"
            , self.p3.score], ["Player 4", self.p4.score]]
        print(tabulate.tabulate(score_table))
        self.deal()
        sorted_hand = sorted(self.p1.hand, key=lambda x: (x[1], x[0]))
        for rank, suit in sorted_hand:
            print(rank + " of " + suit)
        discard_direction = "left" if self.turn % 4 == 0 else "right" \
            if self.turn % 4 == 1 else "top" if self.turn % 4 == 2 else "pass"
        cards = input("choose the cards you want to discard to the " + discard_direction.upper() + 
            ", demarcated with commas: \n").split(',')
        f_cards = [(card.split()[0], card.split()[2]) for card in cards]
        self.player_discard(f_cards, discard_direction)
        # print("turn: " + str(self.turn))
        print(self.p1.hand)
        if self.turn == 0: #whoever has 2 of clubs has to go first
            if (2, 'clubs') in self.p1.hand:
                print("you must play the 2 of clubs to start the game")
            else:
                found = False
                while not found:
                    for player in self.players:
                        if (2, 'clubs') in player.hand:
                            found = True
                

def main():
    print(pyfiglet.figlet_format("HEARTS"))
    a_game = Game()
    a_game.round()

main()
    