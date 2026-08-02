"""
Enterprise Plugin Loader

Automatically discovers

• Node Builders

• Edge Builders

Enterprise V7
"""

import pkgutil
import inspect
import importlib


class PluginLoader:

    @staticmethod
    def load(package):

        builders = []

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):

            module = importlib.import_module(

                f"{package.__name__}.{module_name}"

            )

            for _, cls in inspect.getmembers(

                module,

                inspect.isclass,

            ):

                if cls.__module__ != module.__name__:
                    continue

                if cls.__name__.endswith("Builder"):

                    builders.append(

                        cls()

                    )

        return builders