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
import numpy as np
from datetime import datetime
import multiprocessing as mp
from multiprocessing import Process, Manager


colors =      {'001' : 'red',          '010' : 'blue',          '011' : 'green',    '100' : 'white',    '101' : 'yellow'}
prefession =  {'001' : 'Mathematician','010' : 'Hacker',        '011' : 'Engineer', '100' : 'Analyst',  '101' : 'Developer'}
languaje =    {'001' : 'Python',       '010' : 'C#',            '011' : 'Java',     '100' : 'C++',      '101' : 'JavaScript'}
database =    {'001' : 'Cassandra',    '010' : 'MongoDB',       '011' : 'HBase',    '100' : 'Neo4j',    '101' : 'Redis'}
editor =      {'001' : 'Brackets',     '010' : 'Sublime Text',  '011' : 'Vim',      '100' : 'Atom',     '101' : 'Notepad++'}

COLOR_INDEX = 0
PROFESSION_INDEX = 1
LANGUAJE_INDEX = 2
DATABASE_INDEX = 3
EDITOR_INDEX = 4

POPULATION_LEN = 20000

PARENTS_LEN = 1500
MAX_ITERATIONS = 20000

class Phenotype:

    def __init__(self):
        self.chromosome = []

    def decode(self):
        ''' traduce 0's y 1's (conjunto de genes: 3) en valores segun un diccionario '''
        return [[colors[self.chromosome[i*5+0]],
                 prefession[self.chromosome[i*5+1]],
                 languaje[self.chromosome[i*5+2]],
                 database[self.chromosome[i*5+3]],
                 editor[self.chromosome[i*5+4]]] for i in range(5)]

    def mutate(self):
        ''' muta un fenotipo, optimizado'''
        
        random_feature = random.randint(0,4)
    
        random_1 = random.randint(0, 4)
        random_2 = random.randint(0, 4)
        
        while random_1 == random_2:
            random_2 = random.randint(0, 4)
            
        chromosome_aux = self.chromosome[random_1*5+random_feature]
        self.chromosome[random_1*5+random_feature] = self.chromosome[random_2*5+random_feature]
        self.chromosome[random_2*5+random_feature] = chromosome_aux
    
        self.fitness_function()
       
    def fitness_function(self):
        ''' calcula el valor de fitness del cromosoma segun el problema en particular '''

        self.score = 0
        self.fails = []

        ok_score = 1
        fail_score = -1
        punish_score = -3

        matrix = [[0 for x in range(5)] for x in range(5)]
        chromosome_decode = self.decode()

        for i in range(0, 5):
            for j in range(0, 5):
                matrix[i][j] = chromosome_decode[j][i]

        for i in range(0, 5):
            for j in range(0, 5):
                if matrix[i].count(matrix[i][j]) >= 2 :
                    self.score -= 2
                    
        # 2. El Matematico vive en la casa roja.
        try:
            i = matrix[PROFESSION_INDEX].index('Mathematician')
            if matrix[COLOR_INDEX][i] == 'red':
                self.score += ok_score
            else:
                self.fails.append(2)
                self.score += fail_score
        except:
            self.fails.append(2)
            self.score += punish_score

        # 3. El hacker programa en Python
        try:
            i = matrix[PROFESSION_INDEX].index('Hacker')
            if matrix[LANGUAJE_INDEX][i] == 'Python':
                self.score += ok_score
            else:
                self.fails.append(3)
                self.score += fail_score
        except:
            self.fails.append(3)
            self.score += punish_score

        # 4. El Brackets es utilizado en la casa verde.
        try:
            i = matrix[EDITOR_INDEX].index('Brackets')
            if matrix[COLOR_INDEX][i] == 'green':
                self.score += ok_score
            else:
                self.fails.append(4)
                self.score += fail_score
        except:
            self.fails.append(4)
            self.score += punish_score

        # 5. El analista usa Atom.
        try:
            i = matrix[PROFESSION_INDEX].index('Analyst')
            if matrix[EDITOR_INDEX][i] == 'Atom':
                self.score += ok_score
            else:
                self.score += fail_score
                self.fails.append(5)
        except:
            self.score += punish_score
            self.fails.append(5)

        # 6. La casa verde esta a la derecha de la casa blanca.
        try:
            i = matrix[COLOR_INDEX].index('green')
            if i != 0 and matrix[COLOR_INDEX][i-1] == 'white':
                self.score += ok_score
            else:
                self.fails.append(6)
                self.score += fail_score
        except:
            self.fails.append(6)
            self.score += punish_score

        # 7. La persona que usa Redis programa en Java
        try:
            i = matrix[DATABASE_INDEX].index('Redis')
            if matrix[LANGUAJE_INDEX][i] == 'Java':
                self.score += ok_score
            else:
                self.score += fail_score
                self.fails.append(7)
        except:
            self.score += punish_score
            self.fails.append(7)

        # 8. Cassandra es utilizado en la casa amarilla
        try:
            i = matrix[DATABASE_INDEX].index('Cassandra')
            if matrix[COLOR_INDEX][i] == 'yellow':
                self.score += ok_score
            else:
                self.score += fail_score
                self.fails.append(8)
        except:
            self.score += punish_score
            self.fails.append(8)

        # 9. Notepad++ es usado en la casa del medio.
        try:
            i = matrix[EDITOR_INDEX].index('Notepad++')
            if i == 2:
                self.score += ok_score
            else:
                self.score += fail_score
                self.fails.append(9)
        except:
            self.score += punish_score
            self.fails.append(9)

        # 10. El Desarrollador vive en la primer casa.
        try:
            i = matrix[PROFESSION_INDEX].index('Developer')
            if i == 0:
                self.score += ok_score
            else:
                self.score += fail_score
                self.fails.append(10)
        except:
            self.score += punish_score
            self.fails.append(10)

        # 11. La persona que usa HBase vive al lado de la que programa en JavaScript.
        try:
            i = matrix[DATABASE_INDEX].index('HBase')
            if (i != 4 and matrix[LANGUAJE_INDEX][i+1] == 'JavaScript') or (i != 0 and matrix[LANGUAJE_INDEX][i-1] == 'JavaScript'):
                self.score += ok_score
            else:
                self.score += fail_score
                self.fails.append(11)
        except:
            self.score += punish_score
            self.fails.append(11)

        # 12. La persona que usa Cassandra es vecina de la que programa en C#.
        try:
            i = matrix[DATABASE_INDEX].index('Cassandra')
            if (i != 4 and matrix[LANGUAJE_INDEX][i+1] == 'C#') or (i != 0 and matrix[LANGUAJE_INDEX][i-1] == 'C#'):
                self.score += ok_score
            else:
                self.score += fail_score
                self.fails.append(12)
        except:
            self.score += punish_score
            self.fails.append(12)

        # 13. La persona que usa Neo4J usa Sublime Text.
        try:
            i = matrix[DATABASE_INDEX].index('Neo4j')
            if matrix[EDITOR_INDEX][i] == 'Sublime Text':
                self.score += ok_score
            else:
                self.score += fail_score
                self.fails.append(13)
        except:
            self.fails.append(13)
            self.score += punish_score

        # 14. El Ingeniero usa MongoDB.
        try:
            i = matrix[PROFESSION_INDEX].index('Engineer')
            if matrix[DATABASE_INDEX][i] == 'MongoDB':
                self.score += ok_score
            else:
                self.score += fail_score
                self.fails.append(14)
        except:
            self.score += punish_score
            self.fails.append(14)

        # 15. EL desarrollador vive en la casa azul.
        try:
            i = matrix[PROFESSION_INDEX].index('Developer')
            if matrix[COLOR_INDEX][i] == 'blue':
                self.score += ok_score
            else:
                self.score += fail_score
                self.fails.append(15)
        except:
            self.score += punish_score
            self.fails.append(15)

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
        fit, indi = self.iterar()

        print(f"Fin del proceso, mejor resultado \n - Fitness: {fit} \n - Individuo {indi.chromosome} \n - Individuo {indi.decode()}")

    def printStep(self, counter):
        print("")
        print("###")
        print("Paso ", counter)

        # DEBUG
        # print(id(self.population[0]))
        print("Puntaje:", self.population[0].score)
        print("Fallo:", self.population[0].fails)
        for i in range(0, 5):
            print('Mejor: ', self.population[0].decode()[i])

    def iterar(self):

        counter = 0
        break_condition = False

        pool = mp.Pool(mp.cpu_count())
        
        while not(break_condition):

            # seleccion
            self.population.sort(key=lambda x: x.score, reverse=True)

            self.printStep(counter)

            if(self.population[0].score >= 14):
                break_condition = True
                return self.population[0].score, self.population[0]
            
            parents = self.population[0:PARENTS_LEN]
            random.shuffle(parents)

            next_population = self.cross_over(parents)
            
            # nueva poblacion
            self.population = next_population

            # condicion de corte
            if counter > MAX_ITERATIONS:
                print("### Fin por condicion de corte ###")
                break_condition = True

            counter += 1

        return self.population[0].approves, self.population[0]

    def cross_over(self, parents):
        next_population = []
        
        while(len(next_population) < POPULATION_LEN):
                ran_parent1 = random.randint(0, len(parents)-1)
                ran_parent2 = random.randint(0, len(parents)-1)

                while(ran_parent1 == ran_parent2):
                    ran_parent2 = random.randint(0, len(parents)-1)

                parent_1 = parents[ran_parent1]
                parent_2 = parents[ran_parent2]
                
                child1, child2 = self.crossOver(parent_1, parent_2)
                
                child2.fitness_function()
                child1.fitness_function()
                self.mutate(child1)
                self.mutate(child2)
                next_population.append(child1)
                next_population.append(child2)
                
        return next_population
                
    '''
    operacion: generar individuos y agregarlos a la poblacion
    '''

    def generate(self, i):
        for _ in range(0, i):
            newbie = Phenotype()
            newbie.chromosome = self.createRandomChromosome()
            newbie.fitness_function()
            self.population.append(newbie)
    
    def createRandomChromosome(self):
        colors =      ['001','010','011','100','101']
        prefession =  ['001','010','011','100','101']
        languaje =    ['001','010','011','100','101']
        database =    ['001','010','011','100','101']
        editor =      ['001','010','011','100','101']
        
        newbie = Phenotype()
        
        for _ in range(0, 5):
                random_c = random.randint(0, len(colors)-1)
                newbie.chromosome.append(colors[random_c])
                del colors[random_c]
                
                random_p = random.randint(0, len(prefession)-1)
                newbie.chromosome.append(prefession[random_p])
                del prefession[random_p]
                
                random_c = random.randint(0, len(languaje)-1)
                newbie.chromosome.append(languaje[random_c])
                del languaje[random_c]
                
                random_c = random.randint(0, len(database)-1)
                newbie.chromosome.append(database[random_c])
                del database[random_c]
                
                random_c = random.randint(0, len(editor)-1)
                newbie.chromosome.append(editor[random_c])
                del editor[random_c]
        
        return newbie.chromosome
    
    '''
    operacion: mutación. Cambiar la configuración fenotipica de un individuo
    '''

    def mutate(self, crossed):
        if (random.random() >= 0.60):
            crossed.mutate()
            
        crossed.fitness_function()

    '''
    operacion: cruazamiento. Intercambio de razos fenotipicos entre individuos
    '''

    def crossOver(self, progenitor_1, progenitor_2):
        child_1 = Phenotype()
        child_2 = Phenotype()
        
        child_1.chromosome = progenitor_1.chromosome.copy()
        child_2.chromosome = progenitor_2.chromosome.copy()
        child_1.fitness_function()
        child_2.fitness_function()
        
        return child_1, child_2

random.seed(time.time_ns())
start = time.time()

rid = Riddle()
rid.solve(n_population=POPULATION_LEN)

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Tiempo transcurrido {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))