import os

def process_files(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.fasta'):
            # Create full file paths
            input_file = os.path.join(input_dir, filename)
            name = filename.split('_')[0]  # Extract name before '_strand'
            output_file = os.path.join(output_dir, f"{name}.fasta")

            with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
                lines = infile.readlines()

                # Search for ">hg38" and copy the line and the next line
                for i, line in enumerate(lines):
                    if ">hg38" in line:
                        outfile.write(line)  # Write the ">hg38" line
                        if i + 1 < len(lines):  # Check if there is a next line
                            outfile.write(lines[i + 1])  # Write the next line
                        break  # Stop after the first match

    print("Processing complete.")

def main():
    input_directory = '/ocean/projects/bio200049p/zjiang2/Files/5primedata/bigbed_whole_genome/fasta_dir'
    output_directory = '/ocean/projects/bio200049p/zjiang2/Files/spring24/5UTRfasta'
    process_files(input_directory, output_directory)


if __name__ == "__main__":
    main()
