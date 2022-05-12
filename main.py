import csv
from random import randint
import qrcode
import time

def length(csv_rows):
    """This function will return the no of rows in csv file"""
    c = 0
    for row in csv_rows:
        c += 1
    return c

def display_user_data(row):
    """This function will display user data using single row in data file as argument"""
    name = row[0]
    CA_num = row[1]
    bill_paid = True if row[3] == 'paid' else False
    amount = row[4]


    print("\n****** Hello", name,'******')
    print("Your CA Number is", CA_num)
    if bill_paid:
        print("Your bill for this month has been paid.")
        print("Thank you for using our service", name)
        
    else:
        print("Your bill is due this month with amount .",amount,'\n')

def new_user():
    #greeting
    print('Welcome new user')

    #reading csv file
    f = open("data.csv",'r')
    reader = csv.reader(f)

    #taking user data
    name = input("Enter your name:")
    state = input("Enter your state:")

    #creating unique CA Number
    CA_num = str(length(reader) + 1)
    while len(CA_num) < 4:
        CA_num = '0' + CA_num

    #creating random amount in range of 800 to 3000
    amount = randint(80,300) * 10

    f.close()
    
    #appending User data into data file
    f = open("data.csv",'a')
    writer = csv.writer(f)
    row = [name,CA_num,state,'due',str(amount)]
    writer.writerow(row)
    f.close()
    time.sleep(0.5)
    print("\nuser created succesfully\n")
    display_user_data(row)
    payment_merchant(row)
    
    
def old_user():
    #greeting
    print("\nwelcome User\n")

    #opening csv data file
    f = open("data.csv", 'r')
    reader = csv.reader(f)

    #taking CA number from user
    ca = int(input('Enter Your CA number: '))

    #exiting program if CA is '-1'
    if ca == '-1':
        quit()
    
    #CA Number matches with any entry in data
    for row in reader:
        if int(row[1]) == ca:
            display_user_data(row)
            payment_merchant(row)
            break
    #if CA Number doesn't matches with any entry
    else:
        print("\n*****Invalid CA number: please try again,*****\nor Enter '-1' to exit program\n")
        old_user()
    f.close()

def payment_merchant(row):
    """This function will ask for payment if due"""
    amount = row[4]
    if row[3] == 'due':
        print("You need to pay {} rupees for your electricity bill for this month\n".format(amount))

        pay_now = input("Do you wish to pay now using UPI: [y/n]:").lower()
        if pay_now == 'y':
            qrdata = row[0]+str(amount)
            qr_img = qrcode.make(qrdata)
            qr_img.save(qrdata+'.png')

            print("\nA QRCODE has been generated in this folder, pay through UPI")
            payment_update(row)

        elif pay_now == 'n':
            print("please pay before due date to avoid charges\n")
        else:
            print("please enter valid response[y/n]:")
            payment_merchant(row)

def payment_update(row):
    """This function will update payment in data.csv file"""
    file = [] #for storing all data

    f = open("data.csv",'r')
    reader = csv.reader(f)

    for file_row in reader:
        file.append(file_row)


    #keep in mind that row is the data row being passed to update and file_row(s) are the rows in csv file
    for file_row in file:
        if file_row[1] == row[1]: #if ca number matches , convert 'due' to 'paid'
            file_row[3] = 'paid'
    f.close()

    #all the file will be written in data.csv
    f = open("data.csv",'w')
    writer = csv.writer(f)
    writer.writerows(file)
    f.close()

    print("\nYour payment has been succesfuly updated")



def main():
    #fetching detail from user
    is_new_user = input("Are you a new User [y/n] : ").lower()
    
    # if userInput doesn't match expected criteria {y or n}
    while (is_new_user != "y" and is_new_user != "n"): 
        is_new_user = input("\nPlease Enter accordingly\n'y' if you are new user \n'n' if you are already a user \nor '-1' to exit program.:")
        if is_new_user == '-1':
            quit()

    #if userinpyt match either 'y' or 'n'
    if is_new_user == "y":
        new_user()
    elif is_new_user == "n":
        old_user()

if __name__ == "__main__":
    #greeting
    print("\n******  Welcome to Electricity Billing Portal  ****** ")

    main()

    
 
    
        



