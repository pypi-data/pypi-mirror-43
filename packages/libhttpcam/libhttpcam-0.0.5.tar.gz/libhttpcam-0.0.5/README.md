# Web Cam Access via HTTP REST-API

A library that unified acess to various web cams with integrated HTTP servers.

### Installation
    pip3 install libhttpcam

### Usage
Use `createCam` to create a camera instance.

    from libhttpcam import createCam

    model = 'foscam'
    ip = '10.0.0.30'
    cam, port = createCam('foscam', ip)  # use model's default port

Then set credentials for the camera:

    user = 'me'
    password = 'youllneverguess'
    cam.set_credentials(user, password)
