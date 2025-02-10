import pandas as pd

def read_bpfile_to_dict(filename):
    """
    Reads a file where the first line is a key (transcript name) and the second line is a value.
    Returns a dictionary of the content.
    """
    data = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines)):
            parts = lines[i].split(":")
            remove = parts[0].split("_")
            transcript = remove[0]
            numbers = parts[1].split(";")
            data[transcript] = numbers[1]
    return data

def read_mfe_to_dict(filename):
    """
    Reads a file where the first line is a key (transcript name) and the second line is a value.
    Returns a dictionary of the content.
    """
    data = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines)):
            parts = lines[i].split(":")
            remove = parts[0].split("_")
            transcript = remove[0]
            numbers = parts[1].split(";")
            data[transcript] = numbers[0]
    return data

def read_file_to_dict(filename):
    """
    Reads a file where the first line is a key (transcript name) and the second line is a value.
    Returns a dictionary of the content.
    """
    data = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            transcript = lines[i].strip()
            value = float(lines[i + 1].strip())
            data[transcript] = value
    return data

def extract_energy_numbers(file_path):
    data = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            transcript = lines[i].strip()
            energy_str = lines[i+2].strip().split()[-1][1:-1]  # Extract the number from brackets
            energy = float(energy_str)
            data[transcript] = energy
    return data

def create_excel_file(combine_file, orf_file, mfe_file, cai_file, proline_file, lowcai_file, highcai_file, output_file):
    # Read data from files
    bp_data = read_bpfile_to_dict(combine_file)
    alifold_data = read_mfe_to_dict(combine_file)
    orf_data = read_file_to_dict(orf_file)
    mfe_data = extract_energy_numbers(mfe_file)
    cai_data = read_file_to_dict(cai_file)
    lowcai_data = read_file_to_dict(lowcai_file)
    highcai_data = read_file_to_dict(highcai_file)
    proline_data = read_file_to_dict(proline_file)

    # Find common transcript names in phylop and ORF length data
    common_transcripts = set(alifold_data.keys()).intersection(set(orf_data.keys()))

    # Prepare the data for the DataFrame
    rows = []
    for transcript in common_transcripts:
        row = {
            "Transcript": transcript,
            "bp_percentage": bp_data.get(transcript),
            "MFE from Linearalifold": alifold_data.get(transcript),
            "ORF_length": orf_data.get(transcript),
            "Minimum_free_energy": mfe_data.get(transcript),
            "CAI_values": cai_data.get(transcript),
            "lowCAIcount": lowcai_data.get(transcript),
            "highCAIcount":highcai_data.get(transcript),
            "Proline_count": proline_data.get(transcript)
        }
        rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows)

    # Save DataFrame to Excel file
    df.to_excel(output_file, index=False)

def main():
    combine_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/common_results.txt"
    orf_file = "/ocean/projects/bio200049p/zjiang2/Files/RNAfold/ORF_length/v33_ORFlength.fasta"
    mfe_file = "/ocean/projects/bio200049p/zjiang2/Files/RNAfold/80mod/v33_80mod_1.fold"
    cai_file = "/ocean/projects/bio200049p/zjiang2/Files/RNAfold/CAI/v33_CAI.fasta"
    highcai_file = "/ocean/projects/bio200049p/zjiang2/Files/RNAfold/v33_highCAIcount.fasta"
    lowcai_file = "/ocean/projects/bio200049p/zjiang2/Files/RNAfold/v33_CAIcount.fasta"
    proline_file = "/ocean/projects/bio200049p/zjiang2/Files/RNAfold/proline/v33_3proline_count.fasta"
    output_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/combine_alifold.xlsx"

    create_excel_file(combine_file, orf_file, mfe_file, cai_file, proline_file, lowcai_file, highcai_file, output_file)
    print(f"Processing completed. Check the output file: {output_file}")

if __name__ == "__main__":
    main()

