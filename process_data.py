import numpy as np
import re
from datetime import datetime
from multiprocessing import Pool
from langdetect import detect
import pandas as pd
from tqdm import tqdm
import time


def read_line_from_txt(line):
    regex_date = "^[^-]*"

    datetime_str = line[:15]
    sender = line[18:].split(':')[0]
    text = ''.join(line[15:].split(':')[1:])  # just string, no list
    try:
        datetime_obj = datetime.strptime(datetime_str, "%d.%m.%y, %H:%M")
    except:
        # has a problem with some lines where the format doesn't fit, best to just ignore those for now
        return None
    try:
        lang = detect(text)
    except:
        # print("Could not detect language in text: ", text)
        a = 2
    else:
        if lang != 'he':
            return datetime_obj, sender, text


def messages_to_dataframe(file):
    start_time = time.time()
    df = None
    # cols timedate, sender, content
    # print(file)
    i = 0
    langs = []
    with open(file, 'r', encoding="utf8") as f:
        # unclear if map or for is faster!
        # func returns None if line is hebrew!
        processed_lines = map(read_line_from_txt, [line for line in f])
        # filter the Nones out of the list
        processed_lines = filter(None, processed_lines)
        # does this have to be a list????
        processed_lines = list(processed_lines)
        # Need to improve these for loops
        datetimes = list(map(lambda x: x[0], processed_lines))
        senders = list(map(lambda x: x[1], processed_lines))
        messages = list(map(lambda x: x[2], processed_lines))
    df = pd.DataFrame(list(zip(datetimes, senders, messages)), columns=["timedate", "sender", "text"])
    end_time = time.time()
    # this should be output to a log file
    # print("Loaded %s to dataframe. Time taken: %.3f" % (file, end_time - start_time))
    return df


# idea - generate 'my' responses to messages.
# input is the text so the messages sent to me
# output it a message I would send.
def read_files(files, out_dir):
    # dataframe of text messages
    dfs = []
    p = Pool(processes=len(files))
    processes = [p.apply_async(messages_to_dataframe, args=(file,)) for file in files]
    dfs = [p.get() for p in tqdm(processes)]

    print(dfs[-1].head(10))
    print("Read and processed ", len(dfs), " Whatsapp chats")
    data = pd.concat(dfs)
    data.reset_index()
    data.to_csv(out_dir)
    return data
