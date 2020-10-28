# coding=utf-8
'''
Condiciones
~~~~~~~~~~~
1. Hay 5 casas.
2. El Matematico vive en la casa roja.
3. El hacker programa en Python.
4. El Brackets es utilizado en la casa verde.
5. El analista usa Atom.
6. La casa verde esta a la derecha de la casa blanca.
7. La persona que usa Redis programa en Java
8. Cassandra es utilizado en la casa amarilla
9. Notepad++ es usado en la casa del medio.
10. El Desarrollador vive en la primer casa.
11. La persona que usa HBase vive al lado de la que programa en JavaScript.
12. La persona que usa Cassandra es vecina de la que programa en C#.
13. La persona que usa Neo4J usa Sublime Text.
14. El Ingeniero usa MongoDB.
15. EL desarrollador vive en la casa azul.

Quien usa vim?


Resumen:
Colores = Rojo, Azul, Verde, Blanco, Amarillo
Profesiones = Matematico, Hacker, Ingeniero, Analista, Desarrollador
Lenguaje = Python, C#, JAVA, C++, JavaScript
BD = Cassandra, MongoDB, Neo4j, Redis, HBase
editor = Brackets, Sublime Text, Atom, Notepad++, Vim
'''

import random
import time
from datetime import datetime
import multiprocessing as mp

#Constants
COLOR_INDEX = 0
PROFESSION_INDEX = 1
LANGUAJE_INDEX = 2
DATABASE_INDEX = 3
EDITOR_INDEX = 4
COLORS =      ['red', 'blue', 'green', 'white', 'yellow']
PROFESSIONS =  ['Mathematician', 'Hacker', 'Engineer', 'Analyst', 'Developer']
LANGUAJES =    ['Python', 'C#', 'Java', 'C++', 'JavaScript']
DATABASES =    ['Cassandra', 'MongoDB', 'HBase', 'Neo4j', 'Redis']
EDITORS =      ['Brackets', 'Sublime Text', 'Vim', 'Atom', 'Notepad++']


#Mutithreading config
FIXED_BATCH_COUNT = 0                   #Numero de batches a paralelizar. 0 = No es fijo
FIXED_BATCH_SIZE = 4500                 #Manaño de batch fijo. 0 = No es fijo
BATCH_COUNT_PER_CPU = 0.45              #Cantidad de batches a usar teniendo en cuenta la cantidad de CPUs disponibles. Usado si FIXED_BATCH_COUNT & FIXED_BATCH_SIZE = 0

#Parameters
POPULATION_LEN = 20000                  #Limite de población
PARENT_COUNT = 2500                     #Número de individuos (mejores) usados para generar la próxima generación
PARENT_TO_NEXT_GEN = 2000               #Número de individuos (mejores) que se transfieren a la siguiente generación
MUTATION_RATE = 0.50                    #Probabilidad de que un gen mute
INDIVIDUAL_CROSSOVER_RATE = 0.30        #Probabilidad de que un individuo tenga 2 parents
GENE_CROSSOVER_RATE = 0.60              #Probabilidad de que se haga crossover para un gen

class Phenotype:

    def generate(self):
        self.chromosome = self.createRandomChromosome()
        self.fitness_function()

    def createRandomChromosome(self):
        colors, prefession, languaje, database, editor = ([0,1,2,3,4] for _ in range(5))
        
        chromosome = []
        
        for _ in range(0, 5):
            random_c = random.randint(0, len(colors)-1)
            chromosome.append(colors[random_c])
            del colors[random_c]
            
            random_p = random.randint(0, len(prefession)-1)
            chromosome.append(prefession[random_p])
            del prefession[random_p]
            
            random_c = random.randint(0, len(languaje)-1)
            chromosome.append(languaje[random_c])
            del languaje[random_c]
            
            random_c = random.randint(0, len(database)-1)
            chromosome.append(database[random_c])
            del database[random_c]
            
            random_c = random.randint(0, len(editor)-1)
            chromosome.append(editor[random_c])
            del editor[random_c]
        
        return chromosome
    
    def decode(self):
        ''' traduce 0's y 1's (conjunto de genes: 3) en valores segun un diccionario '''
        return [[COLORS[self.chromosome[i*5+0]], 
                 PROFESSIONS[self.chromosome[i*5+1]],
                 LANGUAJES[self.chromosome[i*5+2]],
                 DATABASES[self.chromosome[i*5+3]],
                 EDITORS[self.chromosome[i*5+4]]] for i in range(5)]

    def mutate(self):
        ''' muta un fenotipo haciendo swap'''
        ''' se puede hacer esto porque cambié la función de inicialización de la población para que no contenga repetidos'''

        col = random.randint(0, 4) #Tipo de característica
        row1 = random.randint(0, 4) #Valor de la caracteristica 1
        row2 = random.randint(0, 4) #Valor de la caracteristica 2

        while row1 == row2:
            row2 = random.randint(0, 4)
    
        auxSwapValue = self.chromosome[row1*5+col]
        self.chromosome[row1*5+col] = self.chromosome[row2*5+col]
        self.chromosome[row2*5+col] = auxSwapValue

        
    def fitness_function(self):
        ''' calcula el valor de fitness del cromosoma segun el problema en particular '''

        self.score = 0

        ok_score = 1
        fail_score = -1
        punish_score = -1
        
        matrix = [[0 for x in range(5)] for x in range(5)]
        
        for i in range(0, 5):
            for j in range(0, 5):
                matrix[i][j] = self.chromosome[j*5+i]

        # 2. El Matematico vive en la casa roja.
        try:
            i = matrix[PROFESSION_INDEX].index(0)
            if matrix[COLOR_INDEX][i] == 0:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score
        
        # 3. El hacker programa en Python
        try:
            i = matrix[PROFESSION_INDEX].index(1)
            if matrix[LANGUAJE_INDEX][i] == 0:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score
        
        # 4. El Brackets es utilizado en la casa verde.
        try:
            i = matrix[EDITOR_INDEX].index(0)
            if matrix[COLOR_INDEX][i] == 2:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score
        
        # 5. El analista usa Atom.
        try:
            i = matrix[PROFESSION_INDEX].index(3)
            if matrix[EDITOR_INDEX][i] == 3:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score
        
        # 6. La casa verde esta a la derecha de la casa blanca.
        try:
            i = matrix[COLOR_INDEX].index(3)
            if i != 0 and matrix[COLOR_INDEX][i-1] == 4:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score
        
        # 7. La persona que usa Redis programa en Java
        try:
            i = matrix[DATABASE_INDEX].index(4)
            if matrix[LANGUAJE_INDEX][i] == 2:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score

        # 8. Cassandra es utilizado en la casa amarilla
        try:
            i = matrix[DATABASE_INDEX].index(0)
            if matrix[COLOR_INDEX][i] == 4:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score
        
        # 9. Notepad++ es usado en la casa del medio.
        try:
            i = matrix[EDITOR_INDEX].index(4)
            if i == 2:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score

        # 10. El Desarrollador vive en la primer casa.
        try:
            i = matrix[PROFESSION_INDEX].index(4)
            if i == 0:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score

        # 11. La persona que usa HBase vive al lado de la que programa en JavaScript.
        try:
            i = matrix[DATABASE_INDEX].index(2)
            if (i != 4 and matrix[LANGUAJE_INDEX][i+1] == 4) or (i != 0 and matrix[LANGUAJE_INDEX][i-1] == 4):
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += fail_score

        # 12. La persona que usa Cassandra es vecina de la que programa en C#.
        try:
            i = matrix[DATABASE_INDEX].index(0)
            if (i != 4 and matrix[LANGUAJE_INDEX][i+1] == 1) or (i != 0 and matrix[LANGUAJE_INDEX][i-1] == 1):
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += fail_score

        # 13. La persona que usa Neo4J usa Sublime Text.
        try:
            i = matrix[DATABASE_INDEX].index(3)
            if matrix[EDITOR_INDEX][i] == 1:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score
        
        # 14. El Ingeniero usa MongoDB.
        try:
            i = matrix[PROFESSION_INDEX].index(2)
            if matrix[DATABASE_INDEX][i] == 1:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score

        # 15. EL desarrollador vive en la casa azul.
        try:
            i = matrix[PROFESSION_INDEX].index(4)
            if matrix[COLOR_INDEX][i] == 1:
                self.score += ok_score
            else:
                self.score += fail_score
        except:
            self.score += punish_score
        
class Riddle:

    def __init__(self):
        self.start_time = time.time()
        self.population = []

    '''
    proceso general
    '''
    def solve(self):
        
        print(f"Creando población con {len(self.population)} individuos")
        self.generateInitialPopulation()
        
        print("Inicio del proceso iterativo")
        indi = self.iterar()

        print("\n****\nFin del proceso, mejor resultado \n - Individuo", indi.chromosome, "\n")
        print("Parámetros \n-->",
                "POPULATION_LEN:", POPULATION_LEN,
                "PARENT_COUNT:", PARENT_COUNT ,
                "PARENT_TO_NEXT_GEN:", PARENT_TO_NEXT_GEN,
                "MUTATION_RATE:", MUTATION_RATE,
                "INDIVIDUAL_CROSSOVER_RATE:",INDIVIDUAL_CROSSOVER_RATE,
                "GENE_CROSSOVER_RATE:", GENE_CROSSOVER_RATE)
        print("\nSolución\n", indi.decode())
        
    def printStep(self, counter):
        print("")
        print("###")
        print("Paso ", counter)
        half = int(len(self.population)/2)
        average = sum(map(lambda x: x.score, self.population[half:]))/half
        print("Promedio: ", average)
        print("Mejor puntaje: ", self.population[len(self.population)-1].score)
        print("Peor puntaje para padre: ", self.population[len(self.population) - PARENT_COUNT].score)

    def getBatchCount(self, cpuCount):
        if FIXED_BATCH_COUNT != 0:
            return FIXED_BATCH_COUNT
        if FIXED_BATCH_SIZE != 0:
            return int(POPULATION_LEN/FIXED_BATCH_SIZE)
        return int(mp.cpu_count()*BATCH_COUNT_PER_CPU)

    def iterar(self):

        counter = 0
        break_condition = False

        pool = mp.Pool(mp.cpu_count())

        batch_count = self.getBatchCount(mp.cpu_count())
        batch_size = int((POPULATION_LEN - PARENT_TO_NEXT_GEN)/batch_count)

        while not(break_condition):
            # seleccion
            self.population.sort(key=lambda x: x.score)
            
            self.printStep(counter)

            pop_len = len(self.population)

            if(self.population[pop_len-1].score >= 14):
                break_condition = True
                return self.population[pop_len-1]
        
            # crossover
            parents = self.population[pop_len - PARENT_COUNT:]
            next_population = self.population[pop_len - PARENT_TO_NEXT_GEN:]
            

            child_lists = pool.starmap(self.crossover_parallel_batch, [(parents, batch_size) for i in range(batch_count)])

            for childs in child_lists:
                for child in childs:
                    next_population.append(child)

            self.population.clear()
            self.population = next_population
            
            # condicion de corte
            if counter > 1000:
                print("### Fin por condicion de corte ###")
                break_condition = True

            counter += 1
        
        pool.close()
        return self.population[0]

    def crossover_parallel_batch(self, parents, batch_size):
        next_population_batch = []

        parent_count = len(parents)

        while len(next_population_batch) < batch_size:
            if (len(next_population_batch) + parent_count) > batch_size:
                for progenitor in parents:
                    otherProgenitor = parents[random.randint(0, parent_count - 1)]
                    next_population_batch.append(self.crossOver(progenitor, otherProgenitor))
                    if len(next_population_batch) >= batch_size:
                        break
            else:
                for progenitor in parents:
                    otherProgenitor = parents[random.randint(0, parent_count - 1)]
                    next_population_batch.append(self.crossOver(progenitor, otherProgenitor))
        
        return next_population_batch

    '''
    operacion: generar individuos y agregarlos a la poblacion
    '''
    def generateInitialPopulation(self):
        for _ in range(POPULATION_LEN):
            newbie = Phenotype()
            newbie.generate()
            self.population.append(newbie)
    
    
    def crossOver(self, progenitor1, progenitor2):
        child = Phenotype()
        child.chromosome = progenitor1.chromosome.copy()

        if random.random() < INDIVIDUAL_CROSSOVER_RATE:
            child.chromosome = self._doCrossOver(child.chromosome, progenitor2.chromosome)

        if random.random() < MUTATION_RATE:
            child.mutate()

        child.fitness_function()

        return child

    def _doCrossOver(self, chromosome1, chromosome2):
        geneToCross = random.randint(0, 4)

        for characteristicToMutate in range(0, 5):
            if random.random() < GENE_CROSSOVER_RATE:
                valueToAdd = chromosome2[geneToCross+characteristicToMutate]
                valueToReplace = chromosome1[geneToCross+characteristicToMutate]
                for i in range(0,5):
                    if chromosome1[i*5+characteristicToMutate] == valueToAdd:
                        chromosome1[i*5+characteristicToMutate] = valueToReplace
                        break
                chromosome1[geneToCross+characteristicToMutate] = valueToAdd
        
        return chromosome1

random.seed(time.time_ns())
start = time.time()

rid = Riddle()
rid.solve()

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("\nTiempo transcurrido {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))