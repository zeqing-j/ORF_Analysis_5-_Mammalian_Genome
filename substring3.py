import os

def read_file(filepath):
    """
    Read the two lines from a file and return them as a tuple (header, alignment).
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
        return lines[0].strip(), lines[1].strip()

def find_largest_common_substring(seq1, seq2):
    """
    Find the largest common substring between two sequences.
    """
    m = len(seq1)
    n = len(seq2)
    
    # Create a table to store lengths of longest common suffixes of substrings
    lcsuff = [[0 for k in range(n+1)] for l in range(m+1)]
    length = 0  # Length of the longest common substring
    row, col = 0, 0  # Ending point of longest common substring
    
    # Build the table in bottom-up fashion
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                lcsuff[i][j] = 0
            elif seq1[i - 1].upper() == seq2[j - 1].upper():  # Convert both to upper case for comparison
                lcsuff[i][j] = lcsuff[i - 1][j - 1] + 1
                if lcsuff[i][j] > length:
                    length = lcsuff[i][j]
                    row, col = i, j
            else:
                lcsuff[i][j] = 0
    
    # If there is no common substring
    if length == 0:
        return ""
    
    # Longest common substring ends at index row-1 in seq1
    result_str = [''] * length
    
    # Traverse up diagonally from the (row, col) cell
    while lcsuff[row][col] != 0:
        length -= 1
        result_str[length] = seq1[row - 1]  # Append current character to result
        row -= 1
        col -= 1
    
    return ''.join(result_str)

def find_substring_positions(full_seq, substring):
    """
    Find the start and end positions of a substring in the full sequence (with dashes included).
    The positions account for dashes, even though they do not exist in the substring.
    """
    no_dash_seq = full_seq.replace('-', '')  # Remove dashes to find actual position
    start_idx = no_dash_seq.find(substring)
    
    if start_idx == -1:
        return None, None
    
    # Now, map this position back to the sequence with dashes
    cur_idx = 0
    start_pos, end_pos = None, None
    
    for i, char in enumerate(full_seq):
        if char != '-':
            if cur_idx == start_idx:
                start_pos = i
            if cur_idx == start_idx + len(substring) - 1:
                end_pos = i
            cur_idx += 1
        if start_pos is not None and end_pos is not None:
            break
    
    return start_pos, end_pos

def process_files(commonfasta_dir, commonseq_dir, output_dir):
    """
    Process the files, find the largest common substring, and write the results to output files.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for seq_filename in os.listdir(commonseq_dir):
        if seq_filename.endswith(".txt"):
            fasta_filename = seq_filename.replace(".txt", ".fasta")
            
            seq_filepath = os.path.join(commonseq_dir, seq_filename)
            fasta_filepath = os.path.join(commonfasta_dir, fasta_filename)
            
            if os.path.exists(fasta_filepath):
                # Read sequences from the files
                _, fasta_alignment = read_file(fasta_filepath)
                _, seq_alignment = read_file(seq_filepath)
                
                # Remove dashes from fasta alignment
                fasta_alignment_no_dashes = fasta_alignment.replace('-', '')
                
                # Convert seq_alignment to uppercase to ensure case-insensitive comparison
                seq_alignment_upper = seq_alignment.upper()
                
                # Find the largest common substring
                common_substring = find_largest_common_substring(fasta_alignment_no_dashes, seq_alignment_upper)
                
                # Find the start and end positions of the common substring in the original fasta sequence (with dashes)
                start, end = find_substring_positions(fasta_alignment, common_substring)
                
                if start is not None and end is not None:
                    # Write the common substring and positions to the output file
                    output_filepath = os.path.join(output_dir, seq_filename.replace(".txt", "_common.txt"))
                    with open(output_filepath, 'w') as output_file:
                        output_file.write(common_substring + '\n')
                        output_file.write(f"{start} {end}\n")
            else:
                print(f"Warning: {fasta_filename} not found in {commonfasta_dir}")

# Main execution
if __name__ == "__main__":
    # Directories for input and output
    utr_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/commonfasta"  # Directory containing .fasta files
    seq_directory = "//ocean/projects/bio200049p/zjiang2/Files/spring24/commonseq"  # Directory containing .txt files
    output_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/commonsubstring"  # Directory for storing result files

    # Process the files and find the longest common substring
    process_files(utr_directory, seq_directory, output_directory)
