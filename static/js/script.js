
 
 // CAMERA SETTINGS.
  Webcam.set({
    width: 220,
    height: 190,
    image_format: 'jpeg',
    jpeg_quality: 100
});
Webcam.attach('.camera');

  // TAKE A SNAPSHOT.
takeSnapShot = function () {
    Webcam.snap(function (data_uri) {

        
        var str = data_uri
        
        console.log(str);
        /* downloadImage('image', data_uri); */
    });
}


// burst capture
burst_snapshot = (n) => {
    
    i=0
    burst = setInterval(function () {
            
            takeSnapShot()
            i = i+1
            console.log(i);
            if (i == n) {
                console.log('done');
                clearInterval(burst)
            }

        },3000)

}




// DOWNLOAD THE IMAGE.
downloadImage = function (name, datauri) {
    var a = document.createElement('a');
    a.setAttribute('download', name + '.jpeg');
    a.setAttribute('href', datauri);
    a.click();
}
