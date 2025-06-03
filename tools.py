from langchain_core.tools import tool
from reddit_scraper import Reddit_Scraper
from langchain_tavily import TavilySearch

scraper = Reddit_Scraper(5)

class Tools:
    def __init__(self,):
        self.tools = [Tools.multiply,
                      Tools.scrape_reddit,
                      Tools.web_search]
    
    @staticmethod
    @tool
    def scrape_reddit(subreddit_name: str) -> str:
        """
        This function is to scrape a subreddit and download the top 5 posts including comments and images
        """
        scraper.scrape_by_subreddit(subreddit_name)
        return "Success"

    @staticmethod
    @tool
    def web_search(query : str) -> str:
        """
        用 TavilySearch 執行網路搜尋，並回傳前兩筆結果的文字描述。

        Args : 
            query : str
                The query to search the web for

        Returns :
            str
                The text description of the top 2 results
        """
        search = TavilySearch(max_results=2)
        return search.invoke(query)

    @staticmethod
    @tool
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b
    
    @property
    def get_tools(self,) -> list[tool]:
        return self.tools

def main():
    tool_list = Tools()
    tool_list.scrape_reddit("photocritique")

if __name__ == "__main__":
    main()