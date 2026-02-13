import mysql.connector

# -------- DATABASE CONNECTION --------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mihir@1221",
    database="bank_db"
)

cur = db.cursor()

print("="*80)
print("      BANK MANAGEMENT SYSTEM")
print("="*80)
1

# -------- LOGIN SYSTEM --------
print("\nLogin Required")
user = input("Enter username: ")
pwd = input("Enter password: ")

if user!="admin" or pwd!="1234":
    print("❌ Wrong login")
    exit()
else:
    print("✅ Login successful\n")


# -------- FUNCTIONS --------

def create_account():
    acc = int(input("Enter account number: "))

    cur.execute("select * from accounts where account_no=%s",(acc,))
    if cur.fetchone():
        print("❌ Account number already exists")
        return

    name = input("Enter name: ")
    phone = input("Enter phone: ")
    bal = int(input("Enter opening balance: "))
    pin = int(input("Set 4-digit PIN: "))

    cur.execute("insert into accounts values(%s,%s,%s,%s,%s)",(acc,name,phone,bal,pin))
    db.commit()
    print("✅ Account created successfully with PIN")


def deposit():
    acc = int(input("Enter account number: "))

    cur.execute("select * from accounts where account_no=%s",(acc,))
    if cur.fetchone()==None:
        print("❌ Account not found")
        return

    amt = int(input("Enter amount to deposit: "))

    cur.execute("update accounts set balance=balance+%s where account_no=%s",(amt,acc))
    db.commit()

    cur.execute("insert into transactions(account_no,type,amount) values(%s,'deposit',%s)",(acc,amt))
    db.commit()

    cur.execute("select balance from accounts where account_no=%s",(acc,))
    newbal = cur.fetchone()[0]

    print("💰 Money deposited")
    print("Updated Balance:", newbal)


def withdraw():
    acc = int(input("Enter account number: "))
    pin = int(input("Enter PIN: "))
    amt = int(input("Enter amount to withdraw: "))

    cur.execute("select balance,pin from accounts where account_no=%s",(acc,))
    data = cur.fetchone()

    if data==None:
        print("❌ Account not found")
    elif data[1] != pin:
        print("❌ Wrong PIN")
    elif data[0] < amt:
        print("❌ Insufficient balance")
    else:
        cur.execute("update accounts set balance=balance-%s where account_no=%s",(amt,acc))
        db.commit()

        cur.execute("insert into transactions(account_no,type,amount) values(%s,'withdraw',%s)",(acc,amt))
        db.commit()

        print("🏧 Withdraw successful")


def check_balance():
    acc = int(input("Enter account number: "))
    cur.execute("select * from accounts where account_no=%s",(acc,))
    data = cur.fetchone()

    if data:
        print("\n----- ACCOUNT DETAILS -----")
        print("Account No :",data[0])
        print("Name       :",data[1])
        print("Phone      :",data[2])
        print("Balance    :",data[3])
        print("---------------------------")
    else:
        print("❌ Account not found")


def show_all():
    cur.execute("select * from accounts")
    data = cur.fetchall()

    print("\n------ ALL CUSTOMERS ------")
    for i in data:
        print(i)


def show_transactions():
    acc = int(input("Enter account number: "))
    cur.execute("select * from transactions where account_no=%s",(acc,))
    data = cur.fetchall()

    if data:
        print("\n---- Transaction History ----")
        print("ID | Acc | Type | Amount | Date")
        print("-"*45)
        for i in data:
            print(i[0], "|", i[1], "|", i[2], "|", i[3], "|", i[4])
    else:
        print("No transaction found")


def delete_account():
    acc = int(input("Enter account number to delete: "))

    cur.execute("select * from accounts where account_no=%s",(acc,))
    if cur.fetchone()==None:
        print("❌ Account not found")
        return

    cur.execute("delete from transactions where account_no=%s",(acc,))
    cur.execute("delete from accounts where account_no=%s",(acc,))
    db.commit()

    print("🗑 Account deleted successfully")


def total_money():
    cur.execute("select sum(balance) from accounts")
    data = cur.fetchone()

    if data[0] is None:
        print("Bank empty")
    else:
        print("🏦 Total money in bank:", data[0])


# -------- MENU --------
while True:
    print("""
====== BANK MENU ======
1 Create Account
2 Deposit Money
3 Withdraw Money (PIN)
4 Check Balance
5 Show All Customers
6 Transaction History
7 Delete Account
8 Total Bank Money
9 Exit
""")

    ch = input("Enter choice: ")

    if ch=="1":
        create_account()
    elif ch=="2":
        deposit()
    elif ch=="3":
        withdraw()
    elif ch=="4":
        check_balance()
    elif ch=="5":
        show_all()
    elif ch=="6":
        show_transactions()
    elif ch=="7":
        delete_account()
    elif ch=="8":
        total_money()
    elif ch=="9":
        print("Thank you for using Bank System")
        break
    else:
        print("Invalid choice")
