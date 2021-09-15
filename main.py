import re
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort,fields, marshal_with
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

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name",type=str,help="Name of the video")
video_update_args.add_argument("views",type=int,help="Views of the video")
video_update_args.add_argument("likes",type=int,help="Likes on the video")


# how an object should be serialize
resource_fields = {
    'id':fields.String,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer
}

class Video(Resource):

    @marshal_with(resource_fields)
    def get(self,video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404,message="Could not find video with that id")
        return result

    @marshal_with(resource_fields)
    def put(self,video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message='Video id taken...')
        video = VideoModel(id=video_id,name=args['name'],views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201 # status return that it is created
    
    #update
    @marshal_with(resource_fields)
    def patch(self,video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404,message="Video can not update, can not update")
        if args["name"]:
            result.name = args['name']
        if args["views"]:
            result.views = args['views']
        if args["likes"]:
            result.likes = args['likes']
        
        # do not need to add any changes , just update and commit it
        db.session.commit()

        return result


    def delete(self,video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204 # 204  No Content

api.add_resource(Video,"/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)