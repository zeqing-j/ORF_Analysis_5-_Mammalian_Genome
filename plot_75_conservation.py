import os
import pandas as pd

# Load the Excel file
excel_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/filter_75_conservation.xlsx"  # Replace with the path to your Excel file
output_file = "/ocean/projects/bio200049p/zjiang2/Files/spring24/plot_conservation_75.xlsx"  # Replace with the desired output file name
data = pd.read_excel(excel_file)

# Directory containing the text files
directory = "/ocean/projects/bio200049p/zjiang2/Files/spring24/nodashfasta"  # Replace with the path to your directory containing text files

# Ensure columns to extract are valid
columns_to_extract = [0, 1, 2] + list(range(8, 13))
if any(idx >= len(data.columns) for idx in columns_to_extract):
    raise ValueError("Specified column indexes exceed the number of columns in the Excel file.")

# Initialize lists to store the new data
start_indices = []
end_indices = []
total_lengths = []

# Process each row in the Excel file
for _, row in data.iterrows():
    # Get the file name from the first row and add ".txt"
    file_name = f"{row[0]}.txt"
    file_path = os.path.join(directory, file_name)

    if not os.path.isfile(file_path):
        start_indices.append(None)
        end_indices.append(None)
        total_lengths.append(None)
        continue

    # Open the corresponding text file
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Ensure the file has a second line
    if len(lines) < 2:
        start_indices.append(None)
        end_indices.append(None)
        total_lengths.append(None)
        continue

    second_line = lines[1].strip()  # The second line of the file

    # Find the start index of the ORF sequence in the second line
    orf_sequence = str(row[2])  # Third column value as a string
    start_index = second_line.find(orf_sequence)

    if start_index == -1:
        start_indices.append(None)
        end_indices.append(None)
        total_lengths.append(len(second_line))
        continue

    # Calculate the start, end indices, and total length
    end_index = start_index + len(orf_sequence)
    total_length = len(second_line)

    start_indices.append(start_index)
    end_indices.append(end_index)
    total_lengths.append(total_length)

# Add the new columns to the DataFrame
data["Start_Index"] = start_indices
data["End_Index"] = end_indices
data["Total_Length"] = total_lengths

# Extract the required columns
selected_columns = [data.columns[idx] for idx in columns_to_extract]
selected_columns += ["Start_Index", "End_Index", "Total_Length"]
filtered_data = data[selected_columns]

# Save the modified DataFrame to a new Excel file
filtered_data.to_excel(output_file, index=False)

print(f"Processed data saved to {output_file}")


