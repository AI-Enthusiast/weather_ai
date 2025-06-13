import os
import aiohttp
from aiohttp import web
import asyncio
import PyPDF2
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.connectors.ai.ollama.ollama_prompt_execution_settings import OllamaChatPromptExecutionSettings
from semantic_kernel.prompt_template import PromptTemplateConfig


# Load OpenWeather API key from file
def get_api_key():
    with open("open_weather_key", "r") as f:
        return f.read().strip()

API_KEY = get_api_key()
print(API_KEY, type(API_KEY))

# Initialize Semantic Kernel with Ollama
async def setup_kernel():
    kernel = Kernel()
    
    # Add Ollama chat completion service
    chat_completion = OllamaChatCompletion(
        ai_model_id="llama3.2",
        host="http://localhost:11434"
    )
    kernel.add_service(chat_completion)
    
    return kernel

# Global kernel instance
kernel = None
# MCP-like minimal server for weather data with AI-powered responses
async def handle_weather(request):
    city = request.query.get("city")
    if not city:
        return web.json_response({"error": "Missing city parameter"}, status=400)
    
    # Fetch weather data
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status != 200:
                return web.json_response({"error": data.get("message", "Unknown error")}, status=resp.status)
            
            # Extract weather information
            weather_data = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "weather": data["weather"][0]["description"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data.get("wind", {}).get("speed", 0),
                "visibility": data.get("visibility", 0) / 1000 if data.get("visibility") else 0  # Convert to km
            }
            
            # Create prompt for AI response
            prompt = f"""
            You are a friendly and knowledgeable weather assistant. Based on the following weather data, provide a helpful and conversational weather report:

            Location: {weather_data['city']}, {weather_data['country']}
            Weather: {weather_data['weather']}
            Temperature: {weather_data['temperature']}°C (feels like {weather_data['feels_like']}°C)
            Humidity: {weather_data['humidity']}%
            Pressure: {weather_data['pressure']} hPa
            Wind Speed: {weather_data['wind_speed']} m/s
            Visibility: {weather_data['visibility']} km

            Please provide:
            1. A natural, conversational summary of the current weather
            2. What it feels like outside
            3. Any recommendations for activities or clothing
            4. Any notable weather patterns or conditions

            Keep the response friendly, informative, and helpful. Don't just list the data - make it conversational and useful for someone planning their day.
            """
            
            try:
                # Use Semantic Kernel to generate AI response
                global kernel
                if kernel is None:
                    kernel = await setup_kernel()
                
                # Set up execution settings
                execution_settings = OllamaChatPromptExecutionSettings(
                    ai_model_id="llama3.2",
                    max_tokens=500,
                    temperature=0.7
                )
                
                # Get AI response
                response = await kernel.invoke_prompt(
                    prompt,
                    settings=execution_settings
                )
                
                ai_response = str(response)
                
                return web.json_response({
                    "city": weather_data["city"],
                    "country": weather_data["country"],
                    "raw_data": weather_data,
                    "ai_response": ai_response,
                    "timestamp": data.get("dt", 0)
                })
                
            except Exception as e:
                print(f"Error generating AI response: {e}")
                # Fallback to basic response if AI fails
                return web.json_response({
                    "city": weather_data["city"],
                    "country": weather_data["country"],
                    "raw_data": weather_data,
                    "ai_response": f"Current weather in {weather_data['city']}: {weather_data['weather']} with a temperature of {weather_data['temperature']}°C. Humidity is {weather_data['humidity']}%.",
                    "timestamp": data.get("dt", 0),
                    "error": "AI response generation failed, showing basic summary"
                })

app = web.Application()
app.router.add_get("/weather", handle_weather)

# Add a chat endpoint for more conversational weather queries
async def handle_weather_chat(request):
    """Handle conversational weather queries"""
    try:
        data = await request.json()
        user_query = data.get("query", "")
        city = data.get("city", "")
        
        if not user_query:
            return web.json_response({"error": "Missing query parameter"}, status=400)
        
        # If city is provided, get weather data first
        weather_context = ""
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        weather_data = await resp.json()
                        weather_context = f"""
                        Current weather data for {weather_data['name']}, {weather_data['sys']['country']}:
                        - Weather: {weather_data['weather'][0]['description']}
                        - Temperature: {weather_data['main']['temp']}°C (feels like {weather_data['main']['feels_like']}°C)
                        - Humidity: {weather_data['main']['humidity']}%
                        - Pressure: {weather_data['main']['pressure']} hPa
                        - Wind Speed: {weather_data.get('wind', {}).get('speed', 0)} m/s
                        """
        
        # Create conversational prompt
        prompt = f"""
        You are a helpful weather assistant. The user asked: "{user_query}"
        
        {weather_context}
        
        Please provide a helpful, conversational response. If weather data is available, use it to answer their question. 
        If no specific weather data is provided, give general weather advice or ask for their location.
        Be friendly, informative, and natural in your response.
        """
        
        # Generate AI response
        global kernel
        if kernel is None:
            kernel = await setup_kernel()
        
        execution_settings = OllamaChatPromptExecutionSettings(
            ai_model_id="llama3.2",
            max_tokens=400,
            temperature=0.7
        )
        
        response = await kernel.invoke_prompt(
            prompt,
            settings=execution_settings
        )
        
        return web.json_response({
            "query": user_query,
            "response": str(response),
            "city": city if city else None
        })
        
    except Exception as e:
        print(f"Error in weather chat: {e}")
        return web.json_response({"error": f"Failed to process query: {str(e)}"}, status=500)

app.router.add_post("/weather/chat", handle_weather_chat)

if __name__ == "__main__":
    web.run_app(app, port=8080)

