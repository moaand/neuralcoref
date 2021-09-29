import io
import re

def process_sentence(lines):
    """
    
    """
    # Skip sent_id & s_type
    lines = lines[2:]

    # Possibly speaker
    cols = lines[0].split()
    speaker = ""
    if cols[1] == "speaker":
        speaker = cols[3]
        lines.pop(0)

    text = lines.pop(0)[9:]
    tokens = []
    corefs = []
    entity_stack = []

    line = lines.pop(0) 
    i = 0   
    while(line != "\n"):
        cols = line.split()
        tokens.append(cols[1])
        pattern = r"Entity=([^|]*)|Entity=(.*)"

        match = re.search(pattern, cols[9])
        if match:
            entity = match[1]
            start_entities = re.findall(r"\(([^\(\)]*)", entity)
            for start_entity in start_entities:
                entity_stack.append({"start": i, "label": start_entity})
            end_entities = re.findall(r"([^\(\)]*\))", entity)

            for end_entities in end_entities:
                entity = entity_stack.pop()
                entity["end"] = i
                corefs.append(entity)
        line = lines.pop(0)
        i += 1
    return speaker, text, tokens, corefs, lines

def process_document(lines):
    """
    
    """
    line = lines.pop(0)
    cols = line.split() # split on whitespace
    name = cols[4]
    part = 000

    lines = lines[7:] # skip 7 rows of meta data
    
    utts_speakers = []
    utts_text = []
    utts_tokens = []
    utts_corefs = []
    # Peek next line, if new line character return to callee
    while(lines != [] and lines[0] != "\n"):
        speaker, text, tokens, corefs, lines = process_sentence(lines)
        utts_text.append(text)
        utts_tokens.append(tokens)
        utts_corefs.append(corefs)
        utts_speakers.append(speaker)

    return (utts_text, utts_tokens, utts_corefs, utts_speakers, name, part), lines


def load_file(full_name, debug=False):
    """
    load a *._conll file
    Input: full_name: path to the file
    Output: list of tuples for each conll doc in the file, where the tuple contains:
        (utts_text ([str]): list of the utterances in the document
         utts_tokens ([[str]]): list of the tokens (conll words) in the document
         utts_corefs: list of coref objects (dicts) with the following properties:
            coref['label']: id of the coreference cluster,
            coref['start']: start index (index of first token in the utterance),
            coref['end': end index (index of last token in the utterance).
         utts_speakers ([str]): list of the speaker associated to each utterances in the document
         name (str): name of the document
         part (str): part of the document
        )
    """
    
    docs = []
    keys = ["utts_text", "utts_tokens", "utts_corefs", "utts_speakers", "name", "part", "lines"]
    with io.open(full_name, "rt", encoding="utf-8", errors="strict") as f:
        lines = list(f)
        while(lines != []):
            doc, lines = process_document(lines)
            docs.append(doc)
            for i in range(len(doc)):
                print(keys[i],doc[i],"\n")
    return docs