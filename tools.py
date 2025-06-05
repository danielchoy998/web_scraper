from langchain_core.tools import tool
from reddit_scraper import Reddit_Scraper
from langchain_tavily import TavilySearch
from models.gemini import generate_image
from rag import add_pdf_files, retrieve
scraper = Reddit_Scraper(5)

class Tools:
    def __init__(self,):
        self.tools = [Tools.retrieve,
                      Tools.multiply,
                      Tools.scrape_reddit,
                      Tools.web_search,
                      Tools.generate_image,
                      Tools.add_pdf_files,
                      ]
    
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
    
    @staticmethod
    @tool
    def generate_image(prompt: str) -> str:
        """Generate an image based on a prompt."""
        generate_image(prompt)
        return "Success"
    
    @staticmethod
    @tool
    def add_pdf_files(file_path: str) -> str:
        """Add a PDF file to the vector store."""
        add_pdf_files(file_path)
        return "Success"

    @staticmethod
    @tool
    def retrieve(query: str) -> str:
        """
        Retrieval-First Tool:
        Use this tool to query our existing PDF/vector database (RAG) about machine learning.
        Only if you cannot find a satisfactory answer here, the agent should fallback to web_search.
        Args:
            query: The information to retrieve from vector store.
        Returns:
            Answer string from RAG or an empty string if not found.
        """
        return retrieve(query)
    
    @property
    def get_tools(self,) -> list[tool]:
        return self.tools

def main():
    tool_list = Tools()
    # tool_list.generate_image("A cat holding a sign that says hello world")
    print(tool_list.retrieve("What is Vision-Language Modeling?"))

if __name__ == "__main__":
    main()