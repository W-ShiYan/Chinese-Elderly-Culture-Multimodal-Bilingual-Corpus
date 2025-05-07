def build_corpus(data_folder):
    corpus = []
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    if file_path.endswith('_ch.txt'):
                        processed_text = preprocess_chinese_text(text)
                    elif file_path.endswith('_en.txt'):
                        processed_text = preprocess_english_text(text)
                    corpus.append({
                        'file_path': file_path,
                        'processed_text': processed_text
                    })
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            elif file.endswith(('.jpg', '.png')):
                features = extract_image_features(file_path)
                if features is not None:
                    corpus.append({
                        'file_path': file_path,
                        'features': features
                    })
    corpus_df = pd.DataFrame(corpus)
    return corpus_df
