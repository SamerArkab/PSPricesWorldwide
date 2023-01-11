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