

Webcam.set({
    width: 640,
    height: 600,
    image_format: 'jpeg',
    jpeg_quality: 100
});
// attach camera to the element
Webcam.attach('#camera');


function project() {
    
    $(".ctn").click(function (e) { 
        e.preventDefault();
        $("#landing-container").css("display", "none");
        $("#camera-page").css("display", "block");

        /* Checking the protocal */
        let WS_URL
        if (location.protocol == 'http:'){
            console.log("HTTP Connection")
            WS_URL = "ws://localhost:8000/ws/camera";
        }
        
        if (location.protocol == 'https:'){
            WS_URL =  "wss://test.msuaiclub.com:443/ws/camera"
        }
        
        // make connection
        const ws = new WebSocket(WS_URL);
        ws.onopen = () => {
          console.log(`Connected to ${WS_URL}`);
        }
        
        // set camera click
        
        var i = 0;
        
        function click() {
            
            setInterval(function () {
                
                if (eventFlag) {
                    takeSnapShot();
                    i = i+1;
                    console.log(i);
                }
                
                
        
            },750);
        }
        
        var flag = 'hand';
        var eventFlag = true
        var onceHM = true
        function event_loop() {
        

                
                k = 0
                setInterval(
                    ()=>{

                        console.log("eventloop new iteration");
                        if (eventFlag) {
                            if (flag == 'hand') {
                                if (onceHM){
                                    $("#info").text("Starting Hand Rec...");
                                    onceHM = false
                                }
                            setTimeout(handRec, 5000);
                            
        
                            
                        }
                
                        if (flag == 'face') {
                            $("#info").text("Starting Face Rec...");
                            setTimeout(faceRec, 5000);
                        }
                        }
                        
                }, 2000
                );
                

                    
               
    
                
                    
                    

        
        
            
        }
        
        // TAKE A SNAPSHOT.
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
        
        
        function handRec() {
            //flag = 'hand';
            $("#info").css("visibility", "visible");
            $('#info').text('Please give a Thumbs Up');
            setTimeout(click,1000);
        
        }
        
        function faceRec() {
            //flag = 'face';
            $("#info").css("visibility", "visible");
            $('#info').text("Please position your face");
            setTimeout(click,3000);
        }
        
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
            // output.innerText = JSON.stringify(data);
        
            console.log(meta_data['id']);
        
            if (meta_data['id'] == 'hand' && flag == 'hand') {
                
                if (data[0] == 'thumbs up') {
        
                    
                    console.log("Face recogntion now!");
                    
                    $('#info').text("Please position your face");
                    flag = 'face';
        
                }
            }
        
            if (meta_data['id'] == 'face') {
                
                
                var name = JSON.stringify(data).slice(52,-3)
                if (name == 'unknown') {

                    
                    eventFlag = false
                    $("#link").css("display", "inline-block");
                    $("#continue").css("display", "inline-block");
                    $("#name-unknown-box").css("display", "block");
                    $("#info").css("display", "none");

                    nameDisplay = "Sorry, you were not recognised."
                    $(".name-display").text(nameDisplay);

                    $("#continue").click(function (e) { 
                        e.preventDefault();
                        $("#name-unknown-box").css("display", "none");
                        $("#info").css("display", "block");
                        eventFlag = true
                        onceHM = true
                    });
                    
                    

                } else {
                    eventFlag = false
                    $("#link").css("display", "none");
                    $("#name-unknown-box").css("display", "block");
                    nameDisplay = "Name: " + name
                    $('#name-display').text(nameDisplay);
                    setTimeout(() => {

                        eventFlag = true
                        $("#name-unknown-box").css("display", "none");
                        $("#info").css("display", "block");
                        onceHM = true
                    },8000)
                }
                 
                
                flag = 'hand';
            }
        
        
          };
        
        
        event_loop();
        
    });

}

project()
