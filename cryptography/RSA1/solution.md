# RSA 1

## Write-Up

For another RSA challenge, we can find this time that the N made by the other is acuatlly small, so our attack would by cracking (factorizing) this modulus. Note that we need to to test numbers up to `49` digits which might take some time, so a regular `factorize()` algorithm will take a little bit more time :

```python
In [2]: from math import sqrt

In [3]: sqrt(1018261336751023520497560395829454421245429586704872293236600679847605951423419167478189648109263)
Out[3]: 1.0090893601416198e+48

In [7]:   int(1.0090893601416198e+48) + 1
Out[7]: 1009089360141619808999578494634632725738702241793

In [8]: len("1009089360141619808999578494634632725738702241793")
Out[8]: 49
```

Here are some solutions and scripts you might find :

1. Check for `http://factordb.com`, a factors database that might contain your modulus (Thanks to `yh_0x7` that put it in there)

2. Execute a `factorize()` algorithm parallaled using `concurrent.future` :

```py
import gmpy2
    ...: import concurrent.futures
    ...: 
    ...: def is_prime(n):
    ...:     return gmpy2.is_prime(n)
    ...: 
    ...: def find_factors(n):
    ...:     factors = []
    ...:     for i in range(1, gmpy2.isqrt(n) + 1, 6):
    ...:         i1 = i + 1
    ...:         i2 = i + 5
    ...:         if is_prime(i1) and n % i1 == 0:
    ...:             print(i1)
                     exit(0)
    ...:         if is_prime(i2) and n % i2== 0:
    ...:             factors.append(i2)
                     exit(0)
    ...:         
    ...:     return factors
    ...: 
    ...: def find_prime_factors(n):
    ...:     with concurrent.futures.ProcessPoolExecutor() as executor:
    ...:         factors = list(executor.map(is_prime, find_factors(n)))
    ...:     return [f for i, f in enumerate(find_factors(n)) if factors[i]]
  find_prime_factors(1018261336751023520497560395829454421245429586704872293236600679847605951423419167478189648109263)
```

3. Use some Quantum computing ressources to factorize it (your will need to have anaccount in `https://quantum-computing.ibm.com` and use your API to execute it), this script is based on the `Shor's Factorization algorithm` which complexity is `O(n3log(n))` :

```py
from qiskit import IBMQ
from qiskit.utils import QuantumInstance
from qiskit.algorithms import Shor

IBMQ.enable_account('YOUR API KEY HERE') # Enter your API token here
provider = IBMQ.get_provider(hub='ibm-q')

backend = provider.get_backend('ibmq_qasm_simulator') # Specifies the quantum device

print('\n Shors Algorithm')
print('--------------------')
print('\nExecuting...\n')

factors = Shor(QuantumInstance(backend, shots=100, skip_qobj_validation=False)) 

N = 1018261336751023520497560395829454421245429586704872293236600679847605951423419167478189648109263
len = 97

result_dict = factors.factor(N=N, a=len) # Where N is the integer to be factored
result = result_dict.factors

print(result)
print('\nPress any key to close')
input()
```

After Factorizing it, here are the factors of our `N` modulus :

```
p = 9942874965373398689
q = 102411157768469768587484356311902427789461430190314198242306101223897141593967
```

Now, using a decryption script, we can decrypt our message :

```py
#! /usr/bin/python3

from Crypto.Util.number import *

f = open('RSA1.txt', 'r')
e = int(f.readline().split("=")[1].strip())
n = int(f.readline().split("=")[1].strip())
enc = int(f.readline().split("=")[1].strip())

# After Factorization
p = 9942874965373398689
q = 102411157768469768587484356311902427789461430190314198242306101223897141593967

d = pow(e, -1, (p-1)*(q-1))

flag = pow(enc, d, n)
flag = long_to_bytes(flag)

print(flag)
```

And here is the output :

```
b'shellmates{U_5h0uld_U53_L4rg3_Numb3r5}'
```

## Flag
shellmates{U_5h0uld_U53_L4rg3_Numb3r5}

## More Information

There was also other techniques that you might test if you don't know what to do with the keys you have :

- [Wikipedia- Coppersmith's Method](https://en.wikipedia.org/wiki/Coppersmith_method)
- [Wikipedia- Coppersmith's Attack](https://en.wikipedia.org/wiki/Coppersmith%27s_attack)
- https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/coppersmith.sage
- https://github.com/ashutosh1206/Crypton/blob/master/RSA-encryption/Attack-Coppersmith/README.md
- https://www.cryptologie.net/article/222/implementation-of-coppersmith-attack-rsa-attack-using-lattice-reductions/
- https://primes.utm.edu/
- Shor's Algorithm :
  - https://jonathan-hui.medium.com/qc-cracking-rsa-with-shors-algorithm-bc22cb7b7767
  - https://quantumcomputinguk.org/tutorials/shors-algorithm-with-code