# General simulation settings
WORLD_SIZE = 900
NUM_TREES = 400000
NUM_BLOBS = 900
YEARS = 200
REPRODUCTION_ENABLED = True

# Energy settings
INITIAL_ENERGY = 10
ENERGY_GAIN_FROM_APPLE = 3
ENERGY_LOSS_PER_STEP = 1

# Aging and Genetics
NUM_GENES = 10  # Number of genes per blob
BASE_DEATH_PROBABILITY = 0.02  # 2% chance per year if gene is active
AGING_THRESHOLDS = [i * 10 for i in range(NUM_GENES)]  # Gene 1 from 10, gene 2 from 20, etc.

# Reproduction settings
BIRTH_ENERGY = 10  # New blobs start with this energy
REPRODUCTION_COOLDOWN = 3  # Min and max years before a blob can reproduce again
REPRODUCTION_MIN_AGE = 15
REPRODUCTION_MAX_DISTANCE = 2

# World Setting
APPLE_GROW_PROBABILITY = 0.2
