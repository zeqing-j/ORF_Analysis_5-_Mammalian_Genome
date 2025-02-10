import os
def process_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        
        i = 0
        while i < len(lines):
            # Check if the line starts with '>'
            if lines[i].startswith('>hg38'):
                # Extract the identifier from the current line
                header_line = lines[i]
                # Extract the ENST ID (e.g., ENST00000263946.7) from the header
                enst_id = header_line.split('_')[-1].split()[0]
                
                # Extract the sequence line (the next line)
                sequence_line = lines[i+1]
                
                # Write both lines to the new file named after the ENST ID
                output_dir = "/ocean/projects/bio200049p/zjiang2/Files/spring24/updatedseq"
                output_file_path = os.path.join(output_dir, f'{enst_id}.txt')
                with open(output_file_path, 'w') as output_file:
                    output_file.write(header_line)
                    output_file.write(sequence_line)
            
            # Move to the next pair of lines
            i += 2

def main():
    # Set the directory containing the txt files
    directory = "/ocean/projects/bio200049p/zjiang2/Files/RNAfold/gencode.v33.base_updatedTSS_EPDnewRefTSS.fa"
    # Process the files and print the results
    process_file(directory)

if __name__ == "__main__":
    main()
