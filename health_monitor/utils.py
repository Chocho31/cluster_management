import re


def parse_env(env, prefix, delimiter):
    result = {}

    for var in env:
        split_var = var.split(delimiter)
        if prefix in split_var[0]:
            key = split_var[0].replace(prefix, '').lower()
            value = split_var[1]

            result[key] = value

    return result


def parse_period(period):
    split = re.split('(\d+)', period)
    number = int(split[1])
    time_period = split[2]

    if time_period == 's':
        return number

    elif time_period == 'm':
        return number * 60

    elif time_period == 'hr':
        return number * 3600
