from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
# Change configuration settings. Define the location of our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# model to store videos
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # max length = 100
    views =  db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # representstion of the object
    def __repr__(self):
        return f'Video(name={name},views={views},likes={likes})'

# only do it ones , to create database
# db.create_all()
 
# If you specify the 'help' value, it will be rendered as the error 
# message when a type error is raised while parsing it
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name",type=str,help="Name of the video",required=True)
video_put_args.add_argument("views",type=int,help="Views of the video",required=True)
video_put_args.add_argument("likes",type=int,help="Likes on the video",required=True)

videos = {}


def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404,message="Can not find video...") #404	Not Found

def abort_if_video__exist(video_id):
    if video_id in videos:
        abort(409,message="Video alreary exist with this id...") # 409	Conflict

class Video(Resource):

    def get(self,video_id):
        abort_if_video_id_doesnt_exist(video_id)
        return videos[video_id]

    def put(self,video_id):
        abort_if_video__exist(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201 # status return that it is created
    
    def delete(self,video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204 # 204  No Content

api.add_resource(Video,"/helloworld/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)