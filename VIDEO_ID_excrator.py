from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    parsed = urlparse(url.strip())
    hostname = (parsed.hostname or "").lower()

    if hostname in {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com"
    }:
        video_id = parse_qs(parsed.query).get("v", [None])[0]

    elif hostname == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]

    elif hostname in {
        "youtube-nocookie.com",
        "www.youtube-nocookie.com"
    }:
        parts = parsed.path.strip("/").split("/")
        video_id = parts[-1] if parts else None

    else:
        raise ValueError("Please provide a supported YouTube URL.")

    if not video_id or len(video_id) != 11:
        raise ValueError("Invalid or unsupported YouTube video URL.")

    return video_id


from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()


def get_transcript(video_id):#the function is used to retive the cpations for a given YT video.

    try:
        transcript_list = api.list(video_id)#fecthes the avaiable captions and all metadata for the given YT video.

        available_languages = [transcript.language_code for transcript in transcript_list]

        print("Available languages:", available_languages)

        transcript = api.fetch(video_id,languages=["en", "te", "hi"])#retrives the actual transcript available in that engilsh.

        transcript_text = " ".join(snippet.text for snippet in transcript)

        if not transcript_text.strip():
            raise ValueError("The transcript is empty.")

        return transcript_text

    except Exception as error:
        print("Transcript retrieval failed:")
        print(type(error).__name__, error)
        return None