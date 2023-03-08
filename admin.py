import sqlite3

class Admin:

    def __init__(self):
        self.username = None
        self.password = None

    def adminLogin(self):
        con = sqlite3.Connection('Logindb.sqlite3')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS "AdminData" (Username text, Password text);')
        cur.execute('''INSERT INTO AdminData (Username, Password) VALUES ('shubha', 'shubha12')''')
        cur.execute('''INSERT INTO AdminData (Username, Password) VALUES ('rashel', 'rashel12')''')
        con.commit()
        while True:
            print("----------------------------------------------------------------")
            self.username = input("Enter  username  :")
            self.password = input("Enter  password  :")
            result = cur.execute("SELECT * FROM AdminData WHERE Username=? AND Password=?",
                                             (self.username, self.password)).fetchone()
            if result:
                print("User login success:")
                return self.username
            else:
                print("Invalid username or password!")
                l_invalid = 1  # password does not match in the database!
                return l_invalid



            break
        con.close()

    def adminDisplayComplaints(self):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS "AdminComplainData" (ComplaintNo INTEGER PRIMARY KEY, Username text, Complain text, Reply text);')
        rec = cur.execute("SELECT * FROM AdminComplainData").fetchall()
        if rec:
            for row in rec:
                print(row)

            while True:
                l_complaintno = input("Enter the complaint number you want to reply to: \t")
                l_check = cur.execute("SELECT Complain FROM AdminComplainData Where ComplaintNo = ?", [l_complaintno]).fetchone()
                if l_check:
                    io_reply = input("Reply:")
                    cur.execute("UPDATE AdminComplainData SET Reply = ? WHERE ComplaintNo = ?", [io_reply, l_complaintno])
                    con.commit()
                else:
                    print("incorrect complaint number")
                break
            con.close()
        else:
            print("You have no complains!")
