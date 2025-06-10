// Géolocalisation pour remplir l’adresse de départ
window.addEventListener('load', () => {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(async (position) => {
            const { latitude, longitude } = position.coords;
            const response = await fetch('https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}');
            const data = await response.json();
            document.getElementById("depart").value = data.display_name;

            // Afficher carte
            const map = L.map('map').setView([latitude, longitude], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);
            L.marker([latitude, longitude]).addTo(map)
                .bindPopup("Votre position")
                .openPopup();
        }, () => {
            alert("Impossible de récupérer votre position.");
        });
    } else {
        alert("Géolocalisation non supportée par votre navigateur.");
    }
});

// Autocomplétion avec Nominatim (OpenStreetMap)
const arriveeInput = document.getElementById("arrivee");
const suggestionsList = document.getElementById("suggestions");

arriveeInput.addEventListener("input", async () => {
    const search = arriveeInput.value;
    if (search.length < 3) {
        suggestionsList.innerHTML = "";
        return;
    }

    const response = await fetch('https://nominatim.openstreetmap.org/search?q=${search}&format=json&addressdetails=1&limit=5');
    const results = await response.json();

    suggestionsList.innerHTML = "";
    results.forEach(place => {
        const li = document.createElement("li");
        li.textContent = place.display_name;
        li.addEventListener("click", () => {
            arriveeInput.value = place.display_name;
            suggestionsList.innerHTML = "";
        });
        suggestionsList.appendChild(li);
    });
});








