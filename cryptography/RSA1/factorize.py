def print_factors(x):
   print("The factors of",x,"are:")
   for i in range(1, (x // 2) + 1):
       if x % i == 0:
           print(i)


num = int(input("Give me number to factorize : "))

print_factors(num)