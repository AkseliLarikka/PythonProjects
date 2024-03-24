# Import necessary modules
from selenium import webdriver  # Web automation library
from selenium.webdriver.common.keys import Keys  # Keys for simulating keyboard input
from selenium.webdriver.common.by import By  # Locator strategies
from selenium.webdriver.support.ui import WebDriverWait  # Wait conditions
from selenium.webdriver.support import expected_conditions as EC  # Expected conditions for waiting
from selenium.webdriver.chrome.service import Service  # Chrome driver service
import string  # String manipulation functions
import random  # Random number generation functions

# store all characters in lists. The characters for passwords are chosen from these
# Store all lowercase letters in a list (s1)
s1 = list(string.ascii_lowercase)

# Store all uppercase letters in a list (s2)
s2 = list(string.ascii_uppercase)

# Store all digits in a list (s3)
s3 = list(string.digits)

# Store all punctuation characters in a list (s4)
s4 = list(string.punctuation)

# Ask the user about the number of characters
user_input = input("How many characters do you want in your password? ")

# Check if the user input is a number and if it's greater than or equal to 8
while True:
    try:
        # Convert user input to an integer
        characters_number = int(user_input)

        # Check if the number is less than 8
        if characters_number < 8:
            print("Your number should be at least 8.")
            user_input = input("Please, Enter your number again: ")
        else:
            # Exit the loop if the condition is met
            break
    except:
        # Handle the case where the input is not a number
        print("Please, Enter numbers only.")
        user_input = input("How many characters do you want in your password? ")

# Shuffle and randomize all lists
random.shuffle(s1)
random.shuffle(s2)
random.shuffle(s3)
random.shuffle(s4)

# Calculate 30% & 20% of the number of characters decided by user
part1 = round(characters_number * (30/100))  # Calculate 30% of characters (for example 30% of 15 characters is about 4 or 5 characters)
part2 = round(characters_number * (20/100))  # Calculate 20% of characters (for example 20% of 15 characters is 3 characters)

# Generation of the password (60% letters and 40% digits & punctuations)
result = []  # Initialize an empty list to store the password characters

# Loop to append lowercase and uppercase letters to the result (60% or two times the 30% of part 1)
for x in range(part1):
    result.append(s1[x])  # Append a lowercase letter
    result.append(s2[x])  # Append an uppercase letter
# Add the lower and upper case letters to the list

# Loop to append digits and punctuation characters to the result (40% or two tiumes the 40% of part 2)
for x in range(part2):
    result.append(s3[x])  # Append a digit
    result.append(s4[x])  # Append a punctuation character
# Add the digits and punctuation characters to the list
# Shuffle the list containing the digits, punctuation, upper, and lower case characters
random.shuffle(result)

# Join result and make the randomized password a defined value
password = "".join(result)

# Necessary defines for the website scraping
# URL of the password strength checker website
website_url = 'https://www.security.org/how-secure-is-my-password/'  

# The generated password to be checked
search_text = password  

# Edit the below value to make the path fitting for your PCs path to chromedriver
# If you don't have Chromedriver, see README.md for details
# Path to the ChromeDriver executable. Double backslashes are used for proper formatting.
chrome_driver_path = "C:\\Users\\aksel\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe"

# Service to run ChromeDriver
service = Service(executable_path=chrome_driver_path)  
# Options for configuring the ChromeDrivers
options = webdriver.ChromeOptions()  
# Initialize the ChromeDriver
driver = webdriver.Chrome(service=service, options=options)  
# Initialize passwd_crack with a default value
passwd_crack = None  

try:
    # Open the website
    driver.get(website_url)

    # Wait for the password input field to be present
    password_input_locator = (By.XPATH, '//*[@id="password"]')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(password_input_locator))

    # Find the search input field
    search_input = driver.find_element(*password_input_locator)

    # Input text into the search field
    search_input.send_keys(search_text)

    # Simulate pressing Enter key
    search_input.send_keys(Keys.RETURN)

    # Wait for the search results to load
    WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="hsimp"]/div[1]/div[3]'))
    )

    # Find the search results
    search_results = driver.find_elements(By.XPATH, '//*[@id="hsimp"]/div[1]/div[3]')

    # Check if there are multiple results or just one
    if len(search_results) > 1:
        print("Multiple search results found. Handling only the first one.")

    # Iterate over the search results
    for result in search_results:
        passwd_crack = result.text

# Handling excpetions
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser window
    driver.quit()

# Function to write the generated password to a file
def passwd_file(filename, password):
    # Open the file with write mode
    with open(filename, "w") as file:
        # Write the password directly to the file
        file.write(password)  
# Define an absolute path for the file (replace with your desired path)
file_path = "examples\\Harjoitustyö\\password.txt"

# Call the function to write the password to the specified file path
passwd_file(file_path, password)

# Print the search result, generated password, and a message to the console
print("Your randomly generated Password is: ", password)
print(passwd_crack)
print("Password is printed in 'password.txt' file as well :)")