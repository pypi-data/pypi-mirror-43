import ujson

from stepist.flow.utils import AttrDict


DEFAULT_REDIS_KWARGS = dict(
    host='localhost',
    port=6379,
    decode_responses=True
)


class AppConfig(AttrDict):

    @classmethod
    def init_default(cls):
        return cls(
            redis_kwargs=DEFAULT_REDIS_KWARGS,
            redis_stats_kwargs=DEFAULT_REDIS_KWARGS,
            pickler=ujson
        )

