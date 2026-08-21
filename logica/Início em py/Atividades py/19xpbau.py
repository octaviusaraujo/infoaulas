import random

bomstpotal = 0
bau = 1

for bau in range(bau,4,1):
    pnts_xp = random.randint(20,50)

    print(f"{bau}° bau possui {pnts_xp} de xp")
    bomstpotal =bomstpotal + pnts_xp

print(f"voce cimentos {bomstpotal} de xp total")