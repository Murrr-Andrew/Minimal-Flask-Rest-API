import json
import os
from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask('VideoAPI')
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)


class Video(Resource):
    """
    Video class for Api
    """
    file = os.path.join(os.getcwd(), 'videos.json')

    def get(self, video_id):
        """
        GET method for Api requests
        """
        try:
            with open(self.file) as f:
                videos = json.load(f)

            if video_id not in videos:
                response = {'message': f'Video with ID {video_id} not found!'}, 404
            else:
                response = videos[video_id], 200

        except FileNotFoundError:
            response = {'message': 'Server error. Try again later!'}, 500

        return response

    def put(self, video_id):
        """
        PUT method for Api requests
        """
        try:
            with open(self.file) as f:
                videos = json.load(f)

            if video_id not in videos:
                response = {'message': f'Video with ID {video_id} not found!'}, 404
            else:
                args = parser.parse_args()
                new_video = {'title': args['title'], 'uploadDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                videos[video_id] = new_video

                with open(self.file, 'w') as f:
                    json.dump(videos, f)

                response = {video_id: videos[video_id]}, 200

        except FileNotFoundError:
            response = {'message': 'Server error. Try again later!'}, 500

        return response

    def delete(self, video_id):
        """
        DELETE method for Api request
        """
        try:
            with open(self.file, 'r') as f:
                videos = json.load(f)

            if video_id not in videos:
                response = {'message': f'Video with ID {video_id} not found!'}, 404
            else:
                videos.pop(video_id)

                with open(self.file, 'w') as f:
                    json.dump(videos, f)

                response = {'message': 'Video has been deleted'}, 200

        except FileNotFoundError:
            response = {'message': 'Server error. Try again later!'}, 500

        return response


class VideoSchedule(Resource):
    """
    Video Schedule class for Api
    """
    file = os.path.join(os.getcwd(), 'videos.json')

    def get(self):
        """
        GET method for Api requests
        """
        try:
            with open(self.file) as f:
                videos = json.load(f)

            response = videos, 200

        except FileNotFoundError:
            response = {'message': 'Server error. Try again later!'}, 500

        return response

    def post(self):
        """
        POST method for Api requests
        """
        try:
            with open(self.file) as f:
                videos = json.load(f)

            args = parser.parse_args()
            video_id = max([int(key) for key in videos.keys()]) + 1
            new_video = {'title': args['title'], 'uploadDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            videos[video_id] = new_video

            with open(self.file, 'w') as f:
                json.dump(videos, f)

            response = {video_id: videos[video_id]}, 200

        except FileNotFoundError:
            response = {'message': 'Server error. Try again later!'}, 500

        return response


api.add_resource(Video, '/videos/<video_id>')
api.add_resource(VideoSchedule, '/videos')

if __name__ == '__main__':
    app.run()
