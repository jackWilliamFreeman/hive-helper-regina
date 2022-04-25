import random

insult_predicate = ['moronic', 'obtuse', 'inane', 'rotund', 'fat', 'surly', 'ignorant', 'charged', 'addicted', 'overt', 'snobbish', 'irrepressible', 'hideous', 'blasphemous','spiteful','churlish','round-headed','purile', 'turgid', 'flappable', 'up-hive', 'impulsive', 'goat-faced', 'inbred']
insults = ['slattern', 'grox fucker', 'turkey', 'whoreson', 'fat cat', 'brigand', 'illiterate', 'cunt', 'whore','lummox','cad','heretic','simpleton','moron','catamite','fatso','virgin','nerd','grognard', 'swine', 'cockroach', 'mutton', 'plebian', 'fucker', 'shithead', 'imbecile']

def get_long_insult():
    insult = f"{insult_predicate[random.randint(0, len(insult_predicate)-1)]} {insults[random.randint(0, len(insults)-1)]}"
    return insult
         
def get_short_insult():
    insult = f"{insults[random.randint(0, len(insults)-1)]}"
    return insult
         