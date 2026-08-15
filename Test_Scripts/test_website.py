from App.website_manager import (

    download_webpage,
    extract_visible_text,
    clean_text,
    save_website_knowledge
)

url = "https://example.com"

html = download_webpage(url)

text = extract_visible_text(html)

cleaned = clean_text(text)

save_website_knowledge(cleaned)

print("Website knowledge saved successfully.")


