
import os
import random
import sys, string
import json
import re

a = list(string.ascii_letters)
random.shuffle(a)

n = [str(i) for i in range(10)]
random.shuffle(n)

specialC = list(string.punctuation)
random.shuffle(specialC)

allChars = a + n + specialC #soma de todas as listas
random.shuffle(allChars) 



def createPassword():

 # Check if the file exists and is not empty
    if os.path.exists("py-password-manager\data.json") and os.path.getsize("py-password-manager\data.json") > 0:
        try:
            with open("py-password-manager\data.json", mode="r", encoding="utf-8") as read_file:
                passwordList = json.load(read_file)
        except json.JSONDecodeError:
            print("Invalid JSON file. Initializing with an empty list.")
            passwordList = []
    else:
        passwordList = []

    
    email = str(input("Do you want to vinculate the password to which e-mail? (this will be your login): "))

    cNumber = int(input("How many characters you want in this password? (minimum recommended: 8): "))


    if cNumber < 8:
        print("Password length too short. Setting to minimum length of 8.")
        cNumber = 8
    elif cNumber > 12:
        print("Password length too long. Setting to maximum length of 12.")
        cNumber = 12

    # Generate the password
    password = ""
    while len(password) < cNumber: #enquanto minha senha for menor que o número indicado
        # Randomly pick a character from the combined list
        password += random.choice(allChars) #a senha anterior + um caractér aleatório da, já aleatório, conjunto somado de n , a , specialC

    print("Generated Password:", password)

    jsonPassword = {
        "email" : email,
        "password" : password
    }

    passwordList.append(jsonPassword) #colocando o novo par de informações na lista de senhas p ser colocado no json posteriormente
    with open("py-password-manager\data.json", mode="w", encoding="utf-8") as write_file:
        json.dump(passwordList, write_file, indent=4)


def accessPassword():
    choosenEmail = input("Do you vinculated your password to which e-mail?: ")

    if os.path.exists("py-password-manager\data.json"):
        with open("py-password-manager\data.json", mode="r", encoding="utf-8") as read_file:
            passData = json.load(read_file)

            for email in passData:
                if choosenEmail == email["email"]:
                    print("Password found! \nPassword: ", email["password"], "\nE-mail:", email["email"])
                    break
                    
                elif choosenEmail != email["email"]:
                    print("ERROR: No password found vinculated to this e-mail.")
                    break
                    
            
            
    else:
        print("No password located in the database. It's suggested that you create a password first.")

def editPassword():

    choosenEmail = input("Do you vinculated your password to which e-mail?: ")


    if os.path.exists("py-password-manager\data.json"):
            with open("py-password-manager\data.json", mode="r", encoding="utf-8") as read_file:
                passData = json.load(read_file)
                passwordList = []
            passwordFound = False

            for pairs in passData:
                    if choosenEmail == pairs["email"]:
                        passwordFound = True
                        print("Password found! \nPassword: ", pairs["password"], "\nE-mail:", pairs["email"])
                        decision = input("Are you sure you want to edit this password vinculated to this e-mail?").strip().lower()

                        if decision == "yes":
                            pairs["email"] = input("Insert a new e-mail to vinculate to your password: ")
                            pairs["password"] = input(f"Insert a new password to vinculate to your e-mail : ")
                            passwordList.append(pairs)

                        
                        else:
                            passwordList.append(pairs)
                    

                    else:
                        passwordList.append(pairs)

            if not passwordFound:
                print(f"There is no password vinculated to this e-mail ({choosenEmail}) in this database.")
    else:
        print("No password located in the database. It's suggested that you create a password first.")


    with open("py-password-manager\data.json", mode="w", encoding="utf-8" ) as write_file:
        json.dump(passwordList, write_file, indent=4) #remember, do not use "" while giving the ident


def deletePassword():

    choosenEmail = input("Do you vinculated your password to which e-mail?: ")


    if os.path.exists("py-password-manager\data.json"):
            with open("py-password-manager\data.json", mode="r", encoding="utf-8") as read_file:
                passData = json.load(read_file)
                passwordList = []
            passwordFound = False

            for pairs in passData:
                    if choosenEmail == pairs["email"]:
                        passwordFound = True
                        print("Password found! \nPassword: ", pairs["password"], "\nE-mail:", pairs["email"])
                        decision = input("Are you sure you want to delete this password vinculated to this e-mail?").strip().lower()

                        if decision == "yes":
                            print("Password successfuly deleted!\n")
                        
                        else:
                            passwordList.append(pairs)
                    

                    else:
                        passwordList.append(pairs)

            if not passwordFound:
                print(f"There is no password vinculated to this e-mail ({choosenEmail}) in this database.")
    else:
        print("No password located in the database. It's suggested that you create a password first.")


    with open("py-password-manager\data.json", mode="w", encoding="utf-8" ) as write_file:
        json.dump(passwordList, write_file, indent=4)


def checkSecurityPassword():

    choosenEmail = input("Do you vinculated your password to which e-mail?: ")


    if os.path.exists("py-password-manager\data.json"):
            
            with open("py-password-manager\data.json", mode="r", encoding="utf-8") as read_file:
                passData = json.load(read_file)


            for pairs in passData:
                    if choosenEmail == pairs["email"]:
                        print("Password found! \nPassword: ", pairs["password"], "\nE-mail:", pairs["email"])

                        password = pairs["password"]
                        passwordLen = len(password)
                        passwordLettersLen = len(''.join([char for char in password if char.isalpha()]))
                        passwordNumbersLen = len(''.join(filter(str.isdigit, password)))
                        passwordCharLen= len(re.findall(r'[!\"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~]',password))

                        print (passwordLettersLen, passwordNumbersLen, passwordCharLen)
                        letterSecurity = round((passwordLettersLen / passwordLen) ,2)* 100 
                        numberSecurity = round((passwordNumbersLen / passwordLen), 2) * 100 
                        chartersSecurity = round((passwordCharLen/ passwordLen), 2) * 100

                        if letterSecurity> 50:
                            print(f"The security level of the password is low. There are to many alphabetical characters. This is the percentage of numbers ({numberSecurity}%), alphabetical letters({letterSecurity}%), and special characters({chartersSecurity}%) in your password.")

                        elif numberSecurity< 25:
                            print(f"The security level of the password is medium. There should be more numbers. This is the percentage of numbers ({numberSecurity}%), alphabetical letters({letterSecurity}%), and special characters({chartersSecurity}%) in your password.")

                        elif chartersSecurity< 25:  
                            print(f"The security level of the password is low. There should be more special characters. This is the percentage of numbers ({numberSecurity}%), alphabetical letters({letterSecurity}%), and special characters({chartersSecurity}%) in your password.")

                        elif letterSecurity< 20:  
                            print(f"The security level of the password is low. There should be more alphabetical letters. This is the percentage of numbers ({numberSecurity}%), alphabetical letters({letterSecurity}%), and special characters({chartersSecurity}%) in your password.")

                        else:
                            print(f"The security level of the password is good. This is the percentage of numbers ({numberSecurity}%), alphabetical letters({letterSecurity}%), and special characters({chartersSecurity}%) in your password.")




                    else:
                        print("ERROR: No password found vinculated to this e-mail.")
    else:
        print("No password located in the database. It's suggested that you create a password first.")

def Menu():

    while True:

        decision = input("Hey, what are you looking for in this program? \n\n1. Create a password;\n2. Access a password; \n3. Delete a password;\n4. Update a password;\n5. Check password security;\n6. Quit app.")
        if decision == "1":
            createPassword()
            pass
 
        elif decision == "2":
            accessPassword()
            pass

        elif decision == "3":
            deletePassword()
            pass

        elif decision == "4":
            editPassword()
            pass

        elif decision == "5":
            checkSecurityPassword()
            pass

        elif decision == "6":

            sys.exit(0)
Menu()