
def validation_pin():
    next=True
    while next or (len(str(pwd1)) != 6):
        try:
            print("Pin must be of 6 digit only")
            pwd1 = int(input("enter you 6 digit pin: " ))
            next = False
        except Exception as ValueError:
            print("You have to enter only NUMBER / DIGIT")
            print("Try Again")
    return True