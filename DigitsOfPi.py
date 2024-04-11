'''def bbp_formula(k):
    # BBP kaava
    f1 = 1/(16**k) * (4/(8*k+1) - 2/(8*k+4) - 1/(8*k+5) - 1/(8*k+6))
    return f1

def calculate_pi(digits):
    pi = sum(bbp_formula(k) for k in range(digits))
    pi = "{:.{}f}".format(pi, digits-1)
    return pi

print(calculate_pi(100))'''
# output: 3.141592653589793115997963468544185161590576171875000000000000000000000000000000000000000000000000000
# therefore incorrect

def calculate_pi(digits):
    # Initialize variables for the algorithm
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    decimal = 0
    counter = 0
    pi_digits = ""
    
    # Loop until we've calculated the required number of digits
    while counter < digits + 1:
        # Check if the next digit of pi can be calculated
        if 4*q+r-t < n*t:
            # Append the next digit to the result
            pi_digits += str(n)
            # Add a decimal point after the first digit
            if counter == 0:
                pi_digits += "."
            # Reset the decimal counter after 10 digits to format the output
            if decimal == 10:
                decimal = 0
            # Increment the digit counter
            counter += 1
            # Calculate the remainder of the division (modulus operation)
            nr = 10*(r-n*t)
            # Calculate the next digit of pi
            n = ((10*(3*q+r))//t)-10*n
            # Multiply q by 10 for the next iteration
            q *= 10
            # Update r for the next iteration
            r = nr
        else:
            # Calculate the new values of the variables for the next iteration
            nr = (2*q+r)*l
            nn = (q*(7*k+2)+r*l)//(t*l)
            q *= k
            t *= l
            l += 2
            k += 1
            n = nn
            r = nr
    # Return the calculated digits of pi
    return pi_digits

# Print the first 100 digits of pi
print(calculate_pi(100))