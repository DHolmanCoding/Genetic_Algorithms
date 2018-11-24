import datetime
import unittest
import genetic_a


def get_fitness(genes):
    return genes.count(1)


def display(candidate, start_time):
    time_elapsed = datetime.datetime.now() - start_time
    print("{}...{}\tFitness: {:3.2f}\tTime Elapsed: {}".format(''.join(map(str, candidate.Genes[:15])),
                                                               ''.join(map(str, candidate.Genes[-15:])),
                                                               candidate.Fitness,
                                                               time_elapsed))


class OneMaxTests(unittest.TestCase):
    def test(self, length=100):
        gene_pool = [0, 1]
        start_time = datetime.datetime.now()

        def runDisplayFitness(candidate):
            display(candidate, start_time)

        def runGetFitness(genes):
            return get_fitness(genes)

        optimal_fitness = length
        best = genetic_a.get_best(runGetFitness, length, optimal_fitness,
                                  gene_pool, runDisplayFitness)
        self.assertEqual(best.Fitness, optimal_fitness)

    def test_benchmark(self):
        genetic_a.Benchmark.run(lambda: self.test(4000))


if __name__ == '__main__':
    unittest.main()
