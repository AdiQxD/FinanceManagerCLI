import os
import time
import datetime
import re

transactionList = []

class transactionClass:
    def __init__(self, discription, sum, type, category, date):
        self.discription = discription
        self.sum = sum
        self.type = type
        self.category = category
        self.date = date

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
        if mainMenuChoiceInt == 1:
            addTransaction()
        elif mainMenuChoiceInt == 2:
            transactionHistory()
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
    transaction = transactionClass(tDiscription, tSum, tType, tCategory, tDate)
    transactionList.append(transaction)
    print(f"Transakcja: {transaction.discription} na kwotę {transaction.sum} została dodana.")
    time.sleep(3)


def transactionHistory():
    clearTerminal()
    print("Test: Historia transakcji")
    time.sleep(2)

def financeAnalise():
    clearTerminal()
    print("Test: Analiza")
    time.sleep(2)

def exitApp():
    clearTerminal()
    print("Test: Opusc aplikacje")
    time.sleep(2)

mainMenu()
