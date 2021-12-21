import os
import librosa
import itertools
import numpy as np
import pandas as pd
from scipy.stats import kurtosis
from scipy.stats import skew
import numpy as np

__all__ = ["voting"]


def voting(scores, dict_genres):
    preds = np.argmax(scores, axis = 1)
    values, counts = np.unique(preds, return_counts=True)
    counts = np.round(counts/np.sum(counts), 2)
    votes = {k:v for k, v in zip(values, counts)}
    votes = {k: v for k, v in sorted(votes.items(), key=lambda item: item[1], reverse=True)}
    return [(fetch_genres(x, dict_genres), prob) for x, prob in votes.items()]


def fetch_genres(key, dict_genres):
    tmp_genre = {v:k for k,v in dict_genres.items()}
    return tmp_genre[key]


def fetch_features(y, sr, n_fft = 1024, hop_length = 512):
    f = {'centroid': None, 'roloff': None, 'flux': None, 'rmse': None,
                'zcr': None, 'contrast': None, 'bandwidth': None, 'flatness': None}
    
    if 0 < len(y):
        y_sound, _ = librosa.effects.trim(y, frame_length=n_fft, hop_length=hop_length)
    f['sample_silence'] = len(y) - len(y_sound)
    f['centroid'] = librosa.feature.spectral_centroid(y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel()
    f['roloff'] = librosa.feature.spectral_rolloff(y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel()
    f['zcr'] = librosa.feature.zero_crossing_rate(y, frame_length=n_fft, hop_length=hop_length).ravel()
    f['rmse'] = librosa.feature.rms(y, frame_length=n_fft, hop_length=hop_length).ravel()
    f['flux'] = librosa.onset.onset_strength(y=y, sr=sr).ravel()
    f['contrast'] = librosa.feature.spectral_contrast(y, sr=sr).ravel()
    f['bandwidth'] = librosa.feature.spectral_bandwidth(y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel()
    f['flatness'] = librosa.feature.spectral_flatness(y, n_fft=n_fft, hop_length=hop_length).ravel()
    
    mfcc = librosa.feature.mfcc(y, n_fft = n_fft, hop_length = hop_length, n_mfcc=13)
    for idx, v_mfcc in enumerate(mfcc):
        f['mfcc_{}'.format(idx)] = v_mfcc.ravel()
        
    def fetch_moments(descriptors):
        res = {}
        for k, v in descriptors.items():
            res['{}_max'.format(k)] = np.max(v)
            res['{}_min'.format(k)] = np.min(v)
            res['{}_mean'.format(k)] = np.mean(v)
            res['{}_std'.format(k)] = np.std(v)
            res['{}_kurtosis'.format(k)] = kurtosis(v)
            res['{}_skew'.format(k)] = skew(v)
        return res
    
    dict_agg = fetch_moments(f)
    dict_agg['tempo'] = librosa.beat.tempo(y, sr=sr)[0]
    
    return dict_agg


def melspectrogram_generator(songs, n_fft=1024, hop_length=256):
    melspec = lambda x: librosa.feature.melspectrogram(x, n_fft=n_fft,
        hop_length=hop_length, n_mels=128)[:,:,np.newaxis]

    tsongs = map(melspec, songs)
    return np.array(list(tsongs))

def make_dataset_dl(path):
    signal, _ = librosa.load(path, sr=None)
    signals = split_song(signal)
    specs = melspectrogram_generator(signals)
    return specs
    
def split_song(X, overlap = 0.5):
    temp_X = []
    xshape = X.shape[0]
    chunk = 33000
    offset = int(chunk*(1.-overlap))
    spsong = [X[i:i+chunk] for i in range(0, xshape - chunk + offset, offset)]
    for s in spsong:
        if s.shape[0] != chunk:
            continue
    temp_X.append(s)
    return np.array(temp_X)