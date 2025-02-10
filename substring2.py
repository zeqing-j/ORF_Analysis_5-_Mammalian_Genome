import os

# Function to find the longest common substring between two strings
def find_longest_common_substring(utr, seq):
    utr_len = len(utr)
    seq_len = len(seq)
    # Create a table to store lengths of longest common suffixes of substrings
    dp = [[0] * (seq_len + 1) for _ in range(utr_len + 1)]
    longest_len = 0
    end_pos_utr = 0

    # Fill dp table
    for i in range(1, utr_len + 1):
        for j in range(1, seq_len + 1):
            if utr[i - 1].lower() == seq[j - 1].lower():  # Ignore case
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > longest_len:
                    longest_len = dp[i][j]
                    end_pos_utr = i

    # Extract the longest common substring
    start_pos_utr = end_pos_utr - longest_len
    return utr[start_pos_utr:end_pos_utr], start_pos_utr, end_pos_utr

# Function to remove dashes from the UTR sequence and find the corresponding indices
def clean_utr(utr_seq):
    cleaned_utr = []
    dash_indices = []

    for idx, char in enumerate(utr_seq):
        if char != '-':
            cleaned_utr.append(char)
        else:
            dash_indices.append(idx)

    return ''.join(cleaned_utr), dash_indices

# Main function to process UTR and seq files
def process_files(utr_dir, seq_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for utr_file in os.listdir(utr_dir):
        if utr_file.endswith('.fasta'):
            name = utr_file.split('.fasta')[0]
            utr_path = os.path.join(utr_dir, utr_file)
            seq_path = os.path.join(seq_dir, f"{name}.txt")

            if not os.path.exists(seq_path):
                print(f"Sequence file for {name} not found. Skipping...")
                continue

            # Read the UTR and seq files
            with open(utr_path, 'r') as utr_f, open(seq_path, 'r') as seq_f:
                utr_lines = utr_f.readlines()
                seq_lines = seq_f.readlines()

                # Ignore the first line and extract the actual sequences
                utr_seq = utr_lines[1].strip()
                seq_seq = seq_lines[1].strip()

                # Clean UTR sequence (remove dashes and record positions of dashes)
                cleaned_utr, dash_indices = clean_utr(utr_seq)

                # Find the longest common substring between cleaned UTR and seq sequence
                lcs, start_utr, end_utr = find_longest_common_substring(cleaned_utr, seq_seq)

                # Adjust the start and end indices for the original UTR sequence (with dashes)
                adjusted_start = start_utr
                adjusted_end = end_utr
                for dash_index in dash_indices:
                    if dash_index < start_utr:
                        adjusted_start += 1
                    if dash_index < end_utr:
                        adjusted_end += 1

                # Extract the corresponding substrings from the original UTR and seq sequences
                utr_substring = utr_seq[adjusted_start:adjusted_end]
                seq_substring = seq_seq[start_utr:end_utr]

                # Create the output file for this name
                output_file = os.path.join(output_dir, f"{name}_common.txt")
                with open(output_file, 'w') as out_f:
                    out_f.write(f"{name}\n")
                    out_f.write(f"{utr_substring}\n")
                    out_f.write(f"{seq_substring}\n")
                    out_f.write(f"{adjusted_start} {adjusted_end}\n")

                print(f"Processed {name} and wrote results to {output_file}")

# Main execution
if __name__ == "__main__":
    # Directories for input and output
    utr_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/commonfasta"  # Directory containing .fasta files
    seq_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/commonseq"  # Directory containing .txt files
    output_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/substringinfo2"  # Directory for storing result files

    # Process the files and find the longest common substring
    process_files(utr_directory, seq_directory, output_directory)

