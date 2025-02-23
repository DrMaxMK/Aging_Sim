import numpy as np
import random
import config

class Tree:
    """A tree that grows apples over time."""
    
    def __init__(self):
        self.has_apple = False  # Starts empty

    def grow_apples(self):
        """Randomly grows an apple with a x% chance per cycle."""
        if not self.has_apple:
            self.has_apple = random.random() < config.APPLE_GROW_PROBABILITY


class Blob:
    """A blob that moves, eats, ages, and has a gene for old-age death."""
    
    def __init__(self, world_size, energy = 10):
        self.x = random.randint(0, world_size - 1)
        self.y = random.randint(0, world_size - 1) 
        self.age = 0  
        self.energy = energy
        self.last_birth_year = -5  # Cooldown for reproduction
        self.has_old_age_gene = False  # 2% chance to die after 50
        # chromosome with on and off genes
        self.chromosome = np.random.choice([0, 1], size=config.NUM_GENES, p=[0.5, 0.5])

    def move(self, world_size):
        """Move the blob randomly in one of four directions."""
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.x = np.clip(self.x + dx, 0, world_size - 1)
        self.y = np.clip(self.y + dy, 0, world_size - 1)

    def eat(self, world):
        """Eats an apple from a tree if available, gaining energy."""
        if isinstance(world.grid[self.x, self.y], Tree) and world.grid[self.x, self.y].has_apple:
            world.grid[self.x, self.y].has_apple = False
            self.energy += 3  

    def step(self, world):
        """Blob takes one step: move, eat, lose energy, age, and possibly die."""
        self.move(world.size)
        self.eat(world)
        self.energy -= config.ENERGY_LOSS_PER_STEP
        self.age += 1  

        # Check for starvation death
        if self.energy <= 0:
            return "starvation"
        
        # Aging Death: Check each gene's probability
        # Gene 1 kills after 10 years, gene 2 after 2 years
        # Gene 0 is control gene
        for gene_index in range(1, config.NUM_GENES):
            if self.chromosome[gene_index] == 1 and self.age >= config.AGING_THRESHOLDS[gene_index]:
                if np.random.rand() < config.BASE_DEATH_PROBABILITY: #kill with p per year
                    return "old_age"

        return "alive"
    
    def can_reproduce(self, other_blob, current_year):
        """Checks if two blobs can reproduce."""
        birth_cooldown = config.REPRODUCTION_COOLDOWN
        if self.age >= config.REPRODUCTION_MIN_AGE and other_blob.age >= config.REPRODUCTION_MIN_AGE:
            dist = abs(self.x - other_blob.x) + abs(self.y - other_blob.y)
            if (dist <= config.REPRODUCTION_MAX_DISTANCE):
                cooldown_self = self.last_birth_year + birth_cooldown  # Cooldown for this blob
                cooldown_other = other_blob.last_birth_year + birth_cooldown
                if current_year >= cooldown_self and current_year >= cooldown_other:
                    return True
        return False
    
    def reproduce(self, other_blob, world_size):
        """Creates a child blob with 50% genes from each parent."""
        child = Blob(world_size, energy=config.BIRTH_ENERGY)

        # Each gene has a 50% chance of coming from either parent
        for i in range(len(self.chromosome)):
            child.chromosome[i] = np.random.choice([self.chromosome[i], other_blob.chromosome[i]])

        # Child starts at (parent's location) with age 0
        child.x, child.y = self.x, self.y
        child.age = 0 #unneccessary but for safety
        return child


class World:
    """A world containing trees and blobs."""
    def __init__(self, size=config.WORLD_SIZE, num_trees=config.NUM_TREES, num_blobs=config.NUM_BLOBS, reproduction=config.REPRODUCTION_ENABLED):
        self.size = size
        self.grid = np.full((size, size), None)  # Empty world
        self.blobs = [Blob(size) for _ in range(num_blobs)]
        self.reproduction = reproduction # can turn on and off
        self.trees = []
        self.stats = [] # Store yearly stats
        self.total_births = 0  # Track cumulative births
        self.plant_trees(num_trees)

    def plant_trees(self, num_trees):
        """Randomly places trees in the world."""
        for _ in range(num_trees):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.grid[x, y] = Tree()
            self.trees.append(self.grid[x, y])

    def grow_apples(self):
        """All trees attempt to grow apples."""
        for tree in self.trees:
            tree.grow_apples()

    def get_gene_distribution(self):
        """Returns the count of ON (1) and OFF (0) genes for each position."""
        gene_matrix = np.array([blob.chromosome for blob in self.blobs])
        gene_counts = np.sum(gene_matrix, axis=0)  # Count how many are ON (1) per gene
        return gene_counts

    def reproduce_blobs(self, year):
        """Allow eligible blobs to reproduce if reproduction is enabled."""
        if not self.reproduction:
            return []

        new_blobs = []
        for i in range(len(self.blobs)):
            for j in range(i + 1, len(self.blobs)):  # Check each pair once
                if self.blobs[i].can_reproduce(self.blobs[j], year):
                    # Spawn a child with inherited genes
                    baby = self.blobs[i].reproduce(self.blobs[j], self.size)
                    new_blobs.append(baby)

                    # Update reproduction cooldown for parents
                    self.blobs[i].last_birth_year = year
                    self.blobs[j].last_birth_year = year

        self.total_births += len(new_blobs)  # Update cumulative births
        return new_blobs

    def step(self, year):
        """Advance the world by one step and record statistics."""
        self.grow_apples()

        alive_before = len(self.blobs)  # Count blobs before step
        dead_from_starvation = []
        dead_from_old_age = []
        alive_blobs = []
        
        for blob in self.blobs:
            death_reason = blob.step(self)
            if death_reason == "starvation":
                dead_from_starvation.append(blob)
            elif death_reason == "old_age":
                dead_from_old_age.append(blob)
            else:
                alive_blobs.append(blob)

        # Update blobs list
        self.blobs = alive_blobs

        # Handle reproduction (if enabled)
        new_births = self.reproduce_blobs(year)
        self.blobs.extend(new_births)

        # Compute statistics
        dead_starvation_count = len(dead_from_starvation)
        dead_old_age_count = len(dead_from_old_age)
        alive_count = len(self.blobs)

        avg_age_alive = np.mean([blob.age for blob in alive_blobs]) if alive_blobs else 0
        avg_age_dead_starvation = np.mean([blob.age for blob in dead_from_starvation]) if dead_from_starvation else 0
        avg_age_dead_old_age = np.mean([blob.age for blob in dead_from_old_age]) if dead_from_old_age else 0

        # Collect death ages
        death_ages = [blob.age for blob in dead_from_starvation + dead_from_old_age]

        # Calculate cumulative deaths
        previous_deaths = self.stats[-1]["cumulative_deaths"] if self.stats else 0
        cumulative_deaths = previous_deaths + dead_starvation_count + dead_old_age_count

        # Track original and newbown population part of whole population
        alive_original = sum(1 for blob in self.blobs if blob.age == year+1)
        alive_newborns = sum(1 for blob in self.blobs if blob.age < year+1)
        print("Alive original: ", alive_original, " and alive new: ", alive_newborns)
        # Store stats
        stats_entry = {
            "year": year,
            "alive": alive_count,
            "alive_original": alive_original,
            "alive_newborns": alive_newborns,
            "dead_from_starvation": dead_starvation_count,
            "dead_from_old_age": dead_old_age_count,
            "cumulative_deaths": cumulative_deaths,
            "born_this_year": len(new_births),
            "cumulative_births": self.total_births,
            "avg_age_alive": avg_age_alive,
            "avg_age_dead_starvation": avg_age_dead_starvation,
            "avg_age_dead_old_age": avg_age_dead_old_age,
            "death_ages": death_ages
        }
        
        self.stats.append(stats_entry)

        # Debugging Print
        #print(f"Year {year} | Alive: {alive_count} | Dead: {dead_count} | Avg Age Alive: {avg_age_alive} | Avg Age Dead: {avg_age_dead}")

    def get_stats(self):
        """Return the collected simulation statistics."""
        return self.stats