import os

def process_files(input_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename)
        
        # Process each file
        with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
            lines = infile.readlines()
            for i in range(0, len(lines), 2):
                name_line = lines[i].strip()  # First line is the name line
                sequence_line = lines[i + 1].strip().replace("-", "")  # Second line is the sequence line without "-"
                
                # Write to the output file
                outfile.write(f"{name_line}\n")
                outfile.write(f"{sequence_line}\n")

    print("Files processed and saved to the new directory.")

# Example usage
input_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/fasta_corrected"  # Replace with your input directory path
output_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/nodashfasta"  # Replace with your output directory path
process_files(input_directory, output_directory)

