"""Config manipulation functions."""
import ast
import inspect
import os
import pathlib
import re
from pathlib import Path

import addict
import pint
import toml
from first import first

units = pint.UnitRegistry()

ENV_VAR_PATTERN = re.compile("@([A-Z_]+)")


def get_caller_path():
    stack = inspect.stack()
    try:
        frame = first(
            stack, key=lambda frame: "kick." in (frame.code_context[0] or [""])
        )
        path = pathlib.Path(frame.filename).parent
    except:
        path = None
    finally:
        del stack

    return path


def get_local_config_path(variant, local_dir=None):
    local_dir = local_dir or get_caller_path() or pathlib.Path(".")
    path = local_dir / "config" / "{}.toml".format(variant)
    if not path.exists():
        path = local_dir / "config" / "config.toml"
    return path


def env_var_or_key(match):
    return os.getenv(match.group(1), match.group(0))


def replace_env_variables(config):
    if isinstance(config, str):
        return ENV_VAR_PATTERN.sub(env_var_or_key, config)
    if isinstance(config, list):
        return [replace_env_variables(v) for v in config]
    if isinstance(config, dict):
        config = addict.Dict(config)
        for key, value in config.items():
            if isinstance(value, str):
                config[key] = ENV_VAR_PATTERN.sub(env_var_or_key, value)
            elif isinstance(value, list):
                config[key] = [replace_env_variables(v) for v in value]
            elif isinstance(value, dict):
                config[key] = replace_env_variables(value)
    return config


def Config(
    app_name,
    project_config_dir=None,
    test=False,
    debug=True,
    paths=None,
    byte_units=None,
    second_units=None,
):
    config_path = get_config_path(app_name, project_config_dir, test, debug)
    config = toml.loads(config_path.read_text())
    config = merge_config_with_env(config, app_name)
    config = replace_env_variables(config)
    config = parse_config_values(config, paths, byte_units, second_units)
    config = addict.Dict(config)

    return config


def _value_from_env(env_key, old_value):
    if isinstance(old_value, str):
        return os.environ[env_key]
    return ast.literal_eval(os.environ[env_key])


def _value_from_file(file_env_key, old_value):
    with open(os.environ[file_env_key]) as f:
        env_value = f.read().strip()

    if isinstance(old_value, str):
        return env_value
    return ast.literal_eval(env_value)


def normalize_app_name(app_name):
    return app_name.upper().replace("-", "_").replace(" ", "_")


def merge_config_with_env(config, app_name, var_name=None):
    app_name = normalize_app_name(app_name)
    for key, val in config.items():
        if not var_name:
            env_key = key.upper()
        else:
            env_key = f"{var_name}_{key}".upper()
        file_env_key = f"{env_key}__FILE"

        if isinstance(val, dict):
            config[key] = merge_config_with_env(val, app_name, env_key)
        elif f"{app_name}_{env_key}" in os.environ:
            config[key] = _value_from_env(f"{app_name}_{env_key}", val)
        elif f"{app_name}_{file_env_key}" in os.environ:
            config[key] = _value_from_file(f"{app_name}_{file_env_key}", val)

    return config


def to_path(value):
    return Path(value).expanduser()


def to_bytes(value):
    return int(units.parse_expression(value).to(units.bytes).magnitude)


def to_seconds(value):
    return int(units.parse_expression(value).to(units.seconds).magnitude)


def parse_config_values(config, paths=None, byte_units=None, second_units=None):
    def convert(config_values, converter):
        for subconfig, *attrs in config_values:
            for attr in attrs:
                if not subconfig[attr]:
                    continue
                subconfig[attr] = converter(subconfig[attr])

    if paths:
        convert(paths, to_path)
    if byte_units:
        convert(byte_units, to_bytes)
    if second_units:
        convert(second_units, to_seconds)

    return config


def get_config_path(app_name, project_config_dir=None, test=False, debug=True):
    app_name = normalize_app_name(app_name)
    if os.getenv(f"{app_name}_CONFIG_PATH"):
        return Path(os.getenv(f"{app_name}_CONFIG_PATH"))

    if os.getenv(f"{app_name}_CONFIG_NAME"):
        config_name = os.getenv(f"{app_name}_CONFIG_NAME")
    elif test:
        config_name = "test"
    elif debug:
        config_name = "develop"
    else:
        config_name = "config"

    config_dir = Path.home() / ".config" / app_name.lower()

    config_path = config_dir / f"{config_name}.toml"
    if config_path.exists():
        return config_path

    project_config_dir = project_config_dir or get_local_config_path(config_name)
    config_path = project_config_dir / f"{config_name}.toml"
    if not config_path.exists():
        raise FileNotFoundError(f"Can't find config '{config_name}.toml'")

    return config_path
