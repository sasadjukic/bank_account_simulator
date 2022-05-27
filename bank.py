

import random
import mysql.connector

class Database:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = 'yourhost',
            user = 'username',
            password = 'password',
            database = 'Bank'
            )

        self.cursor = self.mydb.cursor()

    def store_user_data(self, user_data, account_n, debit_n, pin_n, balance_s) -> None:

        self.sql = '''INSERT INTO account_holders (first_name,
                                                   last_name,
                                                   address,
                                                   city,
                                                   zip,
                                                   country,
                                                   phone,
                                                   email,
                                                   debit_card,
                                                   account_number,
                                                   pin,
                                                   balance)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        self.val = (user_data[0],
                    user_data[1],
                    user_data[2],
                    user_data[3],
                    user_data[4],
                    user_data[5],
                    user_data[6],
                    user_data[7],
                    debit_n,
                    account_n,
                    pin_n,
                    balance_s)

        self.cursor.execute(self.sql, self.val)
        self.mydb.commit()

    def check_account_holder(self, pin_number) -> bool:

        self.sql = f'SELECT * FROM account_holders WHERE pin = {pin_number}'
        self.cursor.execute(self.sql)
        self.is_account_holder = self.cursor.fetchall()

        if self.is_account_holder != []:
            return True
        else:
            return False

    def search_database(self, pin) -> str:

        self.sql = f'SELECT first_name, balance, account_number FROM account_holders WHERE pin = {pin}'
        self.cursor.execute(self.sql)
        self.account_holder = self.cursor.fetchall()

        print(f'Hello {self.account_holder[0][0]}')
        print(f'Account No.: {self.account_holder[0][2]}')
        print(f'Current balance: ${self.account_holder[0][1]}')

        return self.account_holder[0][1]

    def update_data(self, customer_pin, balance) -> None:

        self.sql = f'UPDATE account_holders SET balance = %s WHERE pin = %s'
        self.val = (balance, customer_pin)
        self.cursor.execute(self.sql, self.val)
        self.mydb.commit()

class CardMaker:

    def __init__(self):
        self.first_number = random.randint(1, 9)
        self.card = [random.randint(0, 9) for number in range(14)]
        self.card.insert(0, self.first_number)

    def checksum_main(self) -> tuple:

        index_odd = []
        index_even = []

        index = 0
        for number in self.card:
            if index % 2:
                index_even.append(number)
                index +=1
            else:
                index_odd.append(number)
                index +=1

        return (sum(index_even), index_odd)

    def get_odds(self, card_odds) -> list:

        times_two = [str(number*2) for number in card_odds]
        splitter = []

        for int in times_two:
            if len(int) > 1:
                splitter.append(int[0])
                splitter.append(int[1])
            else:
                splitter.append(int)

        return splitter

    def add_odds(self, card_odds) -> int:

        numbers = [int(iter) for iter in card_odds]
        return sum(numbers)

    def get_card(self, evens, odds) -> str:

        card = ''
        total = evens + odds

        divide_checker = total
        while divide_checker % 10:
            divide_checker +=1

        last_number = divide_checker - total
        self.card.append(last_number)

        for digit in self.card:
            card += str(digit)

        return card

class Bank:

    def __init__(self):
        self.first_name: str = ''
        self.last_name: str = ''
        self.address: str = ''
        self.city: str = ''
        self.zip: int = 0
        self.country: str = ''
        self.phone: str = ''
        self.e_mail: str = ''
        self.account_number: str = ''
        self.debit_card: str = ''
        self.debit_pin: str = ''
        self.balance: str = '0'

    def display_welcome(self) -> None:

        print('\t\t\t\t**************************')
        print('\t\t\t\t********Gekko Bank********')
        print('\t\t\t\t**************************')
        print('\n')

    def check_for_bank_account(self) -> bool:

        while True:
            self.acc_check = input('Are you a current account holder [Y/N]: ').upper()
            if self.acc_check == 'Y':
                return True
            elif self.acc_check == 'N':
                return False
            else:
                print(f"""You think you're a smart cookie, huh?,
                        {self.acc_check} to you...
                        Go back and answer the question, pal.""")

    def get_user_info(self) -> tuple:

        self.first_name = input('Enter your first name: ')
        self.last_name = input('Enter your last name: ')
        self.address = input('Enter your address: ')
        self.city = input('Enter your city: ')
        self.zip = int(input('Enter your zip code: '))
        self.country = input('Enter your country: ')
        self.phone = input('Enter your phone number: ')
        self.e_mail = input('Enter your e-mail address: ')

        return (self.first_name, self.last_name, self.address, self.city, self.zip, self.country, self.phone, self.e_mail)

    def create_account(self) -> str:

        for number in range(18):
            digit = random.randint(0,9)
            self.account_number += str(digit)

        print(f'\n{self.first_name} your new account number is:')
        print(f'{self.account_number[:3]}-{self.account_number[3:16]}-{self.account_number[16:]}')

        return self.account_number

    def create_debit_card(self) -> str:

        cardmaker = CardMaker()
        odds_evens = cardmaker.checksum_main()
        odds = cardmaker.get_odds(odds_evens[1])
        sum_odds = cardmaker.add_odds(odds)
        card = cardmaker.get_card(odds_evens[0], sum_odds)

        print('\nYour new card number is: ')
        print(card[:4], card[4:8],
              card[8:12], card[12:])

        return card

    def create_pin(self) -> str:

        digit = ''
        for number in range(4):
            digit += str(random.randint(0,9))
            self.debit_pin = digit

        print(f'\nYour PIN is: {self.debit_pin}')
        return self.debit_pin

    def initial_deposit(self) -> str:

        make_deposit = input('Would you like to make a deposit on your new account right now[Y/N]?: ')
        if make_deposit.upper() == 'Y':
            cash = input('How much would you like to deposit?: ')
            self.balance = cash
            return self.balance
        else:
            return self.balance

class ATM(Bank):

    def __init__(self) -> None:
        super().__init__()

    def get_pin(self) -> str:

        ask_for_pin = input('Enter your pin number: ')
        return ask_for_pin

    def display_account_action(self) -> str:

        user_action = input('Would you like to deposit[D], withdraw[W] or quit[Q]: ')
        if user_action.upper() == 'D':
            return 'D'
        elif user_action.upper() == 'W':
            return 'W'
        else:
            return 'Q'

    def deposit(self) -> int:

        cash = int(input('How much would you like to deposit to your account?: '))
        balance = int(self.balance) + cash
        print(f'Deposit completed\nYour new available balance is ${balance}')
        return balance

    def withdrawal(self) -> int:

        while True:
            cash = int(input('How much would you like to withdraw from your account?: '))

            if cash > int(self.balance):
                print('Not enough balance to withdraw that much')
                continue
            else:
                balance = int(self.balance) - cash
                print(f'Take your cash\nYour new available balance is ${balance}')
                return balance


def main():
    database = Database()
    atm = ATM()
    atm.display_welcome()

    if atm.check_for_bank_account():
        pin_attempts = 3

        while pin_attempts != 0:
            pin = atm.get_pin()
            acc_info = database.check_account_holder(pin)

            if acc_info:
                cash_available = database.search_database(pin)
                atm.balance = cash_available

                while True:
                    action = atm.display_account_action()
                    if action == 'D':
                        deposit_balance = atm.deposit()
                        atm.balance = deposit_balance
                        database.update_data(pin, atm.balance)
                    elif action == 'W':
                        if atm.balance == "0":
                            print('Not enough balance to make a withdrawal')
                            continue
                        withdrawal_balance = atm.withdrawal()
                        atm.balance = withdrawal_balance
                        database.update_data(pin, atm.balance)
                    else:
                        quit()

            else:
                print('Account has not been found')
                pin_attempts -= 1
                if pin_attempts > 0:
                    print(f'You have {pin_attempts} more attempt(s) at your PIN number')
                    print('\n')
                else:
                    print(f'To get help with your account visit one of our branches MON-FRI from 9:00-17:00')
                    continue

    else:
        personal_info = atm.get_user_info()
        acc_number = atm.create_account()
        debit_card = atm.create_debit_card()
        pin = atm.create_pin()
        opening_deposit = atm.initial_deposit()
        store_data = database.store_user_data(personal_info,
                                              acc_number,
                                              debit_card,
                                              pin,
                                              opening_deposit)

if __name__ == '__main__':
    main()
