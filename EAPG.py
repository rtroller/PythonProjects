from collections import defaultdict
import csv

# Function to process the input file and write the output
def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Read the header and split it
        header = infile.readline().strip().split('|')
        
        # Insert 'SequenceNumber' after the first field (AccountNumber)
        header.insert(1, 'SequenceNumber')
        
        # Set the value in the 4th position (index 3) to 'ItemServiceDate'
        if len(header) > 3:
            header[3] = 'ItemServiceDate'
        
        # Write the updated header to the output file
        outfile.write('|'.join(header) + '\n')
        
        # Dictionary to track the sequence number for each AccountNumber
        account_sequence_counters = defaultdict(int)

        # Process each subsequent line
        for line in infile:
            line = line.strip()  # Remove any surrounding whitespace or newlines
            if line:  # Ensure the line is not empty
                fields = line.split('|')
                
                # Ensure the line has enough columns
                item_adjusted_index = 14  # Index of ItemAdjustedEapgWeight (15th column)
                total_payment_index = 11   # Index of TotalPayment (12th column)
                base_rate_index = 15       # Column to which BaseRateUsed will be added (16th column)
                account_number_index = 0   # Assuming AccountNumber is the 1st column
                
                if len(fields) <= max(item_adjusted_index, total_payment_index, base_rate_index, account_number_index):
                    print(f"Warning: Skipping line due to insufficient columns: {line}")
                    continue
                
                # Retrieve the AccountNumber
                account_number = fields[account_number_index]

                # Sum up the comma-separated values in the ItemAdjustedEapgWeight field
                item_adjusted_values = list(map(float, fields[item_adjusted_index].split(',')))
                total_weight = sum(item_adjusted_values)

                # Divide the TotalPayment by the total weight to calculate BaseRateUsed
                try:
                    total_payment = float(fields[total_payment_index])
                except ValueError:
                    print(f"Error converting TotalPayment to float: {fields[total_payment_index]}")
                    continue

                # Calculate BaseRateUsed and round to two decimal places
                base_rate_used = round(total_payment / total_weight, 2) if total_weight != 0 else 0
                
                # Insert the BaseRateUsed as a new value in the 15th column
                fields[base_rate_index] = f"{base_rate_used:.2f}"

                # Identify the first field with commas to determine number of records
                first_comma_field_index = -1
                for i, field in enumerate(fields):
                    if ',' in field:
                        first_comma_field_index = i
                        break
                
                # Split the first comma-delimited field and find its length
                main_comma_field_values = fields[first_comma_field_index].split(',')
                num_values = len(main_comma_field_values)
                
                # Split other fields with commas and ensure they have the same length as the main field
                split_fields = []
                for field in fields:
                    values = field.split(',')
                    # If the field has commas and is not the main comma-delimited field
                    if len(values) > 1 and len(values) < num_values:
                        # Repeat the last value to match the length of the main field
                        values += [values[-1]] * (num_values - len(values))
                    # If the field does not contain enough values, repeat its last value
                    elif len(values) < num_values:
                        values = [values[0]] * num_values
                    split_fields.append(values)
                
                # Generate records based on the number of values in the main comma field
                for i in range(num_values):
                    new_fields = [values[i] for values in split_fields]

                    # Increment the sequence number for this AccountNumber for each record
                    account_sequence_counters[account_number] += 1
                    sequence_number = account_sequence_counters[account_number]
                    
                    # Calculate new TotalPayment as the product of current ItemAdjustedEapgWeight and BaseRateUsed
                    try:
                        current_weight = float(new_fields[item_adjusted_index])
                        current_base_rate_used = float(new_fields[base_rate_index])
                        new_total_payment = round(current_weight * current_base_rate_used, 2)
                        new_fields[total_payment_index] = f"{new_total_payment:.2f}"
                    except ValueError:
                        print(f"Error calculating new TotalPayment for record: {new_fields}")
                        continue

                    # Add the sequence number to the new_fields list
                    new_fields.insert(account_number_index + 1, str(sequence_number))

                    # Write the new record to the output file
                    new_line = '|'.join(new_fields)
                    outfile.write(new_line + '\n')

# Function to remove the column at index 4
def remove_column_at_index_4(output_file):
    # Read the file and process the rows
    with open(output_file, 'r') as infile:
        reader = csv.reader(infile, delimiter='|')
        rows = [row for row in reader]
    
    # Remove the column at index 4 for each row
    for row in rows:
        if len(row) > 4:
            del row[4]
    
    # Write the updated rows back to the file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='|')
        writer.writerows(rows)

# Specify input and output file paths
input_file = r'C:\Users\RTrol\OneDrive\Desktop\EAPG\EAPG_837_Output_9_9_2024_369.csv'
output_file = r'C:\Users\RTrol\OneDrive\Desktop\EAPG\Output.txt'

# Run the function to process the file
process_file(input_file, output_file)

# Now remove the column at index 4
remove_column_at_index_4(output_file)
