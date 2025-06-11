import os
import aiohttp
from aiohttp import web

# Load OpenWeather API key from file
def get_api_key():
    with open("open_weather_key", "r") as f:
        return f.read().strip()

API_KEY = get_api_key()
print(API_KEY, type(API_KEY))
# MCP-like minimal server for weather data
async def handle_weather(request):
    city = request.query.get("city")
    if not city:
        return web.json_response({"error": "Missing city parameter"}, status=400)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status != 200:
                return web.json_response({"error": data.get("message", "Unknown error")}, status=resp.status)
            return web.json_response({
                "city": data["name"],
                "weather": data["weather"][0]["description"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"]
            })

app = web.Application()
app.router.add_get("/weather", handle_weather)

if __name__ == "__main__":
    web.run_app(app, port=8080)

