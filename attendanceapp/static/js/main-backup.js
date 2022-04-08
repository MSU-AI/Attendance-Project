/* Setting Webcam */
Webcam.set({
    width: 1200,
    height: 1000,
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
    event_loop();
})


/* Defining the event_loop */
var flag = 'hand'
let event_id;
function event_loop() {
    
    event_id = setInterval(() => {
        
        if (flag == 'hand') {
            
            $("#info").text("Starting Hand Rec...");
            setTimeout(function handRec() {
                $("#info").css("visibility", "visible");
                $('#info').text('Please give a Thumbs Up');
                click();
            }, 2000);
        }


        if (flag == 'face') {
            
            $("#info").text("Starting Face Rec...");
            setTimeout(function faceRec() {
                
                $("#info").css("visibility", "visible");
                $('#info').text("Please position your face");
                click();
            }, 2000);
        }
    }, 8000);
}


/*  defining the click function */
let click_id;
var i = 0 ;
function click() {
            
    click_id = setInterval(function () {
        
        setTimeout(takeSnapShot, 2000);
        i = i+1;
        console.log(i);

    },750);
}


/* defining takeSnapShot */
takeSnapShot = function () {
    Webcam.snap(function (data_uri) {
    
        
        var str = data_uri
        
        // Here is where the metadata and payload are defined.
        // Simply create the metadata as a JSON string with key 
        // 'id' and value being the id of the event you wish to process.
    
        // Send the image for face processing:
    
        if (flag == 'face') {
            ws.send('{"id": "face", "token": ' + i + '}' + str);
        }
        
    
        // Send the image for hand processing:
        if (flag == 'hand') {
            ws.send('{"id": "hand", "token": ' + i + '}' + str);
        }
        
    
        // Send data to the dummy handler:
        if (flag == 'dummy') {
            ws.send('{"id": "dummy"}This is dummy data!');
        }
        
    
        // Raise an exception and show error handling
        if (flag == 'error') {
            ws.send('{"id": "error"}Raise an error!');
        }
        
    })};


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
        
    if (meta_data['id'] == 'hand' && flag == 'hand') {
        
        if (data['hand'] == 'thumbs up') {

            clearInterval(click_id)
            clearInterval(event_id)
            console.log("Face recogntion now!");
            $('#info').text("Please position your face");
            flag = 'face';

        }
    }

    if (meta_data['id'] == 'face') {
                
        clearInterval(click_id)
        clearInterval(event_id)        
        var name = data['name']
        if (name == 'unknown') {

            
            $("#info").text(name);
        } else{

            $("#info").text(name);
        }
        flag = 'hand'
        $('#info').text("Starting Hand Recognition");

    }    
}   
