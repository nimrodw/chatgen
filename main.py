from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import torch
import glob
import os
import logging
import logging.handlers

from process_data import read_files


def setup_logger(path_to_log_file):
    # initialise logger
    handler = logging.handlers.WatchedFileHandler(
        os.environ.get("LOGFILE", path_to_log_file))
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
    root.info("Initialised Logger")
    return root


if __name__ == '__main__':
    logger = setup_logger(path_to_log_file="logs/log.log")
    # load data
    files = glob.glob("data/raw/*.txt")
    out_dir = "data/processed/all_data.csv"
    # process_data.messages_to_dataframe('data/raw/WhatsApp Chat mit JB.txt')
    logger.info("Loading data")
    if not os.path.isfile(out_dir):
        # reads files and saves them to a csv
        logger.info("Data CSV file does not exist. Generating new file")
        df = read_files(files, out_dir=out_dir)
    else:
        logger.info("Data CSV file exists, loading CSV")
        # load file from csv
        df = pd.read_csv(out_dir)
        df.reset_index()
    df = df.drop(df.columns[0], axis=1)
    print("Memory Usage: \n", df.memory_usage())
    print("Dataframe Length: ", len(df))

    # preprocess data

    # input data into network
    # train network
