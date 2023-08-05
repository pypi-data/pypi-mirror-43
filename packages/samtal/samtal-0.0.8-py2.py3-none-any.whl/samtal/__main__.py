import logging
import os

from samtal import default_bot


def main():
    bot_user = os.environ.get("BOT_USER")
    bot_password = os.environ.get("BOT_PASSWORD")
    db_file = os.environ.get("BOT_DB_FILE", ":memory:")

    default_bot(
        mattermost_host="framateam.org",
        mattermost_bot_user=bot_user,
        mattermost_bot_password=bot_password,
        sqlite_db=db_file,
    ).run()


if __name__ == '__main__':
    logging.root.setLevel(10)
    main()
