import os
import glob
import csv

types = ('*.jpg', '*.png', '*.jpeg')
images=[]
for files in types:
    images.extend(glob.glob('./a_faire_2/'+files))
total_images = len(images)
num_batches = (total_images + 200 - 1)//200
batches = [images[i * 200:(i+1)*200] for i in range(num_batches)]
# Open CSV file to write image paths and batch numbers
csv_file = 'image_batch_info.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write header row
    writer.writerow(['Image Path', 'Batch Number'])

    # Iterate over batches and write each image path with its batch number
    for batch_index, batch in enumerate(batches):
        for image_path in batch:
            writer.writerow([image_path, batch_index + 1])  # +1 to make batches 1-indexed

print(f"Image paths and batch numbers have been written to {csv_file}.")

