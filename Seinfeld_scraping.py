from playwright.sync_api import sync_playwright
import pandas as pd

start_url = "https://tvquot.es/seinfeld/"

def run (playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(start_url)
    print(page.title())

    quotes_list = []


    for quote in page.locator('li').all():
        for link in quote.locator('a').all():
            url = link.get_attribute('href')
            print(url)



            if url is not None and "seinfeld" in url:
                new_page = browser.new_page()
                new_page.goto(f"https://tvquot.es{url}")
                scripts = new_page.locator('p').all()

                for script in scripts: 
                    data = script.text_content()                                        
                    quotes_list.append(data.strip())
                
            new_page.close()        
                    
               
    browser.close()

    return quotes_list

with sync_playwright() as playwright:
    quotes_list = run(playwright)
    
    
quotes_df = pd.DataFrame(quotes_list, columns=["Quote"])

quotes_df.to_csv("seinfeld_quotes.csv", index=False)

