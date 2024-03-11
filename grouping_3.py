def create_groups(df, max_members=4):
    groups = []
    df.reset_index(drop=True, inplace=True)

    # Normalize and split roles into lists for easier processing
    df['Which role(s) would you like to be considered for?'] = df['Which role(s) would you like to be considered for?'].str.lower().str.split(',')

    # Function to check if a participant is a mentor or judge
    def is_mentor_or_judge(roles_list):
        roles_to_check = ['mentor', 'judge']
        return any(role.strip() in roles_to_check for role in roles_list)

    # Separate DataFrame based on whether they are a mentor or judge
    df['IsMentorOrJudge'] = df['Which role(s) would you like to be considered for?'].apply(is_mentor_or_judge)
    df_mentors_judges = df[df['IsMentorOrJudge']]
    df_researchers = df[~df['IsMentorOrJudge']]

    # Process researchers and research leads
    if not df_researchers.empty:
        df_researchers['Subject(s) of interest for research (Please check the above document attached)'] = df_researchers['Subject(s) of interest for research (Please check the above document attached)'].str.lower().str.split(',').apply(lambda x: [item.strip() for item in x])
        df_research_exploded = df_researchers.explode('Subject(s) of interest for research (Please check the above document attached)')
        subject_grouped = df_research_exploded.groupby('Subject(s) of interest for research (Please check the above document attached)')

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

    # Process mentors and judges
    if not df_mentors_judges.empty:
        role_grouped = df_mentors_judges.groupby('Which role(s) would you like to be considered for?')
        for role, group_df in role_grouped:
            count = len(group_df)
            full_groups, remainder = divmod(count, max_members)

            for i in range(full_groups):
                members_df = group_df.iloc[i*max_members:(i+1)*max_members]
                members_names = members_df['First Name'] + ' ' + members_df['Last Name']
                groups.append({"Role": role.title(), "Group": i+1, "Group Size": max_members, "Members": ', '.join(members_names)})

            if remainder > 0:
                members_df = group_df.iloc[-remainder:]
                members_names = members_df['First Name'] + ' ' + members_df['Last Name']
                groups.append({"Role": role.title(), "Group": full_groups + 1, "Group Size": remainder, "Members": ', '.join(members_names)})

    return groups
