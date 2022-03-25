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
                
    
                
                takeSnapShot();
                i = i+1;
                console.log(i);
        
            },750);
        }
        
        var flag = 'hand';
        
        function event_loop() {
        

                
                
                setInterval(
                    ()=>{
                        if (flag == 'hand') {
                    
                            $("#info").text("Starting Hand Rec...");
                            setTimeout(handRec, 2000);
                            
        
                            
                        }
                
                        if (flag == 'face') {
                            
                            $("#info").text("Starting Face Rec...");
                            setTimeout(faceRec, 2000);
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
            $('#info').text('Please give a Thumbs Up');
            click();
        
        }
        
        function faceRec() {
            //flag = 'face';
            $('#info').text("Please position your face");
            click();
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
                
                $('#info').text(JSON.stringify(data));
                flag = 'hand';
            }
        
        
          };
        
        
        event_loop();
        
    });

}

project()
