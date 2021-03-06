from flask import request
from flask_restplus import Resource

from mission_planner.api import api
from mission_planner.api.path import serializers
from mission_planner.api.path.buisness import compute_path
from mission_planner.graph import get_graph

path_ns = api.namespace('path')


@path_ns.route('')
class Path(Resource):

    @staticmethod
    @path_ns.marshal_with(serializers.mission_result)
    @api.expect(serializers.mission_parameters)
    def post():
        mission_parameters = request.json
        mission_points = [{'x': int(point['x']), 'y': int(point['y'])} for point in mission_parameters['points']]

        graph = get_graph()

        path, hypsometric_profile, distance = compute_path(graph, mission_points)

        return {
                   'path': path,
                   'hypsometric_profile': hypsometric_profile,
                   'total_distance': distance}, 200

    @staticmethod
    def get():
        return 'hello', 200
