import os
import pandas as pd

# Define a codon table for translation
CODON_TABLE = {
    "AUG": "M", "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
    "UAU": "Y", "UAC": "Y", "UAA": "*", "UAG": "*",
    "UGU": "C", "UGC": "C", "UGA": "*", "UGG": "W",
    "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"
}

STOP_CODONS = {"UAA", "UAG", "UGA"}

# Function to translate DNA to amino acids
def translate_dna_to_protein(dna_sequence):
    # Convert T to U for RNA
    rna_sequence = dna_sequence.replace("T", "U")
    # Pad the sequence to be divisible by 3
    if len(rna_sequence) % 3 == 1:
        rna_sequence += "AU"
    elif len(rna_sequence) % 3 == 2:
        rna_sequence += "A"
    # Translate to amino acids
    protein = "".join(CODON_TABLE.get(rna_sequence[i:i+3], "?") for i in range(0, len(rna_sequence), 3))
    return protein

# Load the Excel file
excel_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/new_updatedv2_conservation_75.xlsx"  # Replace with the path to your Excel file
directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/fasta_corrected"  # Replace with the path to your input directory
output_directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/translated_conservation"  # Replace with the path to your output directory

os.makedirs(output_directory, exist_ok=True)

data = pd.read_excel(excel_file)

# Process each row in the Excel file
for _, row in data.iterrows():
    transcript_file = os.path.join(directory, row["Transcript"]+".txt")
    if not os.path.exists(transcript_file):
        print(f"File {row['Transcript']} not found.")
        continue

    # Read the file lines
    with open(transcript_file, "r") as file:
        lines = file.readlines()

    # Process lines in pairs (odd and even lines)
    output_lines = []
    for i in range(1, len(lines), 2):  # Start from the second line (even lines)
        odd_line = lines[i - 1].strip()
        even_line = lines[i].strip()

        start_index, end_index = row["Start Index"], row["End Index"]
        sequence = even_line[start_index:end_index].replace("-", "")

        orf_type = row["ORF Type"].split(" ")[0]

        if orf_type == "uORF":
            if sequence[:3] == "ATG" and sequence[-3:] in {"TAA", "TAG", "TGA"} and len(sequence) % 3 == 0:
                output_lines.append(odd_line)
                output_lines.append(sequence)
        elif orf_type == "oORF":
            if sequence[:3] == "ATG" and len(sequence) % 3 != 0:
                output_lines.append(odd_line)
                output_lines.append(sequence)
        elif orf_type == "NTE":
            if sequence[:3] == "ATG" and len(sequence) % 3 == 0:
                output_lines.append(odd_line)
                output_lines.append(sequence)

    # Write to the output file
    if output_lines:
        output_file = os.path.join(output_directory, row["Transcript"])
        with open(output_file, "w") as file:
            for line in output_lines:
                if line.startswith(">"):  # Header line, write as is
                    file.write(line + "\n")
                else:
                    protein = translate_dna_to_protein(line)
                    file.write(f"{line}\n{protein}\n")

