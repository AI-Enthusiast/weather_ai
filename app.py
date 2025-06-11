import chainlit as cl
import aiohttp


@cl.on_message
async def main(message: cl.Message):
    city = message.content.strip()
    if not city:
        await cl.Message(content="Please provide a city name.").send()
        return
    url = f"http://localhost:8080/weather?city={city}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status != 200:
                await cl.Message(content=f"Error: {data.get('error', 'Unknown error')}").send()
                return
            weather = data["weather"]
            temp = data["temperature"]
            humidity = data["humidity"]
            await cl.Message(
                content=f"Weather in {city}: {weather}, {temp}°C, Humidity: {humidity}%"
            ).send()

