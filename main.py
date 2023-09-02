from datetime import datetime
from read import readinvents, readrents
from write import writeinvent, writerent
from operation import rentitems, returnitems,calculate_return_cost

def displayinvent(inventings):
    print("Inventory:")
    print("ID\tItem Name\tCompany Name\tPrice\tQuantities")
    for itemid, iteminfo in inventings.items():
        print(
            f"{itemid}\t{iteminfo['itemname']}\t{iteminfo['companyname']}\t${iteminfo['prices']:.2f}\t{iteminfo['quantities']}")

def view_rental_history(rentings, inventings):
    print("Rental History:")
    print("Rental ID\tDate\t\tUser\tPhone\tItem\tQuantities")
    for rental in rentings:
        print(
            f"{rental['rentalid']}\t{rental['rentaldate']}\t{rental['username']}\t{rental['phonenumber']}\t{inventings[rental['itemid']]['itemname']}\t{rental['quantities']}")

if __name__ == "__main__":
    inventfiles = "equipment.txt"
    rentalfiles = "rental.txt"

    inventings = readinvents(inventfiles)
    rentings = readrents(rentalfiles)

    print("\nSudikshya Rental")
    print("Kamalpokhari, Kathmandu | Phone No: 900000")
    print("-" * 100)
    print("Welcome to the Event Equipment Rental System, Admin.")

    while True:
        print("\nOptions:")
        print("1. Rent an item")
        print("2. Return an item")
        print("3. View rental history")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your name: ")
            phonenumber = input("Enter your phone number: ")
            displayinvent(inventings)
            itemid = int(input("Enter the ID of the item you want to rent: "))
            quantities = int(input("Enter the quantities you want to rent: "))
            rentalinfos = rentitems(inventings, username, phonenumber, itemid, quantities, rentalfiles)
            if rentalinfos:
                writerent(rentalfiles, rentalinfos)
                writeinvent(inventfiles, inventings)
                print(f"Rental successful. Rental ID: {rentalinfos.split(',')[0]}")

        elif choice == "2":
            view_rental_history(rentings, inventings)
            rentalid = int(input("Enter the ID of the rental you want to return: "))
            if 1 <= rentalid <= len(rentings):
                selected_rental = rentings[rentalid - 1]
                itemname, return_quantities, itemprice, totalcost = calculate_return_cost(inventings, selected_rental)
                
                if returnitems(inventings, selected_rental):
                    print("Item returned successfully. Rental ID:", rentalid)
                    print("Returned Item:", itemname)
                    print("Quantity Returned:", return_quantities)
                    print("Unit Price:", itemprice)
                    print("Total Cost:", totalcost)
                    
                    # Remove the returned rental from the rentals list
                    rentings.pop(rentalid - 1)
                    # Update the rentals file
                    with open(rentalfiles, "w") as file:
                        for rental in rentings:
                            writerent(rentalfiles, rental)
                else:
                    print("Failed to return the item.")
            else:
                print("Invalid rental ID.")

        elif choice == "3":
            view_rental_history(rentings, inventings)
            

        elif choice == "4":
            print("Thank you for using Sudikshya Rental. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")
