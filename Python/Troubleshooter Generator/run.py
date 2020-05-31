"""
Outline
-------

Characters must be generated multiple at once (to prevent duplicate items etc. across characters)
Stats can be 1d20//2 then +/- incrementally from other characters

make text files with all the random things to choose from:
read said text files, splitlines to get choices based on random

characters as classes
"""

# file_paths = {
#     'Standard Equipment' : 'standard_equipnment.txt',
#     'Silly Equipment' : 'silly_equipment.txt',
#     'Service Group' : 'service_groups.txt',
#     'Mutant Powers' : 'mutant_powers.txt',
#     'Secret Societies' : 'secret_societies.txt',
#     'Secret Skills' : 'secret_skills.txt',
#     'Character Quirks' : 'character_quirks.txt',
#     }

# for filepath in file_paths:
#     with open(file_paths[filepath],'w') as txt_file:
#         pass


'''Anti-Mutant: A hate group who hates mutants above and beyond the social norm. They attack registered and even 'suspected' mutants in dark corridors with lead pipes and funball bats. Their members are constantly trying to ferret out the mutant menace that hides among them, and a good percentage are even more paranoid than the average citizen. Ironically, many of them are actually mutants themselves, but remain unregistered.
Communists: This secret society was formed based on the theory that, if the Computer hates Communism so much, then there must be something to it. Their knowledge of historical Communism is poor, leading to Alpha Complex Communists adopting stereotypical Russian accents and clothing. Further confusion about Communism leads to Alpha Complex Communists carrying pictures of Groucho Marx and listening to the 'revolutionary' songs of John Lennon.
Computer Phreaks: Composed of hackers, crackers, computer geeks, and computer game addicts, the Computer Phreaks practice programming in secret — and try to show off how very l33t they are. This can be a very dangerous hobby in Alpha. The line between 'hacker extraordinaire' and 'terminated traitor' is a fine one.
Corpore Metal: Corpore Metal members believes that humans are inferior and outdated. Machines are the wave of the future. CorpMets are obsessed with attaining the perfection of 'bothood', going as far as intentional self-maiming to obtain cybernetic replacements. This secret society, unsurprisingly, also has a large number of rogue bot members.
Death Leopard: Their motto is "live fast, die young, and leave a beautiful set of 6 corpses." Death Leopard is into loud music, explosions, and parties. They are not so much a coherent secret society as a collection of gangs. There are frequent wars within the society, but they will usually band together to deal with outside threats — if only to get back to settling their turf wars in peace.
First Church of Christ Computer Programmer (FCCC-P): They believe that the Computer is God. They have their ownhymns, services, and worship, and obey the Computer much more than the average Alpha Complex citizen. While secret society membership is still against the law, the FCCC-P is generally ignored, or only given a punitive slap-on-the-wrist. There are interfactional conflicts between different sects of the church, and even simple differences in interpretation can lead to bloodshed.
Frankenstein Destroyers: This Luddite society believes that robots are the cause of all mankind's problems. Some blanket this hate to all technology, but the society is mainly focused on destroying the shiny, soulless AI menace.
Free Enterprise: Free Enterprise represents capitalists in The Computer's more communist society. With the increasing amount of authorized capitalism, Free Enterprise has become a pseudo-mafia organization, sometimes adopting stereotypical Italian accents. Free Enterprise runs the Infrared markets in Alpha Complex.
Humanists: The Humanists are aware of just how flawed Alpha Complex is ... at least to some degree. They realize the Computer is insane, and strive to make Alpha Complex a better place for people. They do this by installing hidden backdoor codes in The Computer, reprogramming rogue bots to serve humanity, and planning for the day when they rise up and restore power to the people. That day is just around the corner — and has been for centuries; the Humanists never seem to get much done, as the society is bogged down by process, meetings, and committees.
Illuminati: The Illuminati is a secretive organization whose goals are so well hidden that most members don't know them. No one knows what the goals of this society are, or even how it goes about them. Members may be given orders as simple as 'deliver this', or 'kill him/her', or as unfathomable as 'Take the cap off the pen in the briefing room XLJ11, and dispose of it down the trash chute in X corridor'. Most Illuminati also pose as members of another secret society, in order to keep their true society a secret.
Mystics: Supposedly founded by those seeking enlightenment, the Mystics focus on recreational drug use. Another example of an un-society, there is no grand Mystic goal. Some limit themselves to their own personal visions, while others try to drug food or water supplies to try to 'enlighten' as many as possible.
Pro Tech: Pro Tech members enjoy high technology. They research new technology and steal research by others. Pro-techers can sometimes be identified by the sheer number of beeping nifty gadgets they tend to carry.
Psion: Psion is the pro-mutant group. They believe mutants are superior beings. Heavily run by the 'Controls', a separated and hidden network of telepathic mutants, Psions seek to pave the way for a better, brighter (mutant-run) future.
PURGE: PURGE is an active terrorist organization seeking to violently overthrow The Computer. They have no real ideology about what comes after; they just want the Computer destroyed. PURGE is a terrorist organization, out to destroy the hated Computer no matter how many innocents are lost in the fight.
Romantics: Enticed by the forbidden lore of the "Old Reckoning" (the days before Alpha Complex and the Computer), the Romantics scavenge what details about the past they can. However, due to the suppression of this information, their information is rather flawed, and different sects focus on different aspects of the past.
Sierra Club: The Computer restricts leaving Alpha Complex to Green clearance and above, and then only for good reasons. So, aside from Troubleshooters who may be sent into the great Outdoors, almost no one in Alpha Complex has seen so much as a blade of grass. This great mystique has led to the formation of the Sierra Club, devoted to sneaking out. Some want to escape forever, while others try to bring the wonders of nature to the less fortunate inside.'''