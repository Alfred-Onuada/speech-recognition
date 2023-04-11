from flask import Flask, render_template, request
import os
from recognizer import predict_speaker
import ffmpeg

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']

    # check if the user already exists (his/her folder)
    if os.path.exists(f"./users/{name}"):
        return { "message": "User exists" }

    # create the folder
    os.makedirs(f"./users/{name}")

    for idx in request.files :
        voice = request.files[idx]

        voice.save(f"{os.curdir}/users/{name}/recording_{voice.filename}")

    return { "message": "Success" }

@app.route('/signin', methods=['POST'])
def verify():
    name = request.form['name']

    # check if the user already exists (his/her folder) and audio as well
    if os.path.exists(f"./users/{name}") == False:
        return { "message": "User doesn't exist" }
    
    for idx in request.files:
        testVoice = request.files[idx]

        testVoice.save(f"{os.curdir}/verify/{testVoice.filename}")
        break # i need only one

    input_file = f"{os.curdir}/verify/{testVoice.filename}"
    output_file = f"{os.curdir}/verify/{testVoice.name}.wav"

    stream = ffmpeg.input(input_file)
    audio = stream.audio
    output = ffmpeg.output(audio, output_file)
    ffmpeg.run(output)
    
    verifiedUser = predict_speaker(f"{os.curdir}/verify/{testVoice.name}.wav")

    os.unlink(f"{os.curdir}/verify/{testVoice.name}.wav")
    os.unlink(f"{os.curdir}/verify/{testVoice.filename}")

    print(verifiedUser)

    if verifiedUser != name:
        return { "message": "Not matched" }

    return { "message": "Success" }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))
