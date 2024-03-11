import pandas as pd
from collections import Counter

def create_groups(df, max_members=4):
    groups = []
    df.reset_index(drop=True, inplace=True)
    
    # Define the roles
    roles_to_exclude = ['Mentor', 'Judge']
    
    # Normalize and split the roles for each participant
    # Assumes the roles column is 'Which role(s) would you like to be considered for?'
    df['Which role(s) would you like to be considered for?'] = df['Which role(s) would you like to be considered for?'].str.split(',')
    df_exploded_roles = df.explode('Which role(s) would you like to be considered for?')
    df_exploded_roles['Which role(s) would you like to be considered for?'] = df_exploded_roles['Which role(s) would you like to be considered for?'].str.strip()  # Strip whitespace
    
    # Separate DataFrames based on roles
    df_secondary_roles = df_exploded_roles[df_exploded_roles['Which role(s) would you like to be considered for?'].isin(roles_to_exclude)]
    # Drop duplicates since a person listing multiple roles including mentor should only appear once in the mentor/judge groups
    df_secondary_roles = df_secondary_roles.drop_duplicates(subset=['First Name', 'Last Name', 'Email'])  # Assuming 'Email' or another unique identifier is available

    # Filter out mentors and judges from the primary roles dataframe
    df_primary_filtered = df[~df['Email'].isin(df_secondary_roles['Email'])]  # Use 'Email' or another unique identifier
    
    # Process primary roles (excluding Mentors and Judges)
    # Similar to your existing logic but applied on df_primary_filtered
    process_primary_roles(df_primary_filtered, groups, max_members)
    
    # Process secondary roles (Mentors and Judges)
    process_secondary_roles(df_secondary_roles, groups, max_members)

    return groups

def process_primary_roles(df, groups, max_members):
    df['Subject(s) of interest for research (Please check the above document attached)'] = df['Subject(s) of interest for research (Please check the above document attached)'].str.lower().str.split(',').apply(lambda x: [item.strip() for item in x])
    df_primary_exploded = df.explode('Subject(s) of interest for research (Please check the above document attached)')
    subject_grouped = df_primary_exploded.groupby('Subject(s) of interest for research (Please check the above document attached)')
    
    for subject, group_df in subject_grouped:
        create_group_entries(group_df, subject, "Research", groups, max_members)

def process_secondary_roles(df, groups, max_members):
    role_grouped = df.groupby('Which role(s) would you like to be considered for?')
    
    for role, group_df in role_grouped:
        create_group_entries(group_df, None, role, groups, max_members)

def create_group_entries(group_df, subject, role, groups, max_members):
    count = len(group_df)
    full_groups, remainder = divmod(count, max_members)
    
    for i in range(full_groups):
        members_df = group_df.iloc[i*max_members:(i+1)*max_members]
        members_names = members_df['First Name'] + ' ' + members_df['Last Name']
        group_entry = {"Role": role, "Group": i+1, "Group Size": max_members, "Members": ', '.join(members_names)}
        if subject:
            group_entry["Subject"] = subject
        groups.append(group_entry)

    if remainder > 0:
        members_df = group_df.iloc[-remainder:]
        members_names = members_df['First Name'] + ' ' + members_df['Last Name']
        group_entry = {"Role": role, "Group": full_groups + 1, "Group Size": remainder, "Members": ', '.join(members_names)}
        if subject:
            group_entry["Subject"] = subject
        groups.append(group_entry)