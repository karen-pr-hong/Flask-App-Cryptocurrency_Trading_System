# Flask-App-Cryptocurrency_Trading_System
Final Project for Database Technologies and Web Application course at New York University's Masters Program

Please download the following software in order to run the app:

1. python 3.8
2. mysql (please set the password as "Pword2019!1")
3. pip install the following list of python packages:
    certifi==2019.9.11
    chardet==3.0.4
    get==2019.4.13
    idna==2.8
    mysql-connector-python==8.0.18
    numpy==1.17.4
    panda==0.3.1
    pandas==0.25.3
    post==2019.4.13
    protobuf==3.11.0
    public==2019.4.13
    python-dateutil==2.8.1
    pytz==2019.3
    query-string==2019.4.13
    request==2019.4.13
    requests==2.22.0
    six==1.13.0
    urllib3==1.25.7
    virtualenv==16.7.8
    websockets==8.1
  
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
