import os
import pandas as pd
from Bio import SeqIO

def parse_human_orfs(excel_file):
    """Parse the human ORF data from the Excel file."""
    df = pd.read_excel(excel_file)
    human_orfs = {}
    for _, row in df.iterrows():
        utr_name = row["5' UTR Name"]
        orf_type = row["ORF Type"]
        sequence = row["ORF Sequence"]
        start_index = row["Start Index"]  # Exact position in human sequence
        if utr_name not in human_orfs:
            human_orfs[utr_name] = []
        human_orfs[utr_name].append({
            "type": orf_type,
            "sequence": sequence,
            "start_index": start_index
        })
    return human_orfs

def strict_exact_location_match(human_sequence, species_sequence, orf_seq, start_index):
    """Check if the species has the exact ORF sequence at the same location as in human."""
    return species_sequence[start_index:start_index + len(orf_seq)] == orf_seq

def strict_different_location_match(species_sequence, orf_seq):
    """Check if the species has the exact ORF sequence but at a different location."""
    return orf_seq in species_sequence

def relaxed_match_with_indels(species_sequence, orf_seq, start_codon="atg", stop_codons={"tag", "taa", "tga"}):
    """Check for relaxed matching allowing indels but no substitutions, keeping start and stop codons intact."""
    # Check start codon
    if not species_sequence.startswith(start_codon) or species_sequence[-3:] not in stop_codons:
        return False

    # Allow for indels in multiples of 3 but no substitutions
    indel_tolerance = 3
    i, j, indels = 0, 0, 0
    while i < len(orf_seq) and j < len(species_sequence):
        if orf_seq[i] == species_sequence[j]:
            i += 1
            j += 1
        else:
            # Try an indel of 3 nucleotides
            indels += 1
            if indels > indel_tolerance // 3:
                return False
            j += 3
    return i == len(orf_seq)

def analyze_conservation(fasta_dir, human_orfs):
    """Analyze conservation of ORFs across species in each transcript."""
    conservation_results = []
    for utr_name, orfs in human_orfs.items():
        fasta_file = os.path.join(fasta_dir, utr_name)  # File name already includes ".txt"
        if not os.path.exists(fasta_file):
            continue
        
        # Load the human sequence from the FASTA file
        human_sequence = None
        with open(fasta_file, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):  # Step through pairs of lines
                name_line = lines[i].strip()
                seq_line = lines[i + 1].strip().lower().replace("-", "")
                if name_line.startswith(">hg38"):
                    human_sequence = seq_line  # Keep the human sequence for location-based matching
                    break

        if human_sequence is None:
            print(f"Warning: No human sequence found in {fasta_file}")
            continue

        # Initialize conservation counts for each ORF type
        species_counts = {
            orf["type"]: {"exact_location": 0, "different_location": 0, "relaxed_indels": 0}
            for orf in orfs
        }

        # Check conservation for each species in the FASTA file
        for i in range(0, len(lines), 2):
            name_line = lines[i].strip()
            seq_line = lines[i + 1].strip().lower().replace("-", "")  # Remove gaps from species sequence
            
            # Skip the human sequence (already processed)
            if name_line.startswith(">hg38"):
                continue

            # For each ORF type, check conservation in all three methods
            for orf in orfs:
                orf_seq = orf["sequence"]
                orf_type = orf["type"]
                start_index = orf["start_index"]

                if strict_exact_location_match(human_sequence, seq_line, orf_seq, start_index):
                    species_counts[orf_type]["exact_location"] += 1
                elif strict_different_location_match(seq_line, orf_seq):
                    species_counts[orf_type]["different_location"] += 1
                elif relaxed_match_with_indels(seq_line, orf_seq):
                    species_counts[orf_type]["relaxed_indels"] += 1

        # Store results for each ORF type
        for orf in orfs:
            conservation_results.append({
                "5' UTR Name": utr_name,
                "ORF Type": orf["type"],
                "ORF Sequence": orf["sequence"],
                "Strict Exact Location Count": species_counts[orf["type"]]["exact_location"],
                "Strict Different Location Count": species_counts[orf["type"]]["different_location"],
                "Relaxed Indel Count": species_counts[orf["type"]]["relaxed_indels"]
            })
    return conservation_results

def save_to_excel(conservation_results, output_file):
    """Save the conservation analysis results to an Excel file."""
    df = pd.DataFrame(conservation_results)
    df.to_excel(output_file, index=False)

# Define file paths
input_excel_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/updated_orf_analysis.xlsx"
fasta_dir = "/ocean/projects/bio200049p/zjiang2/Files/spring24/filteredfasta"
output_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/conservation_analysis.xlsx"

# Process the human ORFs and analyze conservation
human_orfs = parse_human_orfs(input_excel_file)
conservation_results = analyze_conservation(fasta_dir, human_orfs)
save_to_excel(conservation_results, output_file)
