import random
from socket import timeout


lower_case = 'abcdefghijklmnopqrstuvwxyz'
upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
number = '0123456789'
symbols = '!@#$%^&*/\?'

all_total = lower_case + upper_case + number + symbols

lenth_of_password = 10

password = "".join(random.sample(all_total, lenth_of_password))


print('--------------------------------------------------------------------')
print('                     -------------------------                      ')
print('                        ------------------                          ')
print('-----------------------get password on your-------------------------')

Name = input('Enter you name associated with the number :')
phone = input('Enter the number: ')
print(' You will receive the OTP shortly for varification on', phone)
input('Enter the OTP received on your number:')
print(Name,' your new generated password is: ',password)
print('INVALID SESSION PLEASE CONTACT BRANCH')