# coding=utf-8
from application import app, manager
from flask_script import Server
import www

# web server
manager.add_command('runserver', Server(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'],
                                        use_debugger=app.config['DEBUG'], use_reloader=True))


def main():
    # app.run()
    manager.run()


if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())


    except Exception as e:
        import traceback

        traceback.print_exc()