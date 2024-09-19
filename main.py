from modules.data_processing import DataProcessor
from modules.text_processing import TextProcessor
from modules.visualizations import Visualizer
import pandas as pd


def process_and_plot(df):
    try:
        # Create character counts
        df2 = DataProcessor.create_character_counts(df)
        Visualizer.plot_character_dialogues(df2)

        # Initialize NLTK components
        text_processor = TextProcessor()
        df = text_processor.process_text(df)

        # Calculate scene and line counts
        speaker_scene_count = DataProcessor.calculate_scene_counts(df)

        # Sort and prepare scene count DataFrame
        scene_count = {k: v for k, v in sorted(speaker_scene_count.items(), key=lambda item: item[1], reverse=True)}
        df_scenes_lines = pd.DataFrame(scene_count).T
        df_scenes_lines.columns = ['# of Scenes', '# of lines spoken']
        df_scenes_lines['# of lines per scene'] = df_scenes_lines['# of lines spoken'] / df_scenes_lines['# of Scenes']
        Visualizer.plot_scenes_lines(df_scenes_lines)

        # Calculate character interactions
        final_dict = DataProcessor.calculate_character_interactions(df)
        Visualizer.plot_interactions(final_dict)

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    try:
        df = DataProcessor.load_data('data/script.csv')

        if not df.empty:
            process_and_plot(df)
        else:
            print("Failed to load data. Please check the file and try again.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
