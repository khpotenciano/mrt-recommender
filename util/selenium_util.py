class SeleniumUtil:

    @classmethod
    def get_links(cls, selenium_elements):
        links = []
        for element in selenium_elements:
            links.append(element.get_attribute('href'))
        return links
