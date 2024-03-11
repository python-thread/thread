try:
    import importlib

    thread_cli = importlib.import_module('thread-cli')
    app = thread_cli.app
except ModuleNotFoundError:

    def app(prog_name='thread'):
        print('thread-cli not found, please install it with `pip install thread-cli`')
        exit(1)
