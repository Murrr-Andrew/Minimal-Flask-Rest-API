from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort


app = Flask('VideoAPI')
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)

videos = {
    '1': {
        'title': 'Hello World in Python',
        'uploadDate': '2023-01-22 16:25:01'
    },
    '2': {
        'title': 'Why Matlab is the best language ever',
        'uploadDate': '2023-01-22 17:15:25'
    }
}


class Video(Resource):
    """
    Video class for Api
    """
    def get(self, video_id):
        """
        GET method for Api requests
        """
        if video_id not in videos:
            abort(http_status_code=404, message=f'Video with ID {video_id} not found!')
        else:
            return videos[video_id], 200

    def put(self, video_id):
        """
        PUT method for Api requests
        """
        if video_id not in videos:
            abort(http_status_code=40, message=f'Video with ID {video_id} not found!')
        else:
            args = parser.parse_args()
            new_video = {
                'title': args['title'],
                'uploadDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            videos[video_id] = new_video
            return {video_id: videos[video_id]}, 200

    def delete(self, video_id):
        """
        DELETE method for Api request
        """
        if video_id not in videos:
            abort(http_status_code=404, message=f'Video with ID {video_id} not found!')
        else:
            videos.pop(video_id)
            return {'message': 'Video has been deleted'}, 200


class VideoSchedule(Resource):
    """
    Video Schedule class for Api
    """
    def get(self):
        """
        GET method for Api requests
        """
        return videos, 200

    def post(self):
        """
        POST method for Api requests
        """
        args = parser.parse_args()
        video_id = max([int(key) for key in videos.keys()]) + 1
        new_video = {
            'title': args['title'],
            'uploadDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        videos[video_id] = new_video

        return {video_id: videos[video_id]}, 200


# Adding resource to the API and the endpoint for it
api.add_resource(Video, '/videos/<video_id>')
api.add_resource(VideoSchedule, '/videos')

if __name__ == '__main__':
    app.run()
