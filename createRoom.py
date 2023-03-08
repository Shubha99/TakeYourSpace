import sqlite3

class CreateRoom:

    def __init__(self):
        self.room_size = None
        self.regular_price = None
        self.room_type = None

    def see_your_room(self, l_usernm):
        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        cur.execute(
             'CREATE TABLE IF NOT EXISTS "boRoomData" (ServiceID INTEGER PRIMARY KEY, Boname text, Servicetype text, SeatID int, Pricing int, Status text, OccupiedBy text);')

        rec = cur.execute("SELECT Boname FROM boRoomData WHERE Boname = (?)", [l_usernm]).fetchall()

        records_without_boname = cur.execute("SELECT ServiceID, Boname, Servicetype, SeatID, Pricing, Status FROM boRoomData WHERE Boname = ? ", [l_usernm]).fetchall()
        if rec:
            for row in records_without_boname:
                print(row)
        else:
            print("No records found. Do you want to make a new room?")
            print("1.Yes")
            print("2.No")

            io_ch = int(input("Choose your option:\t"))
            if io_ch == 1:
                self.MakeARoom(l_usernm)
            else:
                pass
    def MakeARoom(self, l_username):
        print("1.Restaurant ")
        print("2.Movie Theatre")
        print("3.Airplane")
        print("4.Conference Room")
        io_ch = int(input("Choose Service Type: \t"))
        if io_ch == 1:
            room_type = "Restaurant"

        if io_ch == 2:
            room_type = "Movie Theatre"
        if io_ch == 3:
            room_type = "Airplane"
        if io_ch == 4:
            room_type = "Conference Room"

        room_size = int(input("Enter room size"))
        l_total_seats = room_size * room_size
        io_pricing = int(input("Enter regular seat price"))

        con = sqlite3.Connection('TakeYourSpaceDb.sqlite3')
        cur = con.cursor()
        # cur.execute("DROP TABLE boRoomData")

        cur.execute(
            'CREATE TABLE IF NOT EXISTS "boRoomData" (ServiceID INTEGER PRIMARY KEY, Boname text, Servicetype text, SeatID text, Pricing float, Status text, OccupiedBy text);')

        if room_size % 2 == 0:
            num_middle_columns = 2
        else:
            num_middle_columns = 1

        # Define cost multipliers for each zone
        first_row_multiplier = 2.0  # 100% more expensive than regular price
        last_row_multiplier = 0.75  # 25% less expensive than regular price
        middle_columns_multiplier = 1.25  # 25% more expensive than regular price
        remaining_seats_multiplier = 1.0  # same price as regular price

        # Initialize a list of tuples to store the seat IDs and prices
        seats = []

        # Loop through each seat in the room
        for row in range(1, room_size + 1):
            for column in range(1, room_size + 1):
                # Determine the cost multiplier for this seat based on its zone
                if row == 1:
                    cost_multiplier = first_row_multiplier
                elif row == room_size:
                    cost_multiplier = last_row_multiplier
                elif column in range((room_size // 2) + 1 - (num_middle_columns // 2),
                                     (room_size // 2) + 1 + (num_middle_columns // 2)):
                    cost_multiplier = middle_columns_multiplier
                else:
                    cost_multiplier = remaining_seats_multiplier

                # Calculate the cost of this seat based on the regular price and cost multiplier
                seat_cost = io_pricing * cost_multiplier

                # Add the seat ID and price to the list of tuples
                seat_id = "{}{}".format(chr(ord('A') + row - 1), column)

                cur.execute(
                    "INSERT INTO boRoomData (Boname, Servicetype, SeatID, Pricing, Status, OccupiedBy) VALUES (?, ?, ?, ?, ?, ?)",
                    (l_username, room_type, seat_id, seat_cost, 'available', 'naN'))
                seats.append((seat_id, seat_cost))

        con.commit()
        con.close()
