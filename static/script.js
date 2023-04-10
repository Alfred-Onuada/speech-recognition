class VoiceRecorder{
    savedAudio = []; // can be deleted using index
    audioBlobs = [];
    mediaRecorder = null;
    streamBeingCaptured = null;
    mimeType = null;

    record = async () => {
        // check if recording is supported
        if (!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
            alert("User's device doesn't support audio recording")
            return
        }

        if (this.mediaRecorder) {
            alert("Please stop current recording first");
            return;
        }

        try {
            // store the stream
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.streamBeingCaptured = stream;
    
            this.mediaRecorder = new MediaRecorder(stream);
    
            this.mediaRecorder.ondataavailable = (e) => {
                this.audioBlobs.push(e.data);
            }
    
            // start recording (100ms interval)
            this.mediaRecorder.start(500);
        } catch (error) {
            console.log(error);
        }
    };
    stop = (recordingCancelled) => {
        try {
            this.mimeType = this.mediaRecorder.mimeType;

            this.mediaRecorder.onstop = () => {
                if (recordingCancelled == false) {
                    // handle appending the recorded track to a list so user can see it.
                    const sessions = document.getElementById('sessions');
    
                    // build audio
                    const audioBlob = new Blob(this.audioBlobs, { type: this.mimeType });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    
                    this.savedAudio.push(audioBlob);

                    const audioId = this.savedAudio.length - 1;
    
                    const audioElem = document.createElement('audio');
                    audioElem.id = audioId;
                    audioElem.classList.add("audioElem")
                    audioElem.src = audioUrl;
                    audioElem.controls = true;
    
                    sessions.appendChild(audioElem);
                }

                // this basically stops all the active recording sessions
                this.streamBeingCaptured.getTracks().forEach(track => track.stop())
        
                this.audioBlobs = [];
                this.mediaRecorder = null;
                this.streamBeingCaptured = null;
                this.mimeType = null;
            }
    
            this.mediaRecorder.stop();
        } catch (error) {
            console.log(error);
        }
    };
    cancel = () => {
        this.stop(true)
    };
    upload = async () => {    
        const name = document.getElementById('name').value;

        const payload = new FormData()
        payload.append('name', name);

        this.savedAudio.forEach((blob, idx) => {
            let ext = blob.type.split(';')[0].replace(/.*\//, '');
            payload.append(idx, blob, idx+'.'+ext);
        })

        try {
            const resp = await fetch('/upload', {
                method: 'POST',
                body: payload
            })

            const data = await resp.json();

            alert(data.message);
        } catch (error) {
            alert(error);
            console.log(error);
        }
    };
    verify = async () => {    
        const name = document.getElementById('name').value;

        const payload = new FormData()
        payload.append('name', name);

        let voiceSample = this.savedAudio[0];
        let ext = voiceSample.type.split(';')[0].replace(/.*\//, '');
        payload.append(name+'_verify', voiceSample, name+'_verify.'+ext);

        try {
            const resp = await fetch('/signin', {
                method: 'POST',
                body: payload
            })

            const data = await resp.json();

            alert(data.message);
        } catch (error) {
            alert(error);
            console.log(error);
        }
    };
}

const recorder = new VoiceRecorder();

document.getElementById('record') && document.getElementById('record').addEventListener('click', recorder.record);
document.getElementById('stop') && document.getElementById('stop').addEventListener('click', () => recorder.stop(false));
document.getElementById('cancel') && document.getElementById('cancel').addEventListener('click', recorder.cancel);
document.getElementById('upload') && document.getElementById('upload').addEventListener('click', recorder.upload);
document.getElementById('verify') && document.getElementById('verify').addEventListener('click', recorder.verify);

