import requests
import csv

def get_temples_in_gujarat():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area["ISO3166-2"="IN-GJ"]->.search;
    (
    node["amenity"="place_of_worship"](area.search);
    node["religion"="hindu"](area.search);
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        data = response.json()
        temples = []

        for element in data['elements']:
            temple_info = {
                'name': element.get('tags', {}).get('name', 'N/A'),
                'latitude': element.get('lat', 'N/A'),
                'longitude': element.get('lon', 'N/A')
            }
            temples.append(temple_info)

        return temples
    else:
        print(f"Error: {response.status_code}")
        return None

def save_to_csv(temples, filename='temples_in_gujarat.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'latitude', 'longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for temple in temples:
            writer.writerow(temple)

if __name__ == "__main__":
    temples_in_gujarat = get_temples_in_gujarat()
    
    if temples_in_gujarat:
        save_to_csv(temples_in_gujarat)
        print("Data has been saved to temples_in_gujarat.csv.")
    else:
        print("Unable to fetch data or no temples found.")
