import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#problem setup
N_potential_solutions = 20
N_correct_solutions = 2

ids_correct = np.random.choice(range(N_potential_solutions),(N_correct_solutions),replace=False)

#defining the problem using a dict, can be specified as truth table as well
problem = dict( [ (i,int(i in ids_correct)) for i in range(N_potential_solutions) ] )

N_qubits = int(np.ceil(np.log(len(problem))/np.log(2))) #the number of qubits needed
N_bases = 2**N_qubits

print("N_qubits",N_qubits)
print("N_bases",N_bases)

u_bra = np.ones(N_bases,dtype=np.complex) / np.sqrt(N_bases) #equal amplitude on each solution

#building the oracle unitary
oracle_unitary = np.eye(N_bases).astype(np.complex64) #units on diagonal

for key in range(N_bases):
    if ((key in problem) and (problem[key] == 1)):
        oracle_unitary[key,key] = -1+0j

print("oracle_unitary",oracle_unitary)

def reflect_by_vectors(v_in,us_to_reflect_by_list):
    v_reflected_so_far = np.array(v_in)

    for u_to_reflect_by in us_to_reflect_by_list:

        dot = np.sum(u_to_reflect_by * (np.conj(v_reflected_so_far)))
        v_along = dot * u_to_reflect_by

        v_perpendicular = v_reflected_so_far - v_along

        v_reflected_so_far = -1.0*v_perpendicular + v_along

    return v_reflected_so_far

bad_vectors_list = []
good_vectors_list = []

for key in range(N_bases):
    if ((key not in problem) or (problem[key] == 0)):
        bad_basis_now = np.zeros(N_bases)
        bad_basis_now[key] = 1.0
        bad_vectors_list.append(bad_basis_now)
    elif problem[key] == 1:
        good_basis_now = np.zeros(N_bases)
        good_basis_now[key] = 1.0
        good_vectors_list.append(good_basis_now)

def project_to_vectors(v_in,us_to_project_to_list):

    v_projected = np.zeros(N_bases).astype(np.complex)

    v_in_remaining = np.array(v_in)
    for u_to_project_to in us_to_project_to_list:

        dot = np.sum(u_to_project_to * (np.conj(v_in_remaining)))
        v_along = dot * u_to_project_to

        v_projected = v_projected + v_along
        v_in_remaining = v_in_remaining - v_along

    return v_projected


state = np.array(u_bra)

#calculating the stopping step
state_along_goods = project_to_vectors(state,good_vectors_list)
state_along_bads = project_to_vectors(state,bad_vectors_list)
theta = np.arctan2(np.linalg.norm(state_along_goods),np.linalg.norm(state_along_bads))

steps_to_stop = int(np.round(np.pi / (4.0*theta) - 0.5))

print("steps_to_stop",steps_to_stop)

state_evolution_list = []
states_stored = []

for step in range(steps_to_stop+1):

    states_stored.append(np.array(state))

    state_along_goods = project_to_vectors(state,good_vectors_list)
    state_along_bads = project_to_vectors(state,bad_vectors_list)

    state_evolution_list.append([np.linalg.norm(state_along_bads),np.linalg.norm(state_along_goods)])

    print(step,np.linalg.norm(state),np.linalg.norm(state_along_goods),np.linalg.norm(state_along_bads))

    print("Step="+str(step)+" P_correct="+str(np.linalg.norm(state_along_goods)**2.0))

    #Step 1 = apply the oracle_unitary
    state = np.matmul(oracle_unitary,state)

    #Step 2 = reflect by the uniform state u
    state = reflect_by_vectors(state,[u_bra])

state_evolution_np = np.stack(state_evolution_list,axis=0)

#Figure 1 -- state rotation

#circle
xs = np.linspace(0.0,1.0,1000)
ys = np.sqrt(1.0-xs**2.0)

plt.box(on=None)
plt.plot(xs,ys,color = "blue")

for i,(bad,good) in enumerate(state_evolution_np[:steps_to_stop+1]):
    color = cm.rainbow(float(i)/(steps_to_stop))
    plt.plot([0.0,bad],[0.0,good],marker = "o",color = color,markersize = 10,linewidth = 3)

    text_factor = 0.92

    if i == 0:
        plt.text(bad*text_factor,good*text_factor,"Init",fontsize = 12)
    else:
        plt.text(bad*text_factor,good*text_factor,str(i),fontsize = 12)


for i in range(steps_to_stop):
    plt.arrow(
        state_evolution_np[i,0],
        state_evolution_np[i,1],
        0.80*(state_evolution_np[i+1,0]-state_evolution_np[i,0]),
        0.80*(state_evolution_np[i+1,1]-state_evolution_np[i,1]),
        color = "black",
        width = 0.008,
        zorder = 100
        )

plt.title("Grover's algorithm\nPotential solutions="+str(N_potential_solutions)+", correct="+str(N_correct_solutions))

plt.axes().set_aspect('equal')
plt.xlim([-0.1,1.1])
plt.ylim([-0.1,1.1])
plt.grid("on")
plt.xlabel("Amplitude projected to wrong states",fontsize = 14)
plt.ylabel("Amplitude projected to correct states",fontsize = 14)
plt.show()

#Figure 2 -- amplitude concentration on the correct solutions
plt.figure(figsize = (5,len(states_stored)*1.2))
plt.suptitle("Grover's algorithm\nPotential solutions="+str(N_potential_solutions)+", correct="+str(N_correct_solutions))

for i,state in enumerate(states_stored):

    plt.subplot(len(states_stored),1,i+1)

    probs = np.abs(state)**2.0

    for j in range(len(probs)):
        if ((j not in problem) or (problem[j] == 0)):
            color = "blue"
        else:
            color = "green"
        plt.fill_between([j+0.1,j+1-0.1],[0.0,0.0],[probs[j],probs[j]],color = color)

    plt.xlim([0,N_potential_solutions])
    plt.ylim([0.0,1.0/N_correct_solutions])
    plt.ylabel("Prob",fontsize = 14)
    if i == len(states_stored)-1:
        plt.xlabel("Solution id",fontsize = 14)
    else:
        plt.xticks([],[])

plt.show()
