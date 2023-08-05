from funcy import raiser, rcompose
from .common import decorate, tap
from ..nodes import Media




@decorate(accepts=Media, returns=Media)
def like(bot, nodes,  args):
    max = float(args['max']) if 'max' in args else float('inf')

    count = 0

    def increment():
        nonlocal count
        count += 1

    stop = raiser(StopIteration)

    process = rcompose(
        lambda x: stop() if x and count >= max else x,
        # lambda node: node \
        #     if bot.suitable(node) \
        #     else tap(None,lambda: bot.logger.warn('{} not suitable'.format(node))),
        lambda node: like_media(node, bot=bot) \
            if node else None,
        lambda x: tap(x, increment) if x else None,
    )


    liked = map(process, nodes)
    liked = filter(lambda x: x, liked)

    return liked, {}


def like_media(media, bot):
        bot.api.post_like(media.pk)
        bot.logger.info(f'liked media {media}')
        bot.total['likes'] += 1
        bot.sleep('like')
        return media
