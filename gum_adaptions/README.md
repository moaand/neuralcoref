# Neuralcoref with the GUM corpus

This Github fork contains a tweaked version of Huggingfaces Coreference Resolution repository. The code is modified to work with the GUM data, which is an open dataset for coreference created by Georgetown University. Read more here: Georgetown University on their website: https://corpling.uis.georgetown.edu/gum/. We have added this folder called *gum_adaptions* which contains some additional code, for example a parser from the GUM Conll-u format to the Conll format Huggingface use.

## Installation
Firstly, clone this repo. Then, download the GUM-data in the Conll-u format from here: https://github.com/amir-zeldes/gum/tree/master/dep and put it in the _GUM_CONLLU_DATA_ directory that is in the root directory of this repo. Create one fold per category (see academic, textbook etc), and put the corresponding files there. Now you should have all the necessary data. 

The next step is to download anaconda. The simplest way to do this if you are on Mac is through Homebrew (https://formulae.brew.sh/cask/anaconda).

Make sure that you are in the outer neuralcoref directory. Then, run the following commands:

- ```conda env create -f environment.yml```
- ```conda activate project_neural_coref```
- ```conda install pytorch -c pytorch```
- ```python -m spacy download en```
- ```conda install -c conda-forge tensorboardx```
- ```pip install sklearn```
    
## Prepare the data
Go back to this folder (neuralcoref/gum_adaptions/)and run

- ```python split_datasets.py```

This script will take the files in the GUM corpus and make them into three big files: train_file.gold_conllu, dev_file.gold_conllu, test_file.gold_conllu. 
The files each contain a part of the dataset, with the same distribution of the genres. The partition is 70% training data, 15% dev data and 15% test data. It will also parse these created Conll-u files to the correct Conll-format, and be named:  train_file.gold_conll, dev_file.gold_conll, test_file.gold_conll. When the parsing later, they will ignore the .conllu files and only look at the .conll files.

## Parse the datafiles
To parse the conll files, run the following commands:
 - ```python -m neuralcoref.train.conllparser --path neuralcoref/train/data/train```
 - ```python -m neuralcoref.train.conllparser --path neuralcoref/train/data/dev```
 - ```python -m neuralcoref.train.conllparser --path neuralcoref/train/data/test```
 
 This will take the big files created in the previous step, parse them. This will create a numpy/ folder for each of the big files. 
 
## Run the training
 
To train the model, run the following command:

- ```python -m neuralcoref.train.learn --train ./neuralcoref/train/data/train --eval ./neuralcoref/train/data/dev --test ./neuralcoref/train/data/test```

This will execute the training of the model, and output the scores for all datasets after each training phase is completed.

