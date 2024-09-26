def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Read the header and write it to the output file (adding BaseRateUsed to the header)
        header = infile.readline().strip()
        outfile.write(header + '\n')
        
        # Process each subsequent line
        for line in infile:
            line = line.strip()  # Remove any surrounding whitespace or newlines
            if line:  # Ensure the line is not empty
                fields = line.split('|')
                
                # Ensure the line has enough columns
                item_adjusted_index = 14  # Index of ItemAdjustedEapgWeight (15th column)
                total_payment_index = 11   # Index of TotalPayment (12th column)
                base_rate_index = 15       # Column to which BaseRateUsed will be added (16th column)
                
                if len(fields) <= max(item_adjusted_index, total_payment_index, base_rate_index):
                    print(f"Warning: Skipping line due to insufficient columns: {line}")
                    continue
                
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
                
                # Debugging output
                # print(f"Item Adjusted Values: {item_adjusted_values}")
                # print(f"Total Weight: {total_weight}")
                # print(f"Total Payment: {total_payment}")
                # print(f"BaseRateUsed (Rounded): {base_rate_used}")
                
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
                    new_line = '|'.join(new_fields)
                    outfile.write(new_line + '\n')

# Specify input and output file paths
input_file = r'C:\Users\RTrol\OneDrive\Desktop\EAPG\EAPG_837_Output_9_9_2024_369.csv'
output_file = r'C:\Users\RTrol\OneDrive\Desktop\EAPG\Output.txt'

# Run the function
process_file(input_file, output_file)


