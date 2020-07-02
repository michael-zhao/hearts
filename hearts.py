from random import *
import pyfiglet
import tabulate
import colorama

colorama.init() # initializes colorama
class Card:
    """Creates a Card object."""
    def __init__(self, rank, suit):
        super().__init__()
        greater_than_ten = {11: "J", 12: "Q", 13: "K", 14: "A"}
        less_than_ten = {x: str(x) for x in range(2, 11)}
        self.dct = {**less_than_ten, **greater_than_ten}
        self.rank = rank
        self.suit = suit
        self.card = (self.rank, self.suit)
    
    def __repr__(self): # for me
        return f"({self.rank}, {self.suit})"

    def __str__(self): # for end user
        if self.suit == "hearts":
            suit_color = colorama.Fore.RED + '\u2665'
        if self.suit == "diamonds":
            suit_color = colorama.Fore.RED + '\u2666'
        elif self.suit == "spades":
            suit_color = '\u2660'
        elif self.suit == "clubs":
            suit_color = '\u2663'
        return self.dct[self.rank] + suit_color + colorama.Style.RESET_ALL

    def __getitem__(self):
        return Card(rank, suit)
    
    def __setitem__(self, rank, suit):
        self.card = (rank, suit)

class Deck:
    """Creates a deck of cards 2,3,4,5,6,7,8,9,10,J,K,Q,A with suits Spades, Clubs, Hearts, & Diamonds."""
    ranks = [x for x in range(2, 15)]
    #  + list('JQKA')
    suits = ['spades', 'clubs', 'hearts', 'diamonds']
    def __init__(self):
        """Initializes a deck."""
        super().__init__()
        self.cards = [Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]

class Player:
    """Creates a player with a hand of cards."""
    def __init__(self):
        """Initializes a player with an empty hand and a score."""
        super().__init__()
        self.hand = []
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
                rand_card = self.deck.cards[randint(0,51)]
                if rand_card not in player.hand:
                    player.hand.append(rand_card)

    def player_discard(self, cards: list, direction: str): 
        """Discards (passes) 3 cards in the desired direction."""
        # print(cards)
        # print(self.p1.hand)
        if direction == "pass":
            pass
        for card in cards:
            # print("inner loop")
            self.p1.hand.remove(card)
            if direction == "left":
                self.p2.hand.add(card)
            if direction == "right":
                self.p4.hand.add(card)
            if direction == "top":
                self.p3.hand.add(card)
    
    def player_add(self, cards: list, direction: str):
        """
        Receives 3 cards from the player in the opposite direction 
        (e.g. direction=left comes from the right).
        """
        # TODO: implement player from opposite direction gives you 3 cards
        pass

    def pre_round(self):
        """Progresses through a round, ends when each player's hand is empty (len(hand)=0)."""
        # uses tabulate to print a table of scores at the beginning of each round
        score_table = [["Player 1", self.p1.score], ["Player 2", self.p2.score], ["Player 3"
            , self.p3.score], ["Player 4", self.p4.score]]
        print(tabulate.tabulate(score_table, headers=["Player", "Score"]))
        print()

        # deal all 52 cards to the 4 players (13 to each player)
        self.deal()

        # sort the player's hand (assuming p1 is the player); other players don't matter 
        # at least until multiplayer is implemented
        sorted_hand = sorted(self.p1.hand, key=lambda card: (card.suit, card.rank))
        # for rank, suit in sorted_hand:
        #     if rank == 11:
        #         rank = "J"
        #     elif rank == 12:
        #         rank = "Q"
        #     elif rank == 13:
        #         rank = "K"
        #     elif rank == 14:
        #         rank = "A"
        #     print(str(rank) + " of " + suit) # print each card in the player's hand
        print("Your hand:")
        for card in sorted_hand:
            print(card) # prints each card as formatted in Card.__str__()
        # print(sorted_hand) # this just prints the list, so no formatting
        
        # based on American rules (turn 1 left, turn 2 right, turn 3 up, turn 4 none, repeat)
        discard_direction = "left" if self.turn % 4 == 0 else "right" \
            if self.turn % 4 == 1 else "top" if self.turn % 4 == 2 else "pass"

        # use discard_direction and take user input for the desired discarded cards
        cards = input("Choose the cards you want to discard to the " + discard_direction.upper() + 
            ", demarcated with commas: \n").split(',')
        f_cards = [(card.split()[0], card.split()[2]) for card in cards]
        self.player_discard(f_cards, discard_direction)
        # TODO: figure out which cards to choose to pass (p2, p3, p4)
        # print("turn: " + str(self.turn))
        print(self.p1.hand)

    def round(self):
        if self.turn == 0: #whoever has 2 of clubs has to go first
            if (2, 'clubs') in self.p1.hand:
                print("You must play the 2 of clubs to start the game.")
            else:
                found = False
                while not found:
                    for player in self.players:
                        if (2, 'clubs') in player.hand:
                            found = True
                            # TODO: make the NPC w/2 of clubs start first; no one else can
                

def main():
    print(colorama.Fore.CYAN + pyfiglet.figlet_format("HEARTS") + colorama.Style.RESET_ALL)
    a_game = Game()
    a_game.pre_round()

main()
    