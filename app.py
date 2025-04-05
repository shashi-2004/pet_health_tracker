import requests

@app.route('/fetch_activity/<pet_id>')
def fetch_activity(pet_id):
    api_key = "YOUR_FITBARK_API_KEY"  # FitBark API key teeskunna
    url = f"https://api.fitbark.com/v2/activity?pet_id={pet_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return jsonify({"activity": data["daily_activity"]})
    return jsonify({"error": "Unable to fetch activity data"})