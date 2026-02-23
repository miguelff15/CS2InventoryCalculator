# CS2InventoryCalculator

This project is a calculator for the steam market updated value of a Counter-Strike 2 Inventory and its individual items, 
it generates a final report.txt file with these informations.


How to execute the program:
1) Download this project
2) in a terminal with the path set to the main folder (which contains the main.py, resources.py, and README.md)
3) just execute the command : **python3 main.py**
4) then just type steamID64 
5) then type a number between 1 and 5 to choose the currency of the calculation (codes and currency 
names/symbols are printed in the terminal)
6) Just wait for the program to finish execution (it shows a progress bar in the terminal), the summary results will be 
shown in the terminal and the detailed ones will be in the report-YYYY-MM-DD-HH-MM-SS.txt file in the reports directory 
(inside the main directory)


**MORE INFORMATIONS ABOUT THIS PROJECT**:

I decided to create this because it's something I used to do manually, and this way it's automatic, however there are still 
some aspects to consider in this project:

    -Since for each item (that is not repeated), the request module is used to make a request 
    to the Steam API, and this has significant restrictions regarding the regularity of each 
    request from a given IP address (on a given internet connection),it is necessary to use a 
    timeout (time.sleep) of 3.5 seconds between each request, thus preventing the IP address 
    from timing out. In any case, if the number of items is very large, this could happen, as 
    well as the execution of this program many times within the same period.

    -For the reason stated above, this program should be used in a personal context and with 
    few executions in a given period of time. If many executions  are made, the IP address may 
    experience a timeout from making other requests to the Steam pricing API (all other Steam 
    services and pages function normally). This timeout is removed after some minutes/hours.
    
    -Based on the two previous points, this program is slow, and with many items it can be 
    quite time-consuming; on the other hand, it's the only free way to do this without using proxies.
    In any case, it's more practical than going to Steam and manually getting the prices 
    one by one and entering them into an Excel spreadsheet or calculator.



What the program really does?

1) Asks in the terminal for steamID64 profile to consider the inventory calculation
2) Asks in the terminal to choose the currency to consider in the calculation
3) Does a request to get all the skin names and quantities from a user
4) Does requests to get all the steam prices of those items (it uses a cache, so if a user has 2 or more of the same skin, it only does 
one request for that skin)
5) The sum of gross value and net value (estimated (using 0.85*gross_value)) is calculated
6) A report is created with the details (timestamp,steam profile link, gross value, net value (estimated), every skin name with its gross 
value (in the same currency)). This report is an .txt file and its created in the folder reports in the same directory as the other files.


