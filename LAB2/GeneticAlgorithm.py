import random
import numpy as np

def chromosome_encoding(size,len):
    population = []
    for _ in range(size): #outer loop is number of chromosomes generated
        string = ""
        for _ in range(len): #generating a chormosome by choosing 0 or 1
            string += str(random.randint(0,1))
        population.append(string)
    return population

def calc_fitness(chromosome):
    arr = np.ones((3,3))
    row,col = arr.shape
    """
    converting our input chromosome into a 3x3 matrix where eache row represents
    a time_slot and columns are courses. Column value 1 means that course is scheduled 
    in that time slot which is denoted by row num
    """
    i = 0
    for x  in range(row):
        for y in range(col):
            arr[x][y] = int(chromosome[i])
            i+=1

    fitness = 0
    penalty = {0:1, 2:1, 3:2}
    #checking if there are multiple courses in a same timeslot
    overlap_pen = 0
    for time_slot in arr:
        summ = sum(time_slot)
        if summ==0 or summ>1:
            overlap_pen += penalty[summ]
    #checking if one course is being scheduled multiple times
    consistency_pen =0
    for col_idx in range(arr.shape[0]):
        column = arr[:, col_idx]
        summ = sum(column)
        if summ>1 or summ==0:
            consistency_pen+=1

    fitness = -(overlap_pen+consistency_pen)
    return fitness

def sample(selection):
    while True:
        p1 = random.choice(selection)
        p2 = random.choice(selection)
        if p1 != p2:
            return p1,p2
        else:
            continue

def crossover(p1,p2,crossover_rate):
    #single point crossover
    if random.random() < crossover_rate:
        crosspoint = random.randint(0,len(p1)-1)
        temp1,cross1 = p1[:crosspoint],p1[crosspoint:] 
        temp2,cross2 = p2[:crosspoint],p2[crosspoint:]

        ofsprng1 = temp1+cross2
        ofsprng2 = temp2+cross1
        return ofsprng1,ofsprng2
    else:
        return p1,p2    
    
def two_point_crossover(chrmsm1,chrmsm2):
    point1 = random.randint(0,len(chrmsm1)//2)
    point2 = random.randint(point1,len(chrmsm1)-1)
    cross1,temp1,cross2 = chrmsm1[:point1] , chrmsm1[point1:point2] , chrmsm1[point2:]
    cross3,temp2,cross4 = chrmsm2[:point1] , chrmsm2[point1:point2] , chrmsm1[point2:]
    print(point1,point2)
    offspring1 = cross3+temp1+cross4
    offspring2 = cross1+temp2+cross2
    print(offspring1,offspring2) 
    
def mutate(chrmsm,mutation_rate):
    if random.random() < mutation_rate:
        idx = random.randint(0,len(chrmsm)-1)
        if chrmsm[idx] == '0':
            return chrmsm[:idx]+'1'+chrmsm[idx+1:]
        else:
            return chrmsm[:idx]+'0'+chrmsm[idx+1:]
    return chrmsm

def genetic_algorithm(fitness,population_size,total_generation,chromosome_len,crossover_rate,mutation_rate):
    population = chromosome_encoding(population_size,chromosome_len)
    results = {}

    for _ in range(total_generation): ## how many genrations
        new_population = []
        for _ in range(population_size//2):
            parent1,parent2 = sample(population)

            offspring1, offspring2 = crossover(parent1,parent2,crossover_rate)
            
            offspring1 = mutate(offspring1,mutation_rate)
            offspring2 = mutate(offspring2,mutation_rate)

            solution1 = fitness(offspring1)
            solution2 = fitness(offspring2)

            results[solution1] = offspring1
            results[solution2] = offspring2 
            new_population.extend([offspring1,offspring2])

        population = new_population
          
    best = max(results.keys())
            
    return results[best],best
    
    

if __name__ == '__main__':
    courses = []
    with open("LAB2.txt","r") as inp:
        N,T = map(int,inp.readline().strip().split())
        for line in inp:
            courses.append(line.strip())
    inp.close()
    c_len = N*T
    try:
        p_size = int(input("Enter Population size:"))
        total_gen = int(input("How many generation of choromosomes? :"))
        c_rate = int(input("Enter Crossover Rate [1-100] :"))/100
        m_rate = int(input("Enter Mutation Rate [1-100] :"))/100
        print(genetic_algorithm(calc_fitness,p_size,total_gen,c_len,c_rate,m_rate))
    except ValueError:
        print("Values entered must be integer")
