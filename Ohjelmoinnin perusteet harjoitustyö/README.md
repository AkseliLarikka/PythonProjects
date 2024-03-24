# Password Generator and Strength Checker

This Python script generates a secure random password and checks its strength using a password strength checker website. It utilizes the Selenium library for web automation and ChromeDriver for browser interaction.

## Prerequisites

Make sure you have the following installed:

- Python
- ChromeDriver
    - See bottom of README.md for installation instructions
- Selenium for Python
    - See bottom of README.md for installation instructions
- Visual Studio Code (optional)

## Usage

1. Run the script.
2. Enter the desired number of characters for your password. Has to be at least 8.
3. The script will generate a password with a mix of lowercase letters, uppercase letters, digits, and punctuation.
4. The generated password is then checked for strength on a password strength checker website.

## Configuration

- The path to the ChromeDriver executable is set in the script. Adjust the `chrome_driver_path` variable if needed.
- The generated password is saved to a file. You can set the file path using the `file_path` variable. (Default is to save it to the same directory as the the .py file)

## Running the Script

- If you want to run the script from a command prompt, type the command below there. (Make sure that you are in the correct directory)

```bash
python passwd.py
```

- Easiest is to run it through Visual Studio Code (or something similar)

## Example Input/Output

- The script will display the strength of your password from the website and print the generated password.
- The generated password is also saved to a file specified by `file_path`.

### Output

```
How many characters do you want in your password?
```

### Input

```15```

### Output

```
Your randomly generated Password is:  5u48/WE>Iip[qY
It would take a computer about
4 hundred million years
to crack your password
Password is printed in 'password.txt' file as well :)
```

## How to install ChromeDriver

- To get the chrome_driver_path to work, go to https://googlechromelabs.github.io/chrome-for-testing/#stable and download the version corresponding to your chrome version.
- You can find out what version of Chrome you are using by typing "chrome://settings/help" in the address bar or if you click open the three dots from the top-right corner in chrome and choose "help" and "about google chrome". For version ending in 119.0.6045.160 the 119.0.6045.105 chromedriver works.
- After installing the package, unzip it, find the chromedriver.exe, select it, right click it, copy path, insert the copied path between the " " and you are good to go :)

## How to install Selenium WebDriver

- Go into your command prompt of choice (VS code, windows CMD, etc) and type in ```pip install selenium``` or if that does not work go to https://www.geeksforgeeks.org/how-to-install-selenium-in-python/ and follow the instructions.
