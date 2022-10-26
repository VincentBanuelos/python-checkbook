import json
from datetime import datetime
import time
import os.path
import sys

def exit_checkbook(): #function to exit program
        print()
        print("Thanks! Have a great day!") 
        print()  
        sys.exit(0)

print()
print("~~~ Welcome to your terminal checkbook! ~~~")
print()

while True: #repeats until valid pin format
    username = input('''For returning users please enter your existing Username
For new users please enter a Username that is no more than 10 characters long,
one will be automatically made for you: ''')
    if len(username) <= 10:
        break
    else:
        print("Invalid entry. Please enter ensure username is 4 characters long")

if os.path.exists(username + "_transactions.txt"):
    print()
    print(f'Welcome {username}.')
else: 
    print(f'Account not found. Creating new account your new username is {username}')

while True: #repeats until the user exits
    print('''
What would you like to do?
    1) view current balance
    2) withdraw money
    3) deposit money
    !! exit (type .. at any time to exit) !!
    ''')

    while True: 
        user_select = input("Please select an Input (Enter 1-3): ")
        if user_select == "..":
            exit_checkbook()
        elif user_select in "123":
            break
        else:
            print("Invalid entry.")

    if os.path.exists(username + "_transactions.txt"): 
        with open(username + "_transactions.txt") as f:
            transactions = json.load(f) #set transaction list specific to user
    else: 
        f= open(username + "_transactions.txt","w+")
        f.write("[]")
        f.close() 
        with open(username + "_transactions.txt") as f:
            transactions = json.load(f)

    if os.path.exists(username + "_balance.txt"):
        balance = (open(username + "_balance.txt","r"))
    else: 
        f= open(username + "_balance.txt","w+")
        f.write("0")
        f.close() 
        balance = (open(username + "_balance.txt","r"))
 
    if user_select == "1":
        print(f"Your balance is ${balance.read()}.")

    elif user_select == "2":
        while True: #repeats until numeric entry
            change_balance = input("How much would you like to withdraw? ")
            if change_balance == "..":
                exit_checkbook()
            elif change_balance.replace(".","").isdigit():
                break
            else:
                print("This is not a numeric value.")
        
        change_balance = format(float(change_balance), ".2f") #format change_balance to manipulate
        print(f"Withdraw amount: ${change_balance}")
        change_description = input("Description (optional): ") 
        if change_description == "..":
            exit_checkbook()        

        after_change = format((float(balance.read()) - float(change_balance)), ".2f")
        print("")
        print(f"Your new balance is ${after_change}.") #shows updated balance

        balance = (open(username + "_balance.txt", "w"))
        balance.write(str(after_change)) #write new balance back to balance sheet

        transactions.append(
            {
            'id' : len(transactions),
            'type': 'withdraw',
            'amount': "$" + change_balance,
            'date': datetime.now().strftime("%m/%d/%y"),
            'time': datetime.now().strftime("%H:%M"),
            'description': change_description
            }) #add withdraw to transactions list
        
    elif user_select == "3":
        while True: #repeats until numeric entry
            change_balance = input("How much would you like to deposit? ")
            if change_balance == "..":
                exit_checkbook()
            elif change_balance.replace(".","").isdigit():
                break
            else:
                print("This is not a numeric value.")
        change_balance = format(float(change_balance), ".2f") #format change_balance to manipulate
        print(f"Deposit amount: ${change_balance}")
        change_description = input("Description (optional): ")
        if change_description == "..":
            exit_checkbook()

        after_change = format((float(balance.read()) + float(change_balance)), ".2f")
        print("")
        print(f"Your new balance is ${after_change}.") #shows updated balance

        balance = (open(username + "_balance.txt", "w"))
        balance.write(str(after_change)) #write new balance back to balance sheet

        transactions.append(
            {
            'id' : len(transactions),            
            'type': 'deposit',
            'amount': "$" + change_balance,
            'date': datetime.now().strftime("%m/%d/%y"),
            'time': datetime.now().strftime("%H:%M"),
            'description': change_description
            }) #add deposit to transactions list
        
        with open(username + "_transactions.txt", "w") as f:
            json.dump(transactions, f) #dump transactions list into file
    else:
        exit_checkbook()