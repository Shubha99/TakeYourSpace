
import sqlite3

class BusinessOwner:
    def __init__(self):
        self.username = None
        self.password = None

    def businessOwnerLogin(self):
        con = sqlite3.Connection('Logindb.sqlite3')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS "BusinessOwnerData" (Username text, Password text);')
        cur.execute('''INSERT INTO BusinessOwnerData (Username, Password) VALUES ('shubha', 'shubha12')''')
        cur.execute('''INSERT INTO BusinessOwnerData (Username, Password) VALUES ('rashel', 'rashel12')''')
        con.commit()

        while True:
            print("----------------------------------------------------------------")
            self.username = input("Enter  username  :")
            self.password = input("Enter  password  :")

            result = cur.execute("SELECT * FROM BusinessOwnerData WHERE Username=? AND Password=?",
                                 (self.username, self.password)).fetchone()
            if result:
                print("User login success:")
                return self.username
            else:
                print("Invalid username or password!")
                l_invalid = 1  # password does not match in the database!
                return l_invalid
            con.close()
            break


    def businessOwnerNewUser(self):

        con = sqlite3.Connection('Logindb.sqlite3')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS "BusinessOwnerData" (Username text, Password text);')
        self.username = input("Enter  username  :")
        self.password = input("Enter  password  :")

        cur.execute('''INSERT INTO BusinessOwnerData (Username, Password) VALUES (?, ?)''', (self.username, self.password))

        con.commit()

        result = con.execute("SELECT * FROM BusinessOwnerData WHERE Username=? AND Password=?",
                             (self.username, self.password)).fetchone()

        if result:
            print("User login success:")
        else:
            print("User not found")
        con.close()

        return self.username
