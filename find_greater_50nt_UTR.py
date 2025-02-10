import os
import re

def process_files(directory):
    # List to store the results
    results = []

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()

            # Initialize variables to store information
            mfe_structure_line = None
            mfe_value = None

            # Search for "MFE Structure"
            for i, line in enumerate(lines):
                if "MFE Structure" in line:
                    # The next line after "MFE Structure"
                    mfe_structure_line = lines[i + 1].strip()
                    # Remove the final forward and backward bracket and the word inside the bracket
                    mfe_structure = mfe_structure_line.split(' ')[0]  # Remove numbers at the end
                    mfe_structure = mfe_structure.strip()
                    mfe_structure_length = len(mfe_structure)
                    break

            # If the length of the structure line is greater than 50, find "Minimum Free Energy: "
            if mfe_structure_line and mfe_structure_length >= 50:
                for line in lines:
                    if "Minimum Free Energy: " in line:
                        mfe_value = re.search(r"Minimum Free Energy: ([-\d.]+) kcal/mol", line)
                        if mfe_value:
                            mfe_value = mfe_value.group(1)
                            break

            # If all conditions are met, store the result
            if mfe_value:
                result = f"{filename[:-4]}:{mfe_value}"
                results.append(result)

    return results

def main():
    # Set the directory containing the txt files
    directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/newstruc"

    # Process the files and print the results
    output = process_files(directory)
    output_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/greater50UTR.txt"
    with open(output_file, 'w') as f:
        for item in output:
            f.write(item + "\n")

if __name__ == "__main__":
    main()
