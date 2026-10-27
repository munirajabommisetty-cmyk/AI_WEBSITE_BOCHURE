# AI Company Brochure Generator

An AI-powered web application that generates professional company brochures using a company's name and website URL.

The application extracts readable text from a company's website and uses a Large Language Model (LLM) to generate structured brochure content. Users can choose between a locally running **Llama 3.2 model through Ollama** and **Gemini 3.5 Flash**.

## Features

* **AI-powered brochure generation** from company website content.
* **Interactive web interface** built with Streamlit.
* **Website content extraction** using Requests and BeautifulSoup.
* **Multiple LLM options:** Llama 3.2 and Gemini.
* **Local model support** through Ollama.
* **Markdown output** for easy reading and sharing.
* **Downloadable brochures** in Markdown format.
* **Environment-variable configuration** for API key management.
* **Error handling** for common website and model issues.

## How It Works

1. Enter the company name.
2. Provide the company's website URL.
3. Select your preferred language model.
4. Click **Generate Brochure**.
5. The application retrieves and extracts readable website content.
6. The selected LLM processes the extracted information.
7. The generated brochure appears in the Streamlit interface.
8. Review and download the brochure.

## Technology Stack

| Technology       | Purpose                               |
| ---------------- | ------------------------------------- |
| Python           | Core application development          |
| Streamlit        | Web application interface             |
| LangChain        | Prompt management and LLM integration |
| Ollama           | Local LLM execution                   |
| Llama 3.2        | Locally running language model        |
| Gemini 3.5 Flash | Cloud-based language model            |
| Requests         | Website HTTP requests                 |
| BeautifulSoup    | HTML parsing and text extraction      |
| python-dotenv    | Environment variable management       |

## Project Structure.

```text
company-brochure-generator/
│
├── streamlit_brochure_app.py
├── .env
├── .gitignore
└── README.md
```

Adjust this structure if your actual project contains additional files.

## Installation and Setup

### 1. Clone the Repository

Replace the placeholders with your GitHub username and repository name.

```bash
git clone https://github.com/munirajabommisetty-cmyk/AI_WEBSITE_BOCHURE.git

```

### 2. Create a Virtual Environment

For Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install streamlit langchain-core langchain-ollama langchain-google-genai python-dotenv requests beautifulsoup4
```

## Configure Gemini

Create a `.env` file in the project root:

Replace the placeholder with your actual API key.

**Security:** Never commit your real API key to GitHub.

## Configure Ollama

Install Ollama and download the Llama 3.2 model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running before selecting the local model in the application.

## Run the Application

From the project directory, execute:

```bash
python -m Streamlit_project_1.py
```

Open the local URL displayed in the terminal. It is commonly:

```text
http://localhost:8501
```

Run the application through Streamlit's command rather than executing the Python file directly.

## Example Usage

**Input:**

* Company Name: Example Technologies
* Website URL: `https://example.com`
* Selected Model: Llama 3.2 or Gemini

**Expected Output:**

A structured company brochure containing sections such as:

* Company Overview
* Products and Services
* Mission and Vision
* Key Strengths
* Target Audience
* Conclusion

The generated sections depend on the information available on the website and the instructions provided to the language model.

## Limitations

* Some websites block automated requests.
* JavaScript-heavy websites may not provide complete content through basic HTML extraction.
* Generated content may contain inaccurate information and should be reviewed before publication.
* Local inference speed depends on available hardware.
* Gemini requires an internet connection and a valid API key.
* The quality of the brochure depends on the quality and completeness of the extracted website content.

## Future Enhancements

* Export brochures as PDF and DOCX.
* Support additional open-source and hosted language models.
* Improve extraction from JavaScript-heavy websites.
* Add configurable writing styles and brochure templates.
* Add website-link analysis to identify relevant company pages.
* Implement automated tests for scraping and generation.
* Add an editing and preview interface.
* Improve factual verification of generated content.

## Security

* Keep API keys in environment variables.
* Exclude `.env` and `.venv` from version control.
* Review generated content before publishing it.
* Fetch only publicly accessible websites you are permitted to access.

