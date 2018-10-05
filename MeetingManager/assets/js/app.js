const recordAudio = () =>
  new Promise(async resolve => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });

const start = () => mediaRecorder.start();

var audioUrl, audioBlob;

const stop = () =>
  new Promise(resolve => {
    mediaRecorder.addEventListener("stop", () => {
      audioBlob = new Blob(audioChunks);
      audioUrl = URL.createObjectURL(audioBlob);
      console.log(audioUrl);
      var a = document.createElement("a");
      document.body.appendChild(a);
      a.style = "display: none";
      a.href = audioUrl;
      a.download = 'filename.wav';
      a.click();
      document.body.removeChild(a);
      const audio = new Audio(audioUrl);
      const play = () => audio.play();
      resolve({ audioBlob, audioUrl, play });
    });

      mediaRecorder.stop();
    });

  resolve({ start, stop });
});

const sleep = time => new Promise(resolve => setTimeout(resolve, time));

var recorder;
var audio;

const recordAction = async () => {
  recorder = await recordAudio();
  const recordButton = document.getElementById('recordButton');
  recordButton.disabled = true;
  recorder.start();
  /*await sleep(3000);
  const audio = await recorder.stop();
  audio.play();
  await sleep(3000);
  recordButton.disabled = false;*/
}
const stopAction = async () => {
  audio = await recorder.stop();
  recordButton.disabled = false;
}
const playAction = async () => {
  audio.play();
  await sleep(3000);
}

const saveAction = async () => {

}


