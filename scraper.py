from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_serp_and_ai(keyword, brand_name):
    """
    Scrapes SERP and AI Overview presence using Playwright & BeautifulSoup.
    """
    search_url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        
        try:
            page.goto(search_url, timeout=15000)
            page.wait_for_timeout(2000) # Allow dynamic elements/AI Overviews to render
            html_content = page.content()
        except Exception as e:
            print(f"Scraping error: {e}")
            html_content = ""
        finally:
            browser.close()

    if not html_content:
        return {"rank": 99, "ai_present": False}

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check for AI-generated answers / AI Overviews mentioning the brand
    ai_overview_section = soup.find('div', string=lambda t: t and 'AI Overview' in t) or soup.select_one('.exp-container')
    ai_present = False
    if ai_overview_section and brand_name.lower() in ai_overview_section.text.lower():
        ai_present = True

    # Extract traditional organic search ranks
    rank = 99
    organic_results = soup.select('div.g')
    for index, result in enumerate(organic_results, start=1):
        link_tag = result.select_one('a')
        if link_tag and 'href' in link_tag.attrs:
            if brand_name.lower() in link_tag['href'].lower():
                rank = index
                break

    return {"rank": rank, "ai_present": ai_present}