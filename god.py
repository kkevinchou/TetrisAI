import heapq
import random
import time
from tetris import Tetris
from multiprocessing import Process, Queue

def breed(a_trait_set, b_trait_set):
    return [(a_trait_set[i] + b_trait_set[i]) / float(2) for i in range(len(a_trait_set))]

def generate_next_generation_trait_sets(trait_sets, trait_set_results):
    population_size = len(trait_sets)
    num_dominant_trait_sets = population_size / 2

    alpha_trait_set_index = heapq.nlargest(1, trait_set_results, key=trait_set_results.get)[0]
    dominant_trait_set_indexes = heapq.nlargest(num_dominant_trait_sets, trait_set_results, key=trait_set_results.get)

    next_generation_trait_sets = []
    already_paired = {}

    for i in range(len(dominant_trait_set_indexes)):
        if i == alpha_trait_set_index:
            continue

        next_generation_trait_sets.append(breed(trait_sets[i], trait_sets[alpha_trait_set_index]))
        already_paired['{}_{}'.format(i, alpha_trait_set_index)] = True
        already_paired['{}_{}'.format(alpha_trait_set_index, i)] = True

    while len(next_generation_trait_sets) < population_size:
        a_index = random.randint(0, population_size - 1)
        b_index = random.randint(0, population_size - 1)

        if a_index == b_index:
            continue

        if already_paired.get('{}_{}'.format(a_index, b_index)):
            continue

        a_trait_set = trait_sets[a_index]
        b_trait_set = trait_sets[b_index]

        next_generation_trait_sets.append(breed(a_trait_set, b_trait_set))
        already_paired['{}_{}'.format(a_index, b_index)] = True
        already_paired['{}_{}'.format(b_index, a_index)] = True

    return next_generation_trait_sets


def main():
    num_generations = 20
    population_size = 16
    process_map = [None] * population_size
    process_results = {}
    result_queue = Queue()
    trait_sets = [None] * population_size

    if population_size <= 2:
        print 'POPULATION SIZE MUST BE > 2'

    for i in range(population_size):
        trait_sets[i] = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]
        # trait_sets[i] = [4, -4, 3.5, -10]

    for generation in range(num_generations):
        seed = time.time()
        for i in range(population_size):
            process_map[i] = Process(target=Tetris.main, args=[seed, i, result_queue, trait_sets[i]])
            process_map[i].start()

        for process in process_map:
            process.join()

        trait_set_results = {}

        while not result_queue.empty():
            _id, num_updates = result_queue.get()
            trait_set_results[_id] = num_updates

        # trait_set_results[0] = 12
        # trait_set_results[1] = 5
        # trait_set_results[2] = 16

        print 'GENERATION RESULTS:'

        sorted_trait_set_indexes = sorted(trait_set_results.keys(), key=trait_set_results.get, reverse=True)
        for i in range(len(sorted_trait_set_indexes)):
            index = sorted_trait_set_indexes[i]
            print '{}: {}'.format(trait_sets[index], trait_set_results[index])

        trait_sets = generate_next_generation_trait_sets(trait_sets, trait_set_results)

    # sorted_trait_set_indexes = sorted(trait_set_results.keys(), key=trait_set_results.get, reverse=True)
    # print sorted_trait_set_indexes

    # print 'Final Trait Sets:'
    # for i in range(len(sorted_trait_set_indexes)):
    #     index = sorted_trait_set_indexes[i]
    #     print '{}: {}'.format(trait_sets[index], trait_set_results[index])

if __name__ == '__main__':
    main()
