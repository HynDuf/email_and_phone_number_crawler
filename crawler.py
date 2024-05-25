import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Regular expressions for emails and phone numbers
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_REGEX = re.compile(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$')

# Function to extract emails
def extract_emails(text):
    return EMAIL_REGEX.findall(text)

# Function to extract phone numbers
def extract_phone(text):
    return PHONE_REGEX.findall(text)

# Function to fetch and parse web pages
def get_page_content(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

# Function to find and normalize links
def get_links(base_url, soup):
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        parsed_url = urlparse(full_url)
        if parsed_url.scheme in ('http', 'https'):
            links.add(full_url)
    return links

# Main crawling function
def crawl(url, max_depth, visited, lock, depth=0):
    if depth > max_depth or url in visited:
        return None, [], []
    print(f"Investigating {url}...")

    with lock:
        visited.add(url)
    content = get_page_content(url)
    if content is None:
        return None, [], []

    soup = BeautifulSoup(content, 'html.parser')
    emails = extract_emails(content)
    phones = extract_phone(content)

    new_tasks = []
    if depth < max_depth:
        links = get_links(url, soup)
        with lock:
            for link in links:
                if link not in visited:
                    new_tasks.append((link, depth + 1))
    return new_tasks, emails, phones

def parallel_crawl(start_url, max_depth, queue):
    visited = set()
    final_emails = {}
    final_phones = {}
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=64) as executor:
        # Dictionary to keep track of future tasks and their associated URLs and depths
        future_to_url = {
            executor.submit(crawl, start_url, max_depth, visited, lock, 0): (start_url, 0)
        }

        while future_to_url:
            for future in as_completed(future_to_url):
                url, depth = future_to_url.pop(future)
                try:
                    queue.put(("URL_DONE", 0))
                    new_tasks, emails, phones = future.result()
                    with lock:
                        for email in emails:
                            if email not in final_emails:
                                final_emails[email] = url
                                queue.put(("EMAIL", email, url))
                        for phone in phones:
                            if phone not in final_phones:
                                final_phones[phone] = url
                                queue.put(("PHONE", phone, url))
                    if new_tasks:
                        for new_url, new_depth in new_tasks:
                            if new_url not in visited:
                                queue.put(("URL", new_url))
                                future_to_url[executor.submit(crawl, new_url, max_depth, visited, lock, new_depth)] = (new_url, new_depth)
                except Exception as e:
                    print(f"Error crawling {url}: {e}")

    return final_emails, final_phones
