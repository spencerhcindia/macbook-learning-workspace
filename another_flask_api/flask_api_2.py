from ast import arg
from email import message
from flask import Flask, request, abort
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

names = {"spencer": {"age": 28, "gender": "male"}, 
         "tim": {"age": 19, "gender": "male"}}

videos = {}

def abort_if_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video id is not valid")

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, required=True, help="Name of the video is required.")
video_put_args.add_argument("views", type=int, required=True, help="Views of the video is required.")
video_put_args.add_argument("likes", type=int, required=True, help="Likes of the video is required.")

class HelloWorld(Resource):
    def get(self, name):
        return names[name]

    def post(self):
        return {"data": "posted"}

class Video(Resource):
    def get(self, video_id):
        abort_if_id_doesnt_exist(video_id)
        return videos[video_id]
    
    def put(self, video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201


api.add_resource(Video, "/video/<int:video_id>")

api.add_resource(HelloWorld, "/hello/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)