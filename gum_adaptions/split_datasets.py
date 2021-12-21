import os
import argparse
from sklearn.model_selection import train_test_split
from conlluparser import conllu_to_conll


def read_from_files(filenames, target_file, args):
    if os.path.exists(target_file):
        print("There is already a", target_file, "file, erasing")
        os.remove(target_file  )
    with open(target_file, "w") as target:
        for file in filenames:
            f = open(f"{args.data_path}/{file}", "r")
            content = f.read()
            target.write(content + "\n")
            f.close()

def data_partition(args):
    train_set = []
    dev_set = []
    test_set = []
    sub_dirs = os.listdir(args.data_path)
    
    for sub_dir in sub_dirs:
        files = [elem for elem in os.listdir(f"{args.data_path}/{sub_dir}") if elem[0] != "."]
        temp = files
        train, temp = train_test_split(temp, train_size=0.7, test_size=0.3, random_state=13)
        dev, test = train_test_split(temp, train_size=0.5, test_size=0.5, random_state=13)
        train_set.extend([f"{sub_dir}/{file}" for file in train])
        dev_set.extend([f"{sub_dir}/{file}" for file in dev])
        test_set.extend([f"{sub_dir}/{file}" for file in test])

    with open("dataset_partition.txt", "w") as f:
        f.write("Train dataset\n\n")
        for i, _ in enumerate(train_set):
            f.write(train_set[i] + "\n")
        f.write("\n")

        f.write("Dev dataset " + "\n\n")
        for i, _ in enumerate(dev_set):
            f.write(dev_set[i] + "\n")
        f.write("\n")

        f.write("Test dataset " + "\n\n")
        for i, _ in enumerate(dev_set):
            f.write(test_set[i] + "\n")
    return train_set, dev_set, test_set

def main():
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(
        description="Parsing the GUM data from conllu to conll format and splitting into train, dev and test"
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default="../GUM_CONLLU_DATA/",
        help="Path to the GUM data",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default="../neuralcoref/train/data",
        help="Path to where the parsed data should be put",
    )
    args = parser.parse_args()
    print(args)
    train_set, dev_set, test_set = data_partition(args)

    # Make concatted conllu files
    train_path = f"{args.save_path}/train/train_file"
    dev_path = f"{args.save_path}/dev/dev_file"
    test_path = f"{args.save_path}/test/test_file"
    read_from_files(train_set, f"{train_path}.gold_conllu", args)
    read_from_files(dev_set, f"{dev_path}.gold_conllu", args)
    read_from_files(test_set, f"{test_path}.gold_conllu", args)

    # Convert to conll format
    conllu_to_conll(train_path)
    conllu_to_conll(dev_path)
    conllu_to_conll(test_path)

if __name__ == '__main__':
    main()
    print("Parsing completed")
