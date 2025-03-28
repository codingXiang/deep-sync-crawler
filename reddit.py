import praw
from crawlab import save_item
import argparse

import env
from logger import logger

parser = argparse.ArgumentParser(description="Reddit Crawler")
# parser.add_argument('--client-id', type=str, help='Reddit API client-id')
# parser.add_argument('--client-secret', type=str, help='Reddit API client-secret')
# parser.add_argument('--user-agent', type=str, help='Reddit API user-agent')
parser.add_argument('--search', type=str, help='Reddit Search Query')
parser.add_argument('--sort', type=str,
                    help='Reddit Search Sort Type, e.g. relevance, new, top, hot, comments, updated, relevance, relevance2, confidence, topall, controversial, old, random, qa, live, blank',
                    default="relevance")
parser.add_argument('--limit', type=int, help='Reddit Search Result Limit, default is 10', default=10)

args = parser.parse_args()

# === 1. 你的 Reddit 憑證 (請自行替換成有效的 client_id, client_secret, user_agent) ===


# === 2. 初始化 PRAW 物件 ===
reddit = praw.Reddit(
    client_id=env.get("CLIENT_ID"),
    client_secret=env.get("CLIENT_SECRET"),
    user_agent=env.get("USER_AGENT"),
)

# === 3. 設定搜尋參數 ===
# search_query = "virtual+pet"  # 搜尋關鍵字
# sort_type = "relevance"  # 排序方式: relevance(相關性), new(最新), top(最高分), 等
# result_limit = 200  # 嘗試抓取的貼文數量 (實際可能更少)

# === 4. 呼叫 API 進行搜尋 (搜尋範圍: 全域, 即 r/all) ===
search_results = reddit.subreddit("all").search(
    args.search,
    sort=args.sort,
    limit=args.limit
)

fieldnames = ["post_id", "title", "score", "url", "comment_id", "comment_author", "comment_body"]

# === 6. 迭代搜尋結果，爬取每篇貼文 & 其評論 ===
for submission in search_results:
    # 6.1 展開「MoreComments」(避免留言被摺疊)
    submission.comments.replace_more(limit=0)

    # 6.2 取得所有留言 (這裡示範一次性抓全部; 量大時要注意效能)
    comments = submission.comments.list()
    if not comments:
        logger.info(f"No comment: {submission.title}")
        save_item({
            "post_id": submission.id,
            "title": submission.title,
            "score": submission.score,
            "url": submission.url,
            "comment_id": "",
            "comment_author": "",
            "comment_body": ""
        })
    else:
        logger.info(f"Found {len(comments)} comments: {submission.title}")
        # 若有留言，對每則留言各寫一行
        for comment in comments:
            save_item({
                "post_id": submission.id,
                "title": submission.title,
                "score": submission.score,
                "url": submission.url,
                "comment_id": comment.id,
                "comment_author": str(comment.author),
                "comment_body": comment.body
            })
