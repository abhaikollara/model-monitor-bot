from keras.callbacks import Callback
import requests
import warnings
import numpy as np


class botMonitor(Callback):
    """Callback used to stream events to a server.
    Requires the `requests` library.
    Events are sent to `root + '/publish/epoch/end/'` by default. Calls are
    HTTP POST, with a `data` argument which is a
    JSON-encoded dictionary of event data.
    If send_as_json is set to True, the content type of the request will be application/json.
    Otherwise the serialized JSON will be send within a form
    # Arguments
        root: String; root url of the target server.
        path: String; path relative to `root` to which the events will be sent.
        field: String; JSON field under which the data will be stored. The field is used only if the payload is sent
        within a form (i.e. send_as_json is set to False).
        headers: Dictionary; optional custom HTTP headers.
        send_as_json: Boolean; whether the request should be send as application/json.
    """

    def __init__(self,
                 root='http://localhost:5000',
                 path='/model_monitor'):

        super(botMonitor, self).__init__()

        self.root = root
        self.path = path
        self.send_as_json = True
        if requests is None:
            raise ImportError('botMonitor requires '
                              'the `requests` library.')

    def send(self, data):
        try:
            requests.post(self.root + self.path, json=data)
        except requests.exceptions.RequestException:
            warnings.warn('Warning: could not reach RemoteMonitor '
                        'root server at ' + str(self.root))

    def on_train_begin(self, logs=None):
        data = {"Info": "Training started"}
        self.send(data)

    def on_batch_end(self, batch, logs=None, update_freq=100):
        send = {}
        send['batch'] = batch
        if batch % update_freq == 0 and batch >= update_freq:
            logs = logs or {}
            send = {}
            for k, v in logs.items():
                if isinstance(v, (np.ndarray, np.generic)):
                    send[k] = v.item()
                else:
                    send[k] = v
        
            self.send(send)

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        send = {}
        send["Info"] = "Epoch finished"
        send['epoch'] = epoch
        for k, v in logs.items():
            if isinstance(v, (np.ndarray, np.generic)):
                send[k] = v.item()
            else:
                send[k] = v

        self.send(send)