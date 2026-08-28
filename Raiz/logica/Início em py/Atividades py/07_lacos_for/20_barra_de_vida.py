import time

for porcentange in range(10,101,10):
    time.sleep(1)

    barra = "=" * (porcentange //10)
    print("["+barra+"]",porcentange, "%")

