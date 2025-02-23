import world
import config
import analysis
import plotting


# Initialize world using config variables
stage = world.World(
    size=config.WORLD_SIZE,
    num_trees=config.NUM_TREES,
    num_blobs=config.NUM_BLOBS,
    reproduction=config.REPRODUCTION_ENABLED
)

# Get gene distribution at start
initial_gene_distribution = stage.get_gene_distribution()
total_initial = len(stage.blobs)  # Total blobs at start

# Run the simulation
analysis.run_simulation(stage, years=config.YEARS)

# Get gene distribution at the end of the simulation
final_gene_distribution = stage.get_gene_distribution()
total_final = len(stage.blobs) # total at end

# Save and load results
df = analysis.save_results(stage)

# Extract death ages
death_ages = analysis.extract_death_ages(stage)

# Call plotting functions
plotting.plot_population(df)
#plotting.plot_death_histogram(death_ages)
plotting.plot_death_probability(death_ages)
plotting.plot_death_causes(df)  # New plot for deaths by cause

# Get gene distribution at the end of the simulation
final_gene_distribution = stage.get_gene_distribution()
# Call the plotting function
plotting.plot_gene_distribution(initial_gene_distribution, final_gene_distribution, total_initial, total_final)