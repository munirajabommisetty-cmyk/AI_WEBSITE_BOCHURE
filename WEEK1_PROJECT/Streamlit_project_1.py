import os
from urllib.parse import urlparse

import streamlit as st
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

import requests
from bs4 import BeautifulSoup


load_dotenv()

st.set_page_config(
    page_title="AI Company Brochure Generator",
    page_icon="📄",
    layout="wide"
)


brochure_system_prompt = """
You are a professional company research and marketing assistant.

Create a professional company brochure using the supplied website
information.

Include the following sections whenever information is available:

1. Company Overview
2. Products and Services
3. Mission and Vision
4. Key Features and Strengths
5. Target Audience
6. Conclusion

Requirements:
- Use Markdown formatting.
- Use clear headings and bullet points.
- Keep the brochure informative and professional.
- Do not invent facts, statistics, products, or certifications.
- Use only the information available in the supplied website content.
- If information is unavailable, omit that section.
"""

def fetch_website_contents(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove unnecessary HTML elements
    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header"
    ]):
        element.decompose()

    # Extract readable text
    website_text = soup.get_text(
        separator=" ",
        strip=True
    )

    return website_text[:12000]

def get_brochure_user_prompt(company, url):

    website_contents = fetch_website_contents(url)

    user_prompt = f"""
Create a company brochure for {company}.

Website URL:
{url}

Website information:
{website_contents}

Generate a professional Markdown brochure using the
website information provided above.
"""

    return user_prompt

def create_brochure_llama(company, url):

    prompt = ChatPromptTemplate.from_messages([
        ("system", brochure_system_prompt),
        ("user", get_brochure_user_prompt(company, url))
    ])

    model = ChatOllama(
        model="llama3.2:3b",
        temperature=0.3
    )

    chain = prompt | model | StrOutputParser()

    result = chain.invoke({})

    return result


def create_brochure_gemini(company, url):

    if not os.getenv("gemini_api_key"):
        raise ValueError(
            "GOOGLE_API_KEY is missing from your .env file."
        )

    prompt = ChatPromptTemplate.from_messages([
        ("system", brochure_system_prompt),
        ("user", get_brochure_user_prompt(company, url))
    ])

    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.3
    )

    chain = prompt | model | StrOutputParser()

    result = chain.invoke({})

    return result


# =========================================================
# 7. MODEL SELECTION AND VALIDATION
# =========================================================

def generate_brochure(company, url, model_name):

    company = (company or "").strip()
    url = (url or "").strip()

    if not company:
        raise ValueError(
            "Please enter a company name."
        )

    if not url:
        raise ValueError(
            "Please enter a website URL."
        )

    # Add https:// if the user omitted the scheme
    if not urlparse(url).scheme:
        url = "https://" + url

    parsed_url = urlparse(url)

    if (
        parsed_url.scheme not in ("http", "https")
        or not parsed_url.netloc
    ):
        raise ValueError(
            "Enter a valid URL, such as https://example.com"
        )

    if model_name == "Llama 3.2":

        return create_brochure_llama(
            company,
            url
        )

    elif model_name == "Gemini":

        return create_brochure_gemini(
            company,
            url
        )

    else:

        raise ValueError(
            "Please select a valid model."
        )


# =========================================================
# 8. STREAMLIT USER INTERFACE
# =========================================================

st.title("AI Company Brochure Generator")

st.markdown(
    """
    Generate professional company brochures using website content
    and your choice of language model.

    **Available models:** Llama 3.2 and Gemini
    """
)

st.divider()


# Company information section
st.subheader("Company Information")

company_name = st.text_input(
    "Company Name",
    placeholder="Example: GitHub"
)

website_url = st.text_input(
    "Company Website URL",
    placeholder="https://github.com"
)


# Model selection
st.subheader("Model Configuration")

model_name = st.selectbox(
    "Choose your LLM",
    options=[
        "Llama 3.2",
        "Gemini"
    ],
    index=0
)


# Generate button
generate_button = st.button(
    "Generate Brochure",
    type="primary",
    use_container_width=True
)


# =========================================================
# 9. DISPLAY THE GENERATED BROCHURE
# =========================================================

if generate_button:

    try:

        with st.spinner(
            f"Generating brochure using {model_name}..."
        ):

            brochure = generate_brochure(
                company_name,
                website_url,
                model_name
            )

        st.success(
            "Brochure generated successfully!"
        )

        st.divider()

        st.subheader("Generated Company Brochure")

        # Render the Markdown brochure
        st.markdown(brochure)

        # Download generated brochure
        safe_company_name = "".join(
            character if character.isalnum() else "_"
            for character in company_name.strip()
        ).strip("_")

        if not safe_company_name:
            safe_company_name = "company"

        st.download_button(
            label="Download Brochure (.md)",
            data=brochure,
            file_name=f"{safe_company_name}_brochure.md",
            mime="text/markdown",
            use_container_width=True
        )

    except Exception as error:

        st.error(
            f"Brochure generation failed: {error}"
        )

        st.info(
            "Check your website URL, model configuration, "
            "API key, and Ollama status."
        )


# =========================================================
# 10. FOOTER
# =========================================================

st.divider()

st.caption(
    "Built with Python, Streamlit, LangChain, Ollama, and Gemini."
)