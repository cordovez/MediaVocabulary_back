from selectolax.parser import HTMLParser

def parse_top_opinions(html_page):
    results = []
    html = HTMLParser(html_page)
    data = html.css("ol.dcr-hqoq27")

    for item in data:
        opinion = {
            "title": item.css_first("h4.span").text(),
            "url": item.css_first("a").attributes['href']
        }
        results.append(opinion)

    return results



