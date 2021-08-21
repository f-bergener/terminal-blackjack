from random import *


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value


class Player:
    def __init__(self, name):
        self.name = name
        self.bet = None
        self.bankroll = 5000
        self.hand = []
        self.count = None


class Dealer:
    def __init__(self):
        self.name = "Dealer"
        self.hand = []
        self.count = None


class Game:
    def __init__(self):
        self.deck = []
        self.player = None
        self.dealer = Dealer()
        self.handWinner = None
        self.blackjack = False
        self.handOver = False

    def getDeck(self):
        self.deck = []
        suits = ["spades", "diamonds", "clubs", "hearts"]
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        for suit in suits:
            for value in values:
                self.deck.append(Card(suit, value))
        for i in range(2000):
            cardIdxOne = randint(0, len(self.deck) - 1)
            cardIdxTwo = randint(0, len(self.deck) - 1)
            self.deck[cardIdxOne], self.deck[cardIdxTwo] = self.deck[cardIdxTwo], self.deck[cardIdxOne]

    def startGame(self):
        playerName = input("Enter your name: ")
        self.player = Player(playerName)
        print("Welcome to BlackJack " + self.player.name)

    def getBet(self):
        while True:
            try:
                bet = int(input("How much would you like to bet: "))
                if bet > self.player.bankroll or bet <= 0:
                    raise Exception()
                else:
                    self.player.bet = bet
                    self.player.bankroll -= self.player.bet
                    break
            except:
                print("Please enter a valid number that is less than or equal to " +
                      str(self.player.bankroll))
                continue

    def dealCard(self, player):
        card = self.deck.pop()
        player.hand.append(card)

    def deal(self):
        self.getDeck()
        self.getBet()
        for i in range(2):
            self.dealCard(self.player)
            self.dealCard(self.dealer)
        self.player.count = self.getCount(self.player)
        self.dealer.count = self.getCount(self.dealer)
        if self.player.count >= 21:
            self.handOver = True

    def getCount(self, player):
        regularArray = []
        aceArray = []
        count = 0
        for card in player.hand:
            if card.value != "A":
                regularArray.append(card.value)
            else:
                aceArray.append(card.value)
        for value in regularArray:
            if type(value) == str:
                count += 10
            else:
                count += value
        if len(aceArray) > 1:
            if count < 10:
                count += len(aceArray) - 1
                if count <= 10:
                    count += 11
                else:
                    count += len(aceArray)
        elif len(aceArray) == 1:
            if count >= 11:
                count += 1
            else:
                count += 11
        return count

    def printCards(self):
        print("You have ")
        self.printHand(self.player)
        print("Dealer is showing ")
        print(str(self.dealer.hand[1].value) +
              " of " + self.dealer.hand[1].suit)

    def printHand(self, player):
        hand = []
        for card in player.hand:
            hand.append(str(card.value) + " of " + card.suit)
        print(hand)

    def printHands(self):
        print("You had " + str(self.player.count))
        self.printHand(self.player)
        print("Dealer had " + str(self.dealer.count))
        self.printHand(self.dealer)

    def hit(self):
        self.dealCard(self.player)
        self.player.count = self.getCount(self.player)
        if self.player.count >= 21:
            self.handOver = True

    def stay(self):
        self.handOver = True

    def dealerHit(self):
        while self.dealer.count <= 17:
            self.dealCard(self.dealer)
            self.dealer.count = self.getCount(self.dealer)

    def compareHands(self):
        if self.player.count <= 21:
            self.dealerHit()
            if self.dealer.count > 21:
                if self.player.count == 21 and len(self.player.hand) == 2:
                    self.blackjack = True
                print("You won, dealer busted")
                self.handWinner = self.player.name
            elif self.player.count > self.dealer.count:
                if self.player.count == 21 and len(self.player.hand) == 2:
                    self.blackjack = True
                print("You won")
                self.handWinner = self.player.name
            elif self.dealer.count > self.player.count:
                print("Dealer won")
                self.handWinner = self.dealer.name
            else:
                print("Push")
                self.handWinner = "Push"
        else:
            print("Dealer won, you busted")
            self.handWinner = self.dealer.name

    def updateBankroll(self):
        multiplier = 2
        if self.handWinner == self.player.name:
            if self.blackjack == True:
                multiplier = 3
                print("BlackJack!")
            self.player.bankroll += int(self.player.bet * multiplier)
            print("You won " + str(int(self.player.bet * multiplier)))
        elif self.handWinner == self.dealer.name:
            print("You lost " + str(self.player.bet))
        else:
            self.player.bankroll += int(self.player.bet * 1)
        print("You now have " + str(self.player.bankroll))

    def resetForNextHand(self):
        self.player.bet = None
        self.player.hand = []
        self.player.count = None
        self.dealer.hand = []
        self.dealer.count = None
        self.handWinner = None
        self.blackjack = False
        self.handOver = False

    def playHand(self):
        self.deal()
        self.printCards()
        while self.handOver == False:
            move = input("Would you like to hit or stay: ").lower()
            if move != "hit" and move != "stay":
                print("Please provide a valid answer")
                continue
            elif move == "hit":
                self.hit()
                self.printCards()
            else:
                self.stay()
                self.printCards()
        self.compareHands()
        self.printHands()
        self.updateBankroll()
        self.resetForNextHand()

    def playGame(self):
        while self.player.bankroll > 0:
            print("--------------------------------")
            self.playHand()
        print("You ran out of money")


game = Game()
game.startGame()
game.playGame()
