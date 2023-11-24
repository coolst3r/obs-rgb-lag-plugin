import obspython as obs
import time

layer_delay = 1000  # Delay for each layer in milliseconds
freeze_interval = 4000  # Freeze frame interval in milliseconds
freeze_duration = 100  # Duration of freeze frame in milliseconds

def lag_rgb_callback(cd):
    source = obs.obs_frontend_get_current_scene()
    if source is None:
        return

    scene = obs.obs_scene_from_source(source)
    if scene is None:
        obs.obs_source_release(source)
        return

    scene_items = obs.obs_scene_enum_items(scene)
    if scene_items is None:
        obs.obs_scene_release(scene)
        obs.obs_source_release(source)
        return

    layers = []
    for item in scene_items:
        source = obs.obs_sceneitem_get_source(item)
        if source is not None:
            layers.append(source)

    obs.sceneitem_list_release(scene_items)
    obs.obs_scene_release(scene)
    obs.obs_source_release(source)

    for i, layer in enumerate(layers):
        obs.obs_source_release(layer)
        layer = obs.obs_get_source_by_name(f'layer{i+1}')
        if layer is not None:
            obs.obs_source_release(layer)
            layer = obs.obs_get_source_by_name(f'layer{i+1}')
            if layer is not None:
                settings = obs.obs_source_get_settings(layer)
                lag_time = i * layer_delay
                obs.obs_data_set_int(settings, 'delay_ms', lag_time)
                obs.obs_source_update(layer, settings)
                obs.obs_data_release(settings)
                obs.obs_source_release(layer)

    for i in range(0, len(layers), 4):
        obs.obs_source_release(layers[i])
        layer = obs.obs_get_source_by_name(f'layer{i+1}')
        if layer is not None:
            obs.obs_source_release(layer)
            layer = obs.obs_get_source_by_name(f'layer{i+1}')
            if layer is not None:
                settings = obs.obs_source_get_settings(layer)
                obs.obs_data_set_bool(settings, 'freeze_frame', True)
                obs.obs_data_set_int(settings, 'freeze_interval', freeze_interval)
                obs.obs_data_set_int(settings, 'freeze_duration', freeze_duration)
                obs.obs_source_update(layer, settings)
                obs.obs_data_release(settings)
                obs.obs_source_release(layer)

def script_description():
    return "Lag RGB display of each layer by increasing delay and freeze frame every 4 seconds."

def script_load(settings):
    obs.obs_frontend_add_event_callback(lag_rgb_callback)

def script_unload():
    obs.obs_frontend_remove_event_callback(lag_rgb_callback)
