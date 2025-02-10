import os
import pandas as pd

# Define the input and output file paths
input_excel_path = "/ocean/projects/bio200049p/zjiang2/Files/spring24/updatedv2_conservation_75.xlsx"  # Replace with actual path to input excel file
directory_path = "/ocean/projects/bio200049p/zjiang2/Files/spring24/new_translated_conservation"  # Replace with actual directory path containing sequence files
output_excel_path = "/ocean/projects/bio200049p/zjiang2/Files/spring24/new_translation_analysis.xlsx"

# Load the input Excel file
input_df = pd.read_excel(input_excel_path)

# Initialize the results list
results = []

# Iterate over all files in the directory
for file_name in os.listdir(directory_path):
    file_path = os.path.join(directory_path, file_name)

    if not os.path.isfile(file_path):
        continue

    # Extract Transcript, ORF Type, Start Index, and End Index from the file name
    file_info = file_name.replace(".txt", "").split("_")
    transcript = file_info[0]
    orf_type = file_info[1].split("-")[1]
    start_index = int(file_info[2].split("-")[1])
    end_index = int(file_info[3].split("-")[1])

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Process file to extract human sequence
    human_amino_acid_sequence = None
    species_count_in_file = len(lines) // 3
    same_sequence_count = 0
    mutation_count = 0

    for i in range(0, len(lines), 3):
        species_name = lines[i].strip()
        dna_sequence = lines[i + 1].strip()
        amino_acid_sequence = lines[i + 2].strip()

        if i == 0:
            # The first set of lines corresponds to human sequences
            human_amino_acid_sequence = amino_acid_sequence
        else:
            # Compare other species' amino acid sequences to human's
            if amino_acid_sequence == human_amino_acid_sequence:
                same_sequence_count += 1
            else:
                mutation_count += 1

    # Extract total species from input excel file for the current file
    total_species_from_excel = input_df.loc[
        (input_df['Transcript'] == transcript) &
        (input_df['ORF Type'].str.split().str[0] == orf_type) &
        (input_df['Start Index'] == start_index) &
        (input_df['End Index'] == end_index),
        'Total Species'
    ].values
    total_species_from_excel = total_species_from_excel[0] if len(total_species_from_excel) > 0 else None

    # Calculate percentage
    percentage_same = (same_sequence_count / total_species_from_excel) * 100 if total_species_from_excel and total_species_from_excel > 0 else 0
    percentage_mut = (mutation_count / total_species_from_excel) * 100 if total_species_from_excel and total_species_from_excel > 0 else 0

    # Append results
    results.append({
        "Transcript": transcript,
        "ORF Type": orf_type,
        "Start Index": start_index,
        "End Index": end_index,
        "Human Protein Sequence": human_amino_acid_sequence,
        "Total Species (from Excel)": total_species_from_excel,
        "Species Count (in File)": species_count_in_file,
        "Same Sequence Count": same_sequence_count,
        "Mutation Count": mutation_count,
        "Percentage Same (%)": percentage_same,
        "Percentage Mutation (%)": percentage_mut
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save results to an Excel file
results_df.to_excel(output_excel_path, index=False)

