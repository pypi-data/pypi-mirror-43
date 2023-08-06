from TexTor.lexicons import LEXICON
from TexTor.understand import normalize


def get_color(word):
    # http://www.saifmohammad.com/WebDocs/ACL2011-word-colour-associations-poster.pdf
    if word in LEXICON:
        return LEXICON[word]["color"]
    return None


def get_emotion(word):
    if word in LEXICON:
        return LEXICON[word]["emotion"]
    return None


def get_sentiment(word):
    if word in LEXICON:
        return LEXICON[word]["sentiment"]
    return None


def get_subjectivity(word):
    if word in LEXICON:
        return LEXICON[word]["subjectivity"]
    return None


def get_orientation(word):
    if word in LEXICON:
        return LEXICON[word]["orientation"]
    return None


def get_sentence_emotions(sentence):
    sentence = normalize(sentence)
    emotions = []
    words = sentence.split(" ")
    for w in words:
        data = LEXICON.get(w)
        if data and data["emotion"]:
            emotions.append(data["emotion"])
    return emotions


def get_sentence_sentiment(sentence):
    sentence = normalize(sentence)
    emotions = []
    words = sentence.split(" ")
    for w in words:
        data = LEXICON.get(w)
        if data and data["sentiment"]:
            emotions.append(data["sentiment"])
    return emotions


def get_sentence_subjectivity(sentence):
    sentence = normalize(sentence)
    emotions = []
    words = sentence.split(" ")
    for w in words:
        data = LEXICON.get(w)
        if data and data["subjectivity"]:
            emotions.append(data["subjectivity"])
    return emotions


def get_sentence_color(sentence):
    sentence = normalize(sentence)
    emotions = []
    words = sentence.split(" ")
    for w in words:
        data = LEXICON.get(w)
        if data and data["color"]:
            emotions.append(data["color"])
    return emotions


if __name__ == "__main__":
    # word level emotion tagging based on lexicon lookup
    TEST_SENTENCES = ['I love mom\'s cooking',  # happy
                      'I love how you never reply back..',  # sarcasm
                      'I love cruising with my homies',  # excited
                      'I love messing with yo mind!!',  # fear
                      'I love you and now you\'re just gone..',  # sad
                      'This is shit',  # angry
                      'This is the shit']  # excited
    for t in TEST_SENTENCES:
        print("\n"+t)
        print(get_sentence_emotions(t))
        print(get_sentence_color(t))
        print(get_sentence_sentiment(t))
        print(get_sentence_subjectivity(t))

    word = "love"
    print(get_color(word))
    print(get_emotion(word))
    print(get_orientation(word))
    print(get_sentiment(word))
    print(get_subjectivity(word))