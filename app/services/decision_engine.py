def decide_action(sentiment):
    sentiment = sentiment.lower()

    if sentiment == "positive":
        return "AUTO_POST"
    elif sentiment == "neutral":
        return "REVIEW_OPTIONAL"
    else:
        return "NEED_APPROVAL"
