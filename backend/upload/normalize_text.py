import re


def normalize_raw_text(raw_input_text: str):
    raw_text = "".join(raw_input_text).split("\n\n")
    raw_text = [str(i.replace("|", "")) for i in raw_text]
    # raw_text = [str(i.replace("-", "")) for i in raw_text]
    raw_text = [str(i.replace("[", "")) for i in raw_text]
    raw_text = [str(i.replace("]", "")) for i in raw_text]

    raw_text = [str(i.replace("•", "")) for i in raw_text]
    raw_text = [str(i.replace("#", "")) for i in raw_text]
    raw_text = [str(i.replace("_", "")) for i in raw_text]
    raw_text = [str(i.replace("*", "")) for i in raw_text]
    raw_text = [str(i.replace("* * *", "")) for i in raw_text]
    raw_text = [str(i.replace("…", "")) for i in raw_text]
    raw_text = [str(i.replace("...", "")) for i in raw_text]
    raw_text = [str(i.replace("----------------", "")) for i in raw_text]
    raw_text = [str(i.replace("______________________", "")) for i in raw_text]
    raw_text = [str(i.replace("\t", "")) for i in raw_text]
    raw_text = [str(i.replace("\r", "")) for i in raw_text]
    # raw_text = [str(i.replace("\n", "")) for i in raw_text]
    # TODO: remove stops
    raw_text = [" ".join(i.split()) for i in raw_text]
    raw_text = [re.sub('\s\s+', ' ', " ".join(i.split("\n")).strip()) for i in raw_text if i]

    parag = list()
    for index, paragraph in enumerate(raw_text):
        parag.append(paragraph)
        # print(index, " ", paragraph, sep='\t\t')
        # yield paragraph
    return ' '.join(str(i) for i in parag)
    # return parag
