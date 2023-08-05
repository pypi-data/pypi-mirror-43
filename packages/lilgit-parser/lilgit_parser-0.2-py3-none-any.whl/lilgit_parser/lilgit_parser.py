""" LilGit Parser """

from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler

from lilgit_parser.parseHandler import ParseHandler

path_regex = r'(?P<path>(?:(?:/[^/]+)+|/?))'

class LilGitHandler(IPythonHandler):
    def _jupyter_server_extension_paths():
        return [{
            'module': 'lilgit_parser'
        }]

    def load_jupyter_server_extension(nb_server_app):
        """
        Called when the extension is loaded.
        Args:
            nb_server_app (NotebookApp): handle to the Notebook webserver instance.
        """
        web_app = nb_server_app.web_app
        # Prepend the base_url so that it works in a jupyterhub setting
        base_url = web_app.settings['base_url']
        lilgit = url_path_join(base_url, 'lilgit')
        parse = url_path_join(lilgit, 'build')

        handlers = [(f'{parse}{path_regex}',
                     LatexBuildHandler,
                     {"notebook_dir": nb_server_app.notebook_dir}
                    )]
        web_app.add_handlers('.*$', handlers)
