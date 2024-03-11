from collections import Counter
import pandas as pd

def count_subjects(df):
    subjects = []
    for subject in df['Subject(s) of interest for research (Please check the above document attached)'].str.split(','):
        subjects.extend(subject)
    return Counter(subjects)
    # Archive 1
    # subject_counter = Counter(list(df['Subject(s) of interest for research (Please check the above document attached)']))

    # for subject, count in subject_counter.items():
    # print(f"Subject: {subject}\tNumber of Respondents: {count}")


    # Archive 2
    # return Counter(df['Subject(s) of interest for research (Please check the above document attached)'])

def count_subjects(df):
    subject_list = []
    for subjects in df['Subject(s) of interest for research (Please check the above document attached)'].str.split(','):
        subject_list.extend(subjects)
    return Counter(subject_list)

def create_groups(df, max_members=4):
    groups = []
    df = preprocess_data(df.copy())  # Preprocess and ensure we're not modifying the original DataFrame
    df.reset_index(drop=True, inplace=True)

    # Split the DataFrame based on roles
    roles_to_exclude = ['Mentor', 'Judge']
    df_primary_roles = df[~df['Which role(s) would you like to be considered for?'].isin(roles_to_exclude)]  # Researchers and Research Leads
    df_secondary_roles = df[df['Which role(s) would you like to be considered for?'].isin(roles_to_exclude)]  # Mentors and Judges

    # Process primary roles (Researchers and Research Leads)
    df_primary_roles_exploded = df_primary_roles.explode('Subject(s) of interest for research (Please check the above document attached)')
    subject_grouped = df_primary_roles_exploded.groupby('Subject(s) of interest for research (Please check the above document attached)')
    
    for subject, group_df in subject_grouped:
        count = len(group_df)
        full_groups, remainder = divmod(count, max_members)
        
        for i in range(full_groups):
            members_df = group_df.iloc[i*max_members:(i+1)*max_members]
            members_names = members_df['First Name'] + ' ' + members_df['Last Name']
            groups.append({"Role": "Research", "Subject": subject, "Group": i+1, "Group Size": max_members, "Members": ', '.join(members_names)})

        if remainder > 0:
            members_df = group_df.iloc[-remainder:]
            members_names = members_df['First Name'] + ' ' + members_df['Last Name']
            groups.append({"Role": "Research", "Subject": subject, "Group": full_groups + 1, "Group Size": remainder, "Members": ', '.join(members_names)})

    # Process secondary roles (Mentors and Judges) separately
    for role in roles_to_exclude:
        df_role = df_secondary_roles[df_secondary_roles['Which role(s) would you like to be considered for?'] == role]
        count = len(df_role)
        full_groups, remainder = divmod(count, max_members)
        
        for i in range(full_groups):
            members_df = df_role.iloc[i*max_members:(i+1)*max_members]
            members_names = members_df['First Name'] + ' ' + members_df['Last Name']
            groups.append({"Role": role, "Group": i+1, "Group Size": max_members, "Members": ', '.join(members_names)})

        if remainder > 0:
            members_df = df_role.iloc[-remainder:]
            members_names = members_df['First Name'] + ' ' + members_df['Last Name']
            groups.append({"Role": role, "Group": full_groups + 1, "Group Size": remainder, "Members": ', '.join(members_names)})

    return groups

    # Archive 1
    # groups = []
    # for subject, count in subject_counter.items():
    #     full_groups, remainder = divmod(count, max_members)
        
    #     for i in range(full_groups):
    #         groups.append({"Subject": subject, "Group": i+1, "Group Size": max_members})
        
    #     if remainder > 0:
    #         groups.append({"Subject": subject, "Group": full_groups + 1, "Group Size": remainder})
    #     # groups += [f"Subject: {subject}\t Group size: {remainder}"]
    
    # return groups


    # Archive 2
    # groups = []
    # # Reset index to ensure unique labels
    # df.reset_index(drop=True, inplace=True)
    
    # # Expanding the subjects into separate rows
    # # Note: Adjust the splitting based on your actual data format if needed

    # df['Subject(s) of interest for research (Please check the above document attached)'] = df['Subject(s) of interest for research (Please check the above document attached)'].str.split(',')
    # df_exploded = df.explode('Subject(s) of interest for research (Please check the above document attached)')
    
    # subject_grouped = df_exploded.groupby('Subject(s) of interest for research (Please check the above document attached)')
    
    # for subject, group_df in subject_grouped:
    #     count = len(group_df)
    #     full_groups, remainder = divmod(count, max_members)
        
    #     for i in range(full_groups):
    #         members_df = group_df.iloc[i*max_members:(i+1)*max_members]
    #         members_names = members_df['First Name'] + ' ' + members_df['Last Name']
    #         groups.append({"Subject": subject, "Group": i+1, "Group Size": max_members, "Members": ', '.join(members_names)})

    #     if remainder > 0:
    #         members_df = group_df.iloc[-remainder:]
    #         members_names = members_df['First Name'] + ' ' + members_df['Last Name']
    #         groups.append({"Subject": subject, "Group": full_groups + 1, "Group Size": remainder, "Members": ', '.join(members_names)})

    # return groups


    # Archive 3
        # groups = []
    # df.reset_index(drop=True, inplace=True)

    # # Split the DataFrame based on roles
    # roles_to_exclude = ['Mentor', 'Judge']
    # df_primary_roles = df[~df['Which role(s) would you like to be considered for?'].isin(roles_to_exclude)]  # Researchers and Research Leads
    # df_secondary_roles = df[df['Which role(s) would you like to be considered for?'].isin(roles_to_exclude)]  # Mentors and Judges

    # # Process primary roles (Researchers and Research Leads)
    # df_primary_roles['Subject(s) of interest for research (Please check the above document attached)'] = df_primary_roles['Subject(s) of interest for research (Please check the above document attached)'].str.split(',')
    # df_primary_exploded = df_primary_roles.explode('Subject(s) of interest for research (Please check the above document attached)')

    # subject_grouped = df_primary_exploded.groupby('Subject(s) of interest for research (Please check the above document attached)')
    
    # for subject, group_df in subject_grouped:
    #     count = len(group_df)
    #     full_groups, remainder = divmod(count, max_members)
        
    #     for i in range(full_groups):
    #         members_df = group_df.iloc[i*max_members:(i+1)*max_members]
    #         members_names = members_df['First Name'] + ' ' + members_df['Last Name']
    #         groups.append({"Role": "Research", "Subject": subject, "Group": i+1, "Group Size": max_members, "Members": ', '.join(members_names)})

    #     if remainder > 0:
    #         members_df = group_df.iloc[-remainder:]
    #         members_names = members_df['First Name'] + ' ' + members_df['Last Name']
    #         groups.append({"Role": "Research", "Subject": subject, "Group": full_groups + 1, "Group Size": remainder, "Members": ', '.join(members_names)})

    # # Process secondary roles (Mentors and Judges) separately
    # # This assumes you want them grouped by their role, not by subject
    # for role in roles_to_exclude:
    #     df_role = df_secondary_roles[df_secondary_roles['Which role(s) would you like to be considered for?'] == role]
    #     count = len(df_role)
    #     full_groups, remainder = divmod(count, max_members)
        
    #     for i in range(full_groups):
    #         members_df = df_role.iloc[i*max_members:(i+1)*max_members]
    #         members_names = members_df['First Name'] + ' ' + members_df['Last Name']
    #         groups.append({"Role": role, "Group": i+1, "Group Size": max_members, "Members": ', '.join(members_names)})

    #     if remainder > 0:
    #         members_df = df_role.iloc[-remainder:]
    #         members_names = members_df['First Name'] + ' ' + members_df['Last Name']
    #         groups.append({"Role": role, "Group": full_groups + 1, "Group Size": remainder, "Members": ', '.join(members_names)})

    # return groups

def preprocess_data(df):
    # Ensure role and subject fields are consistently formatted
    df['Which role(s) would you like to be considered for?'] = df['Which role(s) would you like to be considered for?'].str.strip()  # Assuming you've renamed the column for simplicity
    df['Subject(s) of interest for research (Please check the above document attached)'] = df['Subject(s) of interest for research (Please check the above document attached)']\
        .str.lower()\
        .str.split(',')\
        .apply(lambda subjects: [subject.strip() for subject in subjects])
    return df