from app import app
from flask import jsonify, request
import requests


@app.route("/api/ping")
def ping():
    return jsonify({"success": True})


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
    return {"posts": sort_by}
