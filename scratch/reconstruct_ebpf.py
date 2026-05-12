import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def reconstruct_ebpf():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found.")
        return

    client = genai.Client(api_key=api_key)

    ko_path = "src/data/blog/ko/posts/260511_ebpf-linux-kernel-semantic-gap.md"
    en_path = "src/data/blog/en/posts/260511_ebpf-linux-kernel-semantic-gap.md"

    if not os.path.exists(ko_path) or not os.path.exists(en_path):
        print("Error: Files not found.")
        return

    with open(ko_path, "r", encoding="utf-8") as f:
        ko_content = f.read()

    with open(en_path, "r", encoding="utf-8") as f:
        en_content = f.read()

    prompt = f"""
You are an expert technical editor. The Korean version of our blog post has lost all its newlines in the body (collapsed into a single line on line 51), making it unreadable.
However, we have a perfectly formatted English version of the same post which has the exact same paragraph structure, tables, blockquotes, and headings.

Your task is to reconstruct the Korean post by restoring all the missing newlines (paragraphs, headings, tables, blockquotes, lists) so that its structure exactly matches the English post, while preserving the exact Korean wording, phrasing, HTML tooltip links, image paths, and frontmatter from the Korean post.

[PERFECTLY FORMATTED ENGLISH VERSION]
{en_content}

[UNFORMATTED KOREAN VERSION]
{ko_content}

[INSTRUCTIONS]
1. Output the fully reconstructed Korean Markdown post.
2. Ensure every paragraph, heading, list item, image, blockquote, and table row is properly separated by newlines, mirroring the English version's structure.
3. Keep the exact Korean phrasing and terms from the unformatted Korean version. Do not re-translate or paraphrase.
4. Keep the Korean frontmatter (title, slug, date, author, faqs, etc.) exactly as is.
5. Do not output any markdown code blocks (fenced backticks) or explanation. Output ONLY the raw markdown content.
"""

    print("Requesting reconstruction from Gemini...")
    response = client.models.generate_content(
        model='gemini-2.5-flash', # Using a high-quality flash model for this task
        contents=prompt
    )

    reconstructed = response.text.strip()
    
    # Clean potential markdown code fence wrapping
    if reconstructed.startswith("```"):
        lines = reconstructed.split("\n")
        if lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        reconstructed = "\n".join(lines).strip()

    # Save reconstructed content
    with open(ko_path, "w", encoding="utf-8") as f:
        f.write(reconstructed)

    print("Success! Saved reconstructed Korean post.")

reconstruct_ebpf()
