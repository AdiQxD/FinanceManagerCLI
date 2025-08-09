import os
import time
import datetime
import re
import json
from decimal import Decimal, ROUND_HALF_UP

class Transaction:
    def __init__(self, description, amount, transaction_type, category, date):
        self.description = description
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.date = date

class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.load_transactions()
    
    def add_transaction(self, transaction):
        if not isinstance(transaction.description, str) or not transaction.description.strip() or len(transaction.description) > 200:
            raise ValueError("Opis jest wymagany (max 200 znaków).")

        if not isinstance(transaction.amount, int) or transaction.amount < 0:
            raise ValueError("Kwota musi być nieujemną liczbą całkowitą (grosze).")

        if transaction.transaction_type not in ("Przychód", "Wydatek"):
            raise ValueError("Typ transakcji musi być 'Przychód' albo 'Wydatek'.")

        if not isinstance(transaction.category, str) or not transaction.category.strip():
            raise ValueError("Kategoria jest wymagana.")

        try:
            datetime.datetime.strptime(transaction.date, "%d.%m.%y")
        except ValueError:
            raise ValueError("Data musi być w formacie DD.MM.RR i istnieć w kalendarzu.")
        
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
                display_error("Błąd podczas wczytywania pliku JSON.")
                self.transactions = []

    def give_transaction_history(self):
        for obj in self.transactions:
            print(f"{obj.description} | {cents_to_amount(obj.amount)} | {obj.transaction_type} | {obj.category} | {obj.date}")

    def give_financial_analysis(self):
        income_amount = 0
        expense_amount = 0
        balance = 0
        for obj in self.transactions:
            if obj.transaction_type == "Przychód":
                income_amount += obj.amount
            elif obj.transaction_type == "Wydatek":
                expense_amount += obj.amount
        balance = income_amount - expense_amount
        print(f"Suma przychodów: {cents_to_amount(income_amount)}\nSuma wydatków: {cents_to_amount(expense_amount)}\nSaldo: {cents_to_amount(balance)}")

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
        except ValueError:
            display_error("Wybrano błędną opcję.")
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
            display_error("Wybrano błędną opcję.")
    
def display_error(text="Błąd bez opisu"):
    clear_terminal()
    print("BŁĄD!")
    print(f"Opis: {text}")
    time.sleep(2)

def amount_to_cents(text:str) -> int:
    text = text.replace(" ", "")
    text = text.replace(",", ".")
    dec = Decimal(text).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(dec * 100)
    
def cents_to_amount(cents: int) -> Decimal:
    return (Decimal(cents).scaleb(-2)).quantize(Decimal("0.00"),rounding=ROUND_HALF_UP)

def display_add_transaction():
    while True:
        clear_terminal()
        transaction_type = input("Podaj typ transakcji\n" \
                        "1. Przychód\n" \
                        "2. Wydatek\n\n" \
                        "Twój wybór: ")
        try:
            type_as_int = int(transaction_type)
        except ValueError:
            display_error("Wybrano błędną opcję.")
            continue
        if type_as_int == 1:
            transaction_type = "Przychód"
            break
        elif type_as_int == 2:
            transaction_type = "Wydatek"
            break
        else:
            display_error("Wybrano błędną opcję.")
    while True:
        clear_terminal()
        amount = str(input("Podaj kwotę transakcji: "))
        try:
            amount = amount_to_cents(amount)
            break
        except ValueError:
            display_error("Podano kwotę w błędnym formacie.")
            continue
    clear_terminal()
    description = input("Podaj opis transakcji: ")
    clear_terminal()
    category = input("Podaj kategorię transakcji: ")
    clear_terminal()
    date = input("Podaj datę transakcji w formacie DD.MM.RR (Jeśli dzisiejsza, kliknij enter): ")
    if date == '':
        date = str(f"{datetime.datetime.now().strftime('%d')}.{datetime.datetime.now().strftime('%m')}.{datetime.datetime.now().strftime('%y')}")
    clear_terminal()
    transaction = Transaction(description, amount, transaction_type, category, date)
    try:
        manager.add_transaction(transaction)
    except ValueError as e:
        display_error(str(e))
        return
    print(f"Transakcja: {transaction.description} na kwotę {cents_to_amount(amount)} została dodana.")
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


