import pandas as pd

def read_excel_file(file_path):
    """
    Reads data from an Excel .xlsx file into a pandas DataFrame.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the Excel file,
                          or None if an error occurs.
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return None
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return None


import pandas as pd

def modify_review_labels(file_path, app_id, column_updates):
    """
    Modifies labels in specified columns of an Excel .xlsx file
    for rows matching the given 'app_id'.

    Args:
        file_path (str): The path to the Excel file.
        app_id (int): The 'app_id' to filter rows.
        column_updates (dict): A dictionary where keys are column names
                               (e.g., 'Genel Duygu', 'AI', 'Oynanıs') and
                               values are the new labels ('nötr', 'olumlu', 'olumsuz').

    Returns:
        bool: True if the changes were successfully written to the file,
              False otherwise.
    """
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return False
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return False

    # Find the rows where 'app_id' matches
    mask = df['app_id'] == app_id

    # Check if any matching rows were found
    if mask.any():
        # Iterate through the column updates and apply changes
        for column, new_label in column_updates.items():
            if column in df.columns:
                df.loc[mask, column] = new_label
            else:
                print(f"Warning: Column '{column}' not found in the Excel file.")

        try:
            # Write the modified DataFrame back to the Excel file
            df.to_excel(file_path, index=False)
            print(f"Successfully updated labels for app_id '{app_id}' in '{file_path}'")
            print(f"Changes applied to columns: {column_updates}")
            return True
        except Exception as e:
            print(f"An error occurred while writing to the Excel file: {e}")
            return False
    else:
        print(f"No rows found with app_id '{app_id}' in '{file_path}'")
        return False



# Example usage:
if __name__ == "__main__":
    excel_file = "./dataset/input/reviews_test.xlsx"  # Replace with the actual path to your file
    data_frame = read_excel_file(excel_file)

    if data_frame is not None:
        print("Successfully read the Excel file:")
        print(data_frame)

        # You can now work with the 'data_frame'
        # For example, print the first 5 rows:
        print("\nFirst 5 rows:")
        print(data_frame.head())

        # Or get some information about the DataFrame:
        print("\nDataFrame info:")
        data_frame.info()



    # Example: Update labels for the first app_id
    first_app_id = 1245620 # Assuming 'app_id' is a column in the DataFrame
    updates = {
        "Grafik": "MERHABAAAA",
        "Ses ve Muzik": "MERHABAAAA",
        "Oyun Dunyasi": "MERHABAAAA",
        "Topluluk ve Sosyal": "MERHABAAAA",
        "Hikaye ve Senaryo": "MERHABAAAA",
        "Performans ve Teknik": "MERHABAAAA",
        "Genel Duygu": "MERHABAAAA",
        "AI": "MERHABAAAA",
        "Oynanis": "MERHABAAAA",

    }
    success = modify_review_labels(excel_file, first_app_id, updates)
    print(f"Update operation successful: {success}\n")