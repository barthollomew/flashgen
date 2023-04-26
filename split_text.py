def split_into_chunks(text, max_tokens=2000):
    words = text.split()
    tokens = 0
    chunks = []
    current_chunk = []

    for word in words:
        word_tokens = len(word)
        if tokens + word_tokens <= max_tokens:
            current_chunk.append(word)
            tokens += word_tokens
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            tokens = word_tokens

    chunks.append(' '.join(current_chunk))
    return chunks
