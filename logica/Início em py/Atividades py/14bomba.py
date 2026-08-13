import time

segundos = 10

while True:
     print(f"Bomba explodindo em {segundos}...")
     time.sleep(1)
     segundos -= 1
     if segundos == 0:
        break
     
print("boom")
     