"""
How to run:
python 01_Element-Wise.py

"""

import apache_beam as beam
import os
from pathlib import Path

# Get the directory of the current script
script_dir = Path(__file__).parent

# # Define the path to the CSV file relative to the script's directory
# file_path = script_dir / 'Data_Source' / 'file_1.csv'

# # Check if the file exists
# if file_path.exists():
#     print("File exists.")
# else:
#     print("File does not exist.")

input_offline = script_dir / 'Data_Source' / "offline.csv"
input_online = script_dir / 'Data_Source' / "online.csv"

print(f"Offline FIle Path : {input_offline}")

if os.path.exists(input_offline):
    print("Offline File exists.")
else:
    print("Offline File does not exist.")

if os.path.exists(input_online):
    print("Online File exists.")
else:
    print("Online File does not exist.")

# Extract productId, and Quantity from line
class Extract(beam.DoFn):
    def process(self, element):
        _, productId, _, _, quantity = element.split(',')
        return [(productId, int(quantity))]
        # return [(productId, quantity)]
    
# Function to print output
class PrintOutput(beam.DoFn):
    def process(self, element):
        print(element)
        yield element

p = beam.Pipeline()

# Read File and extract product id & quantity
offline_data = (
    p 
    | "read offline file" >> beam.io.ReadFromText(str(input_offline), skip_header_lines=1) 
    | "Extract relevant fields from offline file" >> beam.ParDo(Extract())
    # | "Print output" >> beam.ParDo(PrintOutput())
)

# Read File and extract product id & quantity
online_data = (
    p 
    | "read online file" >> beam.io.ReadFromText(str(input_online), skip_header_lines=1) 
    | "Extract relevant fields from online file" >> beam.ParDo(Extract())
    # | "Print output" >> beam.ParDo(PrintOutput())
)

# Combine lines from both files, create sum of quantity per product and get top 5 selling products.
(
    (offline_data, online_data)
    | beam.Flatten()
    | beam.CombinePerKey(sum)
    | beam.Map(lambda product_qty: (product_qty[1], product_qty[0]))
    | beam.combiners.Top.Largest(5)
    | beam.LogElements()
)

p.run()

