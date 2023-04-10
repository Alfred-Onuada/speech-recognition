import os
import glob
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import random

# Set up the folders where the audio samples are stored
folders = [f"./samples/Actor_{i if i >= 10 else '0' + str(i)}" for i in range(1, 25)]
userAudios = [dir for dir in os.listdir('./users/') if dir != '.DS_Store']

# Set up the parameters for preprocessing the audio samples
sr = 16000  # sample rate
duration = 3  # length of audio sample in seconds

# Set up a list to hold the audio features and labels
X = []
y = []

# train on sample audio files
for idx, folder in enumerate(folders):
    # Read and preprocess the audio samples from folders
    for audio_file in glob.glob(os.path.join(folder, '*.wav')):
        # Load the audio sample
        audio, _ = librosa.load(audio_file, sr=sr, duration=duration)
        # Extract the Mel-Frequency Cepstral Coefficients (MFCCs) from the audio sample
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)

        # some audio samples don't follow the regular shape
        if np.array(mfccs).shape != (13, 94):
            print("Invalid")
            print(audio_file)
            print(folder)
            continue

        # Append the MFCCs to the feature list and add the label for this speaker
        X.append(mfccs)
        y.append(idx + 1)  # speaker 1

# train on user audio
for idx, folder in enumerate(userAudios):
    # Read and preprocess the audio samples from folders
    for audio_file in glob.glob(os.path.join("./users/", folder, '*.wav')):
        # Load the audio sample
        audio, _ = librosa.load(audio_file, sr=sr, duration=duration)
        # Extract the Mel-Frequency Cepstral Coefficients (MFCCs) from the audio sample
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)

        # some audio samples don't follow the regular shape
        if np.array(mfccs).shape != (13, 94):
            print("Invalid")
            print(audio_file)
            print(folder)
            continue

        # Append the MFCCs to the feature list and add the label for this speaker
        X.append(mfccs)
        y.append(folder)  # speaker 1


# Convert the feature list to a numpy array
X = np.array(X, dtype=object)

# Split the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

# Train a logistic regression classifier on the training data
clf = LogisticRegression()
clf.fit(X_train.reshape(len(X_train), -1), y_train)

# Evaluate the performance of the classifier on the validation data
accuracy = clf.score(X_val.reshape(len(X_val), -1), y_val)
print('Validation accuracy: {:.2f}%'.format(accuracy * 100))

# Given a new audio sample, extract its features and predict the speaker
def predict_speaker(audio_file):
    # Load the audio sample
    audio, _ = librosa.load(audio_file, sr=sr, duration=duration)
    # Extract the MFCCs from the audio sample
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    # Reshape the MFCCs to match the shape of the training data
    mfccs = mfccs.reshape(1, -1)
    # Predict the speaker label for the new sample
    label = clf.predict(mfccs)
    # Return the predicted speaker label

    return label


if __name__ == '__main__':
    testAudio = [
        './samples/Actor_01/03-01-08-02-02-01-01.wav',
        './samples/Actor_01/03-01-08-01-01-01-01.wav',
        './samples/Actor_01/03-01-05-01-02-01-01.wav', 
        './samples/Actor_01/03-01-06-01-02-02-01.wav',
        './samples/Actor_01/03-01-06-02-01-02-01.wav',
        './samples/Actor_01/03-01-05-02-01-01-01.wav',
        './samples/Actor_02/03-01-08-02-02-01-02.wav',
        './samples/Actor_02/03-01-08-01-01-01-02.wav',
        './samples/Actor_02/03-01-05-01-02-01-02.wav', 
        './samples/Actor_02/03-01-06-01-02-02-02.wav',
        './samples/Actor_02/03-01-06-02-01-02-02.wav',
        './samples/Actor_02/03-01-05-02-01-01-02.wav',
        './samples/Actor_03/03-01-08-02-02-01-03.wav',
        './samples/Actor_03/03-01-08-01-01-01-03.wav',
        './samples/Actor_03/03-01-05-01-02-01-03.wav', 
        './samples/Actor_03/03-01-06-01-02-02-03.wav',
        './samples/Actor_03/03-01-06-02-01-02-03.wav',
        './samples/Actor_03/03-01-05-02-01-01-03.wav',
        './samples/Actor_04/03-01-08-02-02-01-04.wav',
        './samples/Actor_04/03-01-08-01-01-01-04.wav',
        './samples/Actor_04/03-01-05-01-02-01-04.wav', 
        './samples/Actor_04/03-01-06-01-02-02-04.wav',
        './samples/Actor_04/03-01-06-02-01-02-04.wav',
        './samples/Actor_04/03-01-05-02-01-01-04.wav',
        './verify/recording_0.wav',
        './verify/recording_1.wav',
        './verify/recording_2.wav',
    ]

    random.shuffle(testAudio)

    for file in testAudio:
        print(f"Now testing audio from {file}: Speaker {predict_speaker(file)}")