import re
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def initialize_nltk():
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)

    stop_words = set(stopwords.words("spanish"))
    lemma = WordNetLemmatizer()
    return stop_words, lemma


def process_text(df, stop_words, lemma):
    description_list = []
    for description in df['dialogue']:
        description = re.sub(r"[^A-Za-z_ÑñÁáÉéÍíÓóÚú]+", " ", description).lower()
        description = word_tokenize(description)
        description = [word for word in description if word not in stop_words]
        description = [lemma.lemmatize(word) for word in description]
        description_list.append(" ".join(description))
    df["new_script"] = description_list
    return df


def analyze_frequencies(description_list):
    dist = FreqDist(description_list)
    return dist.most_common(50)


def vectorize_text(texts, max_features=50):
    try:
        count_vectorizer = CountVectorizer(max_features=max_features, stop_words="spanish")
        sparce_matrix = count_vectorizer.fit_transform(texts).toarray()
        return count_vectorizer.get_feature_names_out()

    except Exception as e:
        print(f"Error en la vectorización del texto: {e}")
        return []