from collections import Counter
import pandas as pandas

# User input
file_path = input("Enter the file path to the file. Example file type: .csv")
application_df = pd.read_csv(file_path)

# Counter
subject_counter = Counter(list(df['Subject(s) of interest for research (Please check the above document attached)']))

# Archive
# df = pd.read_csv('research_program_responses.csv') # Adjust file path

# subject_counter = df['Subject(s) of interest for research (Please check the above document attached)'].value_counts()

# subject_counter_df = subject_counts.reset_index()
# subject_counter_df.columns['Subject(s) of interest for research (Please check the above document attached)']
