const fetch = require('node-fetch');
const fs = require('fs');

async function getUkraineBorders() {
    try {
        // Fetch GeoJSON data for Ukraine from OpenStreetMap's Nominatim service
        const response = await fetch(
            'https://nominatim.openstreetmap.org/search?country=Ukraine&format=geojson&polygon_geojson=1'
        );
        const data = await response.json();

        // Get the first feature (should be Ukraine)
        const ukraineFeature = data.features[0];
        
        // Extract coordinates from the polygon
        const coordinates = ukraineFeature.geometry.coordinates[0];

        // Format coordinates for Leaflet
        const formattedCoords = coordinates.map(coord => 
            `    [${coord[1]}, ${coord[0]}]`  // Note: Leaflet uses [lat, lng] format
        ).join(',\n');

        // Create the complete content with variable declaration
        const fileContent = `// Ukraine border coordinates for Leaflet
const ukraineBorders = [\n${formattedCoords}\n];

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ukraineBorders;
}`;

        // Write to file
        fs.writeFileSync('ukraine-borders.js', fileContent);
        console.log('Coordinates have been saved to ukraine-borders.js');

    } catch (error) {
        console.error('Error fetching Ukraine borders:', error);
    }
}

getUkraineBorders();