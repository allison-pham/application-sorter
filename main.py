from file_handler import read_file, save_file
from grouping import create_groups
import pandas as pd

def sort_applications(file_path):
    df = read_file(file_path)
    # df = pd.read_csv('research_program_responses.csv') # Adjust file path
    groups = create_groups(df)  # Corrected call
    save_file(pd.DataFrame(groups), 'sorted_groups_with_names.csv')
    print(f"Groups sorted and saved with names to 'sorted_groups_with_names.csv'. Total groups created: {len(groups)}")

if __name__ == "__main__":
    file_path = r"C:\-AL-\all projects\vs code projects\personal-projects\application-sorter\research_program_responses.csv"
    sort_applications(file_path)