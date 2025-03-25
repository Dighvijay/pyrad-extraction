import csv
import os
import pandas as pd

def split_csv(input_csv, output_dir="output_csv_files"):
    # Check if the input file exists
    if not os.path.isfile(input_csv):
        print(f"File '{input_csv}' does not exist.")
        return
    
    # Create a directory to store the output CSV files
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the input CSV file
    with open(input_csv, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)  # Read the header row
        
        for row_number, row in enumerate(csvreader, start=1):
            # Define the output CSV file name
            output_csv = os.path.join(output_dir, f'row_{row_number}.csv')
            
            # Write the row to a new CSV file
            with open(output_csv, mode='w', newline='') as outputfile:
                csvwriter = csv.writer(outputfile)
                csvwriter.writerow(header)  # Write the header
                csvwriter.writerow(row)     # Write the single row
                
            print(f"Created {output_csv}")

def combine_csv(input_dir, output_csv):
    # List all CSV files in the input directory
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the directory.")
        return
    
    # Create/open the output CSV file for writing
    with open(output_csv, mode='w', newline='') as outputfile:
        csvwriter = csv.writer(outputfile)
        
        header_written = False
        for csv_file in csv_files:
            csv_path = os.path.join(input_dir, csv_file)
            
            # Read each input CSV file
            with open(csv_path, mode='r', newline='') as inputfile:
                csvreader = csv.reader(inputfile)
                header = next(csvreader)  # Read the header row
                
                # Write the header only once
                if not header_written:
                    csvwriter.writerow(header)
                    header_written = True
                
                # Write the data rows
                for row in csvreader:
                    csvwriter.writerow(row)
            
            print(f"Processed {csv_file}")

def combine_csv_column_wise(csv_file1, csv_file2, output_file):
    # Read CSV files into dataframes
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    
    # Combine dataframes column-wise
    combined_df = pd.concat([df1, df2], axis=1)
    
    # Save the combined dataframe to the output file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV saved to {output_file}")

def generate_csv_from_folder(images_folder_path, masks_folder_path, label = 255):
    
    image_files = sorted(os.listdir(images_folder_path))
    mask_files = sorted(os.listdir(masks_folder_path))
    output_csv = 'output.csv'
    
    print(mask_files)
    if len(image_files) != len(mask_files):
        raise ValueError("The number of files in the Images and Masks folders do not match.")

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Image', 'Mask', 'Label'])
        # Write the file paths and label
        for image, mask in zip(image_files, mask_files):
            writer.writerow([os.path.join(images_folder_path, image), os.path.join(masks_folder_path, mask), label])

    print(f'CSV file has been created at {output_csv}')
#Example Usage
if __name__ == "__main__":
    #input_dir = '/Users/dighvijaygiri/Codes/pyrad/pyrad_error'
    #output_csv = 'combined_output.csv'
    #combine_csv(input_dir, output_csv)


    # Usage example
    #input_csv = '/home/jovyan/images/sample.csv'
    #split_csv(input_csv)
    
    #combine_csv_column_wise('CBIS_DDSM_TRAIN.csv', 'combined_output.csv', 'results.csv')
    
    generate_csv_from_folder('/Users/dighvijaygiri/Codes/pyrad/Images', '/Users/dighvijaygiri/Codes/pyrad/Masks')