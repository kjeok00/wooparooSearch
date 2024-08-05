import pandas as pd

# Load the original wooparooData.csv file
original_file_path = './Lucky_wooparooData.csv'
original_data = pd.read_csv(original_file_path)

# Initialize the final dataframe structure
final_data_dict = {"Left": [], "Right": [], "Wooparoo": [], "Probability": []}

# Initialize variables
current_wooparoo = ""

# Iterate through the original dataframe to populate the final dataframe
for index, row in original_data.iterrows():
    probability = row['Probability']
    if '우파루가 나올 확률%' in probability:
        # Update current wooparoo name
        current_wooparoo = probability.replace(' 우파루가 나올 확률%', '')
    else:
        # Append the information to the final dictionary
        final_data_dict["Left"].append(row['Left'])
        final_data_dict["Right"].append(row['Right'])
        final_data_dict["Wooparoo"].append(current_wooparoo)
        probability_value = float(probability.replace('%', ''))
        final_data_dict["Probability"].append(probability_value)

# Convert the dictionary to a dataframe
final_df = pd.DataFrame(final_data_dict)

# Save the final dataframe to a new CSV file
output_file_path = './Lucky_convertedWooparooData.csv'
final_df.to_csv(output_file_path, index=False)

print(f"Converted file saved to {output_file_path}")
