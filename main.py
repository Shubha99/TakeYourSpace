
from businessOwner import *
from admin import *
from customer import *
from createRoom import *
import time


def start():  # called function
    print("1. Admin Login :\t")
    print("2. Business Owner Login :\t")
    print("3. Customer Login :\t")
    print()
    adminObj = Admin()
    customerObj = Customer()
    createRoomObj = CreateRoom()
    businessOwnerObj = BusinessOwner()
    ch = int(input("Choose Correct option :"))

    if ch == 1:
        # admin class object creation
        check = adminObj.adminLogin()
        if check == 1:
            start()
        else:
            while True:
                print("1. See Complaints")
                print("2. Logout ")

                ch = int(input("Choose you option:\t"))
                if ch == 1:
                    adminObj.adminDisplayComplaints()
                else:
                    start()
                    break


    elif ch == 2:

        if ch == 2:
            print("1. New User \t")
            print("2. User Login \t")
            opt_c = int(input("Choose Your option :"))
            if opt_c == 1:
                name = businessOwnerObj.businessOwnerNewUser()
            if opt_c == 2:
                name = businessOwnerObj.businessOwnerLogin()
                if name == 1:
                    start()
        while ch != 0 :
            print("1. See Your Room")
            print("2. Make Your Room")
            print("3. Logout ")
            ch = int(input("Choose Your Option:\t"))
            if ch ==1:

                createRoomObj.see_your_room(name)

            elif ch == 2:
                createRoomObj.MakeARoom(name)
            elif ch == 3:
                start()
            else:
                print("Choose the Correct Option")

            time.sleep(2)
    elif ch == 3:

        print("1. New User \t")
        print("2. User Login \t")
        opt_c = int(input("Choose Your option :"))
        if opt_c == 1:
            name = customerObj.customerNewUser()
        if opt_c == 2:
            name = customerObj.customerLogin()
            if name == 1:
                start()
        while True:
            userInput = customerObj.customerSelectService()
            if userInput == 1:
                ret = customerObj.customerBookASeat(name)
                if ret == 11:
                    pass
            if userInput == 2:
                customerObj.customerSeeBookings(name)
                pass
            if userInput == 3:
                customerObj.customerFileAComplaint(name)
                pass
            if userInput == 4:
                customerObj.customerSeeMessages(name)
                pass
            if userInput == 5:
                customerObj.customerModifyBookings(name)
                pass
            if userInput == 6:
                start()
            else:

                pass
start()  # calling function
# =======================================================================