from modules.data_processing import load_data, create_character_counts
from modules.text_processing import initialize_nltk, process_text, analyze_frequencies, vectorize_text
from modules.visualizations import plot_character_dialogues, plot_scenes_lines, plot_interactions
import pandas as pd


def main():
    # Cargar datos
    df = load_data('data/script.csv')

    # Procesar datos
    df2 = create_character_counts(df)
    plot_character_dialogues(df2)

    # Inicializar procesamiento de texto
    stop_words, lemma = initialize_nltk()
    df = process_text(df, stop_words, lemma)

    # Análisis de frecuencias y vectorización
    description_list = df["new_script"].tolist()
    print(analyze_frequencies(description_list))
    print(vectorize_text(description_list))

    # Análisis de escenas y líneas
    speaker_scene_count = {}
    for name, df_group in df.groupby(['episode', 'scene']):
        for speaker_name in df_group.character.unique().tolist():
            if speaker_name in speaker_scene_count:
                speaker_scene_count[speaker_name][0] += 1
                speaker_scene_count[speaker_name][1] += df_group.character.tolist().count(speaker_name)
            else:
                speaker_scene_count[speaker_name] = [1, df_group.character.tolist().count(speaker_name)]
    scene_count = {k: v for k, v in sorted(speaker_scene_count.items(), key=lambda item: item[1], reverse=True)}
    df_scenes_lines = pd.DataFrame(scene_count).T
    df_scenes_lines.columns = ['# of Scenes', '# of lines spoken']
    df_scenes_lines['# of lines per scene'] = df_scenes_lines['# of lines spoken'] / df_scenes_lines['# of Scenes']
    plot_scenes_lines(df_scenes_lines)

    # Analizar interacciones
    char_dict = {}
    for group, group_df in df.groupby(['episode', 'scene']):
        char_in_scene = str(group_df['character'].sort_values().unique().tolist())[1:-1].replace("'", "")
        if char_in_scene in char_dict:
            char_dict[char_in_scene] += 1
        else:
            char_dict[char_in_scene] = 1
    sorted_dict = {k: v for k, v in sorted(char_dict.items(), key=lambda item: item[1], reverse=True)}
    sorted_chars = sorted([
        'Miki Koishikawa', 'Yuu Matsuura', 'Meiko Akizuki', 'Ginta Suou', 'Arimi Suzuki', 'Chiyako Koishikawa',
        'Rumi Matsuura', 'Youji Matsuura', 'Jin Koishikawa', 'Satoshi Miwa', 'Namura', 'Ryoko Momoi', 'Takuji Kijima',
        'Tsutomu Rokutanda'])
    relations = [x + ', ' + y for x in sorted_chars for y in sorted_chars if x != y and x < y]
    relations.extend(
        [x + ', ' + y + ', ' + z for x in sorted_chars for y in sorted_chars for z in sorted_chars if x < y < z])
    final_dict = {k: v for k, v in
                  sorted({x: sorted_dict[x] for x in relations if x in sorted_dict}.items(), key=lambda item: item[1],
                         reverse=True)}
    plot_interactions(final_dict)


if __name__ == "__main__":
    main()
