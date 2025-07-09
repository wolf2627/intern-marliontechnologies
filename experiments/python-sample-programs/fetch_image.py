import requests

"""
Fetches an image from the given URL and returns its binary content and metadata.
Args:
    url (str): The URL of the image to fetch.
Returns:
    dict: Contains 'status', 'content', 'content_type', and 'url' if successful, or 'error' if failed.
"""
url = "https://www.leavitt.com/dA/b23b96683d/featuredImage/blog-construction.jpg/1200w/webp/50q"
try:
    response = requests.get(url)
    response.raise_for_status()
    content_type = response.headers.get('Content-Type', '')
    if not content_type.startswith('image/'):
        print({"error": f"URL does not point to an image. Content-Type: {content_type}"})
    print(f"Fetched image from {url} with content type {content_type}")
    print({
        "status": "success",
        "content": response.content,
        "content_type": content_type,
        "url": url
    })
except Exception as e:
    print({"error": str(e)})