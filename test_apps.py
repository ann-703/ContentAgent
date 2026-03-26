import requests

url = "https://itunes.apple.com/us/rss/topfreeapplications/limit=30/genre=6017/json"
resp = requests.get(url).json()

apps = resp["feed"]["entry"]
for i, entry in enumerate(apps):
    app_id = entry["id"]["attributes"]["im:id"]
    name = entry["im:name"]["label"]
    lookup_url = f"https://itunes.apple.com/lookup?id={app_id}"
    try:
        lookup_resp = requests.get(lookup_url).json()
        rating = lookup_resp["results"][0].get("averageUserRating", "N/A")
    except:
        rating = "N/A"
    print(f"{i+1}. {name} - Rating: {rating}")
