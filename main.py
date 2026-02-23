from resources import execute

## main.py - file containing start functions that gets inputs (steamID and currency) and executes the program
def start():
    print("Hello, welcome to the steam inventory value calculator!")
    print()
    steam_id_valid=False
    while steam_id_valid is False:
        try:
            steam_id=int(input("To start insert here your steamID64 ID: "))
            print()
            
            if(len(str(steam_id))!=17):
                print("SteamID64 needs to be and integer with 17 caracters")
                print("Please try inserting again!")
                print()
            else:
                steam_id_valid=True
        except ValueError:
            print("SteamID64 needs to be an integer with 17 caracters")
            print("Please try inserting again!")
            print()


    currency_valid=False
    currency_menu="Choose the currency for the calculation:\n 1.EUR (€)\n 2.USD ($)\n 3.GBP (£)\n 4.BRL (R$)\n 5.RUB (pуб)\n"

    dict_currency_code={1:3,2:1,3:2,4:7,5:5}
    while currency_valid is False:
        print(currency_menu)
        try:
            user_input= int(input("Choose your currency option (1 to 5): "))
            print()
            if(user_input)<1 or user_input>5:
                print("Currency option invalid. The valid options are 1 to 5 corresponding to the currency´s in the menu above")
                print("Please try inserting again!")
                print()
            else:
                currency_valid=True
        except ValueError:
            print("Currency option needs to be an integer between 1 and 5.")
            print("Please try inserting again!")
            print()

    currency_id=dict_currency_code.get(user_input)

    execute(steam_id,currency_id)
            
        
if __name__ == "__main__":
    start()
