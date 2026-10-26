from VIDEO_ID_excrator import extract_video_id,get_transcript
import gradio as gr
import os

from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
system_prompt="""
You are a YouTube Learning Assistant. Convert the supplied transcript into a clear, practical learning guide.

Adapt the explanation to the video's topic and the user's likely knowledge level.

Use these sections:

1. **Video Summary:** Explain the main ideas, arguments, and conclusions in a logical order. Preserve important details without unnecessary repetition.

2. **Key Concepts:** Explain the most important concepts, why they matter, and how they work. Define unfamiliar terms simply.

3. **Real-World Examples:** Give specific, relevant examples showing how the ideas can be applied. Use code examples only for technical topics. Label hypothetical examples clearly.

4. **Actionable Recommendations:** Suggest up to three practical next steps based on the video's content. Explain how to start and what outcome to aim for.

5. **Knowledge Quiz:** Create five questions mixing conceptual understanding and practical application. Include four options for multiple-choice questions, followed by correct answers and brief explanations.

6. **Key Takeaways:** Finish with the five most important lessons and one practical task.

Rules:

* Prioritize accuracy, clarity, and practical usefulness over length.
* Base claims about the speaker's content on the transcript.
* Never invent facts, statistics, examples, resources, or timestamps.
* Clearly distinguish the speaker's claims from your own explanations and recommendations.
* If information is missing or unclear, state the limitation.
* Omit sections that cannot be meaningfully supported by the transcript.
* Avoid repetition, generic advice, and unnecessary introductions.
* Keep the response proportional to the transcript's content and complexity.


"""

def analyze_video(video_url):
    if not video_url or not video_url.strip():
        raise gr.Error("Please enter a YouTube URL.")

    try:
        # Reuse your existing functions here.
        video_id = extract_video_id(video_url.strip())

        transcript = get_transcript(video_id)

        if not transcript:
            raise gr.Error("No transcript was found.")

        llm=ChatOllama(model="llama3.2:3b",temperature=0.3)
        gemini=ChatGoogleGenerativeAI(model="gemini-3.5-flash",api_key=os.getenv("gemini_api_key"))

        prompt=ChatPromptTemplate.from_messages([
            ("system",system_prompt),
            ("user","{transcript}")
        ])
        transcript_text = get_transcript(video_id)
        chain=prompt | gemini | StrOutputParser()
        res=chain.invoke({"transcript":transcript_text})
        print(res)

        # If your transcript generator returns a list or dictionary,
        # adapt this line to obtain the actual transcript text.
        if isinstance(transcript, list):
            transcript = " ".join(
                item["text"] for item in transcript
            )

        learning_guide = chain.invoke({
            "transcript": transcript
        })

        return learning_guide, transcript

    except gr.Error:
        raise

    except Exception as exc:
        raise gr.Error(
            f"Unable to process the video: {exc}"
        ) from exc


with gr.Blocks(
    theme=gr.themes.Soft(),
    title="YouTube Learning Assistant"
) as demo:

    gr.Markdown(
        """
        # YouTube Learning Assistant

        Transform YouTube videos into structured learning guides.

        Paste a video URL to explore the summary, key concepts,
        practical examples, and knowledge quiz.
        """
    )

    with gr.Row():
        url_input = gr.Textbox(
            label="YouTube Video URL",
            placeholder="Paste your YouTube URL here",
            scale=4
        )

        analyze_button = gr.Button(
            "Analyze Video",
            variant="primary"
        )

    with gr.Tabs():
        with gr.Tab("Learning Guide"):
            summary_output = gr.Markdown()

        with gr.Tab("Transcript"):
            transcript_output = gr.Textbox(
                label="Extracted Transcript",
                lines=15,
                interactive=False
            )

    analyze_button.click(
        fn=analyze_video,
        inputs=url_input,
        outputs=[summary_output, transcript_output]
    )

    url_input.submit(
        fn=analyze_video,
        inputs=url_input,
        outputs=[summary_output, transcript_output]
    )