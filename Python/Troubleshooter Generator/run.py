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
            configs[filename] = list(x.strip() for x in f.readlines() if x.strip()!='')
            random.shuffle(configs[filename])
    return configs


def assign_characters(n_characters):
    character_data = {}
    for i in range(n_characters):
        character_data['Troubleshooter ' + str(i+1)] = {}
    return character_data


def fit_out_characters(character_data, pair_societies=True):
    configs = load_configs()
    for i, character in enumerate(character_data):
        data = {}
    
        service_group_full = configs['service_groups'].pop()    
        data['Service Group Name']= service_group_full.split(': ')[0]
        data['Service Group Description'] = service_group_full.split(': ')[1]

        mutant_power_full = configs['mutant_powers'].pop()
        data['Mutant Power Name']= mutant_power_full.split(': ')[0]
        data['Mutant Power Description'] = mutant_power_full.split(': ')[1]
        
        if pair_societies:
            number_of_groups = len(character_data) // 2
            secret_society_full = configs['secret_societies'][i % number_of_groups]
        else:
            secret_society_full = configs['secret_societies'].pop()
        data['Secret Society Name'] = secret_society_full.split(': ')[0]
        data['Secret Society Description'] = secret_society_full.split(': ')[1]

        skill_1 = configs['secret_skills'].pop()
        skill_2 = configs['secret_skills'].pop()
        skill_3 = configs['silly_skills'].pop()
        data['Secret Skill 1 Name']         = skill_1.split(': ')[0]
        data['Secret Skill 1 Description']  = skill_1.split(': ')[1]
        data['Secret Skill 2 Name']         = skill_2.split(': ')[0]
        data['Secret Skill 2 Description']  = skill_2.split(': ')[1]
        data['Secret Skill 3 Name']         = skill_3.split(': ')[0]
        data['Secret Skill 3 Description']  = skill_3.split(': ')[1]
        
        data['Character Quirk 1'] = configs['character_quirks'].pop()
        data['Character Quirk 2'] = configs['character_quirks'].pop()
        data['Character Quirk 3'] = configs['character_quirks'].pop()
        
        total_standard_equipment = len(configs['standard_equipment'])
        for i, equip in enumerate(configs['standard_equipment']):
            data['Standard Equipment ' + str(i+1)] = equip
        
        data['Additional Equipment 1'] = configs['additional_equipment'].pop()
        data['Additional Equipment 2'] = configs['additional_equipment'].pop()
        data['Additional Equipment 3'] = configs['additional_equipment'].pop()
        


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