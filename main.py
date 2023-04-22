from datetime import date as dt
from models import session
from general_logic import (
    login,
    register_person,
    register_pet,
    owner_login,
    vet_login,
    staff_login,
)


# program body starts here
while True:
    action = input("login or register\n: ")
    if action == "login":
        mail = input("Please enter your email: ")
        password = input("Please enter your password: ")

        person = login(mail, password) #initialising person in general_logic


        if person is None:
            print("Login was unsuccesfull, try again...")
            logged_in = False
            continue

        elif person != None:
            print("Login was succesfull...\n")
            logged_in = True
            pass

        else:
            print("something went wrong with login...")

        if person.type == 1:
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
                    owner_login(person, action)
                    
            if exit == True:
                session.close()
                break
            else:
                continue

        elif person.type == 2:
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
                    staff_login(person, action)
            if exit == True:
                session.close()
                break
            else:
                continue
        
        elif person.type == 3:
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
                    staff_login(person, action)
            if exit == True:
                session.close()
                break
            else:
                continue
        elif person.type == 4:
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
                    vet_login(person, action)

            if exit == True:
                session.close()
                break

            else:
                continue
        
        elif person.type == 5:
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
                    vet_login(person, action)
            if exit == True:
                session.close()
                break

            else:
                continue

        elif person.type == 6:

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
                            staff_login(person, action)

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
                            vet_login(person, action)
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
                session.close()
                break

        elif person.type == 7:

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
                            staff_login(person, action)
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
                            vet_login(person, action)

                if choose == "0":
                    print("\n\n")
                    exit = False
                    break

                elif choose == "q":
                    exit = True
                    break
                    
            if exit == True:
                session.close()
                break

    elif action == "register":
        logged_in = False
        person = register_person()

        haspet = input(
            "Do you want to register a pet?\n(y - yes / n - no): ")

        if haspet.lower() == "y" or haspet.lower() == "yes":
            register_pet(person.id)

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

