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