import requests
from urllib.parse import quote
import time
import csv
from datetime import datetime
import requests
import sys

def getSkinsFromInventory(steamUserId):
    """
    Gets the name and quantity of skins that a user with steamUserId has in his account (only considers sellable/tradable items)
    
    Requires:
    steamUserId is an int value which corresponds to the steamID64 of the profile inventory to be calculated
    """
    skins_owned = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    start_assetid = None
    has_more = True
    print("Getting the skins from the inventory...\n")
    while has_more:
        url ="https://steamcommunity.com/inventory/"+str(steamUserId)+"/730/2?l=english&count=75"
        if start_assetid:
            url += "&start_assetid="+str(start_assetid)
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 429:
                print("Rate limit reached. Waiting 10 seconds...")
                time.sleep(10)
                continue

            if response.status_code == 200:
                data = response.json()
                
                if not data.get('assets'):
                    if not skins_owned:
                        raise Exception("Inventory private or empty, please insert an USERID refered to a public profile and inventory.")
                
                descriptions = {item['classid']: item for item in data['descriptions']}

                for asset in data['assets']:
                    classid = asset['classid']
                    if classid in descriptions:
                        item_info = descriptions[classid]
                        if item_info.get('tradable') == 1:
                            skins_owned.append(item_info['market_name'])
                
                has_more = data.get('more_items', False)
                start_assetid = data.get('last_assetid')
                
                if has_more:
                    time.sleep(1.5)
            else:
                raise Exception("Steam Error: "+str(response.status_code))
                
        except Exception as e:
            raise Exception("Error getting inventory items: " + str(e))
            
    return skins_owned



def getSkinPrice(market_skin_name:str,currency_id:int):
    """
    Gets skin (steam) market price (lowest announced) by the market skin name (formatted)

    Requires:
    market_skin_name ia a str with the skin name with steam formatting
        example: Hydra Gloves ★ | Case Hardened (Field-Tested)
    currency is an int, which corresponds to the currency code in the Steam API
    """
    price=0

    name_prepared=quote(market_skin_name)
    url = "https://steamcommunity.com/market/priceoverview/?appid=730&currency="+str(currency_id)+"&market_hash_name="+name_prepared
    response = requests.get(url)
    data = response.json()

    dict_code_symbol={3:"€",1:"$",2:"£",5:"руб",7:"R$"}
    currency_symbol=dict_code_symbol.get(currency_id)

    if data.get("success"):
        lowest_price = data.get("lowest_price")

        if(lowest_price !=None):
            price=float(lowest_price.replace(currency_symbol,"").replace(",",".").replace(" ", "").replace("--","00"))

        time.sleep(3.5) 

    return (price,currency_symbol)



def create_report(steam_id, total_gross, total_net,dict_skin_prices, dict_skin_quantities,currency):

    temp_calculated = {}
    
    for skin, qty in dict_skin_quantities.items():
        if skin in dict_skin_prices:
            gross_unit = dict_skin_prices[skin][0]
            net_unit = dict_skin_prices[skin][1]
        
            total_skin_gross = qty * gross_unit
            total_skin_net = qty * net_unit
            
            temp_calculated[skin] = (total_skin_gross, total_skin_net)


    sorted_items = dict(sorted(temp_calculated.items(), key=lambda item: item[1][1], reverse=True))
    timestamp_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    timestamp_to_write = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    fileName = "reports/report_"+timestamp_filename+".txt"

    with open(fileName, "w", encoding="utf-8") as f:
        f.write("INVENTORY VALUE REPORT\n")
        f.write("Timestamp: "+timestamp_to_write+"\n")
        f.write("Steam Profile: https://steamcommunity.com/profiles/"+str(steam_id)+"\n\n")
        
        f.write("GROSS VALUE: "+str(total_skin_gross)+currency+"\n")
        f.write("NET VALUE: "+str(total_skin_net)+currency+"\n")
        
        f.write("DETAILED INFO:\n\n")

        f.write("SKIN                                     | GROSS VALUE     | NET VALUE\n")
        f.write("-" * 75 + "\n")

        for skin, data in sorted_items.items():
            g_val = data[0]
            n_val = data[1]

            linha = skin.ljust(40) + " | " + str(round(g_val, 2)).ljust(15) + " | " + str(round(n_val, 2)) + "\n"
            
            f.write(linha)
    return fileName


def listToDict(skins_owned):
    """
    Converts a list with the skins name to a dict with name and quantity (to register quantities)

    Requires:
    skins_owned is a list with strings of the skins owned
    """
    dict_quantity = {}
    for elem in skins_owned:
        if elem not in dict_quantity:
            dict_quantity[elem] = 1
        else:
            dict_quantity[elem] += 1
    return dict_quantity



def calculateFinalValues(dict_prices,dict_quantities):
    """
    Calculates net and gross final values (does the sum of all the skins registered in the dict_prices/dict_quantities)

    Requires:
    dict_prices: is a dict with the format {str:(float,float),...} -> {skin_name:(skin_gross_value,skin_net_value),...}
    dict_quantities: is a dict with the format {str:int,...} -> {skin_name:skin_quantity,...}
    """
    gross_total_general=0
    net_total_general=0
    for skin, qty in dict_quantities.items():
        if skin in dict_prices:
            gross_unit, net_unit = dict_prices[skin]
            gross_total_general += qty * gross_unit
            net_total_general += qty * net_unit

    return (round(gross_total_general,2),round(net_total_general,2))



def execute(steam_id,currency_id):
    """
    Executes the CS2 inventory calculator program

    Requires:
    steam_id is an int with 17 characters containing the steamID64
    currency_id is an int with the code of the currency to be considered in the calculation
    """
    currency_symbol_got=""
    if type(steam_id)!=int and len(str(steam_id))!=17:
        raise Exception ("SteamID64 needs to be and integer with 17 characters")
    
    try:
        skins_owned = getSkinsFromInventory(steam_id)
    except Exception:
        raise Exception("Error finding skins from profile with steamID "+str(steam_id))
    
    total_items = len(skins_owned)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dict_skin_quantities=listToDict(skins_owned)
    dict_skin_prices={}
    for i, skin in enumerate(skins_owned, 1):
            if skin not in dict_skin_prices:
                preco_bruto, currency_symbol_got = getSkinPrice(skin,currency_id) 
                if preco_bruto > 0: 
                    preco_liquido = round(preco_bruto / 1.15, 2)
                    dict_skin_prices[skin]=(preco_bruto,preco_liquido)     

            percentagem = (i / total_items) * 100
            tamanho_barra = 20
            progresso = int((i / total_items) * tamanho_barra)
            barra = "█" * progresso + "-" * (tamanho_barra - progresso)
            sys.stdout.write(f"\rProgress: |{barra}| {percentagem:.1f}% ({i}/{total_items}) Processing: {skin[:20]}...")
            sys.stdout.flush()

    final_values_dict=calculateFinalValues(dict_skin_prices,dict_skin_quantities)
    gross_total_value=final_values_dict[0]
    net_total_value=final_values_dict[1]

    fileName=create_report(steam_id,gross_total_value,net_total_value,dict_skin_prices,dict_skin_quantities,currency_symbol_got)

    print("\nExecution finished successfully!\n")
    print("***FINAL SUMMARY RESULTS***")
    print("GROSS INVENTORY VALUE: "+str(gross_total_value)+currency_symbol_got)
    print("NET INVENTORY VALUE: "+str(net_total_value)+currency_symbol_got)
    

    print("\nCheck the file "+fileName+"in this directory in the reports folder to see the detailed results.")

