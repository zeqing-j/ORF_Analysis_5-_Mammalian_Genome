import os

def calculate_base_percentage(sequence):
    """
    Calculate the percentage of total bases (A, C, T, G) in the sequence
    relative to the total length of the alignment (including dashes).
    """
    total_length = len(sequence)  # Total length including dashes
    base_count = sum(sequence.count(base) for base in 'ACTG')  # Total number of bases (A, C, T, G)

    # Calculate the percentage of bases in the alignment
    base_percentage = (base_count / total_length) * 100 if total_length > 0 else 0
    return base_percentage

def within_threshold(human_percentage, other_percentage, threshold=5):
    """
    Check if the base percentage of other species is within 5% of the human alignment.
    """
    return abs(human_percentage - other_percentage) <= threshold

def remove_common_dashes(alignments, species):
    """
    Remove common dashes from all alignments at the same positions, and also remove
    the alignment and its species if it's the only sequence with a base at that position.
    """
    alignment_length = len(alignments[0])
    to_remove = set()

    # Identify positions to keep (where not all alignments are dashes)
    keep_positions = []
    for i in range(alignment_length):
        non_dash_count = sum(align[i] != '-' for align in alignments)
        if non_dash_count > 1:
            keep_positions.append(i)
        elif non_dash_count == 1:
            # Mark the species/alignment with a base at this position for removal
            for j, align in enumerate(alignments):
                if align[i] != '-':
                    to_remove.add(j)

    # Remove the marked species and their alignments
    filtered_species = [sp for idx, sp in enumerate(species) if idx not in to_remove]
    filtered_alignments = [''.join(align[i] for i in keep_positions) for idx, align in enumerate(alignments) if idx not in to_remove]

    return filtered_species, filtered_alignments

def process_alignment_file(input_file, output_file):
    """
    Process the alignment file, filter alignments based on base percentage, and
    remove common dashes and alignments with unique non-dash characters. Write
    the cleaned alignments to the output file.
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Split the lines into species and alignment
    species = []
    alignments = []

    for i in range(0, len(lines), 2):
        species.append(lines[i].strip())
        alignments.append(lines[i+1].strip())

    # Calculate the human alignment percentage
    human_percentage = calculate_base_percentage(alignments[0])

    # Filter out species whose base percentage differs more than 5% from the human sequence
    filtered_species = [species[0]]
    filtered_alignments = [alignments[0]]
    for i in range(1, len(species)):
        other_percentage = calculate_base_percentage(alignments[i])
        if within_threshold(human_percentage, other_percentage):
            filtered_species.append(species[i])
            filtered_alignments.append(alignments[i])

    # Remove common dashes and any alignment with a unique non-dash character
    final_species, final_alignments = remove_common_dashes(filtered_alignments, filtered_species)

    # Write the output to a new file
    with open(output_file, 'w') as f:
        for i in range(len(final_species)):
            f.write(final_species[i] + '\n')
            f.write(final_alignments[i] + '\n')

def process_all_files(input_dir, output_dir):
    """
    Process all the files in the input directory and write the output in the same filenames
    to the output directory.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):  # Assuming the files are .txt files
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)

            # Process each alignment file and write the output
            process_alignment_file(input_file, output_file)
            print(f"Processed {filename} -> {output_file}")

# Example usage
input_dir = '/ocean/projects/bio200049p/zjiang2/Files/spring24/test1'
output_dir = '/ocean/projects/bio200049p/zjiang2/Files/spring24/testres1'
process_all_files(input_dir, output_dir)
