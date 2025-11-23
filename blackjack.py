import random

suits = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9,
           'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank 
    
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:

    def __init__(self, total = 100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet 

    def lose_bet(self):
        self.total -= self.bet 
        
def take_bet(chips):

    while True:
        
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry that is not an integer!")
        else:
            if chips.bet > chips.total:
                print(f"You do not have that many chips, you have {chips.total} chips left.")
            else:
                break

def hit(deck, hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):

    global playing  

    while True:

        x = input("Enter h for hit or enter s for stand: ")

        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Dealer's turn!")
            playing = False
        else:
            print("Sorry I do not understand that input, please enter h or s only.")
            continue

        break

def show_some(player, dealer):

    print("\nDealer's Hand: ")
    print("The first card is hidden.")
    print(dealer.cards[1])

    
    print("Player's hand: ", *player.cards, sep='\n')

def show_all(player, dealer):

    
    print("Dealer's hand: ", *dealer.cards, sep='\n')
    print(f"The value of dealer's hand: {dealer.value}")

    
    print("Player's hand: ", *player.cards, sep='\n')
    print(f"The value of player's hand: {player.value}")

def player_busts(player, dealer, chips):

    print("You busted, dealer wins!")
    chips.lose_bet()

def player_wins(player, dealer, chips):

    print("You won, CONGRATS!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):

    print("You won, dealer busted!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):

    print("You lost, dealer wins!")
    chips.lose_bet()

def push(player, dealer):
    print("Dealer and player tie! PUSH!")

##################################
#   ACTUAL GAME CODE AND LOGIC   #
##################################

while True:

    # Printing out the opening statement
    
    print("Welcome to Blackjack!")

    # Create and shuffle the deck, deal two cards to each player

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Setup the players chips

    player_chips = Chips()
    
    # Prompt the player for their bet 

    take_bet(player_chips)

    # Show cards (One dealer card hidden!)

    show_some(player_hand, dealer_hand)

    while playing: # Recall from the hit_or_stand function

        # Prompt for player to hit or stand

        hit_or_stand(deck, player_hand)

        # Show cards (One dealer card hidden!)

        show_some(player_hand, dealer_hand)

        # If player hand goes over 21, player busts and break

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)

            break

    # If player hasn't busted, dealer's turn

    if player_hand.value < 21:

        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)

        # Show all cards

        show_all(player_hand, dealer_hand)

        # Running different scenarios

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)   
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)     
        else:
            push(player_hand, dealer_hand)

    # Inform player of their chips

    print(f"\nPlayer total chips are: {player_chips.total}.")

    # Ask to play again

    new_game = input("Would you like to play another game, type yes or no: ")

    if new_game[0].lower() == 'y':
        playing = True
        continue

    else:
        print("Thank you for playing.")

        break
