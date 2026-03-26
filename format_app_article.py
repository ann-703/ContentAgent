import json

with open("apps_data.json", "r") as f:
    apps = json.load(f)

md_content = """# The Top 30 Education Apps Right Now: Features, Ratings, and Real Reviews

If you want to understand where EdTech is heading, just look at what people navigate to when they open the App Store. Here is a comprehensive breakdown of the Top 30 Free Education Apps today. We've pulled their core features straight from the App Store, along with their ratings and real summaries of what users love—and what they don't.

"""

for i, app in enumerate(apps):
    try:
        rev_count = f"{int(app['review_count']):,}"
    except:
        rev_count = str(app['review_count'])
        
    md_content += f"## {i+1}. {app['name']}\n"
    md_content += f"**Rating:** ⭐ {app['rating']} | **Reviews:** {rev_count}\n\n"
    
    md_content += f"**App Store Features:**\n_{app['features']}_\n\n"
    
    if app['pros']:
        md_content += "**What People Love (Top Positive Reviews):**\n"
        for pro in app['pros']:
            md_content += f"- {pro}\n"
        md_content += "\n"
        
    if app['cons']:
        md_content += "**What Needs Work (Top Critical Reviews):**\n"
        for con in app['cons']:
            md_content += f"- {con}\n"
        md_content += "\n"
        
    md_content += "---\n\n"

md_content += """
What education apps are staples on your phone right now? Let me know in the comments.
"""

with open("2026-03-04/substack_top_education_apps.md", "w") as f:
    f.write(md_content)

print("Article generated at 2026-03-04/substack_top_education_apps.md")
