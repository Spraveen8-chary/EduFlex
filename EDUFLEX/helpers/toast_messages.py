# List of toast messages paired with their icons
TOAST_MESSAGES = [
    ("Ready to test your knowledge?", "🎥"),
    ("QuizBuddy welcomes you!", "🚀"),
    ("Think you caught all the details? Let's find out!", "🔍"),
    ("It's quiz time! No spoilers allowed.", "⏳"),
    ("Popped in for a quiz? You're in the right place!", "🍿"),
    ("Get your skill thinking cap on!", "🎓"),
    ("Your next skill challenge awaits!", "🏆"),
    ("Another skill, another quiz!", "🔄"),
    ("Turn those boring courses into victories!", "🎖️"),
    ("Did you pay attention? It's quiz o'clock!", "⏰"),
    ("Learning is fun, but quizzes? Even better!", "🎉"),
    ("Unleash your learning prowess here!", "🦸"),
    ("Knowledge check: Engage!", "🚦"),
    ("New skill learnt? Check. Quiz taken? Pending...", "✅"),
    ("Dive deeper into your learning skills.", "🌊"),
    ("Up for a Course rewind in quiz form?", "⏪"),
    ("Let's decode your recent Course that you studied!", "🧩"),
    ("Adding some quiz spice to your YouTube binge!", "🌶️"),
    ("Transform your learning time into quiz time!", "🔄"),
    ("Here to validate your learning expertise?", "🔍")
]

def get_random_toast():
    """Returns a random toast message and icon."""
    import random
    return random.choice(TOAST_MESSAGES)