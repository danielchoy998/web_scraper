# scrape_reddit.py
import os
import praw
from dotenv import load_dotenv
import requests
import cv2
import numpy as np
import csv

class Reddit_Scraper:
    def __init__(self, limit : int = 10):
        load_dotenv()
        self.limit = limit
        self.reddit = praw.Reddit(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            user_agent=os.getenv("USER_AGENT")
        )
    
    def scrape_by_id(self, id : str):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        submission = self.reddit.submission(id=id)

        # image
        url = submission.url
        if not url or not url.strip():
            print(f"[{id}] URL is empty")
            return 
        try : 
            response = requests.get(url, headers=headers, stream=True)
            if response.status_code == 200:
                resp = response.raw
                img_array = np.asarray(bytearray(resp.read()), dtype="uint8")
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                if img is not None:
                    self.save_image(id, img)
                else:
                    print("img is empty")
            else:
                print(f"Response Error : {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        
        # comments
        comments = submission.comments.list() # [(),(),...]
        scores = submission.score
        self.save_comments(id, comments, scores)
    
    def scrape_by_subreddit(self, subreddit_name : str):
        limit = self.limit
        subreddit = self.reddit.subreddit(subreddit_name)
        for submission in subreddit.new(limit = limit):
            self.scrape_by_id(submission.id)

    def save_image(self, id, img):
        save_dir = "./data/reddit/images"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{id}.jpg")
        cv2.imwrite(save_path, img)
        print(f"Image saved to {save_path}")
 
    def save_comments(self, id, comments, scores):
        save_dir = "./data/reddit/comments"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"photo_review.csv")

        file_exist = os.path.exists(save_path)
        fieldnames = ["image_id","comment_id","comment","score"]
        with open(save_path, "a", newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exist  or os.path.getsize(save_path) == 0:
                writer.writeheader()
            for comment in comments:
                writer.writerow({
                    "image_id": id,
                    "comment_id": comment.id,
                    "comment": comment.body.replace('\n', ' '),
                    "score": scores
                })

        print(f"Comments saved to {save_path}")
def main():
    scraper = Reddit_Scraper(limit = 5)
    print("Test with scraping started")

    # test with single id
    test_id = "rm1erx"
    scraper.scrape_by_id(test_id)
    #test with subreddit
    scraper.scrape_by_subreddit("photocritique")
    print("Test with scraping finished")

if __name__ == "__main__":
    main()

    