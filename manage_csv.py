import pandas as pd
import os

def get_folder_and_link():
    # Load the CSV file into a DataFrame
    # df = pd.read_csv('ig_accounts.csv')
    current_dir = os.getcwd()
    # Navigate to the parent directory
    csv_file_path = os.path.join(current_dir, 'urls.csv')

    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')
    except:
        df = pd.read_csv(csv_file_path, encoding='Windows-1252')

    # Filter rows where the 'status' is NaN
    filtered_df = df[df['status'].isna()]

    # Check if there's any row that meets the condition
    if not filtered_df.empty:
        # Get the first row where 'status' is NaN
        first_row = filtered_df.iloc[0]

        # Print the values of the first row
        # print("Folder name:", first_row['Folder name'])
        # print("YT link:", first_row['YT link'])

        # Update the 'status' of the first row
        df['status'] = df['status'].astype(str)

        # Update the status of the specific row
        df.loc[first_row.name, 'status'] = 'used'

        # Save the updated DataFrame back to the CSV file
        df.to_csv(csv_file_path, index=False)
        # print("Status updated and saved back to CSV.")

        return first_row['Folder name']
    else:
        print("No rows with NaN status were found.")

def update_cell(folder_name):
    current_dir = os.getcwd()
    # Navigate to the parent directory
    csv_file_path = os.path.join(current_dir, 'urls.csv')

    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')
    except:
        df = pd.read_csv(csv_file_path, encoding='Windows-1252')

    # username_to_update = 'chuminhha_184'

    index_to_update = df[df['Folder name'] == folder_name].index

    # Step 3: Update the specific cell
    if not index_to_update.empty:
        # Assuming you want to update the 'email' field
        df.loc[index_to_update, 'status'] = 'done'

    # Step 4: Write the updated DataFrame back to the CSV file
    df.to_csv(csv_file_path, index=False)



