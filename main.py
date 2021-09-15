from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)


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