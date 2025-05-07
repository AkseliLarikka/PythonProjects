# This python code will first ask you to input a number. Then it will tell you all the numbers, said number is dividable by
def jaolliset_luvut(n):
    jaolliset = []
    for i in range(1, n + 1):
        if n % i == 0:
            jaolliset.append(i)
    return jaolliset

luku = int(input("Syötä luku: "))
jaolliset = jaolliset_luvut(luku)

print("Luku", luku, "on jaollinen seuraavilla luvuilla:", jaolliset)
