import pandas as pd
import os

def analyze_species_matches(excel_path, utr_dir, output_excel_path):
    # Load the Excel file
    df = pd.read_excel(excel_path)

    # Add new columns to store match counts
    df["Strict Match Count"] = 0
    df["Relaxed Match Count"] = 0
    df["In Frame Mutation Count"] = 0
    df["Total Species"] = 0

    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        utr_name = row["5' UTR Name"]
        orf_type = row["ORF Type"]
        orf_sequence = row["ORF Sequence"]
        start_idx = row["Start Index"]  # Convert to 0-based indexing
        end_idx = row["End Index"] # Convert to 0-based indexing

        # Construct the path to the UTR file
        utr_file_path = os.path.join(utr_dir, f"{utr_name}")
        if not os.path.isfile(utr_file_path):
            print(f"File {utr_file_path} not found. Skipping row.")
            continue

        # Open and read the UTR file
        with open(utr_file_path, 'r') as f:
            lines = f.readlines()
            if len(lines) < 2:
                print(f"File {utr_file_path} has insufficient lines. Skipping row.")
                continue

            # Get the human sequence
            dashed_human_sequence = lines[1].strip()
            human_subseq = dashed_human_sequence[start_idx:end_idx]

            # Initialize counts
            strict_match_count = 0
            relaxed_match_count = 0
            in_frame_mutation_count = 0

            # Iterate through the species sequences (lines[3], lines[5], ...)
            for species_line_idx in range(3, len(lines), 2):
                species_sequence = lines[species_line_idx].strip()
                species_subseq = species_sequence[start_idx:end_idx]

                # Mechanism 1: Strict Match
                if species_subseq == human_subseq:
                    strict_match_count += 1
                    continue

                # Mechanism 2: Relaxed Match
                species_subseq_no_dash = species_subseq.replace('-', '')
                if orf_sequence.upper() in species_subseq_no_dash:
                    relaxed_match_count += 1
                    continue

                # Mechanism 3: In Frame Mutation
                orf_type_base = orf_type.split(" ")[0]
                if orf_type_base == "uORF":
                    if (species_subseq_no_dash.startswith("ATG") and
                        species_subseq_no_dash.endswith(("TAA", "TAG", "TGA")) and 
                        len(species_subseq_no_dash) % 3 == 0):
                        in_frame_mutation_count += 1
                elif orf_type_base == "oORF":
                    if (species_subseq_no_dash.startswith("ATG") and
                        len(species_subseq_no_dash) % 3 != 0):
                        in_frame_mutation_count += 1
                elif orf_type_base == "NTE":
                    if (species_subseq_no_dash.startswith("ATG") and
                        len(species_subseq_no_dash) % 3 == 0):
                        in_frame_mutation_count += 1

            # Calculate total species for this UTR file
            total_species = (len(lines) - 2) // 2

            # Update row counts
            df.at[index, "Strict Match Count"] = strict_match_count
            df.at[index, "Relaxed Match Count"] = relaxed_match_count
            df.at[index, "In Frame Mutation Count"] = in_frame_mutation_count
            df.at[index, "Total Species"] = total_species

    # Calculate percentages for each match type
    df["Strict Match Percentage"] = df["Strict Match Count"] / df["Total Species"] * 100
    df["Relaxed Match Percentage"] = df["Relaxed Match Count"] / df["Total Species"] * 100
    df["In Frame Mutation Percentage"] = df["In Frame Mutation Count"] / df["Total Species"] * 100

    # Save the updated DataFrame to a new Excel file
    df.to_excel(output_excel_path, index=False)
    print(f"Updated Excel file saved to {output_excel_path}")


# File paths
excel_path = '/ocean/projects/bio200049p/zjiang2/Files/spring24/index_update_orf.xlsx'
utr_dir = '/ocean/projects/bio200049p/zjiang2/Files/spring24/fasta_corrected'
output_excel_path = '/ocean/projects/bio200049p/zjiang2/Files/spring24/new_species_match_analysis.xlsx'

analyze_species_matches(excel_path, utr_dir, output_excel_path)

