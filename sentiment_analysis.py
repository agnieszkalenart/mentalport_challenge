"""
File containing the sentiment analysis of optional text inputs by the user
"""

# standard library imports

# 3rd party imports
from happytransformer import HappyTextClassification

# local imports (i.e. our own code)


# define model
model = HappyTextClassification(
    model_type="DISTILBERT",
    model_name="distilbert-base-uncased-finetuned-sst-2-english",
)

while True:

    text = input("How are you feeling now? ")

    result = model.classify_text(text)

    if text == "exit":
        break
    elif result.score < 0.995:
        print("Welcome to mentalport!")
    elif result.label == "POSITIVE":
        print("You seem to be in a good mood today!")
    else:
        print("You seem down. Let's find some exercises to help")
