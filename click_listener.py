import asyncio
from playwright.async_api import async_playwright, Page, Browser
import pathlib


async def main():
    async with async_playwright() as p:
        directory = pathlib.Path(__file__).parent
        cookies_path = directory / "emis automator\components\cookies.json"

        browser: Browser = await p.chromium.launch(headless=False)

        # browser = await browser.new_context(storage_state=cookies_path)

        page: Page = await browser.new_page()

        # 1. Create the bridge between JS and Python
        async def log_click_binding(source: dict, details: dict):
            # This runs in Python whenever a click happens in the browser
            print("\n-----   CLICK DETECTED   -----")
            for key, value in details.items():
                if value:
                    print(f"{key}: {value}")
            # print(f"\nURL: {source['page'].url}\n")

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

                // try to extract every attribute of the element
                let attributes = [];
                for (let i = 0; i < el.attributes.length; i++) {
                    attributes.push(el.attributes[i].name + '="' + el.attributes[i].value + '"');
                }

                const details = {
                    selector: selector,
                    placeholder: el.getAttribute('placeholder') || null,
                    text: el.innerText || null,
                    other_attributes: attributes,
                };

                // Send the data to the Python function we exposed
                window.pythonLogClick(details);
            }, true);
        """)

        await page.goto(
            "https://litsey.edu.uz/teacher/groups/preview/3315/subject/34?name=Algebra+%28Chuqurlashtirilgan+fanlar%29&group_number=1&tab=study-guide"
        )

        # await page.goto("https://litsey.edu.uz/login")

        print("\n\n\nListening for clicks... (Keep the window open and click things!)")
        # Keep the script running
        while not page.is_closed():
            await asyncio.sleep(1)
        print("\nScript finished\n")


asyncio.run(main())
