/* Setting Webcam */
Webcam.set({
    width: 640,
    height: 600,
    image_format: 'jpeg',
    jpeg_quality: 100
});

// attach camera to the element on screen
Webcam.attach('#camera');

 /* Checking the protocal for local and production testing*/
let WS_URL
if (location.protocol == 'http:'){

    console.log("HTTP Connection")
    WS_URL = "ws://localhost:8000/ws/camera";

 }
 
if (location.protocol == 'https:'){

    WS_URL =  "wss://test.msuaiclub.com:443/ws/camera"

 }
 
/* setting up WebSocket Connection */
const ws = new WebSocket(WS_URL);
ws.onopen = () => {

    // checking state of connection
    console.log(`Connected to ${WS_URL}`);

}
 

/* on the click of this button: transition to Recog page */
$(".ctn").click(function (e) { 
    e.preventDefault();
    $("#landing-container").css("display", "none");
    $("#camera-page").css("display", "block");
    start();
})

// 0 is hand and 1 is face
let flag = 0;

/*  defining the click function */
let i = 0 ;
function click() {
    let initial = flag;        
    while(true){
        setTimeout(takeSnapShot, 2000);
        i = i+1;
        console.log(i);
        if (flag != initial){
            break;
        }
    }        

}

/* defining takeSnapShot */
takeSnapShot = function () {
    Webcam.snap(function (data_uri) {
    
        
        var str = data_uri
        
        // Here is where the metadata and payload are defined.
        // Simply create the metadata as a JSON string with key 
        // 'id' and value being the id of the event you wish to process.
    
        // Send the image for face processing:
    
        if (flag == 1) {
            ws.send('{"id": "face", "token": ' + i + '}' + str);
        }
        
    
        // Send the image for hand processing:
        if (flag == 0) {
            ws.send('{"id": "hand", "token": ' + i + '}' + str);
        }
        
    
        // Send data to the dummy handler:
        if (flag == -1) {
            ws.send('{"id": "dummy"}This is dummy data!');
        }
        
    
        // Raise an exception and show error handling
        if (flag == 'error') {
            ws.send('{"id": "error"}Raise an error!');
        }
        
    })};

// Getting info through the websocket
ws.onmessage = (message) => {
    
    // Decode any metadata we sent:

    meta = message.data.slice(0, message.data.indexOf('}')+1);

    // Get payload data:

    payload = message.data.slice(message.data.indexOf('}')+1);

    // Output some stuff:

    data = JSON.parse(payload);
    meta_data = JSON.parse(meta);
    console.log("Server says:", JSON.stringify(data));
    console.log("Metadata: " + meta);

    console.log(meta_data['id']);
        
    if (meta_data['id'] == 'hand' && flag == 0) {
        
        if (data[0] == 'thumbs up') {
            console.log("Face recogntion now!");
            $('#info').text("Please position your face");
            flag = 1;
            start();
        }
    }

    if (meta_data['id'] == 'face') {
                       
        var name = JSON.stringify(data).slice(52,-3)
        if (name == 'unknown') {

            
            $("#link").css("display", "inline-block");
            $("#continue").css("display", "inline-block");
            $("#name-unknown-box").cs
            s("display", "block");
            $("#info").css("display", "none");

            nameDisplay = "Sorry, you were not recognised."
            $(".name-display").text(nameDisplay);

        } else{

            $("#link").css("display", "none");
            $("#name-unknown-box").css("display", "block");
            nameDisplay = "Name: " + name
            $('#name-display').text(nameDisplay);
            setTimeout(() => {

                $("#name-unknown-box").css("display", "none");
                $("#info").css("display", "block");

            },3000)
        }
        flag = 0;
        start();
}   
}  

function start(){
    if (flag == 0){
        $("#info").text("Starting Hand Rec...");
            setTimeout(function handRec() {
                $("#info").css("visibility", "visible");
                $('#info').text('Please give a Thumbs Up');
                click();
            }, 2000);
    }
    if (flag == 1){
        $("#info").text("Starting Face Rec...");
            setTimeout(function faceRec() {
                
                $("#info").css("visibility", "visible");
                $('#info').text("Please position your face");
                click();
            }, 2000);
    }
}