import os
import re
import openpyxl

# Define stop codons
STOP_CODONS = {"tag", "tga", "taa"}

def find_first_lowercase_part(sequence):
    """Extracts the first part of the sequence until the first uppercase letter."""
    lowercase_part = re.match(r'[a-z]+', sequence)
    return lowercase_part.group(0) if lowercase_part else ''

def find_orfs(sequence):
    """Finds uORFs, oORFs, and NTEs in the lowercase part of the alignment."""
    orfs = []
    pos = 0

    while pos <= len(sequence) - 3:
        # Find start codon ATG
        if sequence[pos:pos+3] == "atg":
            start_pos = pos
            num_start_codons = 1
            pos += 3
            
            # Check for stop codons by moving 3 nucleotides at a time
            while pos <= len(sequence) - 3:
                codon = sequence[pos:pos+3]
                if codon == "atg":
                    num_start_codons += 1
                elif codon in STOP_CODONS:
                    # Found a uORF
                    orfs.append({
                        "type": f"uORF with {num_start_codons} start codons",
                        "sequence": sequence[start_pos:pos+3],
                        "start_pos": start_pos,
                        "end_pos": pos + 2
                    })
                    pos += 3
                    break
                pos += 3
            
            # If we reached the end of lowercase without finding a stop codon
            if pos > len(sequence) - 3:
                if pos == len(sequence):  # End is on the third nucleotide of a codon
                    orfs.append({
                        "type": "NTE",
                        "sequence": sequence[start_pos:],
                        "start_pos": start_pos,
                        "end_pos": len(sequence) - 1
                    })
                else:  # End is not on a complete codon
                    orfs.append({
                        "type": "oORF",
                        "sequence": sequence[start_pos:],
                        "start_pos": start_pos,
                        "end_pos": len(sequence) - 1
                    })
        else:
            pos += 1
    return orfs

def process_files_in_directory(directory_path, output_file):
    """Processes each file in the directory and writes results to an Excel file."""
    # Create a new workbook and add a sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "ORF Analysis"
    sheet.append(["5' UTR Name", "ORF Type", "ORF Sequence", "Start Index", "End Index"])
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Adjust if your files have a different extension
            with open(os.path.join(directory_path, filename), "r") as file:
                lines = file.readlines()

            # Look for the line containing ">hg38" and retrieve the next line as the alignment
            alignment = None
            for i, line in enumerate(lines):
                if line.startswith(">hg38"):
                    alignment = lines[i + 1].strip()
                    break
            
            if alignment:
                # Extract the lowercase portion of the sequence
                lowercase_sequence = find_first_lowercase_part(alignment)
                orfs = find_orfs(lowercase_sequence)

                # Only add to Excel if there are any ORFs found
                if orfs:
                    for idx, orf in enumerate(orfs):
                        sheet.append([
                            filename if idx == 0 else "",  # Only show filename in the first row of the block
                            orf["type"],
                            orf["sequence"],
                            orf["start_pos"],
                            orf["end_pos"]
                        ])

    # Save to Excel
    workbook.save(output_file)


# Example usage
directory_path = "/ocean/projects/bio200049p/zjiang2/Files/spring24/commonseq"
output_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/orf_analysis.xlsx"
process_files_in_directory(directory_path, output_file)
