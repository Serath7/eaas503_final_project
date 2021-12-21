from deep_learning import make_dataset_deep_learning
from deep_learning import voting
from deep_learning import fetch_genres
from joblib import load
from tensorflow.keras.models import load_model

def run(path , genres, model='deep_learning',model_path='C:\\\\Users\\\\ASUS\\\\Desktop\\\\eas503_project\\\\models\\\\cnn_model.h5'):
    X = make_dataset_deep_learning(path)
    model = load_model(model_path)
    try:
        preds = model.predict(X)
        print(preds)
        votes = voting(preds, genres)
        print("File Name - {} Votes-{} song".format(path, votes[0][0]))
        print("Genre Prediction: {}".format(votes[:3]))
        return votes[:3]      
    except Exception as e:
        print(e)
