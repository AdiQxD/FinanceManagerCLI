import os
import time
import datetime
import re
import json
from decimal import Decimal

class Transaction:
    def __init__(self, description, amount, type, category, date):
        self.description = description
        self.amount = amount
        self.type = type
        self.category = category
        self.date = date

class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.load_transactions()
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.save_transactions()

    def save_transactions(self):
        with open("transactions.json", "w") as file:
            data = [obj.__dict__ for obj in self.transactions]
            json.dump(data, file, indent=2)

    def load_transactions(self):
        if os.path.exists("transactions.json"):
            try:
                with open("transactions.json", "r") as file:
                    data = json.load(file)
                    self.transactions = [Transaction(**item) for item in data]
            except json.JSONDecodeError:
                print("Błąd podczas wczytywania pliku JSON.")
                self.transactions = []

    def give_transaction_history(self):
        for obj in self.transactions:
            print(f"{obj.description} | {round(Decimal(obj.amount/100), 2)} | {obj.type} | {obj.category} | {obj.date}")

    def give_financial_analysis(self):
        income_amount = 0
        expense_amount = 0
        balance = 0
        for obj in self.transactions:
            if obj.type == "Przychód":
                income_amount += obj.amount
            elif obj.type == "Wydatek":
                expense_amount += obj.amount
        balance = income_amount - expense_amount
        print(f"Suma przychodów: {round(Decimal(income_amount/100), 2)}\nSuma wydatków: {round(Decimal(expense_amount/100), 2)}\nSaldo: {round(Decimal(balance/100), 2)}")

def check_date_format(x):
    pattern = r"\d{2}.\d{2}.\d{2}"
    return re.fullmatch(pattern, x) is not None
    
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_main_menu():
    while True:
        clear_terminal()
        main_menu_choice = input("Menadzer finansów CLI\n" \
                            "1. Dodaj transakcję\n" \
                            "2. Historia transakcji\n" \
                            "3. Analiza salda\n" \
                            "4. Wyjście\n\n" \
                            "Twój wybór: ")
        try:
            main_menu_choice_as_int = int(main_menu_choice)
        except:
            display_wrong_answer()
            continue
        if main_menu_choice_as_int == 1:
            display_add_transaction()
        elif main_menu_choice_as_int == 2:
            display_transaction_history()
        elif main_menu_choice_as_int == 3:
            display_finance_analysis()
        elif main_menu_choice_as_int == 4:
            exit_app()
            break
        else:
            display_wrong_answer()
    
def display_wrong_answer():
    clear_terminal()
    print("Błędny Wybór")
    time.sleep(2)

def display_add_transaction():
    while True:
        clear_terminal()
        type = input("Podaj typ transakcji\n" \
                        "1. Przychód\n" \
                        "2. Wydatek\n\n" \
                        "Twój wybór: ")
        try:
            type_as_int = int(type)
        except:
            display_wrong_answer()
            continue
        if type_as_int == 1:
            type = "Przychód"
            break
        elif type_as_int == 2:
            type = "Wydatek"
            break
        else:
            display_wrong_answer()
    while True:
        clear_terminal()
        amount = str(input("Podaj kwotę transakcji: "))
        try:
            amount = Decimal(amount)
            amount = int(amount * 100)
            break
        except:
            display_wrong_answer()
            continue
    clear_terminal()
    description = input("Podaj opis transakcji: ")
    clear_terminal()
    category = input("Podaj kategorię transakcji: ")
    clear_terminal()
    while True:
        date = input("Podaj datę transakcji w formacie DD.MM.YY (Jeśli dzisiejsza, kliknij enter): ")
        if date == '':
            date = str(f"{datetime.datetime.now().strftime('%d')}.{datetime.datetime.now().strftime('%m')}.{datetime.datetime.now().strftime('%y')}")
            break
        elif check_date_format(date) == True:
            break
        else:
            display_wrong_answer()
    clear_terminal()
    transaction = Transaction(description, amount, type, category, date)
    manager.add_transaction(transaction)
    print(f"Transakcja: {transaction.description} na kwotę {Decimal(transaction.amount)} została dodana.")
    time.sleep(3)

def display_transaction_history():
    clear_terminal()
    print("Historia transakcji: ")
    manager.give_transaction_history()
    input("Aby wyjść, naciśnij enter: ")

def display_finance_analysis():
    clear_terminal()
    print("Analiza finansów: ")
    manager.give_financial_analysis()
    input("Aby wyjść, naciśnij enter: ")    

def exit_app():
    clear_terminal()
    print("Opuszczanie aplikacji.\nZapisywanie danych.")
    manager.save_transactions()
    time.sleep(2)

manager = FinanceManager()
display_main_menu()


