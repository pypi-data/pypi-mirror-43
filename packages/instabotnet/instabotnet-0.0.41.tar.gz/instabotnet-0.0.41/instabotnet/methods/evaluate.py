import os
import traceback
from ..nodes import Node, node_classes
from .common import decorate
from instagram_private_api.errors import (
    ClientError,
    ClientLoginRequiredError,
    ClientCookieExpiredError,
    ClientConnectionError,
    ClientThrottledError,
    ClientReqHeadersTooLargeError,
)

DEBUG = bool(os.environ.get('DEBUG'))

@decorate(accepts=(*node_classes.values(),), returns=Node)
def evaluate(bot, nodes,  args) -> Node:

    total = args['info']['total_nodes']
    count = 0


    while True:

        try:
            next(iter(nodes))

        except StopIteration:
            break

        except ClientLoginRequiredError as e:
            bot.logger.error(f'\n{e}')
            bot.relogin()
        
        except ClientConnectionError as e:  
            bot.logger.error(f'\n{e}')

        except (ClientReqHeadersTooLargeError, ClientThrottledError) as e:
            bot.logger.error(f'\n{e}')
            bot.sleep(5 * 60)
            
        except ClientError as e: # when trying to see private user
            bot.logger.error(f'\n{e}')
            bot.sleep()

        except Exception as e:
            bot.logger.error('unexpected exception {e}')
            raise

        else:
            count += 1
            percentage = (str(int(count / total * 100)) + '%').center(5)
            bot.logger.info( f'{percentage}:  {count} nodes out of {total}')
            

    # bot.logger.warn(nodes[:3])

    return nodes, {}



