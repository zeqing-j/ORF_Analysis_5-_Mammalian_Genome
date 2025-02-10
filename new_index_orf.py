import os
import pandas as pd

def update_start_end_indices(excel_path, input_directory, output_excel_path):
    # Load the Excel file
    df = pd.read_excel(excel_path)

    # Prepare columns for new start and end indices
    new_rows = []

    for idx, row in df.iterrows():
        utr_file_name = row["5' UTR Name"]
        orf_sequence = row['ORF Sequence'].upper()

        # Find the corresponding file
        utr_file_path = os.path.join(input_directory, utr_file_name)
        if not os.path.isfile(utr_file_path):
            #print(f"File {utr_file_name} not found. Skipping row {idx}.")
            continue

        with open(utr_file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) < 2:
                print(f"File {utr_file_name} is not formatted as expected. Skipping row {idx}.")
                continue

            dashed_human_sequence = lines[1].strip()
            human_sequence = dashed_human_sequence.replace('-', '')

            # Find the ORF sequence in the non-dashed human sequence
            start_index = human_sequence.find(orf_sequence)
            if start_index == -1:
                print(f"ORF sequence not found in human sequence for file {utr_file_name}. Skipping row {idx}.")
                continue

            end_index = start_index + len(orf_sequence)

            i = 0
            track = 0
            while(track < start_index):
                if dashed_human_sequence[i] != "-":
                    track += 1
                i += 1
            print(track)

            while(dashed_human_sequence[i] == "-"):
                i += 1

            final_start_idx = i

            r = track
            j = final_start_idx
            while(r < end_index):
                if dashed_human_sequence[j] != "-":
                    r += 1
                j += 1


            row['Start Index'] = final_start_idx
            row['End Index'] = j
            new_rows.append(row)

    # Create a new DataFrame from the rows that were retained
    new_df = pd.DataFrame(new_rows)

    # Save the updated DataFrame to a new Excel file
    new_df.to_excel(output_excel_path, index=False)

# Example usage
excel_path = '/ocean/projects/bio200049p/zjiang2/Files/spring24/updated_orf_analysis.xlsx'  # Replace with your Excel file path
input_directory = '/ocean/projects/bio200049p/zjiang2/Files/spring24/fasta_corrected'  # Replace with your directory containing the 5' UTR files
output_excel_path = '/ocean/projects/bio200049p/zjiang2/Files/spring24/index_update_orf.xlsx'  # Replace with the desired output Excel file path

update_start_end_indices(excel_path, input_directory, output_excel_path)
