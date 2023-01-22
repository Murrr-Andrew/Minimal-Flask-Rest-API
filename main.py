from flask import Flask
from flask_restful import Resource, Api, reqparse, abort


app = Flask('VideoAPI')
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)

videos = {
    'video1': {'title': 'Hello World in Python'},
    'video2': {'title': 'Why Matlab is the best language ever'}
}


class Video(Resource):
    """
    Video class for Api
    """
    def get(self, video_id):
        """
        Get method for Api requests
        """
        if video_id == 'all':
            return videos, 200
        elif video_id not in videos:
            abort(http_status_code=404, message=f'Video {video_id} not found!')
        else:
            return videos[video_id], 200

    def put(self, video_id):
        """
        Put method for Api requests
        """
        if video_id not in videos:
            abort(http_status_code=404, message=f'Video {video_id} not found!')
        else:
            args = parser.parse_args()
            new_video = {'title': args['title']}
            videos[video_id] = new_video
            return {video_id: videos[video_id]}, 200

    def delete(self, video_id):
        """
        Delete method for Api request
        """
        if video_id not in videos:
            abort(http_status_code=404, message=f'Video {video_id} not found!')
        else:
            videos.pop(video_id)
            return {'message': 'Video has been deleted'}, 200


# Adding resource to the API and the endpoint for it
api.add_resource(Video, '/videos/<video_id>')

if __name__ == '__main__':
    app.run()
