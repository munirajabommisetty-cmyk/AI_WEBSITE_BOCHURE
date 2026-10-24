# YouTube Video Summarizer

An AI-powered application that converts YouTube videos into concise summaries and useful learning materials using transcript extraction, speech-to-text, and locally running large language models.

The goal is to make long educational videos easier to understand by transforming video content into structured, readable information.

## Overview

Watching long videos to find important information can be time-consuming. This project aims to automate that process by accepting a YouTube URL, extracting its transcript, and using a local LLM to generate a meaningful summary.

When accessible captions are unavailable, the planned fallback is to transcribe authorized audio using a speech-to-text model.

## Key Features

* **YouTube URL Processing:** Extract the video ID from a YouTube URL.
* **Transcript Extraction:** Retrieve available captions using `youtube-transcript-api`.
* **Missing Transcript Handling:** Detect unavailable captions and prepare an alternative transcription workflow.
* **Speech-to-Text:** Use Faster Whisper to convert audio into text when the fallback workflow is implemented.
* **AI-Powered Summarization:** Use Ollama with a locally running LLM to summarize transcript content.
* **Learning-Oriented Output:** Extend summaries into key takeaways, important concepts, and other study materials.
* **Local LLM Support:** Run language models locally without requiring a paid LLM API.

> Note: Features described as planned or under development should be marked complete only after implementation and testing.

## Architecture

```text
                  YouTube URL
                       |
                       v
                Extract Video ID
                       |
                       v
              Retrieve Captions
                       |
             +---------+---------+
             |                   |
             v                   v
      Captions Available    Captions Missing
             |                   |
             v                   v
       Transcript Text      Audio Extraction
                                 |
                                 v
                         Faster Whisper
                                 |
                                 v
                           Transcript
             |                   |
             +---------+---------+
                       |
                       v
                 Local LLM
                   Ollama
                       |
                       v
               Video Summary
                       |
                       v
            Key Points and Insights
```

## Tech Stack

| Technology               | Purpose                             |
| ------------------------ | ----------------------------------- |
| Python                   | Core application development        |
| `youtube-transcript-api` | Retrieve available YouTube captions |       |
| Ollama                   | Run local language models           |
| Llama 3.2 3B             | Local LLM for transcript analysis   |
| Requests                 | HTTP requests where needed          |
| Jupyter Notebook         | Development and experimentation     |

Some components may be introduced as development progresses.

## How It Works

### Step 1: Provide a YouTube URL

The user supplies a video URL.

### Step 2: Extract the Video ID

The application identifies the video using the URL.

### Step 3: Retrieve the Transcript

The application attempts to retrieve captions that are accessible through `youtube-transcript-api`.

Caption availability depends on the video, language, and access restrictions.

### Step 4: Handle Missing Captions

If captions cannot be retrieved, the intended fallback is to extract audio through an appropriate, authorized method and transcribe it using Faster Whisper.

This fallback requires a separate audio-extraction implementation.

### Step 5: Generate the Summary

The transcript is passed to a local LLM through Ollama.

The model can be instructed to produce:

* A concise summary.
* Important points.
* Key concepts.
* A structured explanation of the video.

### Step 6: Present the Results

The generated summary can be displayed in a notebook or extended into a web interface.

## Example Output

For an educational video, the intended output could look like this:

```text
VIDEO SUMMARY
A concise explanation of the video's main topic.

KEY TAKEAWAYS
1. Important concept explained in the video.
2. Main argument or lesson.
3. Practical application.

IMPORTANT CONCEPTS
- Concept A
- Concept B
- Concept C

CONCLUSION
A short recap of the most important information.
```

The actual output depends on the video's transcript and the prompt used for summarization.

## Current Development Status

| Component                    | Status                   |
| ---------------------------- | ------------------------ |
| YouTube video ID extraction  | Tested                   |
| Caption retrieval            | Experimented with        |
| Caption language handling    | Under development        |
| Missing-caption handling     | Under development        |
| Audio extraction fallback    | Planned                  |
| Faster Whisper integration   | Planned / to be verified |
| Ollama summarization         | Planned / to be verified |
| Complete end-to-end pipeline | In development           |
| Web interface                | Future enhancement       |

Update this table as individual features are implemented and tested.

## Challenges and Considerations

### 1. Missing Transcripts

Some videos do not expose captions that the transcript library can retrieve. A fallback transcription workflow may be necessary.

### 2. Multiple Languages

Videos can have captions in multiple languages, and automatic captions may not always be available. The application should handle language selection and transcription results carefully.

### 3. Processing Time

Transcribing long videos locally can take time, depending on the selected Whisper model, available hardware, and audio duration.

### 4. LLM Context Limits

Long transcripts may exceed the model's context window. A chunking-and-summarization approach can help process longer videos.

### 5. Summary Accuracy

The generated summary should be grounded in the transcript. Important details can be missed, so the output should not be treated as a guaranteed complete representation of the video.

## Future Enhancements

* Build a Streamlit web interface.
* Add support for multiple caption languages.
* Implement audio extraction and automatic speech-to-text fallback.
* Summarize long videos using chunking and hierarchical summarization.
* Generate chapter-wise summaries and timestamps.
* Extract keywords, important questions, and revision notes.
* Recommend related educational videos.
* Export summaries to Markdown or PDF.
* Add transcript caching to avoid repeated processing.

## Responsible Usage

* Respect YouTube's terms, copyright restrictions, and content-owner permissions.
* Process and download audio only when authorized.
* Do not bypass access controls or technical restrictions.
* Check the licenses of the language models and dependencies you use.

## Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request with a clear description.

