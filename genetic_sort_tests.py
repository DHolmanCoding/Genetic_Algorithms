import datetime
import unittest
import genetic_b


def get_fitness(genes):
    fitness = 1
    gap = 0

    for i in range(1, len(genes)):
        if genes[i] > genes[i - 1]:
            fitness += 1
        else:
            gap += genes[i - 1] - genes[i]
    return Fitness(fitness, gap)


def display(candidate, start_time):
    time_elapsed = datetime.datetime.now() - start_time
    print("{}\t=> {}\t{}".format(
        ', '.join(map(str, candidate.Genes)),
        candidate.Fitness,
        time_elapsed))


class SortedNumbersTests(unittest.TestCase):
    def test_sort_10_numbers(self):
        self.sort_numbers(10)

    def sort_numbers(self, total_numbers):
        gene_pool = [i for i in range(100)]
        time_elapsed = datetime.datetime.now()

        def runDisplay(candidate):
            display(candidate, time_elapsed)

        def runGetFitness(genes):
            return get_fitness(genes)

        optimal_fitness = Fitness(total_numbers, 0)
        best = genetic_b.get_best(runGetFitness, total_numbers, optimal_fitness,
                                  gene_pool, runDisplay)
        self.assertTrue(not optimal_fitness > best.Fitness)

    def test_benchmark(self):
        genetic_b.Benchmark.run(lambda: self.sort_numbers(40))


class Fitness:
    def __init__(self, numbers_in_sequence_ct, total_gap):
        self.NumbersInSequenceCount = numbers_in_sequence_ct
        self.TotalGap = total_gap

    def __gt__(self, other):
        if self.NumbersInSequenceCount != other.NumbersInSequenceCount:
            return self.NumbersInSequenceCount > other.NumbersInSequenceCount
        return self.TotalGap < other.TotalGap

    def __str__(self):
        return "{} Sequential, {} Total Gap".format(
            self.NumbersInSequenceCount,
            self.TotalGap)


if __name__ == '__main__':
    unittest.main()
