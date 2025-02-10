import pandas as pd

def fill_empty_first_column(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Ensure we're only working on the first column
    df.iloc[:, 0] = df.iloc[:, 0].ffill()  # Forward fill NaN values in the first column
    
    # Save the modified DataFrame back to a new Excel file
    df.to_excel(output_file, index=False)

# Example usage
input_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/orf_analysis.xlsx"    # Replace with your input file name
output_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/updated_orf_analysis.xlsx"   # Replace with your desired output file name
fill_empty_first_column(input_file, output_file)
