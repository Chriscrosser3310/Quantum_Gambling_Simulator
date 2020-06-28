import time
import qiskit
from qiskit import IBMQ, assemble, transpile
from qiskit.circuit.random import random_circuit
from qiskit.providers.jobstatus import JOB_FINAL_STATES
from qiskit.providers.aer.noise import NoiseModel
from numpy import arctan, sqrt

# Authenticate an account and add for use during this session. Replace string
# argument with your private token.
# IBMQ.enable_account("3141375be58a07cf2577abe3e44aaeb23fd8ebe07c9666b907bd9ddf0bd6d7aeafefb9bca6860231f853aba2bac26524287dae14860cd123a86fe010bef5e001")

from qiskit import IBMQ, assemble, transpile
from qiskit.circuit.random import random_circuit

provider = IBMQ.load_account()
backend = provider.backends.ibmq_16_melbourne

qr = qiskit.QuantumRegister(8)
cr = qiskit.ClassicalRegister(1)
qc = qiskit.QuantumCircuit(qr, cr)

# Alice chooses ball location
p00 = 0.9
p01 = 0.05
p10 = 0.05

angle1 = arctan(sqrt(p01)/sqrt(p00 + p10))*2
angle2 = arctan(sqrt(p10)/sqrt(p00))*2
qc.ry(angle1, 0)
qc.x(0)
qc.cry(angle2,0,1)
qc.x(0)

# Bob chooses door
bob_choice = 2
if bob_choice == 0:
    qc.i(2)
elif bob_choice == 1:
    qc.x(2)
elif bob_choice == 2:
    qc.x(3)

# Alice opens door
alice_open = 0
if alice_open == 0:
    qc.i(4)
elif alice_open == 1:
    qc.x(4)
elif alice_open == 2:
    qc.x(5)


# Bob switches or not
p0 = 0.5
p1 = 0.5
angle = arctan(sqrt(p1)/sqrt(p0))*2
qc.ry(angle, 6)


qc.barrier(qr)

qc.x([0,4,5,2])
qc.mcx([0,1,4,5], 7)
qc.mcx([4,5,2,3], 7)
qc.x([1,4,3])
qc.mcx([0,1,4,5], 7)
qc.x([0])
qc.mcx([4,5,2,3], 7)
qc.x([4,5,2])
qc.mcx([0,1,4,5], 7)
qc.mcx([4,5,2,3], 7)
qc.x([1,4,3])
qc.cx(6,7)
qc.barrier()
qc.measure(7,0)

qobj = assemble(transpile(qc, backend=backend), backend=backend)
job = backend.run(qobj)
retrieved_job = backend.retrieve_job(job.job_id())

start_time = time.time()
job_status = job.status()
while job_status not in JOB_FINAL_STATES:
    print(f'Status @ {time.time()-start_time:0.0f} s: {job_status.name},'
          f' est. queue position: {job.queue_position()}')
    time.sleep(10)
    job_status = job.status()

result = job.result()
print(result.get_counts())