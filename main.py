import os
import time
import datetime
import re
import json

class Transaction:
    def __init__(self, discription, amount, type, category, date):
        self.discription = discription
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
            print(f"{obj.discription} | {obj.amount} | {obj.type} | {obj.category} | {obj.date}")

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
        print(f"Suma przychodów: {income_amount}\nSuma wydatków: {expense_amount}\nSaldo: {balance}")
                
        
def count_decimal_digits(x):
    amount_as_string = str(x)
    if '.' not in amount_as_string:
        return 0 
    return len(amount_as_string.split('.')[1])

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
        tType = input("Podaj typ transakcji\n" \
                        "1. Przychód\n" \
                        "2. Wydatek\n\n" \
                        "Twój wybór: ")
        try:
            tTypeAsInt = int(tType)
        except:
            display_wrong_answer()
            continue
        if tTypeAsInt == 1:
            tType = "Przychód"
            break
        elif tTypeAsInt == 2:
            tType = "Wydatek"
            break
        else:
            display_wrong_answer()
    while True:
        clear_terminal()
        amount = input("Podaj kwotę transakcji (W formacie X.XX): ")
        try:
            amountAsFloat = float(amount)
        except:
            display_wrong_answer()
            continue

        if count_decimal_digits(amountAsFloat) > 2:
            display_wrong_answer()
        else:
            amount = amountAsFloat
            break
    clear_terminal()
    tDiscription = input("Podaj opis transakcji: ")
    clear_terminal()
    tCategory = input("Podaj kategorię transakcji: ")
    clear_terminal()
    while True:
        tDate = input("Podaj datę transakcji w formacie DD.MM.YY (Jeśli dzisiejsza, kliknij enter): ")
        if tDate == '':
            tDate = str(f"{datetime.datetime.now().strftime('%d')}.{datetime.datetime.now().strftime('%m')}.{datetime.datetime.now().strftime('%y')}")
            break
        elif check_date_format(tDate) == True:
            break
        else:
            display_wrong_answer()
    clear_terminal()
    transaction = Transaction(tDiscription, amount, tType, tCategory, tDate)
    manager.add_transaction(transaction)
    print(f"Transakcja: {transaction.discription} na kwotę {transaction.amount} została dodana.")
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


