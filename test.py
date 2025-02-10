import pandas as pd
import os

def process_excel_and_fasta(excel_file, fasta_directory):
    # Load the Excel file
    df = pd.read_excel(excel_file)
    
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        utr_name = row['5\' UTR Name']
        orf_type = row['ORF Type']
        orf_sequence = row['ORF Sequence']
        start_index = row['Start Index']
        end_index = row['End Index'] + 1  # Adjust end index for substring

        # Find the corresponding FASTA file
        fasta_file_path = os.path.join(fasta_directory, f"{utr_name}")
        if not os.path.exists(fasta_file_path):
            print(f"File {utr_name} not found in {fasta_directory}")
            continue

        # Open and read the FASTA file
        with open(fasta_file_path, 'r') as fasta_file:
            lines = fasta_file.readlines()
            human_sequence = lines[1].strip()  # The second line is the human sequence

            # Check if the ORF sequence exists within the human sequence
            found_index = human_sequence.find(orf_sequence)
            if found_index != -1:
                # Verify if the found sequence has the expected index range
                if found_index != start_index or found_index + len(orf_sequence) != end_index:
                    print(f"different index found in {fasta_file_path}")
                    return  # Stop searching as per the instruction
            else:
                continue

    print("All sequences matched the expected indexes.")

# Example usage
excel_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/updated_orf_analysis.xlsx"
fasta_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/nodashfasta" # Replace with the path to your FASTA directory
process_excel_and_fasta(excel_file, fasta_directory)

