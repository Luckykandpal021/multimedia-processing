// document.getElementById('test').innerHTML = window.Geolocation;
// console.log("this is popup")
// document.getElementById('test').onclick=function(){
//     alert("hello bunny hunny bunny")
// }

// document.getElementById('upload_file_button')


document.getElementById('upload_file_button').addEventListener('change', async function(event) {
    const file = event.target.files[0];
    const videoPlayer = document.getElementById('videoPlayer');

    if (file) {
        const fileName = file.name;

        const apiUrl = "http://127.0.0.1:8000/extract-audio/";

        try {
            // Create a FormData object
            const formData = new FormData();
            formData.append('input_video', file);

            // Make a POST request to the API endpoint
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to extract audio');
            }

            // Once audio is extracted, display the video
            const blob = await response.blob();
            const audioURL = URL.createObjectURL(blob);
            // You can do whatever you want with the audio URL, such as playing it or downloading it
            console.log('Audio extracted successfully:', audioURL);

            // Create a Download Link
            const downloadLink=document.createElement('a');
            downloadLink.href=audioURL;
            console.log(fileName)
            downloadLink.download = fileName.replace(/\.[^/.]+$/, "") + '_audio.mp3'; // Modify the download file name
            downloadLink.style.display='none';

            document.body.appendChild(downloadLink);
            downloadLink.click();
                        // Clean up: remove the download link from the document body
                        document.body.removeChild(downloadLink);




            // Display the video in the video player
            const fileURL = URL.createObjectURL(file);
            videoPlayer.src = fileURL;
            videoPlayer.style.display = 'block';
        } catch (error) {
            console.error('Error extracting audio:', error);
        }
    }
});



// document.getElementById('upload_file_button').addEventListener('change',async function(event) {
//     const file = event.target.files[0];
//     const videoPlayer = document.getElementById('videoPlayer');

//     if (file) {
//         const apiUrl="http://127.0.0.1:8000/extract-audio/";
//         try{
//             const formData = new FormData();
//             formData.append('video',file);

//             // Make a POST Request to the Api End-Point
//             const response = await fetch(apiUrl,{
//                 method:'POST',
//                 body:formData
//             });

//             if (!response.ok){
//                 throw new Error("Failed to Upload Video");
//             }
//             else{
//                 console.log(`response Data:- ${response.body} response.text():- ${response.text()}`)
//             }
//             const fileURL = URL.createObjectURL(file);
//             videoPlayer.src = fileURL;
//             videoPlayer.style.display = 'block';
    
//         }
//         catch(error){
//             console.error('Error uploading or displaying video:', error);
//         }




//     }

// });
