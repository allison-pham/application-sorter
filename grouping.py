from collections import Counter

def count_subjects(df):
    return Counter(df['Subject(s) of interest for research (Please check the above document attached)'])

    # subject_counter = Counter(list(df['Subject(s) of interest for research (Please check the above document attached)']))

    # for subject, count in subject_counter.items():
    # print(f"Subject: {subject}\tNumber of Respondents: {count}")

def create_groups(subject_counter, max_members = 4):
    groups = []
    for subject, count in subject_counter.items():
        full_groups, remainder = divmod(count, max_members)
        groups += [f"Subject: {subject}\t Group size: {remainder}"]
    
    return groups