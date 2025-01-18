from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import json

def get_coordinates(city, country="Ukraine"):
    """Get coordinates for a given city."""
    geolocator = Nominatim(user_agent="my_agent")
    try:
        # Add country to make search more precise
        location = geolocator.geocode(f"{city}, {country}")
        if location:
            return [location.latitude, location.longitude]
        return None
    except GeocoderTimedOut:
        return None

# Dictionary of regions and their cities
regions_cities = {
    "Chernihiv": ["Chernihiv", "Mena"],
    "Dnipro": ["Dnipro", "Gvardiyske", "Mechnikov", "Kryvyi Rih", "Orlivshchyna", "Pavlohrad"],
    "Donetsk": ["Chasiv Yar", "Dobropillya", "Druzhkivka", "Kostyantynivka", "Kramatorsk", 
                "Kurakhova", "Lyman", "Myrnohrad", "Niu York", "Pokrovsk", "Slovyansk"],
    "Kharkiv": ["Babai", "Barvinkove", "Chuhuiv", "Havrylivka", "Hontarivka", "Izyum", 
                "Krasnohrad", "Kupyansk", "Nova Vodolaha", "Saltivka", "Shevchenkove", "Taranivka"],
    "Kherson": ["Kherson", "Bilozerka", "Ivanivka", "Antonivka"],
    "Kropyvnitsky": ["Kirovogradska"],
    "Kyiv": ["Kyiv", "Bucha", "Irpin", "Hostomel"],
    "Lviv": ["Lviv"],
    "Mykolaiv": ["Snihurivka", "Blahodatne"],
    "Odesa": ["Odesa", "Shyryaeve"],
    "Poltava": ["Poltava"],
    "Rivne": ["Rivne"],
    "Sumy": ["Sumy"],
    "Ternopil": ["Ternopil"],
    "Zaporizhzhia": ["Zaporizhzhia", "Zarichne"],
    "Zhytomyr": ["Zhytomyr", "Berdychiv", "Korosten", "Nove Zhyttia"]
}

def main():
    cities_data = []
    
    # Process each city in each region
    for region, cities in regions_cities.items():
        for city in cities:
            print(f"Processing {city}...")
            coords = get_coordinates(city)
            
            if coords:
                city_data = {
                    "name": city,
                    "coordinates": coords
                }
                cities_data.append(city_data)
            else:
                print(f"Could not find coordinates for {city}")
            
            # Add delay to avoid hitting rate limits
            time.sleep(1)
    
    # Convert to JSON format
    json_data = json.dumps(cities_data, indent=2, ensure_ascii=False)
    
    # Save to file
    with open('ukrainian_cities.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
    
    print("\nProcess completed. Data saved to 'ukrainian_cities.json'")
    print(f"Successfully processed {len(cities_data)} cities")

if __name__ == "__main__":
    main()