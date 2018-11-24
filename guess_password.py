import random
import string
import datetime
import unittest
import genetic


def get_fitness(genes, target):
    return sum(1 for expected, actual in zip(target, genes)
               if expected == actual)


def display_fitness(organism, start_time):
    time_elapsed = datetime.datetime.now() - start_time
    print(f"Organism: {''.join(organism.Genes)}\t"
          f"Fitness: {organism.Fitness}\t"
          f"Time Elapsed: {str(time_elapsed)}")


class GuessPasswordTests(unittest.TestCase):
    gene_pool = string.ascii_lowercase + string.ascii_uppercase + " !.,"

    def guess_password(self, target):
        start_time = datetime.datetime.now()

        def runGetFitness(genes):
            return get_fitness(genes, target)

        def runDisplayFitness(candidate):
            display_fitness(candidate, start_time)

        optimal_fitness = len(target)
        best = genetic.get_best(runGetFitness, len(target), optimal_fitness,
                                self.gene_pool, runDisplayFitness)
        self.assertEqual(''.join(best.Genes), target)

    def test_Hello_World(self):
        print("\nInitiating Hello World Unit Test")
        target = "Hello World!"
        self.guess_password(target)

    def test_extremely_complex_password(self):
        print("\nInitiating Extremely Complex Password Unit Test")
        target = "ExtreMEly ComplEX PasSwoRd!..."
        self.guess_password(target)

    def test_Random(self):
        print("\nInitiating Long Password Unit Test")
        length = 150
        target = ''.join(random.choice(self.gene_pool)
                         for _ in range(length))

        self.guess_password(target)

    def test_benchmark(self):
        print("\nInitiating Benchmark Test")
        genetic.Benchmark.run(self.test_Random)


if __name__ == '__main__':
    unittest.main()
