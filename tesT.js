const apiUrl = 'http://127.0.0.1:8000/{endpoint}';
const contextEndpoint = 'get-context';
const captionEndpoint = 'get-caption';
const hashtagsEndpoint = 'get-hashtags';

const imagePath = prompt('Enter the path of the image:');
const images = new File([imagePath], imagePath);

console.log(typeof images);

images.arrayBuffer().then(buffer => {
    const imgBytes = new Uint8Array(buffer);
    const imgStr = new TextDecoder('latin1').decode(imgBytes);

    // Fetch context from image bytes
    fetch(apiUrl.replace('{endpoint}', contextEndpoint), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ img_bytes: imgStr })
    })
    .then(response => response.json())
    .then(data => {
        const context = data.context;
        console.log({ context: context, status: response.status });

        // Fetch caption based on context and mood
        const mood = "calm";
        fetch(apiUrl.replace('{endpoint}', captionEndpoint), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ context: context, mood: mood })
        })
        .then(response => response.json())
        .then(data => {
            console.log({ caption: data.captions, status: response.status });
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Uncomment the following code if you need to fetch hashtags

// const sentence = "Sitting down with my furry friend, I'm grateful for the moments of calm in my life.";
// fetch(apiUrl.replace('{endpoint}', hashtagsEndpoint), {
//     method: 'GET',
//     headers: {
//         'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ sentence: sentence })
// })
// .then(response => response.json())
// .then(data => {
//     console.log({ hashtags: data.hashtags.response, status: response.status });
// })
// .catch(error => {
//     console.error('Error:', error);
// });

