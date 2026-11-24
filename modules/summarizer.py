import re

_model = None


def get_model(model_name):
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(model_name)
    return _model


def split_sentences(text):
    cleaned_text = ' '.join(text.split())
    return [sentence.strip() for sentence in re.split(r'(?<=[.!?])\s+', cleaned_text) if sentence.strip()]


def summarize_text(text, model_name):
    sentences = split_sentences(text)
    if not sentences:
        raise ValueError('The text is empty')
    if len(sentences) == 1:
        return sentences[0]

    model = get_model(model_name)
    embeddings = model.encode(sentences, convert_to_numpy=True, normalize_embeddings=True)
    centroid = embeddings.mean(axis=0)
    centroid_norm = (centroid ** 2).sum() ** 0.5
    if centroid_norm == 0:
        return sentences[0]

    scores = embeddings @ (centroid / centroid_norm)
    selected_count = max(1, round(len(sentences) * 0.3))
    selected_indices = sorted(scores.argsort()[-selected_count:].tolist())
    return ' '.join(sentences[index] for index in selected_indices)
