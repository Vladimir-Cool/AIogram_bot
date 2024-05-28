import random, sys
from time import sleep
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from ..utils.stateblackjack import StepsBlackJack

# Константы:
HEARTS   = chr(9829) # Character 9829 is '♥'.
DIAMONDS = chr(9830) # Character 9830 is '♦'.
SPADES   = chr(9824) # Character 9824 is '♠'.
CLUBS    = chr(9827) # Character 9827 is '♣'.
# HEARTS   = chr(127892) # Character 9829 is '♥'.
# DIAMONDS = chr(9826) # Character 9830 is '♦'.
# SPADES   = chr(9828) # Character 9824 is '♠'.
# CLUBS    = chr(9831) # Character 9827 is '♣'.
BACKSIDE = 'backside'

money = 5000


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


# def display_cards(cards):
#     """Отображение всех карточек в списке карточек."""
#     rows = ['', '', '', '', '']  # Текст, отображаемый в каждой строке
#
#     for i, card in enumerate(cards):
#         rows[0] += ' ___  '  # Распечатайте верхнюю строку карточки.
#         if card == BACKSIDE:
#             # Распечатайте обратную сторону карты:
#             rows[1] += '|## | '
#             rows[2] += '|###| '
#             rows[3] += '|_##| '
#         else:
#             # Распечатайте лицевую сторону карты:
#             rank, suit = card  # Карта представляет собой кортежную структуру данных.
#             rows[1] += '|{} | '.format(rank.ljust(2))
#             rows[2] += '| {}| '.format(suit)
#             rows[3] += '|_{}| '.format(rank.rjust(2, '_'))
#
#     # Распечатайте каждую строку на экране:
#     result = ""
#     for row in rows:
#         result += (f"{row}\r\n")
#     return result

def display_cards(cards):
    result = ""
    for card in cards:
        rank, suit = card
        result += f"({rank} ,{suit})"
    return result



async def start_game(message: Message, state: FSMContext):
    await message.answer('''Blackjack...

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
       Дилер прекращает бить в 17.'''
    )
    await message.answer(f"Сделайте ставку.\r\nСейчас у вас {money} ед. денег.\r\nДля выхода из игры - QUIT")
    await state.update_data(money=money)
    await state.set_state(StepsBlackJack.MAKE_BET)


async def bet(message: Message, state: FSMContext):
    context_data = await state.get_data()
    money = context_data.get("money")


    """Проверка ставки"""
    if message.text.upper() == "QUIT":
        await message.answer("Игра завершена")
        await state.clear()

    elif message.text.startswith("-"):
        if message.text[1:]:
            await message.answer("Cтавка должна быть  больше \"0\"")
    elif message.text.isdecimal():
        if int(message.text) == 0:
            await message.answer("Cтавка должна быть больше \"0\"")
        elif int(message.text) > money:
            await message.answer(f"У вас нету таких денег, у вас всего {money} ед. денег")
        else:
            """Успешная ставка"""
            bet = int(message.text)
            deck = get_deck()
            dealer_hand = [deck.pop(), deck.pop()]
            player_hand = [deck.pop(), deck.pop()]

            await message.answer(f"Отлично, ваша ставка принята - {bet} ед.")
            sleep(1)
            await message.answer(f"DEALER: {get_hand_value(dealer_hand)}\r\n{display_cards(dealer_hand)}")
            await message.answer(f"{message.from_user.first_name.upper()}: {get_hand_value(player_hand)}\r\n{display_cards(player_hand)}")
            await message.answer("Ваш ход:\r\nH - Взять еще карту\r\nS - Пропустить ход\r\nD - Удвоить ставку")

            await state.update_data(bet=bet, money=money - bet, deck=deck,
                                    player_hand=player_hand, dealer_hand=dealer_hand)
            await state.set_state(StepsBlackJack.GAME)
    else:
        await message.answer(f"Нужно ввести число от 1 до {money}")


async def end_game(message: Message, state: FSMContext, money):
    if money:
        await message.answer(f"Сделайте ставку.\r\nСейчас у вас {money} ед. денег.\r\nДля выхода из игры - QUIT")
        await state.update_data(bet=bet, money=money)
        await state.set_state(StepsBlackJack.MAKE_BET)
    else:
        await message.answer("У вас кончились деньги\r\nКонец игры.")
        await state.clear()


async def game(message: Message, state: FSMContext):
    context_data = await state.get_data()
    money = context_data.get("money")
    bet = context_data.get("bet")
    deck = context_data.get("deck")
    dealer_hand = context_data.get("dealer_hand")
    player_hand = context_data.get("player_hand")

    if message.text.upper() == "D" and len(player_hand) == 2:
        if money >= bet:
            bet = bet * 2
            money -= bet
            await message.answer(f"Ставка удвоена.\r\nСтавка: {bet}\r\nДенег осталось: {money}")

    if message.text.upper() in ("H", "D"):
        player_hand.append(deck.pop())

        await message.answer(f"DEALER: {get_hand_value(dealer_hand)}\r\n{display_cards(dealer_hand)}")
        await message.answer(f"{message.from_user.first_name.upper()}: {get_hand_value(player_hand)}\r\n{display_cards(player_hand)}")
        await message.answer("Ваш ход:\r\nH - Взять еще карту\r\nS - Закончить набор карт")

        """Проверка руки Игрока"""
        if get_hand_value(player_hand) > 21:
            await message.answer(f"{message.from_user.first_name} проиграл")
            await end_game(message, state, money)


    elif message.text.upper() == "S":
        """Ход дилера"""
        while get_hand_value(dealer_hand) < 18 and get_hand_value(dealer_hand) <= 21:
            dealer_hand.append(deck.pop())
            await message.answer(f"DEALER: {get_hand_value(dealer_hand)}\r\n{display_cards(dealer_hand)}")
            await message.answer(
                f"{message.from_user.first_name.upper()}: {get_hand_value(player_hand)}\r\n{display_cards(player_hand)}")
            sleep(1)


        player_value = get_hand_value(player_hand)
        dealer_value = get_hand_value(dealer_hand)

        if player_value > dealer_value:
            await message.answer(f"Ты выйграл {bet} ед денег")
            money += bet * 2
        elif player_value == dealer_value:
            await message.answer("Ничья, ставка возвращается вам.")
            money += bet
        elif dealer_value > 21:
            await message.answer(f"Дилер перебрал, ты выйграл {bet} ед денег")
            money += bet * 2
        else:
            await message.answer("Ты проиграл")

        await end_game(message, state, money)



