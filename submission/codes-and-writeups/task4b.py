# Create and test a pipeline dependency

from collections import defaultdict

#read relations data
raw_data_path = 'data/raw/'

file = open(raw_data_path + 'relations.txt', 'r')
Lines = file.readlines()

relations = []

for line in Lines:
    relations.append([int(i) for i in line.split('->')])

# read the list of task ids
file = open(raw_data_path + 'task_ids.txt', 'r')
Lines = file.readlines()
task_ids = [int(i) for i in Lines[0].split(',')]

# read the test starting task and goal task

file = open(raw_data_path + 'question.txt', 'r')
Lines = file.readlines()

start_goal_tasks = []

for i, line in enumerate(Lines):
    #there can be multiple starting tasks as input
    # the starting task is a list
    if i == 0:
        start_goal_tasks.append([int(i) for i in line.split(':')[1].split(',')])
    #the goal task is an integer
    if i == 1:
        start_goal_tasks.append(int(line.split(':')[1]))

#Create a ipa (immediate preceeding assignment) dict for each task
ipa_dict = defaultdict(list)

for ipa, task in relations:
    ipa_dict[task].append(ipa)

#create an empty list for all activities without ipa
for task in task_ids:
    if task not in ipa_dict.keys():
        ipa_dict[task] = []

# Create function

def tasks_pipeline(start,goal,ipa_dict):

    if goal not in ipa_dict.keys():
        print(f'Goal task {goal} is not in the IPA dictionary.')
        return []

    # the list activity is used for the final output
    activity = [goal]

    #get the ipa for the goal activity
    ipa = ipa_dict[goal]

    while len(ipa) > 0:
        # add all the ipas into the activity queue
        activity.extend(ipa)
        # update ipa list for based on activites on current ipa list
        # do not include the ipas for the start activity
        ipa = [ipa_dict[i] for i in ipa if i not in start]
        # flatten the list
        ipa = [task for task_ipa in ipa for task in task_ipa]

    for task in start:
        if task not in activity:
            print(f'Starting task {task} is not required.')

    return sorted(set(activity), key=activity.index,reverse=True)

#Test function

#pipeline = tasks_pipeline(start_goal_tasks[0],start_goal_tasks[1],ipa_dict)
pipeline = tasks_pipeline(start_goal_tasks[0],start_goal_tasks[1],ipa_dict)
print(pipeline)
