# The bagel guessing game

In Bagels, a deductive logic game, you must guess a secret three-digit number based on clues.

The game offers one of the following hints in response to your guess:

“Pico” when your guess has a correct digit in the wrong place,

“Fermi” when your guess has a correct digit in the correct place,

and “Bagels” if your guess has no correct digits.

You have 10 tries to guess the secret number.

## Example run

Bagels, a deductive logic game.
    By Al Sweigart al@inventwithpython.com

    I am thinking of a 3-digit number with no repeated digits.
    Try to guess what it is. Here are some clues:
    When I say:     That means:
    Pico            One digit is correct but in the wrong position.
    Fermi           One digit is correct and in the right position.
    Bagels          No digit is correct.

    For example, if the secret number was 248 and your guess was 843, the
    clues would be Fermi Pico.

I have thought up a number.<br>
You have 10 guesses to get it.<br>
Guess #1:
> 754

Fermi<br>
Do you want to play again? (yes or no)
> yes

Guess #2:
> 782

Pico <br>
Do you want to play again? (yes or no)
> yes

Guess #3:
> 235

Bagels<br>
Do you want to play again? (yes or no)
> yes

Guess #4:
> 894

Fermi Fermi<br>
Do you want to play again? (yes or no)
> yes

Guess #5:
> 864

Fermi Fermi<br>
Do you want to play again? (yes or no)
> yes

Guess #6:
> 814

You got it!<br>
Thanks for playing!

## Exploring the program

Try to find the answers to the following questions. Experiment with some
modifications to the code and rerun the program to see what effect the
changes have.

1. What happens when you change the NUM_DIGITS constant?<br>
ANS:

2. What happens when you change the MAX_GUESSES constant?<br>
ANS:

3. What happens if you set NUM_DIGITS to a number larger than 10?<br>
ANS:

4. What happens if you replace secretNum = getSecretNum() on line 30 with secretNum = '123'?<br>
ANS:

5. What error message do you get if you delete or comment out numGuesses = 1 on line 34?<br>
ANS:

6. What happens if you delete or comment out random.shuffle(numbers) on line 62?<br>
ANS:

7. What happens if you delete or comment out if guess == secretNum: on line 74 and return 'You got it!' on line 75?<br>
ANS:

8. What happens if you comment out numGuesses += 1 on line 44?<br>
ANS:
