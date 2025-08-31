
# CISNR (Centre of Intelligent System & Network Research) Chatbot

![CISNR Chatbot](https://raw.githubusercontent.com/Salman7292/CISNR-Centre-of-Intelligent-System-Network-Research-Chatbot/refs/heads/main/interface/Screenshot%202025-09-01%20025943.png)
![CISNR Chatbot](https://raw.githubusercontent.com/Salman7292/CISNR-Centre-of-Intelligent-System-Network-Research-Chatbot/refs/heads/main/interface/Screenshot%202025-09-01%20030351.png)
![CISNR Chatbot](https://raw.githubusercontent.com/Salman7292/CISNR-Centre-of-Intelligent-System-Network-Research-Chatbot/refs/heads/main/interface/Screenshot%202025-09-01%20025748.png)
![CISNR Chatbot](https://raw.githubusercontent.com/Salman7292/CISNR-Centre-of-Intelligent-System-Network-Research-Chatbot/refs/heads/main/interface/Screenshot%202025-09-01%20025709.png)


An AI-powered chatbot designed for the **Centre of Intelligent System & Network Research (CISNR)**.  
It leverages advanced **LangChain + Gemini AI + Pinecone** to provide intelligent responses, retrieve organizational knowledge, and assist users with queries about CISNR’s services and research activities.

---

## Features

- **CISNR Knowledge Base**: Retrieve accurate information from indexed CISNR documents
- **Gemini AI Integration**: Generate natural, human-like responses
- **Semantic Search with Pinecone**: Vector similarity search for precise answers
- **Flask Backend**: Efficient Python API service
- **Modern Web UI**: Simple and user-friendly interface

---

## Technology Stack

- **Backend**: Python 3.13.x, Flask  
- **AI Components**: LangChain, Google Gemini Pro, Pinecone Vector DB  
- **Environment Management**: Conda, dotenv  
- **Deployment**: Gunicorn (production ready)

---

## Installation

### Prerequisites
- Conda package manager  
- Python 3.13.x  
- Pinecone & Google Gemini API keys  

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/Salman7292/CISNR-Chatbot.git
cd CISNR-Chatbot
````

2. Create and activate the Conda environment:

```bash
conda create -n cisnr-chatbot python=3.13.5
conda activate cisnr-chatbot
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Add your API keys in a `.env` file:

```env
GOOGLE_API_KEY="your-google-api-key"
PINECONE_API_KEY="your-pinecone-api-key"
PINECONE_INDEX_NAME="ncai"
SECRET_KEY="your-secret-key"
```

5. Run the Flask application:

```bash
python app.py
```

6. Open your web browser and go to `http://localhost:5000`

---

## Project Structure

```
│   .env                    # Environment variables
│   app.py                  # Main Flask application
│   requirements.txt        # Python dependencies
│
├───static
│   ├───css                 # CSS stylesheets
│   ├───images              # Application images
│   └───js                  # JavaScript files
│
└───templates
        index.html          # Main chatbot interface
```

---

## Usage

1. Ask a question related to CISNR services or research.
2. The chatbot retrieves relevant documents from Pinecone.
3. Gemini AI generates a precise and contextual answer.
4. Sources are provided for verification.

---

## Configuration

Update the `.env` file with your actual **Google API Key**, **Pinecone API Key**, and other settings.

---

## Contributing

We welcome contributions to improve the CISNR Chatbot.
Please submit **pull requests** or open **issues** for bugs and feature suggestions.

---

## License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## Support

For support or inquiries about the CISNR Chatbot, please open an issue in this repository or contact the development team.

---

```

📌 And here’s your `requirements.txt` (as you shared):  

```

flask
langchain
langchain-google-genai
langchain-pinecone
pinecone-client
python-dotenv
gunicorn
python-dateutil

```

---

Do you also want me to add a **`.gitignore`** file (so `.env` and `__pycache__` won’t be pushed accidentally)?
```
