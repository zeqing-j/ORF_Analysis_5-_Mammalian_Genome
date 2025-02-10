import os

def read_fasta_file(filepath):
    """
    Read the species names and alignments from a FASTA file.
    Returns a list of tuples where each tuple contains (species_name, alignment).
    """
    species_data = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 2):
            species_name = lines[i].strip()
            alignment = lines[i + 1].strip()
            species_data.append((species_name, alignment))
    return species_data

def read_common_substring_file(filepath):
    """
    Read the start and end indices from a 'name_common.txt' file.
    Returns the start and end as integers.
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
        # The third line contains the start and end positions
        start_end = lines[1].strip().split()
        start = int(start_end[0])
        end = int(start_end[1])
    return start, end

def write_output_file(output_filepath, species_substrings):
    """
    Write the species and their corresponding substrings to the output file.
    """
    with open(output_filepath, 'w') as f:
        for species_name, substring in species_substrings:
            f.write(f"{species_name}\n")
            f.write(f"{substring}\n")

def process_files(commonsubstring_dir, fasta_dir, output_dir):
    """
    Process each file in the 'commonsubstring' directory, extract substrings from the corresponding
    FASTA file, and write the output to the 'output' directory.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for common_file in os.listdir(commonsubstring_dir):
        if common_file.endswith("_common.txt"):
            fasta_filename = common_file.replace("_common.txt", ".fasta")
            common_filepath = os.path.join(commonsubstring_dir, common_file)
            fasta_filepath = os.path.join(fasta_dir, fasta_filename)
            
            if os.path.exists(fasta_filepath):
                # Read the start and end indices from the 'name_common.txt' file
                start, end = read_common_substring_file(common_filepath)
                
                # Read the species names and alignments from the corresponding FASTA file
                species_data = read_fasta_file(fasta_filepath)
                
                # Extract the substring for each species' alignment using the start and end indices
                species_substrings = [(species_name, alignment[start:end+1]) for species_name, alignment in species_data]
                
                # Write the output to a new file in the output directory
                output_filename = common_file.replace("_common.txt", ".txt")
                output_filepath = os.path.join(output_dir, output_filename)
                write_output_file(output_filepath, species_substrings)
            else:
                print(f"Warning: {fasta_filename} not found in {fasta_dir}")

# Example usage
commonsubstring_dir = "/ocean/projects/bio200049p/zjiang2/Files/spring24/commonsubstring"
fasta_dir = "/ocean/projects/bio200049p/zjiang2/Files/spring24/orifasta"
output_dir = "/ocean/projects/bio200049p/zjiang2/Files/spring24/fasta_corrected"

process_files(commonsubstring_dir, fasta_dir, output_dir)

