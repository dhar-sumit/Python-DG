# Assuming that we have some email addresses in the "username@companyname.com" format, write a program to print the company name of a given email address. Both user names and company names are composed of letters only.

# We will be using split method efficiently to separate the username and company name of the email address in format: (username@companyname.com)

email = input("Enter your email-id (username@companyname.com):")

user_name, rest_of_the_part = email.split('@')
company_name, rest_of_the_part = rest_of_the_part.split('.')

print(f"User name: {user_name} \nCompany name: {company_name}")