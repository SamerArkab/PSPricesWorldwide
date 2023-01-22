function searchGame() {
    // Get the game name from the input field
    const gameName = document.getElementById('game-input').value;

    document.getElementById('game-input').value = "Loading results...";

    // Create new div elements for displaying the description, and poster
    const descriptionContainer = document.getElementById("description-container");
    const posterImg = document.getElementById("poster");

    // Get the table template and table body elements
    const template = document.getElementById('table-template');
    const tableBody = template.content.querySelector('#table-body');

    const table = document.createElement("table");
    const row = document.createElement("tr");
    const cell = document.createElement("td");

    // Make a request to the Flask API
    fetch(`http://localhost:5000/app/search?game=${gameName}`)
        .then(response => response.json())
        .then(data => {
            // Clear the existing rows from the table
            tableBody.innerHTML = '';
            descriptionContainer.innerHTML = '';

            // Prepare and create the description's container
            cell.innerHTML = data.description;
            row.appendChild(cell);
            table.appendChild(row);
            descriptionContainer.appendChild(table);

            // Update the poster image
            posterImg.src = data.poster;
            //posterImg.style.height = '300px';

            // Iterate over the object and add a row to the table for each item
            for (let i = 0; i < Object.keys(data.prices).length; i++) {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${i+1}</td>
                    <td>${data.prices[i].Country}</td>
                    <td>${data.prices[i].Name}</td>
                    <td>${data.prices[i].Price}</td>
                    <td><input type="checkbox"></td>
                `;
                tableBody.appendChild(tr);
            }

            // Clone the template and append it to the table container element
            const clone = document.importNode(template.content, true);
            document.getElementById('table-container').innerHTML = '';
            document.getElementById('table-container').appendChild(clone);
            document.getElementById('button-relevance').style.display = "block";
        });
}


let images = ["images/presentation/img1.jpg", "images/presentation/img2.jpg", "images/presentation/img3.jpg",
    "images/presentation/img4.jpg", "images/presentation/img5.jpg", "images/presentation/img6.jpg",
    "images/presentation/img7.jpg", "images/presentation/img8.jpg", "images/presentation/img9.jpg",
    "images/presentation/img10.jpg", "images/presentation/img11.jpg", "images/presentation/img12.jpg",
    "images/presentation/img13.jpg", "images/presentation/img14.mp4", "images/presentation/img15.jpg"
];
let currentImage = 0;
let isVideo = false;
let video = document.getElementById("slideshow-video");

// function to update the displayed image/video
function updateMedia() {
    if (isVideo) {
        video.style.display = "block";
        document.getElementById("slideshow-image").style.display = "none";
        document.getElementById("video-source").src = images[currentImage];
    } else {
        document.getElementById("slideshow-image").src = images[currentImage];
        document.getElementById("slideshow-image").style.display = "block";
        video.style.display = "none";
    }
}

function prevMedia() {
    currentImage--;
    if (currentImage < 0) {
        currentImage = images.length - 1;
    }
    isVideo = images[currentImage].endsWith(".mp4");
    updateMedia();
}

function nextMedia() {
    currentImage++;
    if (currentImage >= images.length) {
        currentImage = 0;
    }
    isVideo = images[currentImage].endsWith(".mp4");
    updateMedia();
}

// show the first media when the page loads
isVideo = images[currentImage].endsWith(".mp4");
updateMedia();