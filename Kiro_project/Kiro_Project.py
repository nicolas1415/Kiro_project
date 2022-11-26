import json

filename_tiny = "tiny.json"
filename_medium = "medium.json"
filename_large = "large.json"
filename_huge = "huge.json"


def actualiser(Jobs_temp, liste_operator, liste_machine):
    for L in Jobs_temp:
        if (L[1] != 0):
            L[1] -= 1
    for L in liste_operator:
        if (L[1] != 0):
            L[1] -= 1
    for L in liste_machine:
        if (L[1] != 0):
            L[1] -= 1
    return 0


def get_machine(machine, liste_machine):
    for i in range(len(machine)):
        if liste_machine[machine[i]["machine"]-1][1] == 0:
            return i
    return -1


def get_operator(machine, liste_operator, i):
    for j in range(len(machine[i]["operators"])):
        if liste_operator[machine[i]["operators"][j]-1][1] == 0:
            return j
    return -1


def sol_construct_glouton(filename, filename_out):
    with open(filename, 'r') as file:
        x = json.load(file)

    Jobs = x["jobs"]
    parameters = x["parameters"]
    tasks = x["tasks"]

    total_machine = []
    for i in range(parameters["size"]["nb_tasks"]):
        y = tasks[i]["machines"]
        for j in range(len(y)):
            total_machine.append(y[j]["machine"])

    total_machine_compte = []
    for i in range(parameters["size"]["nb_machines"]):
        compteur = 0
        for j in total_machine:
            if j == i+1:
                compteur += 1
        total_machine_compte.append(compteur)

    Jobs_temp = []
    for i in range(parameters["size"]["nb_jobs"]):
        U = Jobs[i]["sequence"]
        Jobs_temp.append([U, 0, i+1])

    liste_machine = []
    for i in range(parameters["size"]["nb_machines"]):
        liste_machine.append([i+1, 0])
    liste_operator = []
    for i in range(parameters["size"]["nb_operators"]):
        liste_operator.append([i+1, 0])

    T = 1
    temp = True
    temp_fin = []
    temp_debut = []
    while (temp):
        if (len(Jobs_temp) == 0):
            temp = False
        else:
            Y = []
            actualiser(Jobs_temp, liste_machine, liste_operator)
            for L in Jobs_temp:
                if (L[1] == 0 and Jobs[L[2]-1]["release_date"] <= T):
                    H = L[:]
                    H.append(Jobs[L[2]-1]["weight"])
                    H.append(Jobs[L[2]-1]["due_date"])
                    Y.append(H)

            Y = sorted(Y, key=lambda x: (x[4], x[3]))
            for indice in range(len(Y)):
                U = Y[indice]

                int_task = U[0][0]
                # print(int_task)
                machine = tasks[int_task-1]["machines"]
                machine_possible = []
                for i in range(len(machine)):
                    if liste_machine[machine[i]["machine"]-1][1] == 0:
                        machine_possible.append(machine[i]["machine"])
                ind = 0
                min = 900000000
                for k in range(len(machine_possible)):
                    if total_machine_compte[machine_possible[k]-1] < min:
                        min = total_machine_compte[machine_possible[k]-1]
                        ind = machine_possible[k]

                i = get_machine(machine, liste_machine)
                if (i == -1):
                    break
                j = get_operator(machine, liste_operator, i)
                if (j == -1):
                    break

                time = tasks[int_task-1]["processing_time"]
                liste_machine[machine[i]["machine"]-1][1] = time
                liste_operator[machine[i]["operators"][j]-1][1] = time
                vrai_indice = U[2]
                vrai_indice1 = 1
                temp_debut.append(
                    [T, int_task, machine[i]["operators"][j], machine[i]["machine"]])
                for i in range(len(Jobs_temp)):
                    if Jobs_temp[i][2] == vrai_indice:
                        vrai_indice1 = i
                # print(len(U[0]))

                if (len(U[0]) == 1):
                    # print(vrai_indice1)
                    # print(Jobs_temp)
                    del Jobs_temp[vrai_indice1]
                    temp_fin.append([T+time, vrai_indice1])
                else:
                    # print(Jobs_temp)
                    Jobs_temp[vrai_indice1] = [
                        Jobs_temp[vrai_indice1][0][1:], time, vrai_indice]

        T += 1
    # print(temp_debut)
    temp_debut = sorted(temp_debut, key=lambda x: x[1])
    alist = []
    with open(filename_out, 'w') as f:

        for k in range(parameters["size"]["nb_tasks"]):
            task = {
                "task": k+1,
                "start": temp_debut[k][0],
                "machine": temp_debut[k][3],
                "operator": temp_debut[k][2],
            }

            alist.append(task)
        json.dump(alist, f)
    return (alist)


sol_construct_glouton(filename_tiny, "data_tiny.json")
sol_construct_glouton(filename_medium, "data_medium.json")
sol_construct_glouton(filename_large, "data_large.json")
sol_construct_glouton(filename_huge, "data_huge.json")
