import os
import time

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
    clearTerminal()
    print("Test: dodawanie transakcji")
    time.sleep(2)

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
