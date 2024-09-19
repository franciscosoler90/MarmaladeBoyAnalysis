#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import CountVectorizer
import networkx as nx

# Descargar recursos de NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Cargar datos
df = pd.read_csv('data/script.csv', names=["index", "episode", "scene", "character", "dialogue"], header=None)

# Procesar datos
df.drop(0, inplace=True)

# Crear df2 con la cuenta de personajes
df2 = df['character'].value_counts().reset_index()
df2.columns = ['character', 'count']
df2 = df2.head(20)

# Graficar
# Crear gráfico con matplotlib
plt.figure(figsize=(10, 6))
plt.barh(df2['character'], df2['count'], color='crimson', edgecolor='black')
plt.xlabel('Número de diálogos')
plt.title('Número de diálogos según el personaje')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar el gráfico
plt.show()

# Inicializar el lematizador
lemma = WordNetLemmatizer()

description_list = []
for description in df.dialogue:
    # Eliminar caracteres no alfabéticos
    description = re.sub("[^A-Za-z_ÑñÁáÉéÍíÓóÚú]+", " ", description)

    # Convertir a minúsculas
    description = description.lower()

    # Tokenización
    description = nltk.word_tokenize(description)

    # Eliminar stopwords
    description = [word for word in description if word not in set(stopwords.words("spanish"))]

    # Lematización
    description = [lemma.lemmatize(word) for word in description]

    # Reunir el texto procesado
    description = " ".join(description)

    # Añadir a la lista
    description_list.append(description)

df["new_script"] = description_list

fdist = FreqDist(description_list)
print(fdist.most_common(50))

max_features = 50
count_vectorizer = CountVectorizer(max_features=max_features, stop_words="english")
sparce_matrix = count_vectorizer.fit_transform(description_list).toarray()
print("{} palabras más comunes: {}".format(max_features, count_vectorizer.get_feature_names_out()))

speaker_scene_count = {}
for name, df in df.groupby(['episode', 'scene']):
    for speaker_name in df.character.unique().tolist():
        if speaker_name in speaker_scene_count.keys():
            speaker_scene_count[speaker_name][0] += 1
            speaker_scene_count[speaker_name][1] += df.character.tolist().count(speaker_name)
        else:
            speaker_scene_count[speaker_name] = [1, df.character.tolist().count(speaker_name)]
scene_count = {k: v for k, v in sorted(speaker_scene_count.items(), key=lambda item: item[1], reverse=True)}

df_scenes_lines = pd.DataFrame(scene_count).T
df_scenes_lines.columns = ['# of Scenes', '# of lines spoken']
df_scenes_lines['# of lines per scene'] = df_scenes_lines['# of lines spoken'] / df_scenes_lines['# of Scenes']
num = 12
f, axes = plt.subplots(1, 2, figsize=(18, 8))
scenes = df_scenes_lines['# of Scenes'].sort_values(ascending=False).head(num)
scenes_character = [x.title() for x in df_scenes_lines['# of Scenes'].sort_values(ascending=False).head(num).index]
sns.barplot(x=scenes, y=scenes_character, ax=axes[0])
lines_spoken = df_scenes_lines['# of lines spoken'].sort_values(ascending=False).head(num)
lines_spoken_character = [x.title() for x in
                          df_scenes_lines['# of lines spoken'].sort_values(ascending=False).head(num).index]
sns.barplot(x=lines_spoken, y=lines_spoken_character, ax=axes[1])

char_dict = {}
for group, group_df in df.groupby(['episode', 'scene']):
    char_in_scene = str(group_df['character'].sort_values().unique().tolist())[1:-1].replace("'", "")
    if char_in_scene in char_dict.keys():
        char_dict[char_in_scene] += 1
    else:
        char_dict[char_in_scene] = 1

sorted_dict = {k: v for k, v in sorted(char_dict.items(), key=lambda item: item[1], reverse=True)}
sorted_chars = sorted(
    ['Miki Koishikawa', 'Yuu Matsuura', 'Meiko Akizuki', 'Ginta Suou', 'Arimi Suzuki', 'Chiyako Koishikawa',
     'Rumi Matsuura', 'Youji Matsuura', 'Jin Koishikawa', 'Satoshi Miwa', 'Namura', 'Ryoko Momoi', 'Takuji Kijima',
     'Tsutomu Rokutanda'])
relations = [x + ', ' + y for x in sorted_chars for y in sorted_chars if x != y and x < y]
relations.extend(
    [x + ', ' + y + ', ' + z for x in sorted_chars for y in sorted_chars for z in sorted_chars if x < y < z])
final_dict = {k: v for k, v in sorted({x: sorted_dict[x] for x in relations if x in sorted_dict.keys()}.items(),
                                      key=lambda item: item[1], reverse=True)}

x = final_dict.copy()
for key in x.keys():
    keys = key.split(', ')
    if len(keys) == 3:
        if keys[0] + ', ' + keys[1] in x.keys():
            final_dict[keys[0] + ', ' + keys[1]] += 1
        else:
            final_dict[keys[0] + ', ' + keys[1]] = 1

        if keys[0] + ', ' + keys[2] in x.keys():
            final_dict[keys[0] + ', ' + keys[2]] += 1
        else:
            final_dict[keys[0] + ', ' + keys[2]] = 1

        if keys[1] + ', ' + keys[2] in x.keys():
            final_dict[keys[1] + ', ' + keys[2]] += 1
        else:
            final_dict[keys[1] + ', ' + keys[2]] = 1

plt.figure(figsize=(25, 20))
G = nx.Graph()
i = 1
list_d = final_dict.keys()
for key in list_d:
    if len(key.split(',')) == 2:
        key1, key2 = key.split(',')
        key1, key2 = key1.strip(), key2.strip()
        G.add_edge(key1, key2, weight=final_dict[key])
        i += 1

options = {"edgecolors": "tab:blue", "node_size": 5000, "node_color": "tab:cyan", "alpha": 0.5, "width": 0.5}
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx(G, pos, **options)
plt.title("Interacciones entre personajes")
plt.show()
