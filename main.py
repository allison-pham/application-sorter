from file_handler import read_file, save_file
from grouping import count_subjects, create_groups
import pandas as pd

# User input
file_path = input("Enter the file path to your CSV file: ")
application_df = read_file(file_path)

# Counter & create groups
subject_counter = count_subjects(application_df)
groups = create_groups(subject_counter)

# New file
sorted_groups = pd.DataFrame(groups)
save_file(sorted_groups, 'sorted_groups.csv')

# df = pd.read_csv('research_program_responses.csv') # Adjust file path

# subject_counter = df['Subject(s) of interest for research (Please check the above document attached)'].value_counts()

# subject_counter_df = subject_counts.reset_index()
# subject_counter_df.columns['Subject(s) of interest for research (Please check the above document attached)']