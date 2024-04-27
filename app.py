# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask, jsonify, request 
import mysql.connector
import sys
from datetime import datetime
  
## Creating a Flask app ##
app = Flask(__name__)  
config = {
  'user': 'root',
  'password': 'cutevoice101',
  'host': '127.0.0.1',
  'database': 'bank',
  'raise_on_warnings': True
}

## Creating connection variable for mysql ##
connectsql = mysql.connector.connect(**config)
  
## Creating a new customer ##
def create_customer(fname,lname,isadmin, custuserid,password):
      
    query = "insert into bank.customer (first_name, last_name, is_admin, customer_user_id, password) " +  " values ('" + fname + "','" + lname + "'," + isadmin + ",'" + custuserid + "','" + password + "')"
    
    cursor = connectsql.cursor()
    customer = cursor.execute(query)
    connectsql.commit()
    cursor.close()
    return customer


##  Creating account for the customer ##
def create_account(accname,acctype,pin,custid):
      
    query = "insert into bank.account (account_type, account_name, pin, customer_id) " +  " values ('" + acctype + "','" + accname + "'," + pin + "," + str(custid) + ")"
 
    cursor = connectsql.cursor()
    account = cursor.execute(query)
    cursor.close()
    connectsql.commit()
    #close_connection_to_db()
    return account


## Get Customer ID ##
def get_customer_id(custuserid,password):
      
    query = "select id,first_name,last_name from bank.customer where customer_user_id = '" +  custuserid + "' and password = '" + password + "'"
    
    cursor = connectsql.cursor(buffered=True)
    cursor.execute(query)
    customerid = cursor.fetchone()
    cursor.close()

    return customerid


## Getting Complete Customer Information ##
def get_customer_information(custuserid,password):
      
    query = "select first_name, last_name, is_admin, id from bank.customer where customer_user_id = '" +  custuserid + "' and password = '" + password + "'"
    
    cursor = connectsql.cursor(buffered=True)
    cursor.execute(query)
    customerinfo = cursor.fetchone()
    cursor.close()

    return customerinfo


## Getting Customer Account Information ##
def get_account_information(customerid):
      
    query = "select account_name, account_type, pin, id from bank.account where customer_id = " +  str(customerid)
    
    cursor = connectsql.cursor(buffered=True)
    cursor.execute(query)
    accountinfo = cursor.fetchone()
    cursor.close()

    return accountinfo


## Getting Transactions of Customer ##
def get_transaction_information(accountid):
      
    query = "select transaction_amt, transaction_type, transaction_date from bank.transactions where account_id = " +  str(accountid)
    
    cursor = connectsql.cursor(buffered=True)
    cursor.execute(query)
    transactioninfo = cursor.fetchall()
    cursor.close()

    return transactioninfo


## Doing Deposit and Withdrawal Transactions of Customer ##
def deposit_withdraw_transaction(amount, accountid, transacttype):

    today = datetime.today()
    formatted_date = today.strftime("%Y-%m-%d")

    query = "insert into bank.transactions (transaction_amt, transaction_type, transaction_date,account_id) values (" + str(amount) + ",'" + transacttype + "','" + formatted_date + "'," + str(accountid)+ ")"
    
    cursor = connectsql.cursor()
    transactinfo = cursor.execute(query)
    cursor.close()
    connectsql.commit()
    #close_connection_to_db()
    return transactinfo


## Getting Transactions of Customer ##
@app.route('/create-customer', methods=['POST'])
def handle_create_customer():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    data = request.json

    customer = create_customer(data['first_name'], data['last_name'], data['is_admin'], data['customer_user_id'], data['password'])
    customerid = get_customer_id(data['customer_user_id'], data['password'])
    account = create_account(data['account_name'], data['account_type'], data['pin'], customerid[0])

    return "Customer " + str(customerid[0]) + "," + data['first_name'] + " " + data['last_name'] + " added successfully! " , 200, {"Access-Control-Allow-Origin": "*"}
  else:
    return "Content type is not supported."
    

## API Call for Deposting funds ##
@app.route('/deposit-funds', methods=['POST'])
def deposit_funds():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    data = request.json

    customerid = get_customer_id(data['customer_user_id'], data['password'])
    accountid =  get_account_information(customerid[0])    

    account = deposit_withdraw_transaction(data['amount'], accountid[3], "Deposit")

    return "Customer " + str(customerid[1]) + "," + str(customerid[2]) + " had " + data['amount'] + " deposited successfully! " , 200, {"Access-Control-Allow-Origin": "*"}
  else:
    return "Content type is not supported."


## API Call for Withdrawing funds ##
@app.route('/withdraw-funds', methods=['POST'])
def withdraw_funds():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    data = request.json

    customerid = get_customer_id(data['customer_user_id'], data['password'])
    accountid =  get_account_information(customerid[0])    

    account = deposit_withdraw_transaction(data['amount'], accountid[3], "Withdraw")

    return "Customer " + str(customerid[1]) + "," + str(customerid[2]) + " had " + data['amount'] + " withdrew successfully! " , 200, {"Access-Control-Allow-Origin": "*"}
  else:
    return "Content type is not supported."


## API Call for getting Customer Information ##
@app.route('/get-customer-info', methods=['GET'])
def get_customer_info():

    content_type = request.headers.get('Content-Type')
    transactinfo = ""

    if (content_type == 'application/json'):
        data = request.json
        customerinfo = get_customer_information(data['customer_user_id'], data['password'])

        if(customerinfo[2] == 0):
            user_role = "regular user"
        else:
            user_role = "admin user"


        accountinfo = get_account_information(customerinfo[3])

        transactioninfo = get_transaction_information(accountinfo[3])

        all_cust_info =  "Customer " + customerinfo[0] + " " + customerinfo[1] + " has role of " + user_role + "\n"
        all_cust_info = all_cust_info  + "Account name is " + accountinfo[0] + " and is of type " + accountinfo[1]

        for transacts in transactioninfo:
            transactinfo = transactinfo + "\n" + transacts[0] + "," + transacts[1] + "," + transacts[2]

        return all_cust_info + transactinfo ,200, {"Access-Control-Allow-Origin": "*"}
    else:
        return "Content type is not supported."


## Closing the DB connection after every db connection ##
def close_connection_to_db():
    connectsql.close()


## Starting the App Server embedded within Flask ##
if __name__ == '__main__': 
  
    app.run(debug = True) 
