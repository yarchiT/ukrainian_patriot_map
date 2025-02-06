from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import json

def get_coordinates(city, region, country="Ukraine"):
    """Get coordinates for a given city and region."""
    geolocator = Nominatim(user_agent="my_agent")
    try:
        # Try with region first
        location = geolocator.geocode(f"{city}, {region} Oblast, {country}")
        if location:
            return {"coords": [location.latitude, location.longitude], "with_region": True}
        
        # Fallback to city and country
        location = geolocator.geocode(f"{city}, {country}")
        if location:
            return {"coords": [location.latitude, location.longitude], "with_region": False}
        
        return None
    except GeocoderTimedOut:
        return None

# Dictionary of regions and their cities
regions_cities = {
    "Chernihiv": ["Chernihiv", "Mena"],
    "Dnipropetrovsk": ["Dnipro", "Gvardiyske", "Mechnikov", "Kryvyi Rih", "Orlivshchyna", "Pavlohrad"],
    "Donetsk": ["Chasiv Yar", "Dobropillya", "Druzhkivka", "Kostyantynivka", "Kramatorsk", 
                "Kurakhove", "Lyman", "Myrnohrad", "Niu York", "Pokrovsk", "Slovyansk"],
    "Kharkiv": ["Babai", "Barvinkove", "Chuhuiv", "Havrylivka", "Hontarivka", "Izyum", 
                "Krasnohrad", "Kupyansk", "Nova Vodolaha", "Saltivka", "Shevchenkove", "Taranivka"],
    "Kherson": ["Kherson", "Bilozerka", "Ivanivka", "Antonivka"],
    "Kirovogradska": ["Kropyvnytskyi"],
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
    found_with_region = []
    found_without_region = []
    not_found = []
    
    # Process each city in each region
    for region, cities in regions_cities.items():
        for city in cities:
            print(f"Processing {city} in {region} region...")
            result = get_coordinates(city, region)
            
            if result:
                city_data = {
                    "name": city,
                    "coordinates": result["coords"]
                }
                cities_data.append(city_data)
                
                if result["with_region"]:
                    found_with_region.append(f"{city} ({region})")
                else:
                    found_without_region.append(f"{city} ({region})")
            else:
                not_found.append(f"{city} ({region})")
                print(f"Could not find coordinates for {city}, {region}")
            
            time.sleep(1)
    
    # Convert to JSON format and save
    json_data = json.dumps(cities_data, indent=2, ensure_ascii=False)
    with open('ukrainian_cities.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
    
    # Print summary
    print("\nProcess completed. Data saved to 'ukrainian_cities.json'")
    print(f"\nCities found with region ({len(found_with_region)}):")
    for city in found_with_region:
        print(f"- {city}")
        
    print(f"\nCities found without region ({len(found_without_region)}):")
    for city in found_without_region:
        print(f"- {city}")
        
    print(f"\nCities not found ({len(not_found)}):")
    for city in not_found:
        print(f"- {city}")
    
    print(f"\nTotal cities processed: {len(cities_data)} out of {sum(len(cities) for cities in regions_cities.values())}")

if __name__ == "__main__":
    main()