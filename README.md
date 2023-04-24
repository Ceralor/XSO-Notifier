# XSO-Notifier
Simple Flask app for sending notifications to XS Overlay

To run this application, either install Flask to a virtual environment/conda/etc, or to the user/host Python, and either `flask run app.py --host 0.0.0.0` or `python app.py`. The latter will default to port 64029, a spin on XS Overlay's 42069.

It MUST be run on the same Windows/Linux environment that XS Overlay is running in, and cannot be run on a separate host or VM, as XS is only listening on 127.0.0.1 for its UDP API. Use host 0.0.0.0 for the Flask app if you wish to send notifications from external sources, such as Home Assistant. For an example notifier service for Home Assistant:

```
notify:
  - name: "VR XS Overlay"
    platform: rest
    resource: http://yourhostname.local:64209/vr_notify
    method: POST
    title_param_name: title
```

Combine this with something like @LAB02-Research/HASS.Agent in order to detect if `SteamVR.exe` is running and you can selectively target destinations for a notification, so that when you're in VR it'll only send to XS Overlay, and vice versa.