import re
import time
import requests
from bs4 import BeautifulSoup

# Target page we are trying to reach
TARGET_URL = "https://en.wikipedia.org/wiki/Philosophy"


def remove_parentheses(text):
    """Removes text inside parentheses to avoid hitting links inside them,

    while keeping HTML tags intact. A simple regex approach for this demo.
    """
    # This matches outermost parentheses and their contents
    # (Won't handle deeply nested pairs perfectly, but works for most Wiki pages)
    return re.sub(r"\([^()]*\)", "", text)


def find_philosophy(current_url, visited=None, depth=0, max_depth=50):
    if visited is None:
        visited = set()

    print(f"{'  ' * depth}➔ Visiting: {current_url}")

    # Base Case 1: Reached Philosophy!
    if current_url.lower() == TARGET_URL.lower():
        print(f"\n✨ Success! Reached Philosophy in {depth} steps.")
        return True

    # Base Case 2: Max depth reached (to prevent infinite recursion stack)
    if depth >= max_depth:
        print("\n❌ Stopped: Reached maximum recursion depth.")
        return False

    # Base Case 3: Loop detected
    if current_url in visited:
        print("\n🌀 Loop detected! We are stuck in an infinite cycle.")
        return False

    visited.add(current_url)

    # Fetch the page
    headers = {"User-Agent": "WikiPhilosophyBot/1.0 (Educational Script)"}
    try:
        response = requests.get(current_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"\n❌ Error fetching page: {e}")
        return False

    # Pre-process HTML to strip content inside parentheses from text nodes
    # (helps avoid pulling links that are just pronunciation guides or side notes)
    cleaned_html = remove_parentheses(response.text)
    soup = BeautifulSoup(cleaned_html, "html.parser")

    # Find the main content div where the article text resides
    content_div = soup.find(id="mw-content-text")
    if not content_div:
        print("\n❌ Could not find main content.")
        return False

    next_link = None

    # Look through paragraphs and bulleted lists in the main content area
    for paragraph in content_div.find_all(["p", "ul"], recursive=True):
        # Find all anchor tags in this paragraph
        for a in paragraph.find_all("a", href=True):
            # 1. Skip links inside italics/citations (often meta-text or side notes)
            if a.find_parent(["i", "em", "span", "table"]):
                continue

            href = a["href"]

            # 2. Must be a valid internal Wikipedia article link
            # Exclude main page, files, help pages, and external links
            if "/wiki/" in href and not any(
                x in href for x in [":", "Main_Page"]
            ):
                suffix = href.split("/wiki/")[-1]
                next_link = f"https://en.wikipedia.org/wiki/{suffix}"
                break

        if next_link:
            break

    # Base Case 4: Dead end (no valid links found)
    if not next_link:
        print("\n🛑 Dead end: Found a page with no valid outgoing wiki links.")
        return False

    # Be polite to Wikipedia's servers
    time.sleep(0.5)

    # Recursive Step
    return find_philosophy(next_link, visited, depth + 1, max_depth)


if __name__ == "__main__":
    # Feel free to change this starting URL to test different topics!
    starting_url = "https://en.wikipedia.org/wiki/Special:Random"

    print("Starting the journey to Philosophy...\n")
    find_philosophy(starting_url)
