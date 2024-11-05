import os
import sys
import importlib
import inspect
from django.conf import settings
from django.urls import path


class DynamicURL(object):

    def get_classes(self, module_name):
        classes = []
        try:
            # Dynamically import the module if it's not already loaded
            if module_name not in sys.modules:
                importlib.import_module(module_name)
            module = sys.modules[module_name]

            # Get classes defined in this specific module
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == module_name:
                    classes.append(obj)
        except (KeyError, ModuleNotFoundError) as e:
            print(f"Module {module_name} could not be loaded: {e}")

        return classes

    def create_route(self, route):
        params = route.split("/")
        new_route = ""
        for param in params:
            if param.startswith("{") and param.endswith("}"):
                deserialize = param[1:-1].split("__")
                if len(deserialize) > 1:
                    new_route += "/<{}:{}>".format(deserialize[0], deserialize[1])
                else:
                    new_route += "/<{}>".format(param[1:-1])
            else:
                new_route += "/" + param
        return new_route[1:]

    def get_file(self, directory, urls=[], root_dir=""):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and file != "serializers.py":
                    # Convert file path to module path
                    relative_path = os.path.relpath(
                        os.path.join(root, file), settings.BASE_DIR
                    )
                    module_name = relative_path.replace(os.path.sep, ".")[
                        :-3
                    ]  # Remove '.py' extension
                    classes = self.get_classes(module_name)
                    for cls in classes:
                        file_dir = root.replace(
                            str(os.path.join(settings.BASE_DIR, root_dir)), ""
                        ).replace(os.path.sep, "/")
                        file_dir = (
                            file_dir[1:] if file_dir.startswith("/") else file_dir
                        )
                        route = self.create_route(f"{file_dir}/{cls.__name__}")
                        urls.append(
                            path(
                                route,
                                cls.as_view(),
                                name=cls.__name__,
                            )
                        )

        return urls

    def get_urls(self):
        apps_path = os.path.join(settings.BASE_DIR, "api/sync")
        for app in os.listdir(apps_path):
            urls = []
            if app.startswith("_"):
                continue
            app_path = os.path.join(apps_path, app)
            if os.path.isdir(app_path):
                _urls = self.get_file(app_path, root_dir="api/sync")
                urls.extend(_urls)
        return urls
