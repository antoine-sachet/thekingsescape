from bottle import Bottle, template


app = Bottle()


@app.route('/')
@app.route('/play')
def play():
    return "play"


@app.route('/play/move/<start>')
def selectmove(start):
    return template('<b>Move: {{start}} -> ?</b>!',
                    start=start)


@app.route('/play/move/<start>/<end>')
def move(start, end):
    return template('<b>Move: {{start}} -> {{end}}</b>!',
                    start=start, end=end)
