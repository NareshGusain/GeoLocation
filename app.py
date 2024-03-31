from flask import Flask, request, jsonify,render_template
import pandas as pd
import spacy
import ast
import os
from geopy.geocoders import OpenCage
from dotenv import load_dotenv
load_dotenv()

OPENCAGE_API_KEY = os.environ.get('OPENCAGE_API_KEY')
geolocator = OpenCage(OPENCAGE_API_KEY)

# Functions here
def contextToloc(text: str) -> list:
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
    return locations

def location_to_coordinates(locations: list) -> list:
    latitudes = []
    longitudes = []
    for location in locations:
        location = geolocator.geocode(location)
        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)
    return list(zip(latitudes, longitudes))

app = Flask(__name__)

df = pd.read_csv(r'data\final_geo.csv')
df['Locations'] = df['Locations'].apply(ast.literal_eval)

nlp = spacy.load("en_core_web_sm")


@app.route('/')
@app.route('/home')
def main():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_locations():
    user_input = request.json['text']

    # Extract GPE entities
    locations = contextToloc(user_input)

    # Convert locations to lower case for case-insensitive search
    locations_lower = list(set([loc for loc in locations]))
    
    # Search DataFrame for similar locations
    filtered_rows = df[df['Locations'].apply(lambda x: any(isinstance(x, list) and loc.lower() in map(str.lower, x) for loc in locations_lower))]

    # Convert locations to coordinates
    coordinates = location_to_coordinates(locations)

    # Prepare response data
    response_data = {
        'coordinates': coordinates,
        'locations': locations_lower,
        'results': filtered_rows.to_dict(orient='records')
    }
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
