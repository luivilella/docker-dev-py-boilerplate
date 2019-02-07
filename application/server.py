import bottle


@bottle.route('/')
def index():
    return 'Running inside docker :)'


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080)
