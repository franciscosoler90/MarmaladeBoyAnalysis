import pandas as pd


class DataProcessor:
    @staticmethod
    def load_data(file_path):
        """
        Load data from a CSV file into a DataFrame.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: DataFrame containing the data from the file.
        """
        try:
            df = pd.read_csv(file_path, names=["index", "episode", "scene", "character", "dialogue"], header=None)
            return df
        except FileNotFoundError:
            print(f"Error: The file at '{file_path}' was not found.")
            return pd.DataFrame()  # Return an empty DataFrame
        except pd.errors.EmptyDataError:
            print(f"Error: The file at '{file_path}' is empty.")
            return pd.DataFrame()  # Return an empty DataFrame
        except pd.errors.ParserError:
            print(f"Error: There was a problem parsing the file at '{file_path}'.")
            return pd.DataFrame()  # Return an empty DataFrame
        except Exception as e:
            print(f"Unexpected error loading the file: {e}")
            return pd.DataFrame()  # Return an empty DataFrame

    @staticmethod
    def create_character_counts(df):
        """
        Create a DataFrame containing the count of dialogues for each character.

        Args:
            df (pd.DataFrame): DataFrame containing the dialogue data.

        Returns:
            pd.DataFrame: DataFrame with character counts.
        """
        try:
            df2 = df['character'].value_counts().reset_index()
            df2.columns = ['character', 'count']
            df2 = df2.head(20)
            return df2
        except KeyError:
            print("Error: The DataFrame does not contain a 'character' column.")
            return pd.DataFrame()  # Return an empty DataFrame
        except Exception as e:
            print(f"Unexpected error creating character counts: {e}")
            return pd.DataFrame()  # Return an empty DataFrame

    @staticmethod
    def calculate_scene_counts(df):
        speaker_scene_count = {}
        for name, df_group in df.groupby(['episode', 'scene']):
            for speaker_name in df_group.character.unique().tolist():
                if speaker_name in speaker_scene_count:
                    speaker_scene_count[speaker_name][0] += 1
                    speaker_scene_count[speaker_name][1] += df_group.character.tolist().count(speaker_name)
                else:
                    speaker_scene_count[speaker_name] = [1, df_group.character.tolist().count(speaker_name)]

        return speaker_scene_count

    @staticmethod
    def calculate_character_interactions(df):
        char_dict = {}
        for group, group_df in df.groupby(['episode', 'scene']):
            char_in_scene = str(group_df['character'].sort_values().unique().tolist())[1:-1].replace("'", "")
            if char_in_scene in char_dict:
                char_dict[char_in_scene] += 1
            else:
                char_dict[char_in_scene] = 1

        sorted_dict = {k: v for k, v in sorted(char_dict.items(), key=lambda item: item[1], reverse=True)}
        sorted_chars = sorted([
            'Miki Koishikawa', 'Yuu Matsuura', 'Meiko Akizuki', 'Ginta Suou', 'Arimi Suzuki',
            'Chiyako Koishikawa', 'Rumi Matsuura', 'Youji Matsuura', 'Jin Koishikawa',
            'Satoshi Miwa', 'Namura', 'Ryoko Momoi', 'Takuji Kijima', 'Tsutomu Rokutanda'
        ])

        relations = [x + ', ' + y for x in sorted_chars for y in sorted_chars if x != y and x < y]
        relations.extend(
            [x + ', ' + y + ', ' + z for x in sorted_chars for y in sorted_chars for z in sorted_chars if x < y < z]
        )

        final_dict = {k: v for k, v in sorted({x: sorted_dict[x] for x in relations if x in sorted_dict}.items(),
                                              key=lambda item: item[1], reverse=True)}
        return final_dict
