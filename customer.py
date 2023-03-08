import sqlite3
import datetime



class Customer:

    def __init__(self):
        self.username = None
        self.password = None

    def customerLogin(self):

        con = sqlite3.Connection('Logindb.sqlite3')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS "CustomerData" (Username text, Password text);')
        cur.execute('''INSERT INTO CustomerData (Username, Password) VALUES ('shubha', 'shubha12')''')
        cur.execute('''INSERT INTO CustomerData (Username, Password) VALUES ('rashel', 'rashel12')''')
        cur.execute('''INSERT INTO CustomerData (Username, Password) VALUES ('suebee', 'sueB12')''')
        con.commit()

        while True:
            print("----------------------------------------------------------------")
            self.username = input("Enter  username  :")
            self.password = input("Enter  password  :")

            result = con.execute("SELECT * FROM CustomerData WHERE Username=? AND Password=?",
                                 (self.username, self.password)).fetchone()

            if result:
                print("User login success")
                return self.username
            else:
                print("Invalid username or password!")
                invalid = 1 #password does not match in the database!
                return invalid

            con.close()
            break
    def customerNewUser(self):

        con = sqlite3.Connection('Logindb.sqlite3')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS "CustomerData" (Username text, Password text);')
        self.username = input("Enter  username  :")
        self.password = input("Enter  password  :")

        cur.execute('''INSERT INTO CustomerData (Username, Password) VALUES (?, ?)''', (self.username, self.password))

        con.commit()
        record = con.execute("SELECT * FROM CustomerData").fetchall()
        result = con.execute("SELECT * FROM CustomerData WHERE Username=? AND Password=?",
                             (self.username, self.password)).fetchone()

        if result:
            print("User login success")
        else:
            print("User not found")
        con.close()
        return self.username

    def customerSelectService(self):
        print("----------------------------------------------------------------")
        print("1. Book a seat\t")
        print("2. See bookings\t")
        print("3. File a complaint\t")
        print("4. See messages\t")
        print("5. Modify bookings\t")
        print("6. Logout")
        io_user = int(input("Choose your option:"))
        return io_user

    def customerSelectSeller(self):
        print("----------------------------------------------------------------")
        print("1. Business Owner\t")
        print("2. Reseller\t")
        io_user = int(input("Choose your seller:"))
        return io_user

    def customerSelectServiceType(self):
        print("----------------------------------------------------------------")
        print("1.Restaurant ")
        print("2.Movie Theatre")
        print("3.Airplane")
        print("4.Conference Room")
        io_user = int(input("Choose Service Type: \t"))
        if io_user == 1:
            l_servicetype = "Restaurant"
        if io_user == 2:
            l_servicetype = "Movie Theatre"
        if io_user == 3:
            l_servicetype = "Airplane"
        if io_user == 4:
            l_servicetype = "Conference Room"
        return l_servicetype

    def customerBookASeat(self, l_name):
        l_seller = self.customerSelectSeller()
        if l_seller == 1:
            l_servicetype = self.customerSelectServiceType()
            l_ServiceID = self.customerDisplayBusinessOwnerList(l_servicetype, l_name)

        elif l_seller == 2:
            l_servicetype = self.customerSelectServiceType()
            l_ServiceID = self.customerDisplayResellerList(l_servicetype,l_name)
        else:
            l_ServiceID = 11
            print("Incorrect Input\t")
        return l_ServiceID

    def customerSeeBookings(self, l_name):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        record = cur.execute("SELECT * FROM CustomerSeatData Where OccupiedBy = ?", [l_name]).fetchall()
        if record:
            print("Your Bookings are as follows \t")
            column_names = [description[0] for description in cur.description]
            print(column_names)
            for row in record:
                print(row)
        else:
            print("You have no bookings yet")
        cur.close()
        con.close()

    def customerFileAComplaint(self, l_name):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS "AdminComplainData" (ComplaintNo INTEGER PRIMARY KEY, Username text, Complain text, Reply text);')
        l_complaint = input("Enter your complaint:\t")
        cur.execute("INSERT INTO AdminComplainData (Username, Complain) VALUES (?,?)", [l_name, l_complaint])
        con.commit()
        #record = cur.execute("SELECT * FROM AdminComplainData").fetchall()
        #column_names = [description[0] for description in cur.description]
        #print(column_names)
        #for row in record:
        #    print(row)
        cur.close()
        con.close()

    def customerSeeMessages(self, l_name):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        print("----------------------------------------------------------------")
        print("1. See Admin Messages \t")
        print("2. See Seller Messages \t")
        print("3. See Buyer Messages \t")

        io_user = int(input("Choose your option:"))
        if io_user == 1:
            record = cur.execute("SELECT * FROM AdminComplainData WHERE username = ?", [l_name]).fetchall()
            column_names = [description[0] for description in cur.description]
            print(column_names)
            for row in record:
                print(row)
        elif io_user == 2:
            cur.execute(
                'CREATE TABLE IF NOT EXISTS "BuyerSellerNegotiation" (SerialNo INTEGER PRIMARY KEY, Username text, SeatOccupiedBy text, Buyer text, Seller text);')
            record = cur.execute("SELECT * FROM BuyerSellerNegotiation WHERE Username = ?", [l_name]).fetchall()
            if record[0]:
                column_names = [description[0] for description in cur.description]
                print(column_names)
                for row in record:
                    print(row)
                io_Serial = int(input("Input the serial no you want to reply to?"))
                l_buyertxt = input("Enter your text here:\t")
                l_Sellername = cur.execute("SELECT SeatOccupiedBy FROM BuyerSellerNegotiation where SerialNo = ?", [io_Serial]).fetchone()
                if l_Sellername:
                    cur.execute("INSERT INTO BuyerSellerNegotiation (Username, SeatOccupiedBy, Buyer) VALUES (?,?,?)",
                            [l_name, l_Sellername[0], l_buyertxt])
                    con.commit()
                else:
                    print("Incorrect input!")
            else:
                print("You have no messages!")
            #display buyer data
        elif io_user == 3:
            cur.execute(
                'CREATE TABLE IF NOT EXISTS "BuyerSellerNegotiation" (SerialNo INTEGER PRIMARY KEY, Username text, SeatOccupiedBy text, Buyer text, Seller text);')
            record = cur.execute("SELECT * FROM BuyerSellerNegotiation WHERE SeatOccupiedBy = ?", [l_name]).fetchall()
            if record:
                column_names = [description[0] for description in cur.description]
                print(column_names)
                for row in record:
                    print(row)
                io_Serial = int(input("Input the serial no you want to reply to?"))
                l_sellertxt = input("Enter your text here:\t")
                l_buyername = cur.execute("SELECT Username FROM BuyerSellerNegotiation where SerialNo = ?",
                                               [io_Serial]).fetchone()
                if l_buyername:
                    cur.execute("INSERT INTO BuyerSellerNegotiation (Username, SeatOccupiedBy, Seller) VALUES (?,?,?)",
                                [l_buyername[0], l_name, l_sellertxt])
                    con.commit()
                else:
                    print("Incorrect input!")
            else:
                print("You have no messages!")
        con.close()

    def customerModifyBookings(self, l_name):
        print("----------------------------------------------------------------")
        print("Modify Bookings")
        print("1. Resell your booking\t")
        print("2. Exchange your booking\t")
        print("3. Cancel your booking\t")
        print("4. Negotiate/fix with your buyer\t")
        print("5. Go back to bookings\t")
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        rec = cur.execute("SELECT * FROM CustomerSeatData Where OccupiedBy = ?", [l_name]).fetchall()
        if rec:
            cur.close()
            con.close()
            io_userinput = int(input("Choose your modify option:"))
            if io_userinput == 1:
                self.customerResellBooking(l_name) #will have negotiation section
            if io_userinput == 2:
                self.customerExchangeBooking(l_name)
            if io_userinput == 3:
                self.customerCancelBooking(l_name)
                # function for cancel
            if io_userinput == 4:
                self.customerNegotiateWithABuyer(l_name)
            if io_userinput == 5:
                pass
        else:
            print("You have no bookings yet!")
        pass


    def customerDisplayBusinessOwnerList(self, l_srvtype, l_name):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        record = cur.execute("SELECT * FROM boRoomData where Servicetype = ? AND Status = 'available' ", [l_srvtype]).fetchall()
        column_names = [description[0] for description in cur.description]
        if record:
            print(column_names)
            for row in record:
                print(row)
            io_serviceID = int(input("Choose your service ID from the list"))
            l_check = cur.execute("SELECT ServiceID from boRoomData WHERE ServiceID =?", [io_serviceID]).fetchone()
            if l_check:
                now = datetime.datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    #updating bo room data occupied by column
                cur.execute("UPDATE boRoomData SET OccupiedBy = ? WHERE ServiceID = ? AND Servicetype = ?",
                            [l_name, io_serviceID, l_srvtype])
                cur.execute("UPDATE boRoomData SET Status = 'Taken' WHERE ServiceID = ? AND Servicetype = ?",
                            [io_serviceID, l_srvtype])
                l_seatid = cur.execute("SELECT SeatID from boRoomData WHERE ServiceID =?", [io_serviceID]).fetchone()
                l_pricing = cur.execute("SELECT Pricing from boRoomData WHERE ServiceID =?", [io_serviceID]).fetchone()
                l_boname = cur.execute("SELECT Boname from boRoomData WHERE ServiceID =?", [io_serviceID]).fetchone()

                #updating customer seat data
                cur.execute(
                    'CREATE TABLE IF NOT EXISTS "CustomerSeatData" (Srn INTEGER PRIMARY KEY, Boname text, SeatID int, Servicetype text, Price int, OccupiedBy text, timestamp int);')
                cur.execute(
                    "INSERT INTO CustomerSeatData (Boname, SeatID, Servicetype, Price, OccupiedBy, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    [l_boname[0], l_seatid[0], l_srvtype, l_pricing[0], l_name, timestamp])

                rec = cur.execute("SELECT Price FROM CustomerSeatData Where OccupiedBy = ?", [l_name]).fetchall()
                print(f"Your seat is booked under NAME:{l_name} PRICE:${l_pricing[0]} SERVICE TYPE: {l_srvtype}")
                print("----------------------------------------------------------------")
                print("1. Yes\t")
                print("2. No\t")
                io_confirm = int(input("Do you confirm?:"))
                if io_confirm == 1:
                    con.commit()
                else:
                    io_serviceID = 11
            else:
                print("No rooms available for the service")
                io_serviceID = 11
        else:
            print("Service ID does not exist!")
            pass
        cur.close()
        con.close()
        return io_serviceID

    def customerDisplayResellerList(self, l_srvtype, l_name):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS "ResellerSeatData" (ServiceID INTEGER PRIMARY KEY, Boname text, '
                    'SeatID int, Servicetype text, Price int, DiscountRate int, NewPrice int, OccupiedBy text);')
        record = cur.execute("SELECT * FROM ResellerSeatData WHERE Servicetype = ? AND OccupiedBy != ?",
                             [l_srvtype, l_name]).fetchall()
        column_names = [description[0] for description in cur.description]
        if record:
            print(column_names)
            for row in record:
                print(row)
            print("----------------------------------------------------------------")
            print("1. Pick a seat\t")
            print("2. Go back to previous option\t")
            io_user = int(input("Choose your option \t"))
            if io_user == 1:
                now = datetime.datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                io_serviceID = int(input("Choose your Service ID from the list"))
#updating reseller seat data and deletion of the service
                l_SeatOccupiedBy = cur.execute("SELECT OccupiedBy from ResellerSeatData WHERE ServiceID = ? AND Servicetype = ?",[ io_serviceID, l_srvtype]).fetchone()
                cur.execute("UPDATE ResellerSeatData SET OccupiedBy = ? WHERE ServiceID = ? AND Servicetype = ?",
                            [l_name, io_serviceID, l_srvtype]) #list updated

                l_pricing = cur.execute("SELECT NewPrice from ResellerSeatData WHERE ServiceID =?", [io_serviceID]).fetchone()
                l_boname = cur.execute("SELECT Boname from ResellerSeatData WHERE ServiceID = ?", [io_serviceID]).fetchone()
                l_seatid = cur.execute("SELECT SeatID from ResellerSeatData WHERE ServiceID = ?", [io_serviceID]).fetchone()
                cur.execute("DELETE FROM ResellerSeatData WHERE ServiceID = ?", [io_serviceID])
#updating boroomdata column occupied by
                cur.execute("UPDATE boRoomData SET OccupiedBy = ? WHERE Boname = ? AND SeatID = ? AND servicetype = ?",
                            [l_name, l_boname[0], l_seatid[0], l_srvtype])
#updating Customer Seat data
                cur.execute(
                    'CREATE TABLE IF NOT EXISTS "CustomerSeatData" (Srn INTEGER PRIMARY KEY, Boname text, SeatID int, Servicetype text, Price int, OccupiedBy text, timestamp int);')

                rec = cur.execute("SELECT Price FROM CustomerSeatData Where OccupiedBy = ?", [l_name]).fetchall()
                print(f"Your seat is booked under NAME:{l_name} PRICE:${l_pricing[0]} SERVICE TYPE: {l_srvtype}")
                print("----------------------------------------------------------------")
                print("1. Yes\t")
                print("2. Negotiate with the seller\t")
                print("3. No\t")
                io_confirm = int(input("Do you confirm?:"))
                if io_confirm == 1:
                    cur.execute(
                        "INSERT INTO CustomerSeatData (Boname, SeatID, Servicetype, Price, OccupiedBy, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                        [l_boname[0], l_seatid[0], l_srvtype, l_pricing[0], l_name, timestamp])
                    con.commit()
                elif io_confirm == 2:
                    cur.execute(
                        'CREATE TABLE IF NOT EXISTS "BuyerSellerNegotiation" (SerialNo INTEGER PRIMARY KEY, Username text, SeatOccupiedBy text, Buyer text, Seller text);')
                    print("Please mention the seat details ( seat id, service) and the negotiation price!")
                    l_buyertxt = input("Enter your text here:\t")
                    cur.execute("INSERT INTO BuyerSellerNegotiation (Username, SeatOccupiedBy, Buyer) VALUES (?,?,?)",
                                [l_name, l_SeatOccupiedBy[0], l_buyertxt])
                    con.commit()

                else:
                    io_serviceID = 11
            if io_user == 2:
                io_serviceID = 11
        else:
            print("No rooms available for the service")
            io_serviceID = 11
        cur.close()
        con.close()
        return io_serviceID

    def customerResellBooking(self, l_name):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()

        print("1. Yes \t")
        print("2. No \t")
        io_user = int(input("Do you wish to sell your seat?"))

        if io_user == 1:
            l_srvtype = self.customerSelectServiceType()  # roomtype
            record = cur.execute("SELECT * FROM CustomerSeatData Where OccupiedBy = ? AND Servicetype = ?",
                                    [l_name, l_srvtype]).fetchall()
            column_names = [description[0] for description in cur.description]
            if record:
                print(column_names)
                for row in record:
                    print(row)
                io_serviceid = int(input("Select the SRN number you want to sell"))
                l_checker = cur.execute("SELECT * FROM CustomerSeatData Where OccupiedBy = ? AND Srn = ?",
                                        [l_name, io_serviceid]).fetchone()
                if l_checker:
                    io_newprice = int(input("How much do you want to sell the seat for?"))

                    l_price = cur.execute(
                        "SELECT Price FROM CustomerSeatData Where OccupiedBy = ? AND Srn = ?",
                        [l_name, io_serviceid]).fetchone()
                    l_boname = cur.execute(
                        "SELECT Boname FROM CustomerSeatData Where OccupiedBy = ? AND Srn = ?",
                        [l_name, io_serviceid]).fetchone()
                    l_seatid = cur.execute(
                        "SELECT SeatID FROM CustomerSeatData Where OccupiedBy = ? AND Srn = ?",
                        [l_name, io_serviceid]).fetchone()
                    l_discountrat = 100 - ((io_newprice * 100) / l_price[0])

                    cur.execute(
                        'CREATE TABLE IF NOT EXISTS "ResellerSeatData" (ServiceID INTEGER PRIMARY KEY, Boname text, SeatID int, Servicetype text, Price int, DiscountRate int, NewPrice int, OccupiedBy text);')

                    cur.execute(
                        "INSERT INTO ResellerSeatData (Boname, SeatID, Servicetype, Price, DiscountRate, NewPrice, OccupiedBy) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (l_boname[0], l_seatid[0], l_srvtype, l_price[0], l_discountrat, io_newprice, l_name))

                    con.execute("DELETE FROM CustomerSeatData WHERE OccupiedBy = ? AND SeatID = ? AND Servicetype = ?",
                                [l_name, l_seatid[0], l_srvtype])
                    con.commit()
                else:
                    print("You dont have any such service ID under your bookings!")
            else:
                print("You don't have any booking under this service type under your bookings!")

        if io_user == 2:
            pass
        con.close()

    def customerExchangeBooking(self, l_name ):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        rec = cur.execute("SELECT * FROM CustomerSeatData Where OccupiedBy = ?", [l_name]).fetchall()
        if rec:
            record = cur.execute("SELECT * FROM CustomerSeatData Where OccupiedBy = ?",
                                 [l_name]).fetchall()
            column_names = [description[0] for description in cur.description]
            if record:
                print(column_names)
                for row in record:
                    print(row)
                io_serviceid = int(input("Select SRN ID you want to exchange:"))
                io_servicetype = input("Select the service type you want to exchange:")
                l_boname = cur.execute("SELECT Boname FROM CustomerSeatData Where OccupiedBy = ? AND Srn = ? AND Servicetype = ?",
                                     [l_name, io_serviceid, io_servicetype]).fetchone()
                l_seatid = cur.execute("SELECT SeatID FROM CustomerSeatData Where OccupiedBy = ? AND Srn = ? AND Servicetype = ?",
                                     [l_name, io_serviceid, io_servicetype]).fetchone()
                if l_boname:

                    cur.execute("DELETE FROM CustomerSeatData WHERE SRN = ? AND Servicetype = ?", [io_serviceid, io_servicetype])
                    cur.execute("Update boRoomData SET Status = 'available' where Boname = ? AND SeatID = ? AND Servicetype = ? AND OccupiedBy = ?",[l_boname[0], l_seatid[0], io_servicetype, l_name])
                    cur.execute("Update boRoomData SET OccupiedBy = 'naN' where Boname = ? AND SeatID = ? AND Servicetype = ? AND OccupiedBy = ?",
                        [l_boname[0], l_seatid[0], io_servicetype, l_name])
                    con.commit()
                    cur.close()
                    con.close()
                    #change taken to available on boroomdata, delete from customerseatdat list
                    self.customerBookASeat(l_name)

                else:
                    print("You SRN id or service type is incorrect!")
        else:
            print("You have no bookings!")
            pass

    def customerCancelBooking(self, l_name):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        record = cur.execute("SELECT * FROM CustomerSeatData Where OccupiedBy = ?", [l_name]).fetchall()
        column_names = [description[0] for description in cur.description]
        if record:
            print(column_names)
            for row in record:
                print(row)
            io_serviceid = int(input("Enter SRN you wish to cancel.\t"))
            io_servicetype = input("Select the service type you want to cancel\t")
            l_check = cur.execute("SELECT * FROM CustomerSeatData Where OccupiedBy = ? AND Srn = ? AND Servicetype = ?",
                                  [l_name, io_serviceid, io_servicetype]).fetchall()
            if l_check:
                l_boname = cur.execute("SELECT Boname FROM CustomerSeatData Where OccupiedBy = ? AND Srn = ? AND Servicetype = ?",
                                  [l_name, io_serviceid, io_servicetype]).fetchone()
                l_seatid = cur.execute(
                    "SELECT SeatID FROM CustomerSeatData Where OccupiedBy = ? AND Srn = ? AND Servicetype = ?",
                    [l_name, io_serviceid, io_servicetype]).fetchone()
                cur.execute("DELETE FROM CustomerSeatData WHERE OccupiedBy = ? AND Srn = ? AND Servicetype = ?", [l_name, io_serviceid, io_servicetype])
                cur.execute(
                "Update boRoomData SET Status = 'available' where Boname = ? AND SeatID = ? AND Servicetype = ? AND OccupiedBy = ?",
                [l_boname[0], l_seatid[0], io_servicetype, l_name])
                cur.execute("Update boRoomData SET OccupiedBy = 'naN' where SeatID = ? AND Servicetype = ? AND OccupiedBy = ?",
                        [l_seatid[0], io_servicetype, l_name])
                con.commit()
            else:
                print("You have no service ID in that service type!")
        else:
            print("You have no bookings to cancel!")
        #remove seat id from customerdata, make it avaible on boroomdata
        con.close()

    def customerNegotiateWithABuyer(self, l_name):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        record = cur.execute("SELECT * FROM BuyerSellerNegotiation WHERE SeatOccupiedBy  = ?", [l_name]).fetchall()
        x = cur.execute("SELECT * FROM ResellerSeatData WHERE OccupiedBy = ?", [l_name]).fetchall()
        column_names = [description[0] for description in cur.description]
        print(record)
        print(x)
        if x:
            io_seat = int(input("Enter SeatID you want to sell"))
            io_servicetype = input("Enter the service type of the seat")
            io_negotiatedprice = int(input("How much amount are you selling your seat for?"))
            l_newbuyer = cur.execute("SELECT Username FROM BuyerSellerNegotiation WHERE SeatOccupiedBy = ?",
                                             [l_name]).fetchone()
            l_boname = cur.execute("SELECT Boname FROM ResellerSeatData WHERE SeatID = ? AND Servicetype = ?", [io_seat,io_servicetype]).fetchone()
            l_ogprice = cur.execute("SELECT Price FROM ResellerSeatData WHERE SeatID = ? AND Servicetype = ?", [io_seat,io_servicetype]).fetchone()
            cur.execute("DELETE FROM ResellerSeatData WHERE Boname = ? AND SeatID = ? AND Servicetype = ? AND Price = ?",
                                [l_boname[0], io_seat, io_servicetype, l_ogprice[0]])
                    # updating boroomdata column occupied by
            cur.execute("UPDATE boRoomData SET OccupiedBy = ? WHERE Boname = ? AND SeatID = ? AND servicetype = ?",
                                [l_newbuyer[0], l_boname[0], io_seat, io_servicetype])
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("INSERT INTO CustomerSeatData (Boname, SeatID, Servicetype, Price, OccupiedBy, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    [l_boname[0], io_seat, io_servicetype, io_negotiatedprice, l_newbuyer[0], timestamp])
            rec = cur.execute("SELECT Price FROM CustomerSeatData Where OccupiedBy = ?", [l_name]).fetchall()
            print(f"Your seat is booked under NAME:{l_newbuyer[0]} PRICE:${io_negotiatedprice} SERVICE TYPE: {io_servicetype}")
            print("----------------------------------------------------------------")
            print("1. Yes\t")
            print("2. No\t")
            io_confirm = int(input("Do you confirm?:"))
            if io_confirm == 1:
                con.commit()
            else:
                pass
        else:
            print("You have no negotiations/ no sale on reselling seat!")
        con.close()