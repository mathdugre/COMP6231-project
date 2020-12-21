from collections import defaultdict
import os
import random
import time

import redis

r = redis.Redis(host="redis", port=6379, db=0)

pdfs = os.listdir(f"/dataset/papers")
abstracts = os.listdir(f"/dataset/abstracts")

papers = defaultdict(dict)

post_id = 1
for pdf in pdfs:
    slug = pdf[:-4]
    papers[slug]["title"] = slug.replace("_CVPR_2019_paper", "").replace("_", " ")
    papers[slug]["pdf"] = pdf
    papers[slug]["post_id"] = post_id
    post_id += 1

for abstract in abstracts:
    slug = abstract[:-4]
    if slug in papers:
        papers[slug]["abstract"] = abstract

with open("usernames.txt") as fin:
    usernames = set(fin.read().strip().split("\n"))
    users = {
        i: {"username": username, "papers": []}
        for i, username in enumerate(usernames, 1)
    }

counter = 0
for k, v in papers.items():
    users[counter + 1]["papers"].append(v)
    counter = (counter + 1) % len(users)


r.flushdb()
r.set("currPost", len(papers) + 1)
max_followers = int(len(usernames) * 0.4)

for k, v in users.items():
    r.sadd("users", v["username"])

for user_id, user in users.items():
    username = user["username"]

    followers = random.sample(
        list(usernames - {username}), random.randint(0, max_followers)
    )
    for follower in followers:
        try:
            r.sadd(f"{follower}:follows", username)
            r.sadd(f"{username}:followers", follower)
        except:
            pass

    for paper in user["papers"]:
        post_id = paper["post_id"]

        if "pdf" in paper:
            with open(f"/dataset/papers/{paper['pdf']}", "rb") as fin:
                filename = paper["pdf"]
                r.lpush(f"file:{filename}", fin.read(), username)
                r.sadd("filenames", filename)
                r.sadd(f"{username}:files", filename)

        if "abstract" in paper:
            with open(f"/dataset/abstracts/{paper['abstract']}", "rb") as fin:
                r.lpush(f"{username}:posts", post_id)
                r.lpush(
                    f"post:{str(post_id)}",
                    post_id,
                    0,
                    username,
                    paper["title"],
                    fin.read(),
                    time.time(),
                )

                # push post to followers
                followers = [
                    follower.decode() for follower in r.smembers(f"{username}:follows")
                ]
                for follower in followers:
                    r.lpush(f"{follower}:posts", post_id)