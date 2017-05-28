import hillclimber as hc
import bruteforce as bf

answer = ""

while answer != "bf" and answer != "hc":
    answer = raw_input("Bruteforcer (type 'bf') or Hillclimber (type 'hc'): ").lower()

if answer == "bf":
    bf.bruteforce()
elif answer == "hc":
    print answer
    hc.hillclimber()
    "FUCK YOU"
