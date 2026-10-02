from playwright.sync_api import sync_playwright, Browser, Page
from playwright.sync_api import PlaywrightContextManager

class WebMultitool(PlaywrightContextManager):
    browser: Browser
    pages: list[Page]
    current_page: Page
    headless: bool
    kwargs: dict

    def __init__(self, browser: Browser = None, headless: bool = True, **kwargs):
        super().__init__()
        self.kwargs = kwargs
        self.headless = headless
        if browser is None:
            self.browser = sync_playwright().start().chromium.launch(headless=self.headless, **kwargs)
        else:
            self.browser = browser
        self.pages = []
        self.new_page()

    def new_page(self):
        self.current_page = self.browser.new_page(**self.kwargs)
        self.pages.append(self.current_page)
        return self.current_page

    def goto(self, url: str):
        self.current_page.goto(url)

    def wait_for_timeout(self, timeout: int):
        self.current_page.wait_for_timeout(timeout)

# --- Testing ---
if __name__ == "__main__":
    tool = WebMultitool(headless=False)
    tool.new_page()
    tool.goto("https://google.com")
    tool.wait_for_timeout(5000)