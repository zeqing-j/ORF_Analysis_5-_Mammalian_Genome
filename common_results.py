def read_file(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                name, number = line.strip().split(':', 1)
                data[name] = number
    return data

def find_common_entries(file1_data, file2_data):
    common_entries = {}
    for name in file1_data:
        if name in file2_data:
            common_entries[name] = f"{file1_data[name]};{file2_data[name]}"
    return common_entries

def write_common_entries(output_file, common_entries):
    with open(output_file, 'w') as file:
        for name, numbers in common_entries.items():
            file.write(f"{name}:{numbers}\n")

def main():
    file1_path = "/ocean/projects/bio200049p/zjiang2/Files/spring24/greater50UTR.txt"
    file2_path = "/ocean/projects/bio200049p/zjiang2/Files/spring24/bp_percentage.txt"

    # Read the data from the two files
    file1_data = read_file(file1_path)
    file2_data = read_file(file2_path)

    # Find common names and their associated numbers
    common_entries = find_common_entries(file1_data, file2_data)

    # Write the results to a new file
    output_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/common_results.txt"
    write_common_entries(output_file, common_entries)

    print(f"Common entries saved to {output_file}")

if __name__ == "__main__":
    main()

