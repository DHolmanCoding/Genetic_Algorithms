import random
import statistics
import sys
import time


def _generate_parent(target_length, gene_pool, get_fitness):
    genes = []
    while len(genes) < target_length:
        sample_size = min(target_length - len(genes), len(gene_pool))
        genes.extend(random.sample(gene_pool, sample_size))
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)


def _generate_offspring(parent, gene_pool, get_fitness):
    index = random.randrange(0, len(parent.Genes))
    offspring_genes = parent.Genes[:]
    new_gene, alternate = random.sample(gene_pool, 2)
    offspring_genes[index] = alternate if new_gene == offspring_genes[index] else new_gene
    fitness = get_fitness(offspring_genes)
    return Chromosome(offspring_genes, fitness)


def get_best(get_fitness, target_len, optimal_fitness, gene_pool, display):
    random.seed()
    best_parent = _generate_parent(target_len, gene_pool, get_fitness)
    display(best_parent)
    if best_parent.Fitness >= optimal_fitness:
        return best_parent
    while True:
        offspring = _generate_offspring(best_parent, gene_pool, get_fitness)
        if best_parent.Fitness >= offspring.Fitness:
            continue
        display(offspring)
        if offspring.Fitness >= optimal_fitness:
            return offspring
        best_parent = offspring


class Chromosome:
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness


class Benchmark:
    @staticmethod
    def run(fx):
        timings = []
        stdout = sys.stdout
        for i in range(100):
            sys.stdout = None
            start_time = time.time()
            fx()
            seconds = time.time() - start_time
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print("Trial {}:\t"
                      "Mean runtime: {:3.2f} seconds\t"
                      "Cumulative std. dev.: {:3.2f} seconds".format(1 + i,
                                                                     mean,
                                                                     statistics.stdev(timings, mean)
                                                                     if i > 1 else 0)
                      )
