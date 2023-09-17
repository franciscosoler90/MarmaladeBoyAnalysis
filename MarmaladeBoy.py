#Analizando las relaciones de los personajes en ’Marmalade Boy’
#Autor: Francisco José Soler Conchello


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from plotly.offline import init_notebook_mode,iplot
init_notebook_mode(connected=True)
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os

import seaborn as sns


# In[2]:


df = pd.read_csv(r"C:\Users\frans\Downloads\MarmaladeBoy_Script.csv", names=["index","episode","scene","character","dialogue"], header=None)


# In[3]:


df.drop(0,inplace=True)


# In[4]:


df2 = pd.DataFrame(df.character.value_counts()).iloc[:20]


# In[5]:


df2


# In[6]:


trace = go.Bar(y=df2.character, x=df2.index,  marker=dict(color="crimson",line=dict(color='black', width=2)),opacity=0.75)


# In[7]:


fig = make_subplots(rows=1, cols=1,horizontal_spacing=1, subplot_titles=("Marmalade Boy"))


# In[8]:


fig.append_trace(trace, 1, 1)


# In[9]:


fig['layout'].update(showlegend=False ,height=800,title="Número de dialogos según el personaje",paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)')

iplot(fig)


# In[10]:


import re
import nltk
from nltk.corpus import stopwords
import nltk as nlp
from nltk.probability import FreqDist


# In[11]:


description_list=[]
for description in df.dialogue:
    # regex pattern
    description=re.sub("[^A-Za-z_ÑñÁáÉéÍíÓóÚú]+", " ", description)
    description=description.lower()
    description=nltk.word_tokenize(description)
    description=[word for word in description if not word in set(stopwords.words("spanish"))]
    lemma=nlp.WordNetLemmatizer()
    description=[lemma.lemmatize(word) for word in description]
    description=" ".join(description)
    description_list.append(description)


# In[12]:


df["new_script"]=description_list
df


# In[13]:


fdist = FreqDist(description_list)
fdist


# In[14]:


fdist.most_common(50)


# In[15]:


from sklearn.feature_extraction.text import CountVectorizer 

max_features = 50

count_vectorizer = CountVectorizer(max_features=max_features,stop_words = "english")

sparce_matrix = count_vectorizer.fit_transform(description_list).toarray()

print("{} palabras más comunes: {}".format(max_features,count_vectorizer.get_feature_names_out()))


# In[16]:


speaker_scene_count = {}
for name,df in df.groupby(['episode','scene']):
    for speaker_name in df.character.unique().tolist():
        if speaker_name in speaker_scene_count.keys():
            speaker_scene_count[speaker_name][0]+=1
            speaker_scene_count[speaker_name][1]+= df.character.tolist().count(speaker_name)
        else:
            speaker_scene_count[speaker_name] = []
            speaker_scene_count[speaker_name].append(1)
            speaker_scene_count[speaker_name].append(df.character.tolist().count(speaker_name))
scene_count = {k: v for k, v in sorted(speaker_scene_count.items(), key=lambda item: item[1],reverse = True)}
# pd.Series(scene_count).head(20).plot(kind='bar')
scene_count


# In[17]:


df_scenes_lines = pd.DataFrame(scene_count)
df_scenes_lines = df_scenes_lines.T
df_scenes_lines.columns = ['# of Scenes','# of lines spoken']
df_scenes_lines.info()


# In[18]:


df_scenes_lines['# of lines per scene'] = df_scenes_lines['# of lines spoken']/df_scenes_lines['# of Scenes']
num = 12
f, axes = plt.subplots(1, 2,figsize=(18,8))
scenes = df_scenes_lines['# of Scenes'].sort_values(ascending=False).head(num)
scenes_character = [ x.title() for x in df_scenes_lines['# of Scenes'].sort_values(ascending=False).head(num).index]

sns.barplot(x=scenes,y=scenes_character, ax=axes[0])
lines_spoken = df_scenes_lines['# of lines spoken'].sort_values(ascending=False).head(num)
lines_spoken_character = [ x.title() for x in df_scenes_lines['# of lines spoken'].sort_values(ascending=False).head(num).index]
sns.barplot(x=lines_spoken,y=lines_spoken_character, ax=axes[1])


# In[19]:


df = pd.read_csv(r"C:\Users\frans\Downloads\MarmaladeBoy_Script.csv", names=["index","episode","scene","character","dialogue"], header=None)


# In[20]:


char_dict = {}
for group, group_df in df.groupby(['episode','scene']):
#     print(group,group_df)
#     print(group_df['speaker'].sort_values().unique().tolist())
    char_in_scene = str(group_df['character'].sort_values().unique().tolist())[1:-1].replace("'","")
#     print(char_in_scene)
    if char_in_scene in char_dict.keys():
        char_dict[char_in_scene] +=1
    else:
        char_dict[char_in_scene] = 1
        
        
#     break
sorted_dict = {k: v for k, v in sorted(char_dict.items(), key=lambda item: item[1],reverse = True)}
sorted_dict


# In[21]:


sorted_chars =  sorted(['Miki Koishikawa', 'Yuu Matsuura', 'Meiko Akizuki', 'Ginta Suou', 'Arimi Suzuki', 'Chiyako Koishikawa', 'Rumi Matsuura', 'Youji Matsuura',
       'Jin Koishikawa', 'Satoshi Miwa', 'Namura', 'Ryoko Momoi','Takuji Kijima','Tsutomu Rokutanda'])
sorted_chars


# In[22]:


relations = [x+', '+y for x in sorted_chars for y in sorted_chars if x != y and x<y]


# In[23]:


relations.extend([x+', '+y+', '+z for x in sorted_chars for y in sorted_chars for z in sorted_chars if x<y and y<z])
relations


# In[24]:


{x:sorted_dict[x]for x in relations if x in sorted_dict.keys()}


# In[25]:


final_dict  = {k: v for k, v in sorted({x:sorted_dict[x]for x in relations if x in sorted_dict.keys()}.items(), key=lambda item: item[1],reverse = True)}
final_dict


# In[26]:


x = final_dict.copy()
for key in x.keys():
    keys = key.split(', ')
    if len(keys)==3:
        if keys[0]+', '+keys[1] in x.keys():
            final_dict[keys[0]+', '+keys[1]] +=1
        else:
            final_dict[keys[0]+', '+keys[1]]=1
            
        if keys[0]+', '+keys[2] in x.keys():
            final_dict[keys[0]+', '+keys[2]] +=1
        else:
            final_dict[keys[0]+', '+keys[2]]=1
        
        if keys[1]+', '+keys[2] in x.keys():
            final_dict[keys[1]+', '+keys[2]] +=1
        else:
            final_dict[keys[1]+', '+keys[2]]=1


# In[27]:


import networkx as nx
plt.figure(figsize=(25,20))
G = nx.Graph()
i=1
list_d = final_dict.keys()
for key in list_d:
    if len(key.split(','))==2:
        key1,key2 = key.split(',')
        key1,key2 = key1.strip(),key2.strip()
    #     print(key1,key2)
        G.add_edge(key1.strip(), key2.strip(), weight=final_dict[key])
        i+=1
        
        
        
options = {"edgecolors": "tab:blue", "node_size": 30000, "alpha": 0.75}

elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 10]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 10]

# positions for all nodes
pos = nx.spring_layout(G) 

# nodes
nx.draw_networkx_nodes(G, pos, node_color=range(13), **options)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge, width=4, alpha=0.5, edge_color='blue')
nx.draw_networkx_edges(G, pos, edgelist=esmall, width=4, alpha=0.5, edge_color='blue', style='dashed')

all_weights=[]
for (node1,node2,data) in G.edges(data=True):
    all_weights.append(data['weight'])
unique_weights = list(set(all_weights))
for weight in unique_weights:
        #4 d. Form a filtered list with just the weight you want to draw
    weighted_edges = [(node1,node2) for (node1,node2,edge_attr) in G.edges(data=True) if edge_attr['weight']==weight]
    width = weight*len(sorted_chars)*4.0/sum(all_weights)
    nx.draw_networkx_edges(G,pos,edgelist=weighted_edges,width=width)


# labels
nx.draw_networkx_labels(G, pos, font_size=18, font_family='verdana',font_weight='bold',font_color='white')

ax = plt.gca()
ax.margins(0.001)

plt.tight_layout()
plt.axis('off')

plt.show()
