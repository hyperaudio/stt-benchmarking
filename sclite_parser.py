def parse_to_sclite(tokenised_text):
    sentences = []
    speaker = ""
    current_sentence = []
    for token in tokenised_text:
        if speaker != token["speaker"] and len(current_sentence) != 0:
            sentences.append(parse_sentence(current_sentence))
            current_sentence = []
        speaker = token["speaker"]

        current_sentence.append(token)

        if token["punctuation"] in [".", "!", "?"]:
            sentences.append(parse_sentence(current_sentence))
            current_sentence = []

    print(sentences_to_trn(sentences))

def sentences_to_trn(sentences):
    return "\n".join(sentences)

def parse_sentence(sentence_tokens):
    sentence = ""
    for token in sentence_tokens:
        if not token["punctuation"]:
            token["punctuation"] = ""
        sentence += " %s%s" % (token["text"], token["punctuation"])
    sentence += " (%s)" % sentence_tokens[0]["speaker"]
    return sentence.strip()
