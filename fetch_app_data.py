import requests
import json
import time

url = "https://itunes.apple.com/us/rss/topfreeapplications/limit=30/genre=6017/json"
resp = requests.get(url).json()

apps = resp["feed"]["entry"]
results = []

for entry in apps:
    app_id = entry["id"]["attributes"]["im:id"]
    name = entry["im:name"]["label"]
    
    # 1. Look up rating, review count, and description
    lookup_url = f"https://itunes.apple.com/lookup?id={app_id}"
    try:
        lookup_resp = requests.get(lookup_url).json()
        if lookup_resp["resultCount"] > 0:
            app_info = lookup_resp["results"][0]
            rating = app_info.get("averageUserRating", "N/A")
            if rating != "N/A":
                rating = round(rating, 1)
            review_count = app_info.get("userRatingCount", "N/A")
            desc = app_info.get("description", "")
            # keep top 400 chars of features/description
            features = desc[:400].replace('\n', ' ') + "..."
        else:
            rating, review_count, features = "N/A", "N/A", "No description."
    except Exception as e:
        rating, review_count, features = "N/A", "N/A", "Failed to fetch."

    # 2. Get customer reviews
    reviews_url = f"https://itunes.apple.com/us/rss/customerreviews/id={app_id}/sortBy=mostHelpful/json"
    pros = []
    cons = []
    try:
        rev_resp = requests.get(reviews_url).json()
        if "feed" in rev_resp and "entry" in rev_resp["feed"]:
            entries = rev_resp["feed"]["entry"]
            if type(entries) == list:
                for r in entries:
                    if "author" not in r: continue
                    r_rating = int(r.get("im:rating", {}).get("label", "3"))
                    title = r.get("title", {}).get("label", "")
                    content = r.get("content", {}).get("label", "").replace('\n', ' ')[:100] + "..."
                    text = f"{title} - {content}"
                    if r_rating >= 4 and len(pros) < 2:
                        pros.append(text)
                    elif r_rating <= 3 and len(cons) < 2:
                        cons.append(text)
    except Exception as e:
        pass
        
    print(f"Fetched data for {name}... {rating} stars | {review_count} reviews")
    
    results.append({
        "name": name,
        "rating": rating,
        "review_count": review_count,
        "features": features,
        "pros": pros,
        "cons": cons
    })
    
    time.sleep(0.5)

with open("apps_data.json", "w") as f:
    json.dump(results, f, indent=2)
print("Saved to apps_data.json")
