def parse_dictionary(path="cedict_ts.u8"):
    dictionary = set()

    with open(path) as f:
        for line in f:
            if line[0] == "#":
                continue
            chinese_word = line.split()[1]
            dictionary.add(chinese_word)

    return dictionary
