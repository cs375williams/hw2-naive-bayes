"""
This file includes utility functions for HW1. 

Do not modify code in this file. 
"""


import csv
import os
import random
from collections import OrderedDict
from typing import List, Set, Optional, Union


class Dataset:
    """
    Represents a set of training/testing data. self.train is a list of
    Examples, as is self.dev and self.test.
    """

    def __init__(self, name: str = None, include_test: bool = False):
        self.name = name
        self.splits = OrderedDict()
        self.train = []
        self.dev = []

        self.splits['train'] = self.train
        self.splits['dev'] = self.dev

        if include_test:
            self.test = []
            self.splits["test"] = self.test

    def shuffle(self) -> None:
        for split_name in self.splits:
            random.shuffle(self.splits[split_name])


class Example:
    """
    Represents a document (list of words) with a corresponding label.
    """

    def __init__(self, words: List[str], label: Optional[int]):
        self.words = words
        self.label = label

def segment_words(s: str) -> List[str]:
    """
    Splits lines into words on whitespace.

    Args:
        s (str): The line to segment.

    Returns:
        list[str]: List of segmented words in the line.
    """
    return s.split()


def read_file(file_name: str,
              encoding: str = "utf8", mode: str = "word") -> List[str]:
    """
    Reads lines or words from a file.

    Args:
        file_name (str): The filename to read from.
        encoding (str): The encoding to use for reading the file.
        mode (str): How to extract the file contents. If "word", outputs a list
        of words (as strings). If "line", outputs a list of lines (as strings).

    Returns:
        list[str]: List of segmented words or lines in the file.
    """
    outputs = []
    with open(file_name, encoding=encoding) as f:
        for line in f:
            if mode == "word":
                outputs.extend(segment_words(line))
            elif mode == "line":
                outputs.append(line)
            else:
                raise ValueError("Invalid mode: {}".format(mode))
    return outputs


def calculate_accuracy(data: List[Example], classifier) -> float:
    """
    Calculates the classifier's accuracy on a provided dataset.

    Args:
        data (list[Example]): List of examples to evaluate on.
        classifier (Classifier): Classifier to compute accuracy for.

    Returns:
        float: Accuracy of the given classifier on the given dataset.
    """

    if len(data) == 0:
        return 0.0

    predictions = classifier.predict(data)

    correct = 0.0
    for prediction, example in zip(predictions, data):
        if example.label == prediction:
            correct += 1.0
    return correct / len(data)


def load_data(data_dir: str,
              include_test: bool = False,
              dataset_name: str = None) -> Dataset:
    """
    Loads data into a Dataset object.

    Args:
        data_dir (str): Path to the directory containing the data.
        include_test (bool): Whether to load test data (this will only be
                    available to the teaching staff in the autograder).
        dataset_name (str): Optional, name to give to the created dataset.

    Returns:
        Dataset: Dataset containing the loaded data.
    """
    dataset = Dataset(name=dataset_name, include_test=include_test)
    for split_name in dataset.splits:
        with open(os.path.join(data_dir, split_name + ".csv"),
                  newline='', mode="r") as infile:
            reader = csv.DictReader(infile, delimiter="|")
            for row in reader:
                text = row["Text"]
                label = int(row["Label"])
                example = Example(segment_words(text.rstrip('\n')),
                                  label)
                dataset.splits[split_name].append(example)

    dataset.shuffle()
    return dataset


def evaluate(classifier, dataset: Dataset,
             limit_training_set: bool = False) -> None:
    """
    Evaluate a classifier on the training and dev sets, printing the accuracy.

    Args:
        classifier (Classifier): Classifier to evaluate on the dataset.
        dataset (Dataset): Dataset to train and evaluate on.
        limit_training_set (bool): If true, truncate training set to
        only 25% of its full size.
    """
    training_set = dataset.train[:int(0.25 * len(dataset.train))] \
        if limit_training_set else dataset.train

    classifier.train(training_set)

    for split_name in dataset.splits:
        accuracy = calculate_accuracy(training_set
                                      if split_name == "train"
                                      else dataset.splits[split_name],
                                      classifier)
        print('Accuracy ({}): {}'.format(split_name, accuracy))