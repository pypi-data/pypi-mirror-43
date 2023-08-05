from .nodes_edges import nodes_edges
from .make_bots import make_bots
from .populate import populate_object, populate_string
from .assert_good_script import assert_good_script
from .reducer import  reducer
from .support import dotdict, merge
from collections import deque
from functools import reduce
import traceback
import os


from ruamel.yaml import YAML

yaml = YAML()


DEBUG = bool(os.environ.get('DEBUG'))

def execute(script, variables={}) -> [dict]:

    script = obj_from_yaml(script, variables)

    assert_good_script(script)

    bot = make_bots(script)[0]

    script_name = script['name'] if 'name' in script else 'unnmaed script'
    bot.logger.info(f'# SCRIPT {script_name}')

    result = deque()

    try:
        for action in script['actions']:
            action_name = action['name'] if 'name' in action else 'unnmaed action'
            bot.logger.info(f'# ACTION {action_name}')

            nodes, edges = nodes_edges(action, bot)
            begin_state = dotdict(nodes=nodes, bot=bot, data=deque([]), errors=[])
            bot.logger.info(f'# with nodes {nodes}')

            end_state = reduce(reducer, edges, begin_state)
            result.extend(end_state['data'])

    except (KeyboardInterrupt, SystemExit):
        bot.logger.warn('keyboard interrupt')
        exit(0)

    except Exception as exc:
        print(
            exc.__class__.__name__,
            ':',
            exc,
            '\n',
            '\n'.join(traceback.format_exc().split('\n'))
        )
        raise

    else:
        result = dict(reduce(merge, result))
        return result



def obj_from_yaml(script, variables):
    if isinstance(script, str):
        script = populate_string(script, variables)
        return yaml.load(script)
    else:
        return populate_object(script, variables)





    # try:
    #     for action in script['actions']:
    #
    #
    #
    #         threads = []
    #         task = make_task(action)
    #         name = task['name']
    #
    #         for (task, bot) in partitionate(task, bots):
    #             state = dict(nodes=task.nodes, bot=bot, data=dict(), errors=[])
    #             threads += [Reducer(state, task.edges)]
    #             # bot.logger.debug('edges : {}, nodes: {}'.format(edges, list(state['nodes'])))
    #
    #
    #         threads = start(threads)
    #         threads = wait(threads)
    #
    #         data['__' + interaction + '_interaction__'] = [thread.get_data() for thread in threads]
    #         # {'thread' + thread.name: thread.get_data() for thread in threads}
