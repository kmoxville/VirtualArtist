## 🎤 Virtual AI Artist  

## 📌 Project Description  
**Virtual Artist** is a system that uses artificial intelligence to interact with audiences and perform songs in real time. The project combines multiple microservices for text, voice, and animation processing.  

## ⚙️ Technologies  
- **Language:** Python (FastAPI)  
- **Database:** PostgreSQL  
- **Message Queue:** RabbitMQ  
- **Containerization:** Docker, Docker Compose  
- **AI Models:** ChatGPT (dialogue), Whisper (speech recognition), RVC (voice synthesis)  

## 🔧 Architecture  
The project is based on a microservices architecture:  
- **`core`** – manages configuration and infrastructure  
- **`chat_listener`** – collects messages from Twitch/YouTube  
- **`speech_parser`** – converts speech to text  
- **`chat_engine`** – processes messages and generates responses  
- **`avatar_renderer`** – handles voice synthesis and avatar animation  

<p align="center">
  <img src="docs/architecture-diagram.png" alt="Project Architecture" width="600">
</p>

## 🚀 Getting Started  
1. Clone the repository:  
   ```bash
   git clone https://github.com/kmoxville/VirtualArtist.git
   cd virtual-artist
   ```  
2. Create a `.env` file in the project's root directory:  
   ```bash
   APP_PORT=8000
   DATABASE_URL=postgresql://user:password@db:5432/virtual_artist
   POSTGRES_USER=test
   POSTGRES_PASSWORD=test
   POSTGRES_DB=virtual_artist
   RABBITMQ_USER=test
   RABBITMQ_PASSWORD=test
   PYTHONPATH=.
   OPENAI_API_KEY=KEY
   MAIN_LANG=ru
   ```  
3. Start the containers:  
   ```bash
   docker-compose up --build
   ```  
4. Open `http://localhost:8000/docs` to test the API.  
   Open the RabbitMQ dashboard at `http://localhost:15672`.  

## 🐜 License  
MIT License
