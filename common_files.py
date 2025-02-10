import os
import shutil

# Function to filter and move common .txt and .bed files to new directories
def filter_and_move_files(bed_dir, txt_dir, output_bed_dir, output_txt_dir):
    # Ensure the output directories exist
    os.makedirs(output_bed_dir, exist_ok=True)
    os.makedirs(output_txt_dir, exist_ok=True)

    # Get all .bed files and .txt files from the respective directories
    bed_files = {os.path.splitext(f)[0] for f in os.listdir(bed_dir) if f.endswith(".fasta")}
    txt_files = {os.path.splitext(f)[0] for f in os.listdir(txt_dir) if f.endswith(".txt")}

    # Find common files (same name without extension)
    common_files = bed_files.intersection(txt_files)

    # Move the common .bed and .txt files to their respective output directories
    for file_name in common_files:
        bed_file_path = os.path.join(bed_dir, f"{file_name}.fasta")
        txt_file_path = os.path.join(txt_dir, f"{file_name}.txt")
        
        # Move the .bed file to the output_bed_dir
        shutil.move(bed_file_path, os.path.join(output_bed_dir, f"{file_name}.fasta"))
        
        # Move the .txt file to the output_txt_dir
        shutil.move(txt_file_path, os.path.join(output_txt_dir, f"{file_name}.txt"))

def main():
    bed_dir = "/ocean/projects/bio200049p/zjiang2/Files/spring24/5UTRfasta"  # Replace with the actual path to the directory containing .bed files
    txt_dir = "/ocean/projects/bio200049p/zjiang2/Files/spring24/updatedcommonseq"  # Replace with the actual path to the directory containing .txt files
    output_bed_dir = "/ocean/projects/bio200049p/zjiang2/Files/spring24/commonfasta"  # Replace with the desired output directory for common .bed files
    output_txt_dir = "/ocean/projects/bio200049p/zjiang2/Files/spring24/commonseq"  # Replace with the desired output directory for common .txt files

    filter_and_move_files(bed_dir, txt_dir, output_bed_dir, output_txt_dir)

if __name__ == "__main__":
    main()
