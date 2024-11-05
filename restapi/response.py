from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json


class DictResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.

    :param data: Data to be dumped into json. By default only ``dict`` objects
      are allowed to be passed due to a security flaw before ECMAScript 5. See
      the ``safe`` parameter for more information.
    :param encoder: Should be a json encoder class. Defaults to
      ``django.core.serializers.json.DjangoJSONEncoder``.
    :param safe: Controls if only ``dict`` objects may be serialized. Defaults
      to ``True``.
    :param json_dumps_params: A dictionary of kwargs passed to json.dumps().
    """

    def __init__(
        self,
        message="",
        data=None,
        error=None,
        validation_error=None,
        encoder=DjangoJSONEncoder,
        safe=False,
        json_dumps_params=None,
        **kwargs,
    ):
        self.message = message
        self.data = data
        self.error = error
        self.validation_error = validation_error
        self.encoder = encoder
        self.safe = safe
        self.json_dumps_params = json_dumps_params
        self.kwargs = kwargs
        self.data_dict = {}
        if safe and not isinstance(self.data, dict):
            raise TypeError(
                "In order to allow non-dict objects to be serialized set the "
                "safe parameter to False."
            )
        if self.json_dumps_params is None:
            self.json_dumps_params = {}
        self.kwargs.setdefault("content_type", "application/json")

        if not isinstance(message, str):
            raise ValueError(f"Message should be str not {type(message)}.")

        self._data()
        data = json.dumps(self.data_dict, cls=self.encoder, **self.json_dumps_params)
        super().__init__(content=data, **self.kwargs)

    def _data(self):
        self.data_dict = {
            "message": self.message,
            **({"data": self.data} if self.data else {}),
            **({"error": self.error} if self.error else {}),
            **(
                {"validation_error": self.validation_error}
                if self.validation_error
                else {}
            ),
        }
