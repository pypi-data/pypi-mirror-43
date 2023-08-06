from .core import Reactor, Plan
from importlib import import_module
import json
import sys
import os

def import_obj(path):
    # Ensure the current directory is on the path
    current_dir = os.path.abspath('.')
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    # Split the object name and the module path
    module_path, handler_name = path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, handler_name)
    for attr in module_path.split('.')[1:]:
        module = getattr(module, attr)
    obj = getattr(module, handler_name)
    if obj is None:
        raise ValueError('Unable to import object: {}'.format(path))
    return obj

def main():
    args = sys.argv[1:]
    if len(args) < 0:
        print('A configuration file is required')
        sys.exit(1)
    
    path = args[0]
    with open(path, 'r') as f:
        config = f.read()
    if path.endswith('.yaml') or path.endswith('.yml'):
        import yaml
        data = yaml.safe_load(config)
    else:
        data = json.loads(config)


    reactor = Reactor()
    if type(data) == dict:
        plans = []
        for key, value in data.items():
            plans.append({'name': key, **value})
    elif type(data) == list:
        plans = data
    else:
        raise ValueError('Configuration must have an array or object at the top level')

    for plan in plans:
        name = plan.get('name', None)
        background = plan.get('background', True)
        schedule_type = plan.get('schedule_type', None)
        schedule_args = plan.get('schedule', None)
        action_path = plan.get('action')
        func = import_obj(action_path)

        if background:
            action = reactor.background_action(func)
        else:
            action = reactor.action(func)

        if type(schedule_args) != dict:
            raise ValueError('schedule_args must be an object')
        if schedule_type == 'calendar':
            schedule = reactor.schedule_calendar(**schedule_args)
        elif schedule_type == 'interval':
            schedule = reactor.schedule_interval(**schedule_args)
        else:
            raise ValueError('schedule_type must be either calendar or interval')

        reactor.plans.append(Plan(schedule, action, name=name))

    if '--debug' in args:
        reactor._debug()
    else:
        reactor.run()

if __name__ == '__main__':
    main()
