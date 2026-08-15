from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Hello! Please respond with a short sentence confirming that Gemini is working."
)

print(response.text)


