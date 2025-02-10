import os
from collections import defaultdict

def calculate_conservation_rate(codon_group):
    """
    Calculate the conservation rate for the first two nucleotides and the third nucleotide of codons in a group.
    """
    num_codons = len(codon_group)
    first_two_count = defaultdict(int)
    third_count = defaultdict(int)

    for codon in codon_group:
        if len(codon) == 3:  # Ensure valid codon length
            first_two_count[codon[:2]] += 1
            third_count[codon[2]] += 1

    # Calculate conservation rates
    first_two_conservation = max(first_two_count.values()) / num_codons if first_two_count else 0
    third_conservation = max(third_count.values()) / num_codons if third_count else 0

    return first_two_conservation, third_conservation

def process_files(input_dir, output_dir):
    """
    Process files in the input directory, calculate conservation rates, and write to the output directory.
    """
    for file_name in os.listdir(input_dir):
        if not file_name.endswith(".txt"):
            continue

        # Parse the file name to generate the output file name
        output_file_name = file_name
        output_file_path = os.path.join(output_dir, output_file_name)

        # Read and parse the file
        with open(os.path.join(input_dir, file_name), "r") as file:
            lines = file.readlines()

        species_dna_lengths = defaultdict(list)
        for i in range(0, len(lines), 3):
            species = lines[i].strip()
            dna_sequence = lines[i+1].strip()

            species_dna_lengths[len(dna_sequence)].append(dna_sequence)

        # Find the DNA length with the highest number of species
        most_common_length = max(species_dna_lengths.keys(), key=lambda x: len(species_dna_lengths[x]))
        dna_sequences = species_dna_lengths[most_common_length]

        # Separate DNA sequences into codons and organize into compare list
        compare = []
        max_codons = max(len(seq) // 3 for seq in dna_sequences)

        for i in range(max_codons):
            codon_group = []
            for seq in dna_sequences:
                codon_start = i * 3
                codon_end = codon_start + 3
                if codon_end <= len(seq):
                    codon_group.append(seq[codon_start:codon_end])
            compare.append(codon_group)

        # Calculate conservation rates for each codon group
        conservation = []
        for codon_group in compare:
            first_two_rate, third_rate = calculate_conservation_rate(codon_group)
            conservation.append((first_two_rate, third_rate))

        # Format the conservation rates for output
        conservation_str = ";".join(f"{first},{third}" for first, third in conservation)

        # Write to the output file
        with open(output_file_path, "w") as output_file:
            output_file.write(conservation_str + "\n")

# Define input and output directories
input_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/new_translated_conservation"
output_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/codon_conservation"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Process the files
process_files(input_directory, output_directory)
