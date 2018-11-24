import random
import statistics
import sys
import time


def _generate_parent(length, gene_pool, get_fitness):
    genes = []
    while len(genes) < length:
        sample_size = min(length - len(genes), len(gene_pool))
        genes.extend(random.sample(gene_pool, sample_size))
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)


def _mutate(parent, gene_pool, get_fitness):
    offspring_genes = parent.Genes[:]
    index = random.randrange(0, len(parent.Genes))
    newGene, alternate = random.sample(gene_pool, 2)
    offspring_genes[index] = alternate if newGene == offspring_genes[index] else newGene
    fitness = get_fitness(offspring_genes)
    return Chromosome(offspring_genes, fitness)


def get_best(get_fitness, target_len, optimal_fitness, gene_pool, display):
    random.seed()

    def runMutate(parent):
        return _mutate(parent, gene_pool, get_fitness)

    def runGenerateParent():
        return _generate_parent(target_len, gene_pool, get_fitness)

    for improvement in _get_improvement(runMutate, runGenerateParent):
        display(improvement)
        if not optimal_fitness > improvement.Fitness:
            return improvement


def _get_improvement(new_child, generate_parent):
    best_offspring = generate_parent()
    yield best_offspring
    while True:
        child = new_child(best_offspring)
        if best_offspring.Fitness > child.Fitness:
            continue
        if not child.Fitness > best_offspring.Fitness:
            best_offspring = child
            continue
        yield child
        best_offspring = child


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
                print("{} {:3.2f} {:3.2f}".format(
                    1 + i, mean,
                    statistics.stdev(timings, mean) if i > 1 else 0))
