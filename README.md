# Weather AI

A conversational weather application that combines real-time weather data with AI-generated, natural language weather reports.

## Features

- Real-time weather data for any city using the OpenWeather API
- AI-powered, conversational weather summaries using Semantic Kernel and Ollama (llama3.2)
- Recommendations for activities and clothing
- Simple chat interface powered by Chainlit

## Requirements

- Python 3.x
- OpenWeather API key
- Ollama running locally with the llama3.2 model
- Python packages:
  - aiohttp
  - chainlit
  - semantic_kernel
  - PyPDF2 (imported, not required for core functionality)

## Setup

1. **Clone the repository:**
   ```powershell
   git clone <your-repo-url>
   cd weather_ai
   ```

2. **Install dependencies:**
   ```powershell
   pip install aiohttp chainlit semantic-kernel PyPDF2
   ```

3. **Add your OpenWeather API key:**
   - Create a file named `open_weather_key` in the project root.
   - Paste your OpenWeather API key into this file (no extra spaces or newlines).

4. **Install and run Ollama with the llama3.2 model:**
   - Download and install Ollama from [https://ollama.com/](https://ollama.com/)
   - In a terminal, run:
     ```powershell
     ollama run llama3.2
     ```
   - Ensure Ollama is running on `http://localhost:11434`.

## Usage

1. **Start the backend server:**
   ```powershell
   python mcp_server.py
   ```
   The server will run on port 8080.

2. **Start the Chainlit chat interface:**
   ```powershell
   chainlit run app.py
   ```
   This will open a browser window with the chat interface.

3. **Chat:**
   - Enter a city name to get a conversational weather report. e.g. "Salem, US" for Salem Oregon (the best Salem)

## API Endpoints

- `GET /weather?city={city_name}`
  - Returns weather data and an AI-generated report for the specified city.
- `POST /weather/chat`
  - Accepts JSON with `query` and optional `city` fields for more conversational queries.

## Project Structure

- `mcp_server.py` — Backend server for weather data and AI responses
- `app.py` — Chainlit chat frontend
- `open_weather_key` — Your OpenWeather API key (not included in repo)

## License

MIT License

Copyright (c) 2025 CDacker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgements

- [OpenWeather](https://openweathermap.org/)
- [Ollama](https://ollama.com/)
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel)
- [Chainlit](https://www.chainlit.io/)
