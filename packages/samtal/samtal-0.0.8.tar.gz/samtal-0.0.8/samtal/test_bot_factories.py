from samtal import default_bot
from samtal.core.bot import Bot


def test_a_default_runnable_bot_can_be_created():
    bot = default_bot(
        mattermost_host="http://mattermost/",
        mattermost_bot_user="neo",
        mattermost_bot_password="matrix")
    assert bot is not None
    assert isinstance(bot, Bot)
