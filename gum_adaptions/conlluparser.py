import io
import re
import os


def process_sentence(lines, i):
    """

    """
    # Skip sent_id & s_type
    lines = lines[2:]

    # Possibly adressee or speaker
    cols = lines[0].split()
    while(cols[1] != "speaker" and cols[1] != "text"):
        lines.pop(0)
        # Possibly speaker
        cols = lines[0].split()

    speaker = "-"
    if cols[1] == "speaker":
        speaker = cols[3]
        lines.pop(0)

    # redefined later
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
        # print(line)
        match = re.search(pattern, cols[9])
        if match:
            entity = match[1]
            start_entities = re.findall(r"\(([^\(\)]*)", entity)
            for start_entity in start_entities:
                entity_stack.append({"label": start_entity, "start": i})
            end_entities = re.findall(r"([^\(\)]*\))", entity)

            for _ in end_entities:
                entity = entity_stack.pop()
                entity["end"] = i
                corefs.append(entity)
        line = lines.pop(0)
        i += 1

    text = ' '.join(tokens) + ' '
    return speaker, text, tokens, corefs, lines, i


def process_document(lines, part):
    """

    """
    index = 0
    line = lines.pop(0)
    cols = line.split()  # split on whitespace
    name = cols[4]

    lines = lines[7:]  # skip 7 rows of meta data

    utts_speakers = []
    utts_text = []
    utts_tokens = []
    utts_corefs = []

    # Peek next line, if new line character return to callee
    while(lines != [] and lines[0] != "\n"):
        speaker, text, tokens, corefs, lines, index = process_sentence(
            lines, index)
        utts_text.append(text)
        # Changed back to append, since that's what they seem to do
        utts_tokens.append(tokens)
        utts_corefs.append(corefs)
        utts_speakers.append(speaker)

    # Remove an extra empty line between docs
    lines.pop(0)
    return {'utts_text': utts_text, 'utts_tokens': utts_tokens, "utts_corefs": utts_corefs,
            "utts_speakers": utts_speakers, "name": name, "part": part}, lines


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
    keys = ["utts_text", "utts_tokens", "utts_corefs",
            "utts_speakers", "name", "part", "lines"]
    part = 0
    with io.open(full_name, "rt", encoding="utf-8", errors="strict") as f:
        lines = list(f)
        while(lines != []):
            doc, lines = process_document(lines, (part))
            docs.append(doc)
            part += 1
            # for i in range(len(doc)):
            #    print(keys[i],doc[i],"\n")

    return docs


def get_dash_string(number):
    return "- \t" * number


def write_to_conll_file(docs, fullname):
    with io.open(fullname, "w", encoding="utf-8", errors="strict") as f:
        # begin document (bc/cctv/00/cctv_0005); part 003
        for doc in docs:
            f.write(
                f"#begin document ({doc['name']}); part {('000'+str(doc['part']))[-3:]}\n\n")
            coref_to_int = {}
            coref_counter = 0
            # Allt som är samma för dokumentet, part och docnome
            for sentence_index, token_list in enumerate(doc['utts_tokens']):
                # speaker
                speaker = doc['utts_speakers'][sentence_index]
                corefs = doc['utts_corefs'][sentence_index]
                for index, token in enumerate(token_list):
                    start_corefs = sorted([ref for ref in corefs if(
                        ref['start'] == index)], key=lambda d: d['end'], reverse=True)
                    end_corefs = sorted([ref for ref in corefs if(
                        ref['end'] == index)], key=lambda d: d['start'])
                    coref_info = ''
                    if not (start_corefs or end_corefs):
                        coref_info = '-'

                    if start_corefs:
                        for ref in start_corefs:
                            coref_label = ref['label']
                            if not coref_label in coref_to_int:
                                coref_to_int[coref_label] = coref_counter
                                coref_counter += 1
                            coref_info += f"({coref_to_int[coref_label]}"
                            if ref['start'] == ref['end']:
                                coref_info += ")|"
                            else:
                                coref_info += "|"

                    if end_corefs:
                        for ref in end_corefs:
                            if not ref['start'] == ref['end']:
                                coref_info += f"{coref_to_int[ref['label']]})|"
                    if coref_info[-1] == '|':
                        coref_info = coref_info[:-1]
                    f.write(
                        f"{doc['name']} \t {doc['part']} \t {index} \t {token} \t {get_dash_string(5)} {speaker} \t {get_dash_string(3)} \t {coref_info}\n")
                f.write("\n")
            f.write("#end document\n")

def conllu_to_conll(fullname):
    docs = load_file(fullname+'.gold_conllu')
    if os.path.exists(f"{fullname}.gold_conll"):
        print("There is already a", f"{fullname}.gold_conll", "file, erasing")
        os.remove(f"{fullname}.gold_conll")
   
    write_to_conll_file(docs, f"{fullname}.gold_conll")

#full = '/Users/moaandersson/Documents/project_datascience/project-datascience/neuralcoref/neuralcoref/train/data/train/GUM_bio_chao'
#conllu_to_conll(full)
