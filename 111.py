import os
import pandas as pd

folder_path = "D:\VIDEOS"
file_names = os.listdir(folder_path)
df = pd.DataFrame(file_names, columns=["File Name"])

# Save the DataFrame to a CSV file
output_csv_path = "urls.csv"
df.to_csv(output_csv_path, index=False)

print(f"File names have been written to {output_csv_path}")