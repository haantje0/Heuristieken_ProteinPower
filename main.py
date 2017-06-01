import hillclimber as hc
import bruteforce as bf

answer = ""

# ask the user what algorithm it wants to use
while answer != "bf" and answer != "hc":
    answer = raw_input("Bruteforcer (type 'bf') or Hillclimber (type 'hc'): ").lower()

# start the chosen algorithm
if answer == "bf":
    bf.bruteforce()
elif answer == "hc":
    hc.hillclimber()
