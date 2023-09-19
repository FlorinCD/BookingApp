import collections
import math
import time
import tkinter
from queue import Queue
import csv
from tkinter import *
from datetime import datetime
from datetime import timedelta
import os

'''
Flight class will be use to manipulate the flights from items folder and will be the parent class for Reservation class
'''


check_dic = {} # dict for checking if all the data files are in the project


class Flight:
    all = []  # here are stored the Flight objects that are instantiated

    def __init__(self, company: str = "", ticket_price: float = 0.0, location: str = "", destination: str = "", stopover: str = ""):
        self.company = company
        self.location = location
        self.destination = destination
        self.stopover = stopover
        self.ticket_price = ticket_price
        Flight.all.append(self)

    def show_flight(self):
        return print(self.company, self.ticket_price, self.location, self.destination, self.stopover)

    @classmethod
    def instantiate_from_csv(cls):  # instantiating all the objects from items file
        with open('items.csv', 'r') as f:
            reader = csv.DictReader(f)
            items = list(reader)

        for item in items:
            Flight(item.get('company'), item.get('price'),item.get('location'),item.get('destination'), item.get('stopover'))

    def __repr__(self):
        return f"Flight('{self.company}','{self.ticket_price}','{self.location}','{self.destination}','{self.stopover}')"

    @classmethod
    def show_all_flights(cls):  # returns the text from items file with all flights as string
        file = open('items.csv', 'r')
        reader_set = csv.reader(file)
        text = "Company  Price  Location  Destination  Stopover\n\n"
        for i, row in enumerate(reader_set):
            if i != 0:
                text += f"{row[0], row[1], row[2], row[3], row[4]}\n"
        file.close()
        return text


'''
The Reservation class is used to manipulate the bookings that are made and the data from reservations file
'''


class Reservation(Flight):
    last_date_update = ""  # variables used for booking update
    name_update = ""
    type_cls_update = ""
    fly_type_update = ""
    dat_update = ""
    comp_name_update = ""
    loc_update = ""
    destinat_update = ""
    price_update = ""
    stop_update = ""
    location_flight = ""
    destination_flight = ""
    company_name = ""
    client_name = ""
    locat = ""
    dest = ""
    update_info = False  # marks if the data for update booking are valid
    all_reservations = []  #
    instantiate_bool = False  # here are stored the Reservation objects that are instantiated
    real_object = False  # it marks if the data input from user is correct in order to add it to the file

    @classmethod
    def delete_reservation(cls, name, dat):  # deletes the specific booking
        delete_info = False
        f = open('reservations.csv', 'r+')
        L = []
        reader = csv.reader(f)
        found = False
        for row in reader:
            if row and row[0] == name and row[7] == dat:
                found = True
                continue
            if row and row[0]: L.append(row)
        f.close()
        if not found:
            pass
            # print("There's no reservation on this name or on this date!")
        else:
            f = open('reservations.csv', 'w+', newline="")
            writer = csv.writer(f)
            writer.writerows(L)
            f.close()
        return found

    @classmethod
    def get_set(cls):  # gets a set with all the flights data
        s = set()
        file = open('items.csv', 'r')
        reader_set = csv.reader(file)
        for i, row in enumerate(reader_set):
            if i != 0:
                s.add((row[0],row[1],row[2],row[3],row[4]))
        file.close()
        return s

    @classmethod
    def search_for_a_client(cls, name):  # returns a string with all the bookings made on a specific name
        person_bool = False
        Reservation.client_name += name
        file = open('reservations.csv', 'r')
        reader_set = csv.reader(file)
        person_list = ""
        for row in reader_set:
            if row[0] == Reservation.client_name:
                person_bool = True
                person_list += f"{row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]}\n"
        if person_bool:
            pass
            # print(f"All reservations of {Reservation.client_name} are: ")
        else:
            person_list = "The name does not exist in the database or is wrongly written!"
            # print(f"{Reservation.client_name} does not exist in the database or is wrongly written!")
        file.close()
        return person_list

    @classmethod
    def search_for_a_company(cls, name):  # returns a string with all the bookings made on a specific company
        company_bool = False
        Reservation.company_name += name
        file = open('reservations.csv', 'r')
        reader_set = csv.reader(file)
        company_list = ""
        for row in reader_set:
            if row[4] == Reservation.company_name:
                company_bool = True
                company_list += f"{row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]}\n"
        if company_bool:
            pass
            # print("All reservations made on this airline company are: ")
            # print(company_list)
        else:
            # print("There is no reservation on this company or it doesn't exist in the database (or wrongly written)!")
            company_list = "There is no reservation on this company or it doesn't exist in the database (or wrongly written)!"
        file.close()
        return company_list

    @classmethod
    def search_for_a_flight(cls, l, d):  # returns a string with all the bookings made on a specific flight
        loc_dest_bool = False            # location -- destination
        Reservation.location_flight = l
        Reservation.destination_flight = d
        file = open(r'reservations.csv', 'r')
        reader_set = csv.reader(file)
        flights_list = ""
        for row in reader_set:
            if row[5] == Reservation.location_flight and row[6] == Reservation.destination_flight:
                loc_dest_bool = True
                flights_list += f"{row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]}\n"
        if loc_dest_bool:
            pass
            # print("All the flights with this location and destination are: ")
            # print(flights_list)
        else:
            flights_list += "There is no flight on that specific route!"
            # print("There is no flight on that specific route!")
        # print(Reservation.location_flight, Reservation.destination_flight)
        file.close()
        return flights_list

    def __init__(self, person_name: str = "", class_type: str = "", flight_type: str = "",ticket_price: float = 0.0, company: str = "", location: str = "", destination: str = "", date: str = "", stopover: str = ""):
        super(Reservation, self).__init__(
            company, ticket_price, location, destination, stopover
        )
        self.person_name = person_name
        self.class_type = class_type
        self.flight_type = flight_type
        self.date = date
        self.company = company
        self.location = location
        self.destination = destination
        self.stopover = stopover
        self.ticket_price = ticket_price
        # print(person_name, class_type, flight_type, date, company, location, destination, ticket_price, stopover)
        l_class_type = ["first class", "second class"]
        l_flight_type = ["one-way", "round-trip"]

        if (company, ticket_price, location, destination, stopover) in Reservation.get_set() and self.class_type in l_class_type and self.flight_type in l_flight_type and Reservation.check_date(self.date) and not Reservation.check_for_samedate(self.person_name, self.date):
            self.real_object = True
        else:
            # print("The information is wrong.. please try again following the suggestions. ")
            self.real_object = False
        Reservation.all_reservations.append(self)

    def ad_reser_tofile(self):  # adds the booking to the reservations file
        # print(self.real_object)
        if self.real_object:
            with open('reservations.csv', 'a', newline='') as f:
                thewriter = csv.writer(f)
                if self.person_name != "":
                    thewriter.writerow([self.person_name, self.class_type, self.flight_type, self.ticket_price, self.company,
                                        self.location, self.destination, self.date, self.stopover])

    @classmethod
    def instantiate_reservations(cls):  # instantiates all the objects from reservations file
        Reservation.instantiate_bool = True
        with open('reservations.csv', 'r') as f:
            reader = csv.DictReader(f)
            items = list(reader)

        for item in items:
            Reservation(item.get('person_name'), item.get('class_type'), item.get('flight_type'),item.get('ticket_price'), item.get('company'), item.get('location'), item.get('destination'), item.get('date'), item.get('stopover'))
        Reservation.instantiate_bool = False

    def __repr__(self):
        return f"Reservation('{self.person_name}','{self.company}','{self.class_type}','{self.flight_type}',{self.ticket_price},'{self.location}','{self.destination}','{self.date}','{self.stopover}')"

    @classmethod
    def update_reservation(cls, name, class_type, flight, price, comp, loc, dest, date, stop):  # updates the booking
        f = open('reservations.csv', 'r+')
        L = []
        reader = csv.reader(f)
        found = False
        Reservation.name_update += name
        # print(Reservation.get_set())
        # print(name, class_type, flight, price, comp, loc, dest, date, stop)
        for row in reader:
            if row and row[0] == Reservation.name_update and row[7] == Reservation.last_date_update:
                found = True
                Reservation.type_cls_update += class_type
                Reservation.fly_type_update += flight
                Reservation.price_update += price
                Reservation.comp_name_update += comp
                Reservation.loc_update += loc
                Reservation.destinat_update += dest
                Reservation.dat_update += date
                Reservation.stop_update += stop
                l_class_type = ["first class", "second class"]
                l_flight_type = ["one-way", "round-trip"]
                if (Reservation.comp_name_update, Reservation.price_update, Reservation.loc_update, Reservation.destinat_update, Reservation.stop_update) in Reservation.get_set() and Reservation.type_cls_update in l_class_type and Reservation.fly_type_update in l_flight_type and Reservation.check_date(Reservation.dat_update) and not Reservation.check_for_samedate(name, date):
                    row[1] = Reservation.type_cls_update
                    row[2] = Reservation.fly_type_update
                    row[3] = Reservation.price_update
                    row[4] = Reservation.comp_name_update
                    row[5] = Reservation.loc_update
                    row[6] = Reservation.destinat_update
                    row[7] = Reservation.dat_update
                    row[8] = Reservation.stop_update
                    Reservation.update_info = True
                if not Reservation.update_info:
                    pass
                    # print("The information for that specific flight is wrong! Please look up at the flights table!")
            if row and row[0]: L.append(row)
        # print(Reservation.comp_name_update, Reservation.price_update, Reservation.loc_update, Reservation.destinat_update, Reservation.stop_update)
        f.close()
        if not found:
            pass
            # print("There's no reservation on this name!")
        else:
            f = open('reservations.csv', 'w+', newline="")
            writer = csv.writer(f)
            writer.writerows(L)
            f.close()

    @classmethod
    def get_route(cls, l, d):  # function that use a DFS searching algorithm to find a path
        graph = {}             # between a location and a destination
        route = []
        file = open('items.csv', 'r')
        reader_set = csv.reader(file)
        Reservation.locat += l
        Reservation.dest += d
        for i, row in enumerate(reader_set):
            if i != 0:
                if row[2] not in graph:
                    graph[row[2]] = [row[3]]
                    if row[4] != "" and row[4] not in graph[row[2]]:
                        graph[row[2]].append(row[4])
                if row[2] in graph:
                    if row[3] not in graph[row[2]]:
                        graph[row[2]].append(row[3])
                    if row[4] != "" and row[4] not in graph[row[2]]:
                        graph[row[2]].append(row[4])
                if row[3] not in graph:
                    graph[row[3]] = []
                if row[4] not in graph:
                    graph[row[4]] = []

        # print(Reservation.locat, Reservation.dest)
        my_route = ""
        if Reservation.locat not in graph:
            my_route += "The given location of flight is not on our table!"
            return my_route

        def bfs(graph, node, destinat, been, r):  # the DFS algorithm
            queue = Queue()
            paths = {node: [node]}
            queue.put(node)
            been.add(node)

            while not queue.empty():
                u = queue.get()
                if u == destinat:
                    r["Route"] = paths[u]
                    break
                if u in graph:
                    for n in graph[u]:
                        if n not in been:
                            paths[n] = paths[u] + [n]
                            queue.put(n)
                            been.add(n)

        r = {"Route": []}
        been = set()
        bfs(graph, Reservation.locat, Reservation.dest, been, r)
        # print(r["Route"])
        if not r["Route"]:
            # print(f"There's no route to get from {Reservation.locat} to {Reservation.dest}!")
            my_route += "There is no route for that location or destination!"
        else:
            # print(f"The route from {Reservation.locat} to {Reservation.dest} is: ")
            for i, city in enumerate(r["Route"]):
                if i != len(r["Route"])-1:
                    my_route += city + ' -> '
                else:
                    my_route += city
            # print(my_route)
        file.close()
        return my_route

    @classmethod
    def show_reservations(cls):  # returns a text with all the bookings from reservations file as a string
        file = open('reservations.csv', 'r')
        reader_set = csv.reader(file)
        text = "Name | Class type | Flight type | Ticket price | Company | Location | Destination | Date | Stopover\n\n"
        for i, row in enumerate(reader_set):
            if i != 0:
                text += f"{row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]}\n"
        file.close()
        return text

    @classmethod
    def check_date(cls, test_str):  # verifies if the input date is valid
        format = "%d-%m-%Y"

        max_date = datetime.now()
        max_date += timedelta(days=365)  # the input date can't be over 1 year

        current_date = datetime.now()  # current date
        res = True
        try:
            res = bool(datetime.strptime(test_str, format))
        except ValueError:
            res = False
        if res:  # comparing if the input date is valid
            input_date = datetime.strptime(test_str, "%d-%m-%Y")
            # print(current_date, input_date, max_date)
            if current_date.date() <= input_date.date() <= max_date.date():
                pass
            else:
                res = False
        return res

    @classmethod
    def check_for_samedate(cls, name, date):  # a method that checks if the user makes or updates a booking on a date
        file = open('reservations.csv', 'r')  # that is on his other booking
        reader_set = csv.reader(file)         # we can't have 2 bookings with the same name on the same date
        find = False
        for i, row in enumerate(reader_set):
            if row[0] == name and row[7] == date:
                find = True
                break
        file.close()
        return find


def show_all_flights():  # displays all the flights
    Flight.instantiate_from_csv()
    flights_window = Toplevel()
    flights_window.geometry("560x700")
    flights_window.resizable(False, False)
    flights_window.title('All flights')
    flights_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
    flights_window.config(bg="#d7c5ed")
    text1 = Flight.show_all_flights()
    label_flights = Label(flights_window, text=f"All flights from all companies: ", bg="#d7c5ed", font=('Abadi Bold', 16)).pack()
    Label(flights_window, text=text1, bg="#d7c5ed", font=('Abadi Bold', 14)).pack()


def find_route():  # finds a route between the input location and input destination
    def inputed():
        label1_final_route = Label(route_window,
                                   text="                                                                                              "
                                        "                                                          ***"
                                   , bg="#284f24", font=('Abadi Bold', 14))
        label1_final_route.place(x=100, y=400)

    def click_info_route():  # functionality to the find_route button
        inputed()

        text_location = entry_location.get()
        entry_location.delete(0, END)

        text_destination = entry_destination.get()
        entry_destination.delete(0, END)
        text_final_route = Reservation.get_route(text_location, text_destination)

        label_final_route = Label(route_window, text=text_final_route, bg="#284f24",font=('Abadi Bold', 14))
        label_final_route.place(x=100, y=400)

        Reservation.locat = ""
        Reservation.dest = ""

    route_window = Toplevel()  # find_route window
    route_window.geometry("900x600")
    route_window.resizable(False, False)
    route_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
    route_window.title(f"Let's find a route")

    startframe = tkinter.Frame(route_window)
    canvas = tkinter.Canvas(startframe, width=1280, height=720)  # width=1280, height=720)
    startframe.pack()
    canvas.pack()

    # Escape / raw string literal
    image_book = tkinter.PhotoImage(file=r"Routes.png")
    route_window.one = image_book  # to prevent the image garbage collected.
    canvas.create_image((0, 0), image=image_book, anchor='nw')

    label_route = Label(route_window, text="Create a route from a location to a destination", bg="#284f24", font=('Abadi Bold', 14))
    label_route.place(x=250, y=10)

    label_location = Label(route_window, text="Enter the location: ", bg="#284f24",font=('Abadi Bold', 14))
    label_location.place(x=20, y=100)
    entry_location = Entry(route_window, width=30)
    entry_location.place(x=200, y=105)

    label_destination = Label(route_window, text="Enter the destination: ", bg="#284f24", font=('Abadi Bold', 14))
    label_destination.place(x=20, y=140)
    entry_destination = Entry(route_window, width=30)
    entry_destination.place(x=225, y=145)

    button_route = Button(route_window, text="Submit")
    button_route.config(font=("Ink free", 10, 'bold'), bg="#045c39", fg="#a9abd1")
    button_route.config(command=click_info_route)
    button_route.place(x=75, y=190)


def search():  # the searching window
    def search_for_client():  # the searching for a client window
        search_client_window = Toplevel()
        search_client_window.resizable(False, False)
        search_client_window.geometry("900x598")
        search_client_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
        search_client_window.title('Search for a client')

        startframe = tkinter.Frame(search_client_window)
        canvas = tkinter.Canvas(startframe, width=1280, height=720)
        startframe.pack()
        canvas.pack()

        image_book = tkinter.PhotoImage(file=r"searchclientphoto.png")
        search_client_window.one = image_book  # to prevent the image garbage collected.
        canvas.create_image((0, 0), image=image_book, anchor='nw')

        text_client = entry_s_for_client.get()
        clientsreserv = Reservation.search_for_a_client(text_client)
        if clientsreserv == "The name does not exist in the database or is wrongly written!":
            text_client = "Wrong information"
            label_client_window = Label(search_client_window, text=f"{text_client}!",
                                        font=("Abadi Bold", 11), bg="#e3daeb")
        else:
            label_client_window = Label(search_client_window, text=f"{text_client}'s reservations:",font=("Abadi Bold", 11), bg="#e3daeb")
        label_client_window.place(x=300, y=20)

        Reservation.client_name = ""
        label_sub_for_client = Label(search_client_window, text=clientsreserv, font=("Abadi Bold", 11), bg="#e3daeb")
        label_sub_for_client.place(x=70, y=70)

    def search_for_company():  # the searching for a company window
        search_company_window = Toplevel()
        search_company_window.resizable(False, False)
        search_company_window.geometry("900x598")
        search_company_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
        search_company_window.title("Search for a company's reservations")

        startframe = tkinter.Frame(search_company_window)
        canvas = tkinter.Canvas(startframe, width=1280, height=720)
        startframe.pack()
        canvas.pack()

        image_book = tkinter.PhotoImage(file=r"searchclientphoto.png")
        search_company_window.one = image_book  # to prevent the image garbage collected.
        canvas.create_image((0, 0), image=image_book, anchor='nw')

        text_company = entry_s_for_company.get()
        companyreserv = Reservation.search_for_a_company(text_company)
        if companyreserv == "There is no reservation on this company or it doesn't exist in the database (or wrongly written)!":
            text_company = "Wrong information"
            label_company_window = Label(search_company_window, text=f"{text_company}!",
                                         font=("Abadi Bold", 11), bg="#e3daeb")
        else:
            label_company_window = Label(search_company_window, text=f"{text_company}'s reservations:", font=("Abadi Bold", 11), bg="#e3daeb")
        label_company_window.place(x=300, y=20)

        Reservation.company_name = ""
        label_sub_for_company = Label(search_company_window, text=companyreserv, font=("Abadi Bold", 11), bg="#e3daeb")
        label_sub_for_company.place(x=70, y=70)

    def search_for_flight():  # the searching for a flight window
        search_flight_window = Toplevel()
        search_flight_window.resizable(False, False)
        search_flight_window.geometry("900x598")
        search_flight_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
        search_flight_window.title("Search for a flight")

        startframe = tkinter.Frame(search_flight_window)
        canvas = tkinter.Canvas(startframe, width=1280, height=720)
        startframe.pack()
        canvas.pack()

        image_book = tkinter.PhotoImage(file=r"searchclientphoto.png")
        search_flight_window.one = image_book  # to prevent the image garbage collected.
        canvas.create_image((0, 0), image=image_book, anchor='nw')

        text_location = entry_s_for_location.get()
        text_destiantion = entry_s_for_destination.get()
        flightsreserv = Reservation.search_for_a_flight(text_location, text_destiantion)
        if flightsreserv == "There is no flight on that specific route!":
            label_flight_window = Label(search_flight_window,text=f"There is no reservation on that flight!****", font=("Abadi Bold", 11), bg="#e3daeb")
            label_flight_window.place(x=300, y=20)
        if text_location == "Enter the name of the location" or text_destiantion == "Enter the name of the destination":
            label_flight_window = Label(search_flight_window,
                                        text=f"Error. Please enter the location and the destination!!",
                                        font=("Abadi Bold", 11), bg="#e3daeb")
        else:
            if flightsreserv != "There is no flight on that specific route!":
                label_flight_window = Label(search_flight_window, text=f"{text_location} to {text_destiantion} route reservations:", font=("Abadi Bold", 11), bg="#e3daeb")
            else:
                label_flight_window = Label(search_flight_window,
                                            text=f"There is no book on that flight or the information is wrongly written!!", font=("Abadi Bold", 11), bg="#e3daeb")
        label_flight_window.place(x=300, y=20)

        Reservation.location_flight = ""
        Reservation.destination_flight = ""
        label_sub_for_flight = Label(search_flight_window, text=flightsreserv, font=("Abadi Bold", 11), bg="#e3daeb")
        label_sub_for_flight.place(x=70, y=70)

    search_window = Toplevel()  # searching main window
    search_window.resizable(False, False)
    search_window.geometry("900x600")
    search_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
    search_window.title('Search')

    startframe = tkinter.Frame(search_window)
    canvas = tkinter.Canvas(startframe, width=1280, height=720)  # width=1280, height=720)
    startframe.pack()
    canvas.pack()

    image_book = tkinter.PhotoImage(file=r"searchback.png")
    search_window.one = image_book  # to prevent the image garbage collected.
    canvas.create_image((0, 0), image=image_book, anchor='nw')

    # this is for searching for a client - all the bookings created on a specific name
    label_s_for_client = Label(search_window, text="Search for a client's reservations:", font=("Abadi Bold", 11), bg="#e3daeb")
    label_s_for_client.place(x=260, y=20)
    entry_s_for_client = Entry(search_window, width=30)
    entry_s_for_client.place(x=280, y=50)
    entry_s_for_client.insert(0, "Enter the full name")

    button_s_for_client = Button(search_window, text="Submit")
    button_s_for_client.config(font=("Ink free", 10, 'bold'), bg="#045c39", fg="#a9abd1")
    button_s_for_client.config(command= search_for_client)
    button_s_for_client.place(x=470, y=50)

    # this is for searching for a company - all the bookings created on a specific company
    label_s_for_company = Label(search_window, text="Search for all reservations made at a specific company:", font=("Abadi Bold", 11), bg="#e3daeb")
    label_s_for_company.place(x=260, y=100)
    entry_s_for_company = Entry(search_window, width=30)
    entry_s_for_company.place(x=280, y=130)
    entry_s_for_company.insert(0, "Enter the company's name")

    button_s_for_company = Button(search_window, text="Submit")
    button_s_for_company.config(font=("Ink free", 10, 'bold'), bg="#045c39", fg="#a9abd1")
    button_s_for_company.config(command= search_for_company)
    button_s_for_company.place(x=470, y=130)

    # this is for searching for a flight - all the bookings created with the same location - destination
    label_s_for_flight = Label(search_window, text="Search for all reservations made at a specific flight:", font=("Abadi Bold", 11), bg="#e3daeb")
    label_s_for_flight.place(x=260, y=180)
    entry_s_for_location = Entry(search_window, width=30)
    entry_s_for_location.place(x=280, y=210)
    entry_s_for_location.insert(0, "Enter the name of the location")
    entry_s_for_destination = Entry(search_window, width=30)
    entry_s_for_destination.place(x=280, y=240)
    entry_s_for_destination.insert(0, "Enter the name of the destination")

    button_s_for_flight = Button(search_window, text="Submit")
    button_s_for_flight.config(font=("Ink free", 10, 'bold'), bg="#045c39", fg="#a9abd1")
    button_s_for_flight.config(command=search_for_flight)
    button_s_for_flight.place(x=470, y=220)


def bookings():

    def book_flight():  # book a flight window

        def click_info_book():  # functionality to the submit button from book_flight window
            text1 = entry1.get()
            entry1.delete(0, END)

            text2 = entry2.get()
            entry2.delete(0, END)

            text3 = entry3.get()
            entry3.delete(0, END)

            text4 = entry4.get()
            entry4.delete(0, END)

            text5 = entry5.get()
            entry5.delete(0, END)

            text6 = entry6.get()
            entry6.delete(0, END)

            text7 = entry7.get()
            entry7.delete(0, END)

            text8 = entry8.get()
            entry8.delete(0, END)

            text9 = entry9.get()
            entry9.delete(0, END)
            reservation1 = Reservation(text1, text2, text3, text4, text5, text6, text7, text8, text9)
            reservation1.ad_reser_tofile()
            if reservation1.real_object:
                label_book_bool = Label(book_window, text="The booking has been created! ****", font=("Abadi Bold", 11),
                                        bg="#e3daeb", fg="#1a781f")
                label_book_bool.place(x=30, y=360)
            else:
                label_book_bool = Label(book_window, text="The booking has not been created!", font=("Abadi Bold", 11),
                                        bg="#e3daeb", fg="#ff0303")
                label_book_bool.place(x=30, y=360)
            # all the input data are used for reservations class constructor

        book_window = Toplevel()  # book_flight window
        book_window.geometry("560x600")
        book_window.resizable(False, False)
        book_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
        book_window.title('Book your flight now')

        startframe = tkinter.Frame(book_window)
        canvas = tkinter.Canvas(startframe, width=1280, height=720)  # width=1280, height=720)
        startframe.pack()
        canvas.pack()

        # Escape / raw string literal
        image_book = tkinter.PhotoImage(file=r"BookFlight.png")
        book_window.one = image_book  # to prevent the image garbage collected.
        canvas.create_image((0, 0), image=image_book, anchor='nw')

        label1 = Label(book_window, text="Full name: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label1.place(x=20, y=10)
        entry1 = Entry(book_window, width=30)
        entry1.place(x=110, y=10)
        label1_right = Label(book_window, text="(eg: Stones Matthew)", font=("Abadi Bold", 11), bg="#e3daeb")
        label1_right.place(x=300, y=10)

        label2 = Label(book_window, text="Class type: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label2.place(x=20, y=40)
        entry2 = Entry(book_window, width=30)
        entry2.place(x=110, y=40)
        label2_right = Label(book_window, text="(second class or first class)", font=("Abadi Bold", 11), bg="#e3daeb")
        label2_right.place(x=300, y=40)

        label3 = Label(book_window, text="Flight type: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label3.place(x=20, y=70)
        entry3 = Entry(book_window, width=30)
        entry3.place(x=110, y=70)
        label3_right = Label(book_window, text="(one-way or round-trip)", font=("Abadi Bold", 11), bg="#e3daeb")
        label3_right.place(x=300, y=70)

        label4 = Label(book_window, text="Ticket price: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label4.place(x=20, y=130)
        entry4 = Entry(book_window, width=30)
        entry4.place(x=110, y=130)
        label4_right = Label(book_window, text="(the price of that specific flight)", font=("Abadi Bold", 11),
                             bg="#e3daeb")
        label4_right.place(x=300, y=130)

        label5 = Label(book_window, text="Company: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label5.place(x=20, y=100)
        entry5 = Entry(book_window, width=30)
        entry5.place(x=110, y=100)
        label5_right = Label(book_window, text="(the company of that airplane)", font=("Abadi Bold", 11), bg="#e3daeb")
        label5_right.place(x=300, y=100)

        label6 = Label(book_window, text="Location: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label6.place(x=20, y=160)
        entry6 = Entry(book_window, width=30)
        entry6.place(x=110, y=160)
        label6_right = Label(book_window, text="(the location of the airplane)", font=("Abadi Bold", 11), bg="#e3daeb")
        label6_right.place(x=300, y=160)

        label7 = Label(book_window, text="Destination: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label7.place(x=20, y=190)
        entry7 = Entry(book_window, width=30)
        entry7.place(x=110, y=190)
        label7_right = Label(book_window, text="(the destination of the flight)", font=("Abadi Bold", 11), bg="#e3daeb")
        label7_right.place(x=300, y=190)

        label8 = Label(book_window, text="Date: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label8.place(x=20, y=220)
        entry8 = Entry(book_window, width=30)
        entry8.place(x=110, y=220)
        label8_right = Label(book_window, text="(current date eg: 02-03-2022)", font=("Abadi Bold", 11), bg="#e3daeb")
        label8_right.place(x=300, y=220)

        label9 = Label(book_window, text="Stopover: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label9.place(x=20, y=250)
        entry9 = Entry(book_window, width=30)
        entry9.place(x=110, y=250)
        label9_right = Label(book_window, text="(the stopover of that flight)", font=("Abadi Bold", 11), bg="#e3daeb")
        label9_right.place(x=300, y=250)

        button_book = Button(book_window, text="Submit")
        button_book.config(font=("Ink free", 10, 'bold'), bg="#045c39", fg="#a9abd1")
        button_book.config(command=click_info_book)
        button_book.place(x=250, y=530)

    def show_all_reservations():  # function that displays all bookings
        Reservation.instantiate_reservations()
        reservations_window = Toplevel()
        reservations_window.resizable(False, False)
        reservations_window.geometry("1000x800")
        reservations_window.title('All reservations')
        reservations_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
        reservations_window.config(bg="#d7c5ed")
        text_reservations = Reservation.show_reservations()
        label_flights = Label(reservations_window, text=f"All flights from all companies: ", bg="#d7c5ed",
                              font=('Abadi Bold', 16)).pack()
        Label(reservations_window, text=text_reservations, bg="#d7c5ed", font=('Abadi Bold', 14)).pack()

    def update_reservation():

        def button_update_reservation():  # functionality to the update button
            text1_update = entry1.get()
            entry1.delete(0, END)

            text2_update = entry2.get()
            entry2.delete(0, END)

            text3_update = entry3.get()
            entry3.delete(0, END)

            text4_update = entry4.get()
            entry4.delete(0, END)

            text5_update = entry5.get()
            entry5.delete(0, END)

            text6_update = entry6.get()
            entry6.delete(0, END)

            text7_update = entry7.get()
            entry7.delete(0, END)

            text8_update = entry8.get()
            entry8.delete(0, END)

            text9_update = entry9.get()
            entry9.delete(0, END)

            text_last_date = entry_last_date.get()
            entry_last_date.delete(0, END)
            Reservation.last_date_update += text_last_date
            Reservation.update_reservation(text1_update, text2_update, text3_update, text4_update, text5_update, text6_update, text7_update, text8_update, text9_update)

            if Reservation.update_info:
                label_book_bool = Label(reservations_window, text="The update of the booking has been made!     *****",
                                        font=("Abadi Bold", 11), bg="#e3daeb", fg="#1a781f")
                label_book_bool.place(x=30, y=400)
            else:
                label_book_bool = Label(reservations_window, text="The update of the booking has failed! Try again.****",
                                        font=("Abadi Bold", 11), bg="#e3daeb", fg="#ff0303")
                label_book_bool.place(x=30, y=400)
            Reservation.update_info = False
            Reservation.name_update = ""
            Reservation.type_cls_update = ""
            Reservation.fly_type_update = ""
            Reservation.comp_name_update = ""
            Reservation.loc_update = ""
            Reservation.destinat_update = ""
            Reservation.stop_update = ""
            Reservation.dat_update = ""
            Reservation.last_date_update = ""
            Reservation.price_update = ""

        reservations_window = Toplevel()  # update booking window
        reservations_window.resizable(False, False)
        reservations_window.geometry("560x600")
        reservations_window.title('Update booking')
        reservations_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')

        startframe = tkinter.Frame(reservations_window)
        canvas = tkinter.Canvas(startframe, width=1280, height=720)
        startframe.pack()
        canvas.pack()

        image_book = tkinter.PhotoImage(file=r"update_booking.png")
        reservations_window.one = image_book  # to prevent the image garbage collected.
        canvas.create_image((0, 0), image=image_book, anchor='nw')
        label_title = Label(reservations_window, text="Enter your name and the new information", font=("Abadi Bold", 11), bg="#e3daeb")
        label_title.place(x=150, y=30)

        label1 = Label(reservations_window, text="Full name: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label1.place(x=20, y=70)
        entry1 = Entry(reservations_window, width=30)
        entry1.place(x=110, y=70)
        label1_right = Label(reservations_window, text="(Your name)", font=("Abadi Bold", 11), bg="#e3daeb")
        label1_right.place(x=300, y=70)

        label2 = Label(reservations_window, text="Class type: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label2.place(x=20, y=130)
        entry2 = Entry(reservations_window, width=30)
        entry2.place(x=110, y=130)
        label2_right = Label(reservations_window, text="(second class or first class)", font=("Abadi Bold", 11), bg="#e3daeb")
        label2_right.place(x=300, y=130)

        label3 = Label(reservations_window, text="Flight type: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label3.place(x=20, y=160)
        entry3 = Entry(reservations_window, width=30)
        entry3.place(x=110, y=160)
        label3_right = Label(reservations_window, text="(one-way or round-trip)", font=("Abadi Bold", 11), bg="#e3daeb")
        label3_right.place(x=300, y=160)

        label5 = Label(reservations_window, text="Company: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label5.place(x=20, y=190)
        entry5 = Entry(reservations_window, width=30)
        entry5.place(x=110, y=190)
        label5_right = Label(reservations_window, text="(the company of that airplane)", font=("Abadi Bold", 11), bg="#e3daeb")
        label5_right.place(x=300, y=190)

        label4 = Label(reservations_window, text="Ticket price: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label4.place(x=20, y=220)
        entry4 = Entry(reservations_window, width=30)
        entry4.place(x=110, y=220)
        label4_right = Label(reservations_window, text="(the price of that specific flight)", font=("Abadi Bold", 11), bg="#e3daeb")
        label4_right.place(x=300, y=220)

        label6 = Label(reservations_window, text="Location: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label6.place(x=20, y=250)
        entry6 = Entry(reservations_window, width=30)
        entry6.place(x=110, y=250)
        label6_right = Label(reservations_window, text="(the location of the airplane)", font=("Abadi Bold", 11), bg="#e3daeb")
        label6_right.place(x=300, y=250)

        label7 = Label(reservations_window, text="Destination: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label7.place(x=20, y=280)
        entry7 = Entry(reservations_window, width=30)
        entry7.place(x=110, y=280)
        label7_right = Label(reservations_window, text="(the destination of the flight)", font=("Abadi Bold", 11), bg="#e3daeb")
        label7_right.place(x=300, y=280)

        label8 = Label(reservations_window, text="Date: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label8.place(x=20, y=310)
        entry8 = Entry(reservations_window, width=30)
        entry8.place(x=110, y=310)
        label8_right = Label(reservations_window, text="(current date eg: 02-03-2022)", font=("Abadi Bold", 11), bg="#e3daeb")
        label8_right.place(x=300, y=310)

        label9 = Label(reservations_window, text="Stopover: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label9.place(x=20, y=340)
        entry9 = Entry(reservations_window, width=30)
        entry9.place(x=110, y=340)
        label9_right = Label(reservations_window, text="(the stopover of that flight)", font=("Abadi Bold", 11), bg="#e3daeb")
        label9_right.place(x=300, y=340)

        label_last_date = Label(reservations_window, text="Last date: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label_last_date.place(x=20, y=100)
        entry_last_date = Entry(reservations_window, width=30)
        entry_last_date.place(x=110, y=100)
        label_last_date = Label(reservations_window, text="(Last date of your specific booking)", font=("Abadi Bold", 11), bg="#e3daeb")
        label_last_date.place(x=300, y=100)

        button_book = Button(reservations_window, text="Submit")
        button_book.config(font=("Ink free", 10, 'bold'), bg="#045c39", fg="#a9abd1")
        button_book.config(command=button_update_reservation)
        button_book.place(x=250, y=530)

    def delete_booking():

        def button_delete_booking():  # functionality to the delete button
            text_entry_name = entry_name_delete.get()
            text_entry_date = entry_date_delete.get()
            label_show_delete = Label(delete_window, text="", font=("Abadi Bold", 12),bg="#ffdf40", fg="#871204")
            if Reservation.delete_reservation(text_entry_name, text_entry_date):
                label_show_delete.config(text="Your booking has been deleted!! ✔", bg="#ffdf40", fg="#0a660f")
                label_show_delete.place(x=220, y=220)
            else:
                label_show_delete.config(text="The input information is wrong!!  ✖")
                label_show_delete.place(x=220, y=220)
            entry_name_delete.delete(0, END)
            entry_date_delete.delete(0, END)

        delete_window = Toplevel()
        delete_window.resizable(False, False)
        delete_window.geometry("560x600")
        delete_window.title('Delete booking')
        delete_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')

        startframe = tkinter.Frame(delete_window)
        canvas = tkinter.Canvas(startframe, width=1280, height=720)
        startframe.pack()
        canvas.pack()

        image_book = tkinter.PhotoImage(file=r"DeletePhoto.png")
        delete_window.one = image_book  # to prevent the image garbage collected.
        canvas.create_image((0, 0), image=image_book, anchor='nw')

        label_title_delete = Label(delete_window, text="Delete your booking", font=("Abadi Bold", 12), bg="#e3daeb")
        label_title_delete.place(x=220, y=20)
        label_name_delete = Label(delete_window, text="Your name: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label_name_delete.place(x=20, y=100)
        entry_name_delete = Entry(delete_window, width=30)
        entry_name_delete.place(x=200, y=100)
        label_date_delete = Label(delete_window, text="Date of booking: ", font=("Abadi Bold", 11), bg="#e3daeb")
        label_date_delete.place(x=20, y=150)
        entry_date_delete = Entry(delete_window, width=30)
        entry_date_delete.place(x=200, y=150)
        button_submit_delete = Button(delete_window, text="Submit")
        button_submit_delete.config(font=("Ink free", 12, 'bold'), bg="#dead0b", fg="#2279c9")
        button_submit_delete.place(x=420, y=120)
        button_submit_delete.config(command=button_delete_booking)

    def read_me_funct():
        right_date = datetime.now()
        right_date = right_date.date()
        right_date += timedelta(days=365)

        read_me_window = Toplevel()  # readme window
        read_me_window.resizable(False, False)
        read_me_window.geometry("1200x670")
        read_me_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
        read_me_window.title('Readme')

        startframe = tkinter.Frame(read_me_window)
        canvas = tkinter.Canvas(startframe, width=1280, height=720)
        startframe.pack()
        canvas.pack()

        image_book = tkinter.PhotoImage(file=r"ReadMePhoto.png")
        read_me_window.one = image_book  # to prevent the image garbage collected.
        canvas.create_image((0, 0), image=image_book, anchor='nw')

        label_read_title = Label(read_me_window, text="Read the information", font=("Abadi Bold", 15), bg="#e3daeb")
        label_read_title.place(x=500, y=40)

        label_read_1 = Label(read_me_window, text=f"◉ The date for booking must be between {datetime.now().date()} and {right_date}!", font=("Abadi Bold", 14), bg="#e3daeb")
        label_read_1.place(x=300, y=120)

        label_read_2 = Label(read_me_window, text=f"◉ You can't create more bookings with the same name on the same date!", font=("Abadi Bold", 14), bg="#e3daeb")
        label_read_2.place(x=300, y=170)

        label_read_3 = Label(read_me_window, text=f"◉ You can't update your booking on the same day as before!", font=("Abadi Bold", 14), bg="#e3daeb")
        label_read_3.place(x=300, y=220)

        label_read_4 = Label(read_me_window, text=f"◉ Follow the intructions in paranthesis when updating or booking!", font=("Abadi Bold", 14), bg="#e3daeb")
        label_read_4.place(x=300, y=270)

        label_read_5 = Label(read_me_window, text=f"◉ Open the 'Show all flights' window to see all the information you need!", font=("Abadi Bold", 14), bg="#e3daeb")
        label_read_5.place(x=300, y=320)

    bookings_window = Toplevel()  # the main bookings window
    bookings_window.resizable(False, False)
    bookings_window.geometry("650x720")
    bookings_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
    bookings_window.title('Bookings')

    startframe = tkinter.Frame(bookings_window)
    canvas = tkinter.Canvas(startframe, width=1280, height=720)
    startframe.pack()
    canvas.pack()

    image_book = tkinter.PhotoImage(file=r"Bookings_photo.png")
    bookings_window.one = image_book  # to prevent the image garbage collected.
    canvas.create_image((0, 0), image=image_book, anchor='nw')

    button_book = Button(bookings_window, text='Book a flight', relief=RAISED, font=('Abadi Bold', 14), bg="#dbcef0", fg="white")
    button_book.config(activebackground="#c6aded")
    button_book.place(x=260, y=120)
    button_book.config(command=book_flight)

    button_show = Button(bookings_window, text='Show all bookings', relief=RAISED, font=('Abadi Bold', 14), bg="#dbcef0", fg="white")
    button_show.config(activebackground="#c6aded")
    button_show.place(x=240, y=190)
    button_show.config(command=show_all_reservations)

    button_update = Button(bookings_window, text='Update your booking', relief=RAISED, font=('Abadi Bold', 14), bg="#dbcef0", fg="white")
    button_update.config(activebackground="#c6aded")
    button_update.place(x=230, y=260)
    button_update.config(command=update_reservation)

    button_delete = Button(bookings_window, text='Delete your booking', relief=RAISED, font=('Abadi Bold', 14), bg="#dbcef0", fg="white")
    button_delete.config(activebackground="#c6aded")
    button_delete.place(x=235, y=330)
    button_delete.config(command=delete_booking)

    button_read_me = Button(bookings_window, text='Readme', relief=RAISED, font=('Abadi Bold', 14), bg="#dbcef0", fg="white")
    button_read_me.config(activebackground="#c6aded")
    button_read_me.place(x=278, y=400)
    button_read_me.config(command=read_me_funct)


def check_allfiles():
    # check if all files, images and all data is accessible
    try:
        with open('items.csv', 'r') as f:
            reader = csv.DictReader(f)
            check_dic["items.csv"] = 1
    except:
        check_dic["items.csv"] = 0
    try:
        with open('reservations.csv', 'r') as f:
            reader = csv.DictReader(f)
            check_dic["reservations.csv"] = 1
    except:
        check_dic["reservations.csv"] = 0

    if os.path.exists("airplaneicon_ZAk_icon.ico"):
            check_dic["airplaneicon_ZAk_icon.ico"] = 1
    else:
        check_dic["airplaneicon_ZAk_icon.ico"] = 0

    if os.path.exists("MainWindowPhotoTry.png"):
        check_dic["MainWindowPhotoTry.png"] = 1
    else:
        check_dic["MainWindowPhotoTry.png"] = 0

    if os.path.exists("BookFlight.png"):
        check_dic["BookFlight.png"] = 1
    else:
        check_dic["BookFlight.png"] = 0

    if os.path.exists("Bookings_photo.png"):
        check_dic["Bookings_photo.png"] = 1
    else:
        check_dic["Bookings_photo.png"] = 0

    if os.path.exists("DeletePhoto.png"):
        check_dic["DeletePhoto.png"] = 1
    else:
        check_dic["DeletePhoto.png"] = 0

    if os.path.exists("ReadMePhoto.png"):
        check_dic["ReadMePhoto.png"] = 1
    else:
        check_dic["ReadMePhoto.png"] = 0

    if os.path.exists("Routes.png"):
        check_dic["Routes.png"] = 1
    else:
        check_dic["Routes.png"] = 0

    if os.path.exists("searchback.png"):
        check_dic["searchback.png"] = 1
    else:
        check_dic["searchback.png"] = 0

    if os.path.exists("searchclientphoto.png"):
        check_dic["searchclientphoto.png"] = 1
    else:
        check_dic["searchclientphoto.pnga"] = 0

    if os.path.exists("update_booking.png"):
        check_dic["update_booking.png"] = 1
    else:
        check_dic["update_booking.png"] = 0

    for i, element in enumerate(check_dic):
        if check_dic[element] == 0:
            return False
    return True


def show_errors():
    show_errors_window = Toplevel()
    show_errors_window.geometry("500x650")
    show_errors_window.resizable(False, False)
    show_errors_window.title('Show the errors')
    show_errors_window.config(bg="#a3c7e3")
    for i, element in enumerate(check_dic):
        text = element
        if check_dic[element] == 0:
            label_x = Label(show_errors_window, text=f"{text} ✖", font=("Abadi Bold", 14), bg="#e3daeb", fg="#ff0303")
            label_x.place(x=30, y=50 * (i + 1))
        else:
            label_x = Label(show_errors_window, text=f"{text} ✔", font=("Abadi Bold", 14), bg="#e3daeb", fg="#1a781f")
            label_x.place(x=30, y=50 * (i + 1))


'''
The main menu of the GUI
'''


def main():
    if check_allfiles():
        main_window = Tk()
        main_window.geometry("560x600")
        main_window.resizable(False, False)
        main_window.title('FlightBooking')
        main_window.iconbitmap(r'airplaneicon_ZAk_icon.ico')
        image_main_window = PhotoImage(file='MainWindowPhotoTry.png', master=main_window)

        canvas = Canvas(main_window)
        canvas.create_image(0, 0, image=image_main_window, anchor="nw")
        canvas.create_text(80, 570, text="Despina Florin © 2022", font=('Abadi Bold', 10))
        canvas.pack(fill="both", expand=True)

        button1 = Button(main_window, text='Show all flights', relief=RAISED, font=('Abadi Bold', 14), bg="#745eb8", fg="white")
        button1.config(activebackground="#575a99")
        button1.place(x=215, y=150)
        button1.config(command=show_all_flights)

        button2 = Button(main_window, text="Bookings", relief=RAISED, font=('Abadi Bold', 14), bg="#745eb8", fg="white")
        button2.config(activebackground="#575a99")
        button2.place(x=235, y=200)
        button2.config(command=bookings)

        button3 = Button(main_window, text="Find me a route of flights", relief=RAISED, font=('Abadi Bold', 14), bg="#745eb8", fg="white")
        button3.config(activebackground="#575a99")
        button3.place(x=170, y=100)
        button3.config(command=find_route)

        button4 = Button(main_window, text="Search", relief=RAISED, font=('Abadi Bold', 14), bg="#745eb8", fg="white")
        button4.config(activebackground="#575a99")
        button4.place(x=240, y=50)
        button4.config(command=search)

        main_window.mainloop()
    else:
        main_window = Tk()
        main_window.geometry("500x200")
        main_window.resizable(False, False)
        main_window.title('Error')
        main_window.config(bg="#d7c5ed")

        label_error1 = Label(main_window, text=f"You don't have all the files.", font=("Abadi Bold", 14), bg="#e3daeb")
        label_error1.place(x=20, y=50)

        label_error2 = Label(main_window, text=f"Please read the ReadMe file and follow the instructions.", font=("Abadi Bold", 14), bg="#e3daeb")
        label_error2.place(x=20, y=100)

        label_error3 = Label(main_window, text=f"Check the errors: ", font=("Abadi Bold", 14), bg="#e3daeb")
        label_error3.place(x=20, y=150)

        button_check_error = Button(main_window, text="Check", relief=RAISED, font=('Abadi Bold', 14), bg="#7da3f5", fg="white")
        button_check_error.config(activebackground="#575a99")
        button_check_error.place(x=200, y=145)
        button_check_error.config(command=show_errors)
        main_window.mainloop()


if __name__ == '__main__':
    main()






