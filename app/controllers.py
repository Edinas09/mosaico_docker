from app import app, cache
from flask import jsonify, request
import requests
import hashlib



@app.route("/api/ping")
def ping():
    return jsonify({"success": True})

def create_md5(tags, sortBy, direction):
    parameters = f"tags={tags}sortBy={sortBy}direction{direction}"
    md5 = hashlib.md5(parameters.encode()).hexdigest()
    return md5


@app.route("/api/posts")
def posts():

    args = request.args
    tags = args.get("tags")
    sortBy = args.get("sortBy", "id")
    direction = args.get("direction", "asc")

    if not tags:
        response = {"error": "Tags parameter is required"}
        return response, 400

    if sortBy not in ("id", "reads", "likes", "popularity"):
        response = {"error": "sortBy parameter is invalid"}
        return response, 400

    if direction not in ("asc", "desc"):
        direction = "asc"

    ls_tags = tags.split(",")
    posts_dict = {}

    md5 = create_md5(tags, sortBy, direction)

    result = cache.get(md5)
    if result:
        return result

    for tags in ls_tags:
        result = requests.get(
            f"https://api.hatchways.io/assessment/blog/posts?tag={tags}&sortBy={sortBy}&direction={direction}"
        )
        posts = result.json()["posts"]
        # print(posts)
        result_dict = {}

        for post in posts:
            result_dict[post["id"]] = post

        posts_dict.update(result_dict)

    lst_dict = list(posts_dict.values())
    sort_by = sorted(
        lst_dict,
        key=lambda j: j[sortBy],
        reverse=True if direction == "desc" else False,
    )
    result = {"posts": sort_by}
    cache.set(md5, result)

    return result
