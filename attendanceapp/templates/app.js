// CAMERA SETTINGS.

  Webcam.set({
    width: 220,
    height: 190,
    image_format: 'jpeg',
    jpeg_quality: 100
});
// attach camera to the element
Webcam.attach('.camera');



  // TAKE A SNAPSHOT.
takeSnapShot = function () {
    Webcam.snap(function (data_uri) {

        
        var str = data_uri
        

        ws.send(str)
    });
}




// burst capture
burst_snapshot = (n) => { // n is the number of picture you need
    
    i=0
    burst = setInterval(function () {
            
            takeSnapShot()
            i = i+1
            console.log(i);
            if (i == n) {
                console.log('done');
                clearInterval(burst)
            }

        },3000) // 3000 is 3 seconds per image

}



/* Checking the protocal */
let WS_URL
if (location.protocal == 'http:'){
    WS_URL = "ws://localhost:8000/ws/camera";
}

if (location.protocal == 'https:'){
    WS_URL =  "wss://test.msuaiclub.com:443/ws/camera"
}

const FPS = 3;
const ws = new WebSocket(WS_URL);
ws.onopen = () => {
  console.log(`Connected to ${WS_URL}`);
}

let output = document.createElement("p")
ws.onmessage = (message) => {
        dataFromServer = JSON.parse(message.data);
        console.log("Server says:", JSON.stringify(dataFromServer));
        output.innerText = JSON.stringify(dataFromServer)
      };

