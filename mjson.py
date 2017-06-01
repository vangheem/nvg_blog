from datetime import datetime
from zope.dottedname.resolve import resolve

import json
import re


_type_marker = 'type://'


class BaseTypeSerializer(object):
    klass = None
    toklass = None

    @classmethod
    def get_type_name(kls):
        return "%s.%s" % (kls.klass.__module__, kls.klass.__name__)

    @classmethod
    def serialize(kls, obj):
        if hasattr(obj, 'aq_base'):
            obj = obj.aq_base
        data = kls._serialize(obj)
        results = {
            'type': kls.get_type_name(),
            'data': data
        }
        return _type_marker + dumps(results)

    @classmethod
    def _serialize(kls, obj):
        return kls.toklass(obj)

    @classmethod
    def deserialize(kls, data):
        return kls._deserialize(data)

    @classmethod
    def _deserialize(kls, data):
        return kls.klass(data)


class setSerializer(BaseTypeSerializer):
    klass = set
    toklass = list


class datetimeSerializer(BaseTypeSerializer):
    klass = datetime

    @classmethod
    def _serialize(kls, obj):
        return obj.isoformat()

    @classmethod
    def _deserialize(kls, data):
        return datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')


_serializers = {
    set: setSerializer,
    datetime: datetimeSerializer
}


class Deferred:
    pass


def custom_handler(obj):
    _type = type(obj)
    if _type.__name__ == 'instance':
        _type = obj.__class__
    if _type in _serializers:
        serializer = _serializers[_type]
        return serializer.serialize(obj)
    else:
        return None
    return obj


def custom_decoder(d):
    if isinstance(d, list):
        pairs = enumerate(d)
    elif isinstance(d, dict):
        pairs = d.items()
    result = []
    for k, v in pairs:
        if isinstance(v, str):
            if v.startswith(_type_marker):
                v = v[len(_type_marker):]
                results = loads(v)
                try:
                    _type = resolve(results['type'])
                    serializer = _serializers[_type]
                    v = serializer.deserialize(results['data'])
                except ImportError:
                    pass
        elif isinstance(v, (dict, list)):
            v = custom_decoder(v)
        result.append((k, v))
    if isinstance(d, list):
        return [x[1] for x in result]
    elif isinstance(d, dict):
        return dict(result)


def loads(data):
    return json.loads(data, object_hook=custom_decoder)


def dumps(data):
    return json.dumps(data, default=custom_handler)
