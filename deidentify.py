import os
import csv
import shutil

if __name__ == '__main__':

    # load and save folders
    original_results_folder = os.path.join(os.path.dirname(__file__), 'results')
    new_results_folder = os.path.join(os.path.dirname(__file__), 'results_deidentified')
    os.makedirs(new_results_folder, exist_ok = True)

    for subject_folder in os.listdir(original_results_folder):
        subject_folder_path = os.path.join(original_results_folder, subject_folder)
        new_subject_folder_path = os.path.join(new_results_folder, subject_folder)
        os.makedirs(new_subject_folder_path, exist_ok = True)

        # skip if not a folder
        if os.path.isfile(subject_folder_path):
            continue
        
        
        for file in os.listdir(subject_folder_path):
            file_path = os.path.join(subject_folder_path, file)

            # skip if not a file
            if os.path.isdir(file_path):
                continue

            elif file == 'consentInfo.csv':
                continue
            
            elif file == 'gaussian_uncorrelated.csv' or file == 'gaussian_vcorrelated.csv' or file == 'unweighted_uncorrelated.csv' or file == 'unweighted_vcorrelated.csv' or file == 'summaryData.csv':
                
                new_save_path = os.path.join(new_subject_folder_path, file)
                new_lines = []
                # read the data and remove identifiers
                with open(file_path, mode = 'r', newline = '') as f:
                    reader = csv.reader(f)
                    lines = list(reader)

                    for i, line in enumerate(lines):
                        if i == 0:
                            header = line[1:]
                            continue
                        new_line = line[1:]
                        new_lines.append(new_line.copy())
                
                # save the new data to the deidentified results folder
                with open(new_save_path, mode = 'w', newline = '') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    for line in new_lines:
                        assert(len(line) == len(header))
                        writer.writerow(line)
                
            else: 
                source_path = file_path
                dest_path = os.path.join(new_subject_folder_path, file)
                shutil.copy(source_path, dest_path)

        
                
                
                
                        




    