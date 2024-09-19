import pandas as pd


def load_data(file_path):
    df = pd.read_csv(file_path, names=["index", "episode", "scene", "character", "dialogue"], header=None)
    df.drop(0, inplace=True)
    return df


def create_character_counts(df):
    df2 = df['character'].value_counts().reset_index()
    df2.columns = ['character', 'count']
    df2 = df2.head(20)
    return df2
