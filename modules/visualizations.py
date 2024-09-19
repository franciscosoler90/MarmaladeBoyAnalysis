import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx


class Visualizer:
    @staticmethod
    def plot_character_dialogues(df2):
        sns.set(style="whitegrid")
        plt.figure(figsize=(12, 8))
        colors = sns.color_palette("viridis", n_colors=len(df2))
        bars = plt.barh(df2['character'], df2['count'], color=colors, edgecolor='black')
        for bar in bars:
            plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2, f'{bar.get_width()}',
                     va='center', ha='left', fontsize=10, color='black')
        plt.xlabel('Número de diálogos', fontsize=12)
        plt.ylabel('Personaje', fontsize=12)
        plt.title('Número de diálogos según el personaje', fontsize=14)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_scenes_lines(df_scenes_lines):
        num = 12
        f, axes = plt.subplots(1, 2, figsize=(18, 8))
        scenes = df_scenes_lines['# of Scenes'].sort_values(ascending=False).head(num)
        scenes_character = [x.title() for x in
                            df_scenes_lines['# of Scenes'].sort_values(ascending=False).head(num).index]
        sns.barplot(x=scenes, y=scenes_character, ax=axes[0])
        lines_spoken = df_scenes_lines['# of lines spoken'].sort_values(ascending=False).head(num)
        lines_spoken_character = [x.title() for x in
                                  df_scenes_lines['# of lines spoken'].sort_values(ascending=False).head(num).index]
        sns.barplot(x=lines_spoken, y=lines_spoken_character, ax=axes[1])
        plt.show()

    @staticmethod
    def plot_interactions(final_dict):
        graph = nx.Graph()
        for key, weight in final_dict.items():
            nodes = key.split(', ')
            if len(nodes) == 2:
                key1, key2 = nodes
                graph.add_edge(key1.strip(), key2.strip(), weight=weight)
        plt.figure(figsize=(25, 20))
        pos = nx.spring_layout(graph, seed=42)
        nx.draw_networkx(graph, pos, edgecolors="tab:blue", node_size=5000, node_color="tab:cyan", alpha=0.5, width=0.5)
        plt.title("Interacciones entre personajes")
        plt.show()
