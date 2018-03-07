from bs4 import BeautifulSoup
from urllib.request import urlopen
import smtplib
import getpass
import time

'''
Work in progress.

This script takes s gmail address, a password, and a desired shoe name as as a string. The more precise the 
show name entered the better, it will parse the Nike men's shoes page every minute until it finds a match
and then it will email you that the shoe was found.
'''

email_serv = smtplib.SMTP('smtp.gmail.com', 587)
email = input('Enter your email: ')
password = getpass.getpass()
rawg = input("Enter desired shoe: ")
goal = rawg.title()

found = False

while not found:

    shoe_client = urlopen('https://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3')
    shoe_html = shoe_client.read()
    shoe_soup = BeautifulSoup(shoe_html, 'html.parser')
    shoe_client.close()

    shoe_page = shoe_soup.find('div',{'class': 'exp-gridwall-standard'})
    shoes = shoe_page.findAll('div', {'class': 'grid-item-info'})

    for shoe in shoes:
        shoe_name = shoe.find('p', {'class': 'product-display-name nsg-font-family--base edf-font-size--regular nsg-text--dark-grey'}).text

        if goal in shoe_name:

            email_serv.starttls()
            email_serv.login(email, password)
            msg = f'{shoe_name} found!'
            email_serv.sendmail(email, email, msg)
            email_serv.quit()
            print('Found!')
            found = True
            break

        else:
            print('Not found...')
            pass

    time.sleep(60)

quit()