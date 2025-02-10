import os

# Function to read FASTA file, skipping the first line and removing "-"
def read_fasta(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        sequence = lines[1].strip().replace("-", "")  # Skip the first line and remove dashes
    return sequence

# Function to read .txt sequence file, skipping the first line
def read_seq(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        sequence = lines[1].strip()  # Skip the first line
    return sequence

# Function to find the longest common substring (case-insensitive)
def longest_common_substring(seq1, seq2):
    seq1_upper = seq1.upper()  # For comparison, ignore case differences
    seq2_upper = seq2.upper()

    # Initialize variables for storing the result
    longest_substring = ""
    start_index_in_utr = -1
    end_index_in_utr = -1

    # Use dynamic programming to find the longest common substring
    lengths = [[0] * (len(seq2_upper) + 1) for _ in range(len(seq1_upper) + 1)]
    
    for i in range(1, len(seq1_upper) + 1):
        for j in range(1, len(seq2_upper) + 1):
            if seq1_upper[i - 1] == seq2_upper[j - 1]:
                lengths[i][j] = lengths[i - 1][j - 1] + 1
                if lengths[i][j] > len(longest_substring):
                    longest_substring = seq2[j - lengths[i][j]:j]  # Extract the substring from seq2
                    start_index_in_utr = i - lengths[i][j]  # Record the starting index in the UTR sequence
                    end_index_in_utr = i - 1  # Record the ending index in the UTR sequence

    return longest_substring, start_index_in_utr, end_index_in_utr

# Function to process files from the utr and seq directories and find longest common substring
def process_files(utr_dir, seq_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for utr_file in os.listdir(utr_dir):
        if utr_file.endswith(".fasta"):
            utr_name = os.path.splitext(utr_file)[0]
            utr_path = os.path.join(utr_dir, utr_file)
            seq_path = os.path.join(seq_dir, utr_name + ".txt")

            # Check if corresponding seq file exists
            if os.path.exists(seq_path):
                output_file = os.path.join(output_dir, utr_name + "_common.txt")

                # Check if output file already exists
                if os.path.exists(output_file):
                    continue

                utr_sequence = read_fasta(utr_path)
                seq_sequence = read_seq(seq_path)

                # Find the longest common substring
                common_substring, start_index, end_index = longest_common_substring(utr_sequence, seq_sequence)

                # Write the result to a new file in the output directory
                output_file = os.path.join(output_dir, utr_name + "_common.txt")
                with open(output_file, 'w') as f_out:
                    f_out.write(f"{utr_name}\n")  # First line: name
                    f_out.write(f"{common_substring}\n")  # Second line: longest common substring
                    f_out.write(f"{start_index} {end_index}\n")  # Third line: start and end indices in utr

# Main execution
if __name__ == "__main__":
    # Directories for input and output
    utr_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/commonfasta"  # Directory containing .fasta files
    seq_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/commonseq"  # Directory containing .txt files
    output_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/substringinfo"  # Directory for storing result files

    # Process the files and find the longest common substring
    process_files(utr_directory, seq_directory, output_directory)

