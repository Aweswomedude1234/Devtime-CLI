import random

REMINDERS = ["Your legs haven't been compiled in {minutes} minutes.",
             "Walking is just debugging, but for your body.", 
             "Your chair is not a permanent residence.", 
             " 'sudo get_water' ", 
             "Your code won't walk away from you in five minutes", 
             "You have successfully stared at a rectangle. Impressive. Now get moving.", 
             "The terminal shall survive in your absence.", 
             "Go on without me", 
             'git commit -m "Went Outside"',
             "Have you tried turning yourself off and on again?"]

def remind(minutes):
    message = random.choice(REMINDERS)

    print()
    print("=" * 40)
    print("DEV BREAK")
    print("=" * 40)
    print("Tip: ", message.format(minutes=minutes))
    print("Few minutes from the screen will help you in the long run!")
    print("=" * 40)
    print()