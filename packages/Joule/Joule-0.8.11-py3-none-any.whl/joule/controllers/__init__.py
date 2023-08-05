from aiohttp import web
from joule.controllers import (
    root_controller,
    stream_controller,
    folder_controller,
    data_controller,
    module_controller,
    interface_controller)

routes = [
    web.get('/', root_controller.index),
    web.get('/dbinfo', root_controller.dbinfo),
    web.get('/version', root_controller.version),
    web.get('/version.json', root_controller.version_json),
    # --- stream controller routes ---
    # list all streams
    web.get('/streams.json', stream_controller.index),
    web.get('/stream.json', stream_controller.info),
    web.put('/stream/move.json', stream_controller.move),
    web.put('/stream.json', stream_controller.update),
    web.post('/stream.json', stream_controller.create),
    web.delete('/stream.json', stream_controller.delete),
    # --- folder routes ---
    web.get("/folder.json", folder_controller.info),
    web.put('/folder/move.json', folder_controller.move),
    web.put('/folder.json', folder_controller.update),
    web.delete('/folder.json', folder_controller.delete),
    # --- data routes ---
    web.get('/data', data_controller.read),
    web.get('/data.json', data_controller.read_json),
    web.get('/data/intervals.json', data_controller.intervals),
    web.post('/data', data_controller.write),
    web.delete('/data', data_controller.remove),
    # --- module routes ---
    web.get('/modules.json', module_controller.index),
    web.get('/module.json', module_controller.info),
    web.get('/module/logs.json', module_controller.logs),
    # --- interface routes ---
    web.get('/interface/{id}', interface_controller.proxy),
    web.get('/interface/{id}/{path:.*}', interface_controller.proxy),
    web.post('/interface/{id}/{path:.*}', interface_controller.proxy)

    # TODO: routes for stream tags /streams/tags
]
