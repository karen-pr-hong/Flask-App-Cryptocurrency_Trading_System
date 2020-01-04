# Flask-App-Cryptocurrency_Trading_System
Final Project for Database Technologies and Web Application course at New York University's Masters Program

Please download the following software in order to run the app:

1. python 3.8
2. mysql (please set the password as "Pword2019!1")
3. pip install the following list of python packages:
(1.) certifi
(2.) chardet
(3.) get
(4.) idna
    (5.) mysql-connector-python
    (6.) numpy
    (7.) panda
    (8.) pandas
    (9.) post
    (10.) protobuf
    (11.) public
    (12.) python-dateutil
    (13.) pytz
    (14.) query-string
    (15.) request
    (16.) requests
    (17.) six
    (18.) urllib3
    (19.) virtualenv
    (20.) websockets
  
Steps to run the app (Please run the app in a Windows system)
1. download the whole "webApplication" folder
2. run the whole sql file "create_trading_system_database" in mysql workbench
3. open the first powershell window and change directory to the location of the "webApplication" folder
4. run "$env:FLASK_DEBUG=1" in the command line in the first powershell window
5. run "flask run" in the command line in the first powershell window
6. open a second powershell window and change directory to the location of the "webApplication" folder
7. run "python .\websocket_coinbase.py" in the second powershell window
8. copy and paste the http link that showed up in the first powershell window after you type "flask run" to a browser
9. Start trading!

Note: if you try to purchase cryptocurrency that cost more than your cash balance, the sysyem will ignore the transaction, it will only process valid transaction. The system also don't allow you to sell crypto currency that you don't have in the sysytem.
