import random

class QueenSolution:
    def __init__(self, board_size):
        self.board_size = board_size
        self.queen_positions = [random.randint(0, board_size - 1) for _ in range(board_size)]
        self.fitness_score = self.calculate_fitness()

    def calculate_fitness(self):
        safe_pairs = 0
        for i in range(self.board_size):
            for j in range(i + 1, self.board_size):
                if (self.queen_positions[i] != self.queen_positions[j] and 
                    abs(self.queen_positions[i] - self.queen_positions[j]) != abs(i - j)):
                    safe_pairs += 1
        return safe_pairs

class GeneticNQueensSolver:
    def __init__(self, board_size=8, population_size=100):
        self.board_size = board_size
        self.population_size = population_size
        self.population = [QueenSolution(board_size) for _ in range(population_size)]
        self.current_generation = 0

    def find_best_solution(self):
        return max(self.population, key=lambda x: x.fitness_score)

    def select_parents(self):
        tournament = random.sample(self.population, 3)
        return max(tournament, key=lambda x: x.fitness_score)

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, self.board_size - 1)
        child_positions = parent1.queen_positions[:crossover_point] + parent2.queen_positions[crossover_point:]
        child = QueenSolution(self.board_size)
        child.queen_positions = child_positions
        return child

    def mutate(self, solution):
       
        if random.random() < 0.2: 
            pos = random.randint(0, self.board_size - 1)
            solution.queen_positions[pos] = random.randint(0, self.board_size - 1)
            solution.fitness_score = solution.calculate_fitness()
        return solution

    def evolve_population(self):
        new_population = []
        
        
        new_population.append(self.find_best_solution())

        while len(new_population) < self.population_size:
            parent1 = self.select_parents()
            parent2 = self.select_parents()
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)

        self.population = new_population
        self.current_generation += 1

    def run(self, max_generations=1000):
        best_solution = self.find_best_solution()
        max_fitness = self.board_size * (self.board_size - 1) // 2

        print(f"Starting with best fitness: {best_solution.fitness_score}")

        while best_solution.fitness_score < max_fitness and self.current_generation < max_generations:
            self.evolve_population()
            best_solution = self.find_best_solution()
            
            if self.current_generation % 50 == 0:
                print(f"Generation {self.current_generation}, Best fitness: {best_solution.fitness_score}")

        if best_solution.fitness_score == max_fitness:
            print(f"\nSolution found in generation {self.current_generation}!")
            self.print_solution(best_solution)
        else:
            print("\nNo perfect solution found within the generation limit.")
            print("Best solution found:")
            self.print_solution(best_solution)

    def print_solution(self, solution):
        print("Queen positions (column per row):", solution.queen_positions)
        print("Chessboard representation:")
        for row in range(self.board_size):
            line = ["Q" if solution.queen_positions[row] == col else "." for col in range(self.board_size)]
            print(" ".join(line))

if __name__ == "__main__":
    solver = GeneticNQueensSolver(board_size=8, population_size=100)
    solver.run()