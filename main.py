from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date as dt

from general_logic import (


)

# program body starts here
while True:
    action = input("login or register\n: ")
    if action == "login":
        logged_in = True
        mail = input("Please enter your email: ")
        password = input("Please enter your password: ")

        login = init_login(mail, password) #initialising in general_logic

        login.login()
        if login.log == "No":
            print("Login was unsuccesfull, try again...")
            continue

        elif login.log == "Yes":
            print("Login was succesfull...")
            pass

        if login.person_type == 1:
            while True:
                action = input(
                "\n\nWhat should we do?\n1) my pets\n2) my visits\n3) add pet \n0) log out \nq) Exit program \n: ")
                print()
                if action == "0":
                    print("\n\n")
                    exit = False
                    break

                elif action == "q":
                    exit = True
                    break
                else:
                    owner_login(login, action)
                
            if exit == True:
                break
            else:
                continue

        elif login.person_type == 2:
            while True:

                action = input("\n\nwhat action should we do?\n1) List every owner\n2)"
                       " List every vet\n3) List every pet"
                       "\n0) log out\nq) quit the program \n: ")
                print()
                if action == "0":
                    print("\n\n")
                    exit = False
                    break

                elif action == "q":
                    exit = True
                    break
                
                else:
                    staff_login(login, login.person_type, action)
            if exit == True:
                break
            else:
                continue
        
        elif login.person_type == 3:
            while True:

                action = input("\n\nwhat action should we do?\n1) List every owner\n2)"
                       " List every vet\n3) List every pet\n4) Add my pet\n"
                       "5) List my pets\n0) log out\nq) quit the program \n: ")
                print()
                if action == "0":
                    print("\n\n")
                    exit = False
                    break

                elif action == "q":
                    exit = True
                    break
                else:
                    staff_login(login, login.person_type, action)
            if exit == True:
                break
            else:
                continue
        elif login.person_type == 4:
            while True:

                action = input("What action should we perform?\n"
                "1) add a new entry in visits\n2) List my med history\n"
                "3) add my speciality \n"
                "0) log out\nq) exit program\n:")
                print()

                if action == "0":
                    print("\n\n")
                    exit = False
                    break

                elif action == "q":
                    exit = True
                    break

                else:
                    vet_login(login, login.person_type, action)

            if exit == True:
                break

            else:
                continue
        
        elif login.person_type == 5:
            while True:

                action = input("What action should we perform?\n"
                "1) add a new entry in visits\n2) List my med history\n"
                "3) add my speciality \n4) add my pet\n5) List my pets\n"
                "0) log out\nq) exit program\n:")
                print()

                if action == "0":
                    print("\n\n")
                    exit = False
                    break

                elif action == "q":
                    exit = True
                    break

                else:
                    vet_login(login, login.person_type, action)
            if exit == True:
                break

            else:
                continue

        elif login.person_type == 6:

            while True:
                choose = input(
                    "do you want to enter as staff or vet?\n1)Staff member\n2)Vet\n0)Log out\nq) Exit program\n: ")
                if choose == "1":
                    while True:

                        print("You logged as staff\n")
                        action = input("\n\nwhat action should we do?\n1) List every owner\n2)"
                            " List every vet\n3) List every pet"
                            "\n0) log out\nq) quit the program \n: ")
                        print()
                        if action == "0":
                            exit = False
                            break

                        elif action == "q":
                            exit = True
                            break

                        else:
                            staff_login(login, login.person_type, action)

                elif choose == "2":
                    print("You are in vet sub menu")
                    while True:

                        action = input("What action should we perform?\n"
                        "1) add a new entry in visits\n2) List my med history\n"
                        "3) add my speciality \n"
                        "0) log out\nq) exit program\n:")
                        print()

                        if action == "0":
                            exit = False
                            break

                        elif action == "q":
                            exit = True
                            break
                        else:
                            vet_login(login, login.person_type, action)
                    if exit == True:
                        break

                    else:
                        continue

                if choose == "0":
                    print("\n\n")
                    exit = False
                    break

                elif choose == "q":
                    exit = True
                    break
                    
            if exit == True:
                break

        elif login.person_type == 7:

            while True:
                choose = input(
                "do you want to enter as staff or vet?\n1)Staff member\n2)Vet\n0)Log out\nq) Exit program\n: ")

                if choose == "1":
                    while True:

                        action = input("\n\nwhat action should we do?\n1) List every owner\n2)"
                            " List every vet\n3) List every pet\n4) Add my pet\n"
                            "5) List my pets\n0) go to selection menu\nq) quit the program \n: ")
                        print()
                        if action == "0":
                            action = None
                            exit = False
                            break

                        elif action == "q":
                            exit = True
                            break
                        else:
                            staff_login(login, login.person_type, action)
                    if exit == True:
                        break
                    else:
                        continue

                elif choose == "2":
                    while True:

                        action = input("What action should we perform?\n"
                        "1) add a new entry in visits\n2) List my med history\n"
                        "3) add my speciality \n4) add my pet\n5) List my pets\n"
                        "0) go to selection menu \nq) exit program\n:")
                        print()

                        if action == "0":
                            exit = False
                            break

                        elif action == "q":
                            exit = True
                            break

                        else:
                            vet_login(login, login.person_type, action)

                if choose == "0":
                    print("\n\n")
                    exit = False
                    break

                elif choose == "q":
                    exit = True
                    break
                    
            if exit == True:
                break

    elif action == "register":
        logged_in = False


            haspet = input(
                "Do you want to register a pet?\n(y - yes / n - no): ")

            if haspet.lower() == "y" or haspet.lower() == "yes":
                register_pet(logged_in, person, None)

            elif haspet.lower() == "n" or haspet.lower() == "no":
                log = input(
                    "do you want to return to main menu? (y - yes / n - exit): ")
                if log == "n":
                    break

                else:
                    continue

            else:
                continue
            print("registration has been succesfull!")
        else:
            continue
curs.close()
connection.close()
