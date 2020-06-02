import random
import os


    
def roll_initial_stats(attributes,skills):
    stats = {
        x : random.randint(1,10) for x in attributes
        }
    additional_stats = { x : stats[skills[x]] for x in skills}
    stats.update(additional_stats)
    
    return stats

def run_stat_roulette(
    character_stat_list,
    n_rounds=5
    ):
    """
    Goes in turns stealing points for stats from one character and giving them to another.
    """
    n_characters = len(character_stat_list)
    available_stats = {
        x : set(character_stat_list[0])
        for x in range(n_characters-1)
        }
    print(available_stats)
    def steal_points(amount, self_index, steal_attempts=0):
        if steal_attempts > 20:
            return False
        else:
            while(True):
                available_targets = set(range(n_characters-1)) - {self_index}
                target_index = random.sample(available_targets, 1).pop()

                target_available_stats = available_stats[target_index]
                self_available_stats = available_stats[self_index]
                stealable_stats = target_available_stats & self_available_stats
                # if no skills are available to steal:
                if len(stealable_stats) == 0:
                    steal_attempts+=1
                    # try again with another random target
                    steal_points(amount, self_index, steal_attempts)
                # if skills are available to steal:
                else:
                    # choose a skill
                    chosen_skill = random.sample(stealable_stats,1).pop()
                    # make it unavailable for future
                    available_stats[self_index].remove(chosen_skill)
                    available_stats[target_index].remove(chosen_skill)
                    # update your own stats and the targets stats
                    character_stat_list[self_index][chosen_skill] += amount
                    character_stat_list[target_index][chosen_skill] -= amount
                    return True
    
    for round_number in range(n_rounds):
        for character_number in range(n_characters-1):
            steal_points(round_number, character_number)
    
    return character_stat_list

def get_full_stats(
    n_characters,
    attributes = ['Violence','Brains','Chutzpah','Mechanics'],
    skills = {
        'Athletics' : 'Violence',
        'Guns' : 'Violence',
        'Melee' : 'Violence',
        'Throw' : 'Violence',
        'Science' : 'Brains',
        'Psychology' : 'Brains',
        'Bureaucracy' : 'Brains',
        'Alpha Complex' : 'Brains',
        'Bluff' : 'Chutzpah',
        'Charm' : 'Chutzpah',
        'Intimidate' : 'Chutzpah',
        'Stealth' : 'Chutzpah',
        'Operate' : 'Mechanics',
        'Engineer' : 'Mechanics',
        'Program' : 'Mechanics',
        'Demolitions' : 'Mechanics'        
        }
    ):
    initial_stats = [roll_initial_stats(attributes, skills) for i in range(n_characters)]
    stats_updated = run_stat_roulette(initial_stats, n_rounds=5)
    return stats_updated


def read_txt_files():
    all_files = os.listdir()
    txt_files = [x[:-4] for x in all_files if '.txt' in x]
    return txt_files


def load_configs(files='all'):
    if files == 'all':
        files = read_txt_files()
    configs = {}
    for filename in files:
        with open(filename + '.txt', 'r') as f:
            configs[filename] = set(x.strip() for x in f.readlines())
    return configs


def fit_out_characters(n_characters):
    configs = load_configs()

    for i in range(n_characters-1):
        data = {}

        service_group_full = random.sample(configs['service_groups'], 1).pop()    
        data['Service Group Name']= service_group_full.split(': ')[0]
        data['Service Group Description'] = service_group_full.split(': ')[1]

        mutant_power_full = random.sample(configs['mutant_powers'], 1).pop()
        data['Mutant Power Name']= mutant_power_full.split(': ')[0]
        data['Mutant Power Description'] = mutant_power_full.split(': ')[1]

        secret_society_full = random.sample(configs['secret_societies'], 1).pop()
        data['Secret Society Name'] = secret_society_full.split(': ')[0]
        data['Secret Society Description'] = secret_society_full.split(': ')[1]

        skill_1 = random.sample(configs['secret_skills'], 1).pop()
        skill_2 = random.sample(configs['secret_skills'], 1).pop()
        skill_3 = random.sample(configs['silly_skills'], 1).pop()
        data['Secret Skill 1 Name']         = skill_1.split(': ')[0]
        data['Secret Skill 1 Description']  = skill_1.split(': ')[1]
        data['Secret Skill 2 Name']         = skill_2.split(': ')[0]
        data['Secret Skill 2 Description']  = skill_2.split(': ')[1]
        data['Secret Skill 3 Name']         = skill_3.split(': ')[0]
        data['Secret Skill 3 Description']  = skill_3.split(': ')[1]
        
        data['Character Quirk'] = random.sample(configs['character_quirks'], 1).pop()

        for i, equip in enumerate(configs['standard_equipment']):

# csv_columns = [
#     'Base Equipment 1-n',
#     'Additional Equipment 1-n'
#     'Violence',
#     'Brains',
#     'Chutzpah',
#     'Mechanics',
#     'Athletics',
#     'Guns',
#     'Melee',
#     'Throw',
#     'Science',
#     'Psychology',
#     'Bureaucracy',
#     'Alpha Complex',
#     'Bluff',
#     'Charm',
#     'Intimidate',
#     'Stealth',
#     'Operate',
#     'Engineer',
#     'Program',
#     'Demolitions'
# ]


# csv_columns = [
#     'Service Group Name',
#     'Service Group Description',
#     'Mutant Power Name',
#     'Mutant Power Description',
#     'Secret Society',
#     'Secret Skill 1 Name',
#     'Secret Skill 1 Description',
#     'Secret Skill 2 Name',
#     'Secret Skill 2 Description',
#     'Secret Skill 3 Name',
#     'Secret Skill 3 Description',
#     'Character Quirk 1',
#     'Character Quirk 2',
#     'Base Equipment 1-n',
#     'Additional Equipment 1-n'
#     'Violence',
#     'Brains',
#     'Chutzpah',
#     'Mechanics',
#     'Athletics',
#     'Guns',
#     'Melee',
#     'Throw',
#     'Science',
#     'Psychology',
#     'Bureaucracy',
#     'Alpha Complex',
#     'Bluff',
#     'Charm',
#     'Intimidate',
#     'Stealth',
#     'Operate',
#     'Engineer',
#     'Program',
#     'Demolitions'
# ]