import random

file_paths = {
    'Standard Equipment' : 'standard_equipnment.txt',
    'Additional Equipment' : 'additional_equipment.txt',
    'Service Group' : 'service_groups.txt',
    'Mutant Powers' : 'mutant_powers.txt',
    'Secret Societies' : 'secret_societies.txt',
    'Secret Skills' : 'secret_skills.txt',
    'Character Quirks' : 'character_quirks.txt',
    'Silly Skills' : 'silly_skills.txt'
    }
    
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

# x = get_full_stats(n_characters=3)

def load_configs(
    file_paths = {
        'standard_equipnment.txt',
        'additional_equipment.txt',
        'service_groups.txt',
        'mutant_powers.txt',
        'secret_societies.txt',
        'secret_skills.txt',
        'character_quirks.txt',
        'silly_skills.txt'
        }
        ):
    
    configs = {}
    for x in file_paths:
        name = file_paths[x] - '.txt'
        with open(file_paths[x],'r') as _file 
        configs[name] = _file.readlines()


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