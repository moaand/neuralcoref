# Neuralcoref with the GUM corpus

This Github repo contains a tweaked version of Huggingfaces Coreference Resolution repository. Their repository is called *Neuralcoref*.

## Installation
Firstly, clone this repo. Once you have the repo, you will hade downloaded all necessary code and data for running the code. 

The next step is to download anaconda. The simplest way to do this if you are on mac is through Homebrew.

Make sure that you are in the project-datascience/neuralcoref directory. Then, run the following commands:

- ```conda env create -f environment.yml```
- ```conda activate project_neural_coref```
- ```conda install pytorch -c pytorch```
- ```python -m spacy download en```
- ```conda install -c conda-forge tensorboardx```
- ```pip install sklearn```
    
## Prepare the data
Go back to the root folder (project-datascience/)and run

- ```python split_datasets.py```

This script will take the files in the GUM corpus and make them into three big files: train_file.gold_conllu, dev_file.gold_conllu, test_file.gold_conllu. 
The files each contain a part of the dataset, with the same distribution of the genres. The partition is 70% training data, 15% dev data and 15% test data. 

## Parse the datafiles
To parse the conll-u files, run the following commands:
 - ```python -m neuralcoref.train.conllparser --path neuralcoref/train/data/train```
 - ```python -m neuralcoref.train.conllparser --path neuralcoref/train/data/dev```
 - ```python -m neuralcoref.train.conllparser --path neuralcoref/train/data/test```
 
 This will take the big files created in the previous step, and create corresponding .conll files. The new .conll files will be placed in the same directory.
 When the training runs later, they will ignore the .conllu files and only look at the .conll files.
 
## Run the training
 
To train the model, run the following command:

- ```python -m neuralcoref.train.learn --train ./neuralcoref/train/data/train --eval ./neuralcoref/train/data/dev --test ./neuralcoref/train/data/test```

This will execute the training of the model, and output the scores for all datasets after each training phase is completed.

