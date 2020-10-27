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

colors =      ['red', 'blue', 'green', 'white', 'yellow']
prefession =  ['Mathematician', 'Hacker', 'Engineer', 'Analyst', 'Developer']
languaje =    ['Python', 'C#', 'Java', 'C++', 'JavaScript']
database =    ['Cassandra', 'MongoDB', 'HBase', 'Neo4j', 'Redis']
editor =      ['Brackets', 'Sublime Text', 'Vim', 'Atom', 'Notepad++']

COLOR_INDEX = 0
PROFESSION_INDEX = 1
LANGUAJE_INDEX = 2
DATABASE_INDEX = 3
EDITOR_INDEX = 4

#Parameters
POPULATION_LEN = 20000                  #Limite de población
PARENT_COUNT = 2800                     #Número de individuos (mejores) usados para generar la próxima generación
PARENT_TO_NEXT_GEN = 1400               #Número de individuos (mejores) que se transfieren a la siguiente generación
MAX_GENE_MUTATION = 20                  #Cantidad máxima de mutaciones en un individuo
MUTATION_RATE = 0.14                    #Probabilidad de que un gen mute
INDIVIDUAL_CROSSOVER_RATE = 0.5         #Probabilidad de que un individuo tenga 2 parents
GENE_CROSSOVER_RATE = 0.6               #Probabilidad de que se haga crossover para un gen

class Phenotype:

    def __init__(self):
        # crear un individuo
        self.chromosome = self.createRandomChromosome()
        self.fitness_function()

    def createRandomChromosome(self):
        h = 5
        geneMatrix = [[] for y in range(h)]

        chromosome = []
        for i in range(0,5):
            for j in range(0,5):
                randomValue = random.randint(0,4)

                while geneMatrix[i].count(randomValue) > 0:
                    randomValue = random.randint(0,4)
                
                geneMatrix[i].append(randomValue)

        for i in range(0,5):
            for j in range(0,5):
                chromosome.append(geneMatrix[j][i])
        
        return chromosome
    
    def decode(self):
        ''' traduce 0's y 1's (conjunto de genes: 3) en valores segun un diccionario '''
        return [[colors[self.chromosome[i*5+0]], 
                 prefession[self.chromosome[i*5+1]],
                 languaje[self.chromosome[i*5+2]],
                 database[self.chromosome[i*5+3]],
                 editor[self.chromosome[i*5+4]]] for i in range(5)]

    def mutate(self):
        ''' muta un fenotipo haciendo swap'''
        ''' se puede hacer esto porque cambié la función de inicialización de la población para que no contenga repetidos'''

        chromosome_change = 0
        for i in range(0, MAX_GENE_MUTATION):
            if random.random() < MUTATION_RATE:
                chromosome_change += 1
        
        while chromosome_change > 0:
            
            col = random.randint(0, 4) #Tipo de característica
            row1 = random.randint(0, 4) #Valor de la caracteristica 1
            row2 = random.randint(0, 4) #Valor de la caracteristica 2

            while row1 == row2:
                row2 = random.randint(0, 4)
        
            auxSwapValue = self.chromosome[row1*5+col]
            self.chromosome[row1*5+col] = self.chromosome[row2*5+col]
            self.chromosome[row2*5+col] = auxSwapValue
            
            chromosome_change -= 1
        
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
    def solve(self, n_population):
        
        self.generate(n_population)
        print(f"Poblacion creada con {len(self.population)} individuos")

        print("Inicio del proceso iterativo")
        indi = self.iterar()

        print(f"Fin del proceso, mejor resultado \n - Individuo {indi.chromosome} \n - Individuo {indi.decode()}")
        print("Parámetros. PARENT_COUNT:", PARENT_COUNT , "POPULATION_LEN ", POPULATION_LEN, "MAX_GENE_MUTATION ", MAX_GENE_MUTATION, "MUTATION_RATE ", MUTATION_RATE)
        
    def printStep(self, counter):
        print("")
        print("###")
        print("Paso ", counter)
        half = int(len(self.population)/2)
        average = sum(map(lambda x: x.score, self.population[half:]))/half
        print("Promedio ", average)
        print("Mejor puntaje ", self.population[len(self.population)-1].score)
        print("Mejor individuo ", self.population[len(self.population)-1].decode())
        print("--- ")
        print("Peor puntaje para padre", self.population[len(self.population) - PARENT_COUNT].score)
        print("Peor padre ", self.population[len(self.population) - PARENT_COUNT].decode())

    def iterar(self):

        counter = 0
        break_condition = False

        pool = mp.Pool(mp.cpu_count())

        batch_count = int(mp.cpu_count()/2)
        batch_size = int((POPULATION_LEN - PARENT_TO_NEXT_GEN)/batch_count)

        while not(break_condition):
            
            # seleccion
            self.population.sort(key=lambda x: x.score)
            
            self.printStep(counter)
            
            if(self.population[len(self.population)-1].score >= 14):
                break_condition = True
                return self.population[len(self.population)-1]
        
            # crossover
            parents = self.population[len(self.population) - PARENT_COUNT:]
            next_population = self.population[len(self.population) - PARENT_TO_NEXT_GEN:]
            

            child_lists = pool.starmap(self.crossover_parallel_batch, [(parents, batch_size) for i in range(batch_count)])

            for childs in child_lists:
                for child in childs:
                    next_population.append(child)

            self.population.clear()
            self.population = next_population
            
            
            # condicion de corte
            if counter > 20000:
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
                    next_population_batch.append(self.crossOver(progenitor))
        
        return next_population_batch

    '''
    operacion: generar individuos y agregarlos a la poblacion
    '''
    def generate(self, i):
        for x in range(0,i):
            newbie = Phenotype()
            self.population.append(newbie)
    
    
    def crossOver(self, progenitor1, progenitor2):
        child = Phenotype()
        child.chromosome = progenitor1.chromosome.copy()

        if random.random() < INDIVIDUAL_CROSSOVER_RATE:
            child.chromosome = self._doCrossOver(child.chromosome, progenitor2.chromosome)

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
rid.solve(n_population = POPULATION_LEN)

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Tiempo transcurrido {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))