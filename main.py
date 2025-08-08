import os
import time
import datetime
import re
import json

transactionList = []

class Transaction:
    def __init__(self, discription, sum, type, category, date):
        self.discription = discription
        self.sum = sum
        self.type = type
        self.category = category
        self.date = date

class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.loadTransactions()
    
    def addTransaction(self, transaction):
        self.transactions.append(transaction)
        self.saveTransaction()

    def saveTransaction(self):
        with open("transactions.json", "w") as file:
            data = [obj.__dict__ for obj in self.transactions]
            json.dump(data, file, indent=2)

    def loadTransactions(self):
        if os.path.exists("transactions.json"):
            try:
                with open("transactions.json", "r") as file:
                    data = json.load(file)
                    self.transactions = [Transaction(**item) for item in data]
            except json.JSONDecodeError:
                print("Błąd podczas wczytywania pliku JSON.")
                self.transactions = []

    def showTransactionHistory(self):
        for obj in self.transactions:
            print(f"{obj.discription} | {obj.sum} | {obj.type} | {obj.category} | {obj.date}")

    def transactionAnalise(self):
        incomeSum = 0
        expenseSum = 0
        balance = 0
        for obj in self.transactions:
            if obj.type == "Przychód":
                incomeSum =+ obj.sum
            elif obj.type == "Wydatek":
                expenseSum =+ obj.sum
        balance = incomeSum - expenseSum
        print(f"Suma przychodów: {incomeSum}\nSuma wydatków: {expenseSum}\nSaldo: {balance}")
                
        
def decimalCount(x):
    xStr = str(x)
    if '.' not in xStr:
        return 0 
    return len(xStr.split('.')[1])

def dateFormatCheck(x):
    pattern = r"\d{2}.\d{2}.\d{2}"
    return re.fullmatch(pattern, x) is not None
    
def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def mainMenu():
    while True:
        clearTerminal()
        mainMenuChoice = input("Menadzer finansów CLI\n" \
                            "1. Dodaj transakcję\n" \
                            "2. Historia transakcji\n" \
                            "3. Analiza salda\n" \
                            "4. Wyjście\n\n" \
                            "Twój wybór: ")
        try:
            mainMenuChoiceInt = int(mainMenuChoice)
        except:
            wrongAnswer()
            continue
        if mainMenuChoiceInt == 1:
            addTransaction()
        elif mainMenuChoiceInt == 2:
            transactionsHistory()
        elif mainMenuChoiceInt == 3:
            financeAnalise()
        elif mainMenuChoiceInt == 4:
            exitApp()
            break
        else:
            wrongAnswer()
    
def wrongAnswer():
    clearTerminal()
    print("Błędny Wybór")
    time.sleep(2)

def addTransaction():
    while True:
        clearTerminal()
        tType = input("Podaj typ transakcji\n" \
                        "1. Przychód\n" \
                        "2. Wydatek\n\n" \
                        "Twój wybór: ")
        try:
            tTypeAsInt = int(tType)
        except:
            wrongAnswer()
            continue
        if tTypeAsInt == 1:
            tType = "Przychód"
            break
        elif tTypeAsInt == 2:
            tType = "Wydatek"
            break
        else:
            wrongAnswer()
    while True:
        clearTerminal()
        tSum = input("Podaj kwotę transakcji (W formacie X.XX): ")
        try:
            tSumAsFloat = float(tSum)
        except:
            wrongAnswer()
            continue

        if decimalCount(tSumAsFloat) > 2:
            wrongAnswer()
        else:
            tSum = tSumAsFloat
            break
    clearTerminal()
    tDiscription = input("Podaj opis transakcji: ")
    clearTerminal()
    tCategory = input("Podaj kategorię transakcji: ")
    clearTerminal()
    while True:
        tDate = input("Podaj datę transakcji w formacie DD.MM.YY (Jeśli dzisiejsza, kliknij enter): ")
        if tDate == '':
            tDate = str(f"{datetime.datetime.now().strftime('%d')}.{datetime.datetime.now().strftime('%m')}.{datetime.datetime.now().strftime('%y')}")
            break
        elif dateFormatCheck(tDate) == True:
            break
        else:
            wrongAnswer()
    clearTerminal()
    transaction = Transaction(tDiscription, tSum, tType, tCategory, tDate)
    manager.addTransaction(transaction)
    print(f"Transakcja: {transaction.discription} na kwotę {transaction.sum} została dodana.")
    time.sleep(3)

def transactionsHistory():
    clearTerminal()
    print("Historia transakcji: ")
    manager.showTransactionHistory()
    input("Aby wyjść, naciśnij enter: ")

def financeAnalise():
    clearTerminal()
    print("Analiza finansów: ")
    manager.transactionAnalise()
    input("Aby wyjść, naciśnij enter: ")    

def exitApp():
    clearTerminal()
    print("Opuszczanie aplikacji.\nZapisywanie danych.")
    manager.saveTransaction()
    time.sleep(2)

manager = FinanceManager()
mainMenu()


