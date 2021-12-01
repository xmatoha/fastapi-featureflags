import json
import requests


class FeatureFlags(object):
    conf_from_json = None
    conf_from_url = None
    features = {}

    @staticmethod
    def load_conf_from_url(conf_from_url):
        FeatureFlags.conf_from_url = conf_from_url
        params = requests.get(conf_from_url).json()
        for k, v in params.items():
            FeatureFlags.features[k] = v

    @staticmethod
    def load_conf_from_json(conf_from_json):
        FeatureFlags.conf_from_json = conf_from_json
        with open(conf_from_json, "r") as f:
            params = json.loads(f.read())
            for k, v in params.items():
                FeatureFlags.features[k] = v

    @staticmethod
    def reload_feature_flags():
        FeatureFlags.features = {}
        if FeatureFlags.conf_from_url:
            FeatureFlags.load_conf_from_url(FeatureFlags.conf_from_url)
            return True
        elif FeatureFlags.conf_from_json:
            FeatureFlags.load_conf_from_json(FeatureFlags.conf_from_json)
            return True
        else:
            return False

    @classmethod
    def handle_feature(cls, feature_name):
        features = cls.features
        if features.get(feature_name, False) is False:
            features[feature_name] = False

    @classmethod
    def is_enabled(cls, feature_name):
        features = cls.features
        return features.get(feature_name, False)

    @classmethod
    def get_features(cls):
        return cls.features

    @classmethod
    def enable_feature(cls, feature_name):
        cls.features[feature_name] = True
        return cls.features[feature_name]

    @classmethod
    def disable_feature(cls, feature_name):
        cls.features[feature_name] = False
        return cls.features[feature_name]


def feature_flag(feature_name):
    def decorator(function):
        def wrapper(*args, **kwargs):
            FeatureFlags.handle_feature(feature_name)
            if FeatureFlags.is_enabled(feature_name):
                # print("Feature Enabled:", feature_name)
                return function(*args, **kwargs)
            else:
                # print("Feature Disabled:", feature_name)
                return True

        return wrapper

    return decorator


def feature_enabled(feature_name):
    FeatureFlags.handle_feature(feature_name)
    return FeatureFlags.is_enabled(feature_name)
