from flask import Flask, request, abort
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

#comment out after running for the first time
# db.create_all()

names = {"spencer": {"age": 28, "gender": "male"}, 
         "tim": {"age": 19, "gender": "male"}}



video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, required=True, help="Name of the video is required.")
video_put_args.add_argument("views", type=int, required=True, help="Views of the video is required.")
video_put_args.add_argument("likes", type=int, required=True, help="Likes of the video is required.")


class Video(Resource):
    def get(self, video_id):
        result = VideoModel.query.get(id=video_id)
        return result 
    
    def post(self, video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201
    
    def delete(self, video_id):
        abort_if_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204


api.add_resource(Video, "/video/<int:video_id>")

api.add_resource(HelloWorld, "/hello/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)