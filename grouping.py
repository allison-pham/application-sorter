def create_groups(df, max_members=4):
    groups = []
    df.reset_index(drop=True, inplace=True)

    # Normalize the 'Role' column to lowercase for consistent comparison
    df['NormalizedRoles'] = df['Which role(s) would you like to be considered for?'].str.lower()

    # Mark participants as 'Mentor/Judge' if their roles include 'mentor' or 'judge'
    df['GroupCategory'] = df['NormalizedRoles'].apply(lambda roles: 'Mentor/Judge' if 'mentor' in roles or 'judge' in roles else 'Research')

    # Separate the DataFrame based on the GroupCategory
    df_research = df[df['GroupCategory'] == 'Research']
    df_mentors_judges = df[df['GroupCategory'] == 'Mentor/Judge']

    # Process Research participants
    if not df_research.empty:
        # Assuming the 'Subject(s) of interest for research' need to be split and exploded
        df_research['Subjects'] = df_research['Subject(s) of interest for research (Please check the above document attached)'].str.lower().str.split(',').apply(lambda x: [item.strip() for item in x])
        df_research_exploded = df_research.explode('Subjects')

        subject_grouped = df_research_exploded.groupby('Subjects')
        for subject, group_df in subject_grouped:
            process_group(group_df, subject, groups, max_members, "Research")

    # Process Mentors and Judges
    if not df_mentors_judges.empty:
        role_grouped = df_mentors_judges.groupby('NormalizedRoles')
        for roles, group_df in role_grouped:
            process_group(group_df, roles, groups, max_members, "Mentor/Judge")

    return groups

def process_group(group_df, identifier, groups, max_members, category):
    count = len(group_df)
    full_groups, remainder = divmod(count, max_members)
    
    for i in range(full_groups):
        members_df = group_df.iloc[i*max_members:(i+1)*max_members]
        members_names = members_df['First Name'] + ' ' + members_df['Last Name']
        groups.append({"Category": category, "Identifier": identifier, "Group": i+1, "Group Size": max_members, "Members": ', '.join(members_names)})

    if remainder > 0:
        members_df = group_df.iloc[-remainder:]
        members_names = members_df['First Name'] + ' ' + members_df['Last Name']
        groups.append({"Category": category, "Identifier": identifier, "Group": full_groups + 1, "Group Size": remainder, "Members": ', '.join(members_names)})
