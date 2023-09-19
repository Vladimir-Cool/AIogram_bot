"""Блэкджек.
Классическая карточная игра, также известная как «21»."""

import random, sys

# Константы:
HEARTS   = chr(9829) # Character 9829 is '♥'.
DIAMONDS = chr(9830) # Character 9830 is '♦'.
SPADES   = chr(9824) # Character 9824 is '♠'.
CLUBS    = chr(9827) # Character 9827 is '♣'.

BACKSIDE = 'backside'


def get_bet(maxBet):
    """Спрашиваем игрока, какую сумму он хочет поставить на этот раунд."""
    while True:  # Keep asking until they enter a valid amount.
        print(f'Сколько вы ставите? (1-{maxBet}, или QUIT)')
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Спасибо за игру!')
            sys.exit()

        if not bet.isdecimal():
            continue  # Если игрок не ввел сумму, спросите еще раз.

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet  # Игрок сделал ставку.


def get_deck():
    """Возвращает список кортежей (ранга, масти) для всех 52 карт."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  # Добавляем карты с номерами.
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))  # Добавляем карты с картинками.
    random.shuffle(deck)
    return deck


def display_hands(playerHand, dealerHand, showDealerHand):
    """Покажите карты игрока и дилера.
        Скрыть первую карту дилера, если showDealerHand - False."""
    print()
    if showDealerHand:
        print('DEALER:', get_hand_value(dealerHand))
        display_cards(dealerHand)
    else:
        print('DEALER: ???')
        # Скрыть первую карту дилера:
        display_cards([BACKSIDE] + dealerHand[1:])

    # Show the player's cards:
    print('ИГРОК:', get_hand_value(playerHand))
    display_cards(playerHand)


def get_hand_value(cards):
    """Возвращает стоимость карт. Лицевые карты стоят 10, тузы – стоит 11 или 1
    (эта функция выбирает наиболее подходящее значение туза."""

    value = 0
    numberOfAces = 0

    # Добавьте ценность для карт без туза.:
    for card in cards:
        rank = card[0]  # карта представляет собой кортеж типа (rank, suit)
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):  # Карты-картинки приносят 10 очков.
            value += 10
        else:
            value += int(rank)  # Пронумерованные карты стоят аналогичное количество.

    # Добавьте значение тузов:
    value += numberOfAces  # Добавьте 1 за каждый туз.
    for i in range(numberOfAces):
        # Если можно добавить еще 10 без перебора, сделайте так:
        if value + 10 <= 21:
            value += 10

    return value


def display_cards(cards):
    """Отображение всех карточек в списке карточек."""
    rows = ['', '', '', '', '']  # Текст, отображаемый в каждой строке

    for i, card in enumerate(cards):
        rows[0] += ' ___  '  # Распечатайте верхнюю строку карточки.
        if card == BACKSIDE:
            # Распечатайте обратную сторону карты:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Распечатайте лицевую сторону карты:
            rank, suit = card  # Карта представляет собой кортежную структуру данных.
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    # Распечатайте каждую строку на экране:
    for row in rows:
        print(row)


def get_move(playerHand, money):
    """Запрашивает у игрока ход и возвращает «H» для хода, «S» для пропуска и «D» для удвоения ставки.."""
    while True:  # Продолжайте цикл, пока игрок не сделает правильный ход.
        # Определите, какие ходы может сделать игрок:
        moves = ['(H)it', '(S)tand']

        # Игрок может удвоить ставку на своем первом ходу, говорим ему это, когда у него будет ровно две карты:
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        # Получаем ход игрока:
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move  # Игрок сделал ход.
        if move == 'D' and '(D)ouble down' in moves:
            return move  # Игрок сделал ход.


def main():
    print('''Blackjack...

     Правила:
       Постарайтесь приблизиться к 21, не превышая его.
       Короли, дамы и валеты приносят 10 очков.
       Тузы приносят 1 или 11 очков.
       Карты от 2 до 10 имеют свою номинальную стоимость.
       (H)это взять еще одну карту.
       (S)перестану брать карты.
       В первой игре вы можете (D)удвоить ставку, чтобы увеличить ставку.
       но должен ударить ровно еще раз, прежде чем встать.
       В случае ничьей ставка возвращается игроку.
       Дилер прекращает бить в 17.''')

    money = 5000
    while True:  # Основной цикл игры.
        # Проверьте, закончились ли у игрока деньги:
        if money <= 0:
            print("Деньги кончились!")
            print("Хорошо, что ты играл не на реальные деньги.")
            print('Спасибо за игру!')
            sys.exit()

        # Позвольте игроку ввести свою ставку на этот раунд:
        print('Money:', money)
        bet = get_bet(money)

        # Раздайте дилеру и игроку по две карты из колоды:
        deck = get_deck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # Обрабатывать действия игрока:
        print('Ставка:', bet)
        while True:  # Продолжайте цикл, пока игрок не встанет или не проиграет.
            display_hands(playerHand, dealerHand, False)
            print()

            # Проверьте, есть ли у игрока перебор:
            if get_hand_value(playerHand) > 21:
                break

            # Получите ход игрока: H, S или D:
            move = get_move(playerHand, money - bet)

            # Обработка действий игрока:
            if move == 'D':
                # Игрок удваивает ставку, он может увеличить ставку:
                additionalBet = get_bet(min(bet, (money - bet)))
                bet += additionalBet
                print(f'Ставка увеличена до {bet}.')
                print('Ставка:', bet)

            if move in ('H', 'D'):
                # Ход/удвоение требует еще одной карты.
                newCard = deck.pop()
                rank, suit = newCard
                print(f'Ты взял {rank} {suit}.')
                playerHand.append(newCard)

                if get_hand_value(playerHand) > 21:
                    # Игрок разорен:
                    continue

            if move in ('S', 'D'):
                # Пропуск/удвоение ставки останавливает ход игрока.
                break

        # обрабатывать действия дилера:
        if get_hand_value(playerHand) <= 21:
            while get_hand_value(dealerHand) < 17:
                # Ход дилера:
                print('Ход дилера...')
                dealerHand.append(deck.pop())
                display_hands(playerHand, dealerHand, False)

                if get_hand_value(dealerHand) > 21:
                    break  # Дилер разорился.
                input('Press Enter to continue...')
                print('\n\n')

        # Покажите финальные руки:
        display_hands(playerHand, dealerHand, True)

        playerValue = get_hand_value(playerHand)
        dealerValue = get_hand_value(dealerHand)
        # Укажите, выиграл ли игрок, проиграл или сыграл вничью:
        if dealerValue > 21:
            print(f'Дилер перебрал! ты выйграл ${bet}!')
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('Ты проиграл!')
            money -= bet
        elif playerValue > dealerValue:
            print(f'Ты выйграл ${bet}!')
            money += bet
        elif playerValue == dealerValue:
            print('Ничья, ставка возвращается вам.')

        input('Press Enter to continue...')
        print('\n\n')


if __name__ == '__main__':
    main()