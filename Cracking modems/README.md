# Documentation for my first attempt at "breaking into" a modem/router

## Premise

My grandparents got a new router and I took the old one with me to do this exercise.

## Technical specs



## Idea process

1. My first idea was to use some sort of network sniffer to get inside the router. After some googling I figured that would not do.
2. I remembered a tool called [Kraken](https://github.com/jasonxtn/Kraken) I used in some TryHackMe exercise I once did and my angle of attack changed to brute forcing the modem. Finger's crossed the default password is still there
3. I installed Kali Linux as a virtual machine as this seems like a fitting place to also start learning using Kali
4. I tried installing Kraken on Kali but ran into some python version error I couldn't be bothered to clear so I searched [the Kali tools page](https://www.kali.org/tools/) and found [bruteforce-salted-openssl](https://www.kali.org/tools/bruteforce-salted-openssl/#bruteforce-salted-openssl-1) which seems fitting for my use case
