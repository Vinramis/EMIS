import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # 1. Create the bridge between JS and Python
        async def log_click_binding(source, details):
            # This runs in Python whenever a click happens in the browser
            print("--- CLICK DETECTED ---")
            print(f"Selector:    {details['selector']}")
            if details['placeholder']:
                print(f"Placeholder: {details['placeholder']}")
            if details['text']:
                print(f"Text:        {details['text']}")
            print(f"URL:         {source['page'].url}\n")

        await page.expose_binding("pythonLogClick", log_click_binding)

        # 2. Inject JS to listen for all clicks
        await page.add_init_script(r"""
            document.addEventListener('mousedown', (e) => {
                const el = e.target;
                
                // Build a basic CSS selector
                let selector = el.tagName.toLowerCase();
                if (el.id) selector += '#' + el.id;
                if (el.className && typeof el.className === 'string') {
                    selector += '.' + el.className.trim().split(/\s+/).join('.');
                }

                const details = {
                    selector: selector,
                    placeholder: el.getAttribute('placeholder') || null,
                    text: el.innerText ? el.innerText.substring(0, 30) : null
                };

                // Send the data to the Python function we exposed
                window.pythonLogClick(details);
            }, true);
        """)

        await page.goto("https://www.google.com")
        
        print("Listening for clicks... (Keep the window open and click things!)")
        # Keep the script running
        await asyncio.Event().wait()

asyncio.run(main())