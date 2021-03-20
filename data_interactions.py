import pandas as pd

data_prefix = "data/"
result_prefix = "results/"
result_ext = ".csv"


def save(path, data):
    f = open(path, "w")
    f.write(data)
    f.close()


def save_data(chat_id, data):
    save(data_prefix + str(chat_id), data)


def save_result(chat_id, df):
    path = get_result_path(chat_id)
    df.to_csv(path)
    return path


def get_result_path(chat_id):
    return result_prefix + str(chat_id) + result_ext


def get_df(chat_id):
    f = open(data_prefix + str(chat_id), "r")
    file_path = f.read()
    f.close()
    return get_df_bypath(file_path)


def get_df_bypath(path):
    return pd.read_csv(path, index_col=0)