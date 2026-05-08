from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_data(train_texts, test_texts):
    vectorizer = TfidfVectorizer(max_features=5000)
    
    X_train = vectorizer.fit_transform(train_texts).toarray()
    X_test = vectorizer.transform(test_texts).toarray()
    
    return X_train, X_test, vectorizer