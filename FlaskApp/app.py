from argparse import ArgumentParser

import graphene
from flask import Flask
from flask_graphql import GraphQLView
from flask_pydantic import validate

from lib.api import register, info
from lib.models import Track
from lib.storage import storage

app = Flask(__name__)


@app.route('/api/track', methods=['POST'])
@validate()
def register_track(body: Track):
    return register(body)


@app.route('/api/track/<track_id>', methods=['GET'])
@validate()
def track_info(track_id: str):
    return info(track_id)


def init_graphql(app):
    class Project(graphene.ObjectType):
        id = graphene.String(default_value="id")
        public_name = graphene.String(default_value="Fake Project")

    class Track(graphene.ObjectType):
        project = graphene.Field(Project)
        max_parallel_pools = graphene.Int()
        min_pool_acceptance_rate = graphene.Float()
        max_hourly_appeals = graphene.Int()
        check_interval_minutes = graphene.Int()
        soft_alert_multiplier = graphene.Float()

        def resolve_project(self, info):
            return Project()

    class Query(graphene.ObjectType):
        tracks = graphene.List(Track, limit=graphene.Int(), pattern=graphene.String())

        def resolve_tracks(self, info, limit: int, pattern: str):
            all_tracks = list(map(lambda track: Track(
                max_parallel_pools=track.max_parallel_pools,
                min_pool_acceptance_rate=track.min_pool_acceptance_rate,
                max_hourly_appeals=track.max_hourly_appeals,
                check_interval_minutes=track.check_interval_minutes,
                soft_alert_multiplier=track.soft_alert_multiplier,
                project=Project()
            ), list(filter(lambda tr: pattern in tr.name, storage.get_all_tracks()))))

            return all_tracks[:limit]


    app.add_url_rule(
        '/graphql/tracks',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=graphene.Schema(query=Query),
            graphiql=True
        )
    )


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    init_graphql(app)
    app.run(host=args.host, port=args.port)
