from random import *
import pyfiglet
import tabulate
import colorama
import functools

colorama.init() # initializes colorama

# @functools.total_ordering
class Card:
    """
    A Card object that keeps track of the card's rank, suit, and card (?) which consists.
    of a (rank, suit) tuple.
    """
    greater_than_ten = {11: "J", 12: "Q", 13: "K", 14: "A"}
    less_than_ten = {x: str(x) for x in range(2, 11)}
    r_less_than_ten = {str(x): x for x in range(2, 11)}
    r_greater_than_ten = {"J": 11, "Q": 12, "K": 13, "A": 14}
    reverse_dct = {**r_less_than_ten, **r_greater_than_ten}
    dct = {**less_than_ten, **greater_than_ten}
    def __init__(self, rank, suit):
        """Creates a Card object, given a rank and suit."""
        super().__init__()
        self.set_rank_and_suit(rank, suit)
        #self.card = (self.__rank, self.__suit)
    
    def __repr__(self): # for me
        """The representation of a Card object."""
        return f"({self.__rank}, {self.__suit})"

    def __str__(self): # for end user, requires use of some Unicode-enabled font
        """
        The string representation (print() or str()) of a Card object. Uses red/black and 
        the Unicode symbols for spade/club/heart/diamond in the following format: 10♠.
        """
        if self.__suit == "hearts":
            suit_color = colorama.Fore.RED + '\u2665'
        elif self.__suit == "diamonds":
            suit_color = colorama.Fore.RED + '\u2666'
        elif self.__suit == "spades":
            suit_color = '\u2660'
        elif self.__suit == "clubs":
            suit_color = '\u2663' 
        return Card.dct[self.__rank] + suit_color + colorama.Style.RESET_ALL

    def __eq__(self, comp):
        if not isinstance(comp, Card):
            return False
        return self.__rank == comp.__rank and self.__suit == comp.__suit

    def __lt__(self, comp):
        if not isinstance(comp, Card):
            return False
        return self.__rank < comp.__rank and self.__suit == comp.__suit

    ## need for data encapsulation??
    # def get_card(self):
    #     """Retrieves """
    #     return self.card

    def get_rank(self):
        """Returns the rank of the card."""
        return self.__rank

    def get_suit(self):
        """Returns the suit of the card."""
        return self.__suit

    def set_rank_and_suit(self, rank, suit):
        """Sets the rank and suit of a card."""
        if not isinstance(rank, int) or \
            (isinstance(rank, int) and (rank < 2 or rank > 14)):
            raise TypeError("Please enter an integer (2 - 10) or 'J,' 'Q,' 'K,' or 'A.'")
        if not isinstance(suit, str):
            raise TypeError("Please enter 'spades,' 'clubs,' 'hearts,' or 'diamonds.'")
        self.__rank = rank
        self.__suit = suit

def int_repr(rank_string):
    """The integer representation of Card rank and suit."""
    # pretty much only necessary for taking input (e.g. of cards to discard)
    return Card.reverse_dct[rank_string]

class Deck:
    """A deck of cards 2,3,4,5,6,7,8,9,10,J,K,Q,A with suits Spades, Clubs, Hearts, & Diamonds."""
    ranks = [x for x in range(2, 15)]
    #  + list('JQKA')
    suits = ['spades', 'clubs', 'hearts', 'diamonds']
    def __init__(self):
        """Initializes a deck."""
        super().__init__()
        self.cards = [Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]

class Player:
    """A player with a hand of cards and a score."""
    def __init__(self):
        """Initializes a player with an empty hand and a score of 0."""
        super().__init__()
        self.hand = []
        # self.game_scores = [] # keeps track of player's score each round
        self.score = 0 
        # can use this to keep track of previous round scores; just keep appending to table list?

class Game:
    """Records the Hearts game state."""
    round_winner = None
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

    def player_discard(self, cards: dict, direction: str): 
        """Discards (passes) 3 cards in the desired direction."""
        # print(cards)
        # print(self.p1.hand)
        # use a dict e.g. {pX: [4C, 5H, 3C]}
        if direction == "pass":
            pass
        for card in cards:
            # print("inner loop")
            self.p1.hand.remove(card)
            if direction == "left":
                self.p2.hand.append(card)
            if direction == "right":
                self.p4.hand.append(card)
            if direction == "top":
                self.p3.hand.append(card)
    
    def min_rank_in_suit(self, hand, suit):
        hand.sort(key=lambda card: (card.get_suit(), card.get_rank()))
        #get_first = lambda suit: 

    def find_optimal_discard(self, hand, direction):
        """NPC decisionmaking for passing cards in a certain direction."""
        num_spades = 0
        num_hearts = 0
        num_clubs = 0
        num_dia = 0

        passed_cards = []
        for card in hand:
            if card.get_suit() == 'spades':
                num_spades += 1
            elif card.get_suit() == 'hearts':
                num_hearts += 1
            elif card.get_suit() == 'clubs':
                num_clubs += 1
            elif card.get_suit() == 'diamonds':
                num_dia += 1
        
        for card in hand:
            # TODO: add an "algorithm" to figure out optimal card choices (i.e. if statements)
            if card.get_rank() == 2 and card.get_suit() == 'clubs':
                passed_cards.append(card)
            if card.get_rank() == 12 and card.get_suit() == 'spades':
                if num_spades > 2:
                    passed_cards.append(card)
        return passed_cards

    def player_add(self, cards: list, direction: str):
        """
        Receives 3 cards from the player in the opposite direction 
        (e.g. direction=left comes from the right).
        """
        # TODO: implement player from opposite direction gives you 3 cards
        if direction == "pass":
            pass
        # for card in cards:


    def pre_round(self):
        """Sets up for a round (trick/hand)."""
        # uses tabulate to print a table of scores at the beginning of each round
        if self.turn > 0:
            score_table = [[colorama.Fore.MAGENTA + str(self.turn) + colorama.Style.RESET_ALL, 
                self.p1.score, self.p2.score, self.p3.score, self.p4.score,
                Game.round_winner]]
            print(tabulate.tabulate(score_table
                , headers=[colorama.Fore.MAGENTA + "Hand" + colorama.Style.RESET_ALL, 
                "Player 1", "Player 2",
                "Player 3", "Player 4", "Winner"], tablefmt="github"
            ))
            print()

        # deal all 52 cards to the 4 players (13 to each player)
        self.deal()

        # sort the player's hand (assuming p1 is the player); other players don't matter 
        # at least until multiplayer is implemented
        self.p1.hand.sort(key=lambda card: (card.get_suit(), card.get_rank()))
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
        for card in self.p1.hand:
            print(card, end=" ") # prints each card as formatted in Card.__str__(), end arg keeps it on same line
        # print(sorted_hand) # this just prints the list, so no formatting
        print("\n-----------------")

        # based on American rules (turn 1 left, turn 2 right, turn 3 up, turn 4 none, repeat)
        discard_direction = "left" if self.turn % 4 == 0 else "right" \
            if self.turn % 4 == 1 else "top" if self.turn % 4 == 2 else "pass"

        # use discard_direction and take user input for the desired discarded cards
        cards = []
        while len(cards) < 3:
            if len(cards) > 0:
                print("Please make sure you are discarding exactly three (3) cards.\n"
                "Here is your current selection: ")
                for card in cards:
                    card_obj = Card(int_repr(card.split()[0]), card.split()[2])
                    print(card_obj, end=" ")
            cards += input(f"Choose the {3-len(cards)} " + ("cards" if 3-len(cards) != 1 else "card") + 
            " you want to discard to the " + discard_direction.upper() + 
            ", with the following format: [RANK] of [SUIT] "
                 "(e.g. 2 of diamonds), demarcated with commas: \n").split(',')
        print() #newline
        discarded_cards = dict.fromkeys(self.players)
        f_cards = [Card(int_repr(card.split()[0]), card.split()[2]) for card in cards]
        # print(f_cards[0].get_rank(), f_cards[0].get_suit())
        # print(f_cards[0])
        self.player_discard(discarded_cards, discard_direction)
        # print(self.p1.hand)
        self.p1.hand.sort(key=lambda card: (card.get_suit(), card.get_rank()))
        # print(self.p1.hand)
        # TODO: figure out which cards to choose to pass (p2, p3, p4)
        # print("turn: " + str(self.turn))
        npc_discard = None # placeholder
        self.player_add(npc_discard, discard_direction)
        print("Your current hand is: ")
        for card in self.p1.hand:
            print(card, end=" ")
        print()

    def round(self):
        """Progresses through a round, ends when each player's hand is empty (len(hand)=0)."""
        while len(self.p1.hand) == 0 and len(self.p2.hand) == 0 and len(self.p3.hand) == 0 and\
            len(self.p4.hand) == 0:
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
    print(colorama.Fore.CYAN + pyfiglet.figlet_format("HEARTS") + 
        colorama.Style.RESET_ALL)
    a_game = Game()
    while a_game.p1.score < 100 and a_game.p2.score < 100\
         and a_game.p3.score < 100 and a_game.p4.score < 100:
        a_game.pre_round()
        a_game.round()
        a_game.turn += 1

main()
    