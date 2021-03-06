#-*- coding: utf-8 -*-
import tree_creation
from crossover import Crossover
from tree import Tree
from polish_notation import get_polish_notation, calculate_polish_notation, notation_to_str
from functions import TwoVariableFunction, Function
from reproduction import Reproductor
from random import choice, randint
from constants import MUTATION_PROBABILITY, POPULATION_NUMBER, TARGET_VALUES,\
    TREE_NUMBER, FOREST_NUMBER, ITERATIONS_COUNT, VARIABLE_VALUES_SET,\
    NODAL_MUTATION_PROBABILITY, TARGET_RESULT, CROSS_PROBABILITY, REPRODUCTION_PROBABILITY, ALLOWABLE_ERROR
from copy import deepcopy
from math import isinf


results = []


def generate_init_population():
    trees = []
    j = 0
    while j < TREE_NUMBER:
        depth = (j+1)/2 + 1 # (j+100)/100 + 1
        tree_creator = tree_creation.TreeCreator(depth)
        if j % 2 == 0:
            tree_creator.create(False)
        else:
            tree_creator.create(True)
        t = tree_creator.tree
        trees.append(Tree(t.init_tree, t.tree_map))
        print(Tree.tree_map_to_string(t.tree_map))
        print(t.init_tree)
        print("")
        j += 1
    return trees


def reproduce(trees):
    rep = Reproductor(trees)
    return list(rep.select())


def cross_trees(population):
    result_trees = []
    parent1 = choice(population)
    parent2 = choice(population)
    j = randint(1, CROSS_PROBABILITY)
    if j <= 9:
        cr = Crossover(parent1, parent2)
        if cr.cross():
            result_trees.append(cr.new_tree1)
            result_trees.append(cr.new_tree2)
    return result_trees


def mutate_trees(population):
    for individual in population:
        value = randint(1, NODAL_MUTATION_PROBABILITY)
        if value == 1:
            individual.mutate_from_term_to_term()
        else:
            value = randint(1, NODAL_MUTATION_PROBABILITY)
            if value == 1:
                individual.mutate_from_func_to_func()
            else:
                value = randint(1, MUTATION_PROBABILITY)
                if value == 1:
                    individual.mutate_from_func_to_term()
                else:
                    value = randint(1, MUTATION_PROBABILITY)
                    if value == 1:
                        individual.mutate_from_term_to_func()
    return population


def check_fitness(trees):
    errors = []
    for one_tree in trees:
        if len(one_tree.tree_map) == 0:
            continue
        sum_error = 0
        good_individual = True
        for i in range(0, len(VARIABLE_VALUES_SET)):
            error = Reproductor.get_error(one_tree, TARGET_VALUES[i], VARIABLE_VALUES_SET[i])
            if error > ALLOWABLE_ERROR:
                good_individual = False
            sum_error += error
        if isinf(sum_error):
            continue
        errors.append(sum_error)
        if good_individual or sum_error < TARGET_RESULT:
            print("RESULT")
            print(Tree.tree_map_to_string(one_tree.tree_map))
            print(one_tree.init_tree)
            one_tree.fitness = sum_error
            results.append(one_tree)
    print("MIN FITNESS RESULT: ", min(errors))
    print "AVERAGE FITNESS: ", sum(errors)/len(errors)
    print "length ", len(errors)
    print "results "
    for r in results:
        print "fitness ", r.fitness
        print Tree.tree_map_to_string(r.tree_map)


def create_new_generation(population):
    i = 0
    new_population = []
    while i < POPULATION_NUMBER:
        offspring = cross_trees(population)
        if len(offspring) > 0:
            new_population += offspring
            i += 2
        j = randint(1, REPRODUCTION_PROBABILITY)
        if j <= 2:
            new_population.append(choice(population))
            i += 1
    return new_population


def main():

    init_population = generate_init_population()
    result = False
    counter = 0

    while counter < ITERATIONS_COUNT:
        print("************************************************************************************************************"
              "************************************************************************************************************")
        print(counter)
        best_individuals = deepcopy(reproduce(init_population))

        if len(best_individuals) == 0:
            print("Reproduction empty")
            break

        new_generation = deepcopy(create_new_generation(best_individuals))
        mutated_trees = deepcopy(mutate_trees(new_generation))
        check_fitness(mutated_trees)
        init_population = deepcopy(mutated_trees)

        if len(init_population) == 0:
            print("Empty population")
            break
        counter += 1

    print("End")
    if len(results) > 0:
        print("")
        print "MIN RESULT"
        print Tree.tree_map_to_string(min(results))
        print min(results).init_tree
        print min(results).fitness


main()