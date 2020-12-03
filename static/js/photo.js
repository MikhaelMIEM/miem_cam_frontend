(function() {
  var streaming = false;
  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;
  var downloadbutton = null;

  function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');
    downloadbutton = document.getElementById('downloadbutton')

    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function(err) {
      console.log("An error occurred: " + err);
    });

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        streaming = true;
      }
    }, false);

    startbutton.addEventListener('click', function(ev){
      takepicture();
      ev.preventDefault();
    }, false);

    downloadbutton.addEventListener('click', function(ev){
      downloadpicture();
      ev.preventDefault();
    }, false);
    
    //clearphoto();
  }

  function clearphoto() {
    var context = canvas.getContext('2d');
    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
  }

  function takepicture() {
    var context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);//, video.videoWidth, video.videoHeight);
    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
  }

  function download(filename, data) { 
    var element = document.createElement('a'); 
    element.setAttribute('href',  data); 
    element.setAttribute('download', filename); 
    document.body.appendChild(element); 
    element.click(); 
    document.body.removeChild(element); 
  } 

  function downloadpicture() {
    var data = canvas.toDataURL('image/png');
    download('snapshot.png', data)
  }


  window.addEventListener('load', startup, false);
})();