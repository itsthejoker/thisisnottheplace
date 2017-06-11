import requests

from addict import Dict


api = Dict()

api.base = 'http://pixelcanvas.io'
api.pixel = '/api/pixel'
api.online = '/api/online'
api.timesync = '/api/timesync'
api.bigchunk = '/api/bigchunk/{}'
api.me = '/api/me'  # needs predetermined valid fingerprint as arg

# /api/ws is a GET call that seems to happen randomly (<5min) that places a __cfduid cookie each time
# it's called with a seemingly random UID string. It doesn't look like the __cfduid cookie is actually
# getting used for anything, as deleting the cookie as soon as it's placed does not have an effect on
# the running of the application.
api.ws = '/api/ws'

# General API notes:
#
# The ReCaptcha service does run, but does not seem to call consistently. If there are too many
# questionable calls, then the API returns a 422 error requesting a token. To the best of our current
# understanding, that token is generated client-side with materials already available. In testing, the
# token was requested twice before ReCaptcha was called, and we have not had a request for a token since.
# All normal placement API calls take place with a null token.
#
# The assignment of the token happens on line 2687 of the prettified client JS file:
# r = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : null
# Normal traffic does not show anything that appears to be token-related.
#
# The fingerprint must be passed in each call, but is independent of the IP address being called from,
# as different fingerprints on the same network will still trigger the same cooldown. This is possibly
# related to the token generation.

config = Dict()

config.fingerprint = '9b2fc8a7efd7d2e71314e8d6b54d74bc'
# config.token = '03AOPBWq8YFIAgVezbrEnzEtxgpYLKXthXVlvrNdS-SqxTq88goUA4IFAuLq6z96eMObLjvmKwefYexcjVK3qSP-kWtq2IfspFOzZRfX70fSYC7351cDxrd7iM5-LPfLbOrGyOwG7eL7yMc_vQ07l-N2cp1YnesAcvjQKZPKuFqQjTFeXkuQfUOrNf954vB2xKv7838UV4L7yZx0bahzQF6Cp_Go8ATcCzoee12189u0X_ycOhEUmc_r6f2v9laTZenghYaka_eLPyneXE4r2-_JLAw2kyE3KnwzVZfgnpPZ11fuXoI7pWjUgQtsnJMDiKu-U3ZRRXTMjtTr9RPIpLkpSbQleS6kgLpecbanI_XmGhJ0igDj2wqclGGJYWcfEOehylDuns_8kXAaBgua0zDi5D-UE-aO7cfQ'
config.token = None
config.api = api

def place_pixel(x, y, color, config=config):
    """
    Send a POST request to pixelcanvas at specified coordinates to place a pixel.

    :param x: integer; the x coordinate on the canvas
    :param y: integer; the y coordinate on the canvas
    :param color: integer; 0-15 with each color being a number
    :param config: config dict object
    :return: True if successful, false if not
    """
    data = {
        'x': x,
        'y': y,
        'color': color,
        'fingerprint': config.fingerprint,
        'token': config.token
    }

    result = requests.post(config.api.base + config.api.pixel, json=data)

    if int(result.status_code) == 200:
        return True
    elif int(result.status_code) == 422:
        return "Token Requested"
    return False

