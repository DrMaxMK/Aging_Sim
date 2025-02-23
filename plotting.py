import matplotlib.pyplot as plt
import numpy as np

def plot_population(df):
    """Plots the population breakdown over time."""
    plt.figure(figsize=(8, 5))

    plt.bar(df["year"], df["alive_original"], label="Alive Original", color="blue")
    plt.bar(df["year"], df["alive_newborns"], bottom=df["alive_original"], label="Alive Newborns", color="green")
    plt.bar(df["year"], df["cumulative_deaths"], bottom=df["alive"], label="Cumulative Dead", color="red")

    plt.xlabel("Year")
    plt.ylabel("Population Count")
    plt.title("Cumulative Population Over Time")
    plt.legend()
    plt.show()

def plot_death_histogram(death_ages):
    """Plots a histogram of ages at which blobs died."""
    plt.figure(figsize=(8, 5))
    plt.hist(death_ages, bins=20, edgecolor="black")
    plt.xlabel("Age at Death")
    plt.ylabel("Number of Blobs")
    plt.title("Histogram of Blob Death Ages")
    plt.show()

def plot_death_probability(death_ages):
    """Plots the probability of death at each age."""
    if death_ages:
        unique_ages, death_counts = np.unique(death_ages, return_counts=True)
        total_deaths = np.sum(death_counts)
        death_probabilities = death_counts / total_deaths  # Normalize

        plt.figure(figsize=(8, 5))
        plt.bar(unique_ages, death_probabilities, edgecolor="black")
        plt.xlabel("Age at Death")
        plt.ylabel("Probability of Death")
        plt.title("Normalized Death Probability by Age")
        plt.show()
    else:
        print("No deaths recorded, unable to generate probability plot.")

def plot_death_causes(df):
    """Plots a stacked bar chart of deaths due to starvation vs. old age."""
    plt.figure(figsize=(8, 5))

    plt.bar(df["year"], df["dead_from_starvation"], label="Death by Starvation", color="red")
    plt.bar(df["year"], df["dead_from_old_age"], bottom=df["dead_from_starvation"], label="Death by Old Age", color="orange")

    plt.xlabel("Year")
    plt.ylabel("Number of Deaths")
    plt.title("Deaths by Cause Over Time")
    plt.legend()
    plt.show()

def plot_gene_distribution(initial_genes, final_genes, total_initial, total_final):
    """Plots the normalized distribution of ON genes at the start vs. end of simulation."""
    import matplotlib.pyplot as plt
    import numpy as np

    genes = np.arange(len(initial_genes))  # Gene positions
    bar_width = 0.4  # Width of each bar

    # Avoid division by zero in case of edge cases
    initial_distribution = (initial_genes / total_initial * 100) if total_initial > 0 else np.zeros_like(initial_genes)
    final_distribution = (final_genes / total_final * 100) if total_final > 0 else np.zeros_like(final_genes)

    plt.figure(figsize=(8, 5))

    # Plot initial distribution (shifted left)
    plt.bar(genes - bar_width / 2, initial_distribution, width=bar_width, label="Initial Population", color="blue", alpha=0.7)

    # Plot final distribution (shifted right)
    plt.bar(genes + bar_width / 2, final_distribution, width=bar_width, label="Final Population", color="red", alpha=0.7)

    plt.xlabel("Gene Position")
    plt.ylabel("Percentage of Population with Gene ON (%)")
    plt.title("Normalized Gene ON Distribution Before vs. After Simulation")
    plt.xticks(genes)  # Ensure correct gene labels on x-axis
    plt.ylim(0, 100)  # Percentage scale
    plt.legend()
    plt.show()