# Stephen James
# 2026-06-21
# Week 1 Programming Assignment 2
# Purpose: Create a menu-driven program that can create, read, update,
# and delete Redis sets.

import redis

from datetime import datetime


# Connect to the local Redis database.
r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

choice = ""

# Display the menu until the user chooses to exit.
while choice != "6":
    print("Type in a number and press enter to execute the menu option.")
    print("1. Query for set members")
    print("2. Add a new set")
    print("3. Update members of a set")
    print("4. Delete a set")
    print("5. Delete all data from the database")
    print("6. Exit the program")
    choice = input()

    # ***READ SECTION***
    # Retrieve and display the members of a specific set.
    if choice == "1":
        print("\nEnter the key of the set you wish to query:")
        key = input()

        print("\nThe cardinality of the set is:")
        print(r.scard(key))

        print("\nThe member values of the set are:")
        print(r.smembers(key))
        print()

    # ***CREATE SECTION***
    # Create a new set and add the number of members requested by the user.
    elif choice == "2":
        print("\nEnter the key you wish to add:")
        key = input()

        print("\nEnter how many members will this set have:")
        number_of_members = int(input())

        count = 0
        while count < number_of_members:
            print("\nEnter the next member value:")
            member = input()
            r.sadd(key, member)
            count = count + 1
        print()

    # ***UPDATE SECTION***
    # Update a set by adding, removing, or deleting all members.
    elif choice == "3":
        print("\nEnter the key of the set you wish to update:")
        key = input()

        update_choice = ""
        while update_choice != "4":
            print("\nPlease type in a number and press enter to execute the menu option")
            print("1. Add new member")
            print("2. Remove member")
            print("3. Remove all members")
            print("4. Exit Update Menu")
            update_choice = input()

            # Add a new member to the set.
            if update_choice == "1":
                print("\nEnter the new member value:")
                member = input()
                r.sadd(key, member)

                print("\nThe cardinality of the set is now:")
                print(r.scard(key))

            # Remove one member from the set.
            elif update_choice == "2":
                print("\nEnter the member value you wish to remove:")
                member = input()
                r.srem(key, member)

                print("\nThe cardinality of the set is now:")
                print(r.scard(key))

            # Remove all members from the set.
            elif update_choice == "3":
                print("\nRemoving all set members...")
                while r.scard(key) > 0:
                    print("Removing Member: {}...".format(r.spop(key)))

                print("\nThe cardinality of the set is now:")
                print(r.scard(key))

            elif update_choice == "4":
                print()

            else:
                print("\nThat is not a valid update menu option.")

    # ***DELETE SECTION***
    # Delete a specific set from the Redis database.
    elif choice == "4":
        print("\nEnter the key of the set you wish to delete:")
        key = input()

        print("\nRemoving the set from the database...")
        r.delete(key)
        print("Set removed.\n")

    # ***DELETE SECTION***
    # Delete all data from the Redis database.
    elif choice == "5":
        print("\nRemoving all data from the database...")
        r.flushdb()
        print("All data removed.\n")

    elif choice == "6":
        print()

    else:
        print("\nThat is not a valid menu option.\n")

# Display end of program message.
print("Program has ended!")
print("The date and time is", datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
