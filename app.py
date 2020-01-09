from flask import Flask,request,Response,render_template
from cctv import CCTV
from servo import MyServo

app = Flask(__name__)

token = "zyg19960622"

cctv = CCTV(save_path='/Users/mike/Desktop/cctv/')
# cctv.start_record()
s0 = MyServo(18)
s1 = MyServo(23,default_postion=90)


@app.route('/video')
def index():
    return render_template('index.html')

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/stop')
def get_user():
    cctv.stop_record()
    return "Stopped"


@app.route('/reposition')
def servo_reposition():
    if request.args['token'] == token:
        servo_id = int(request.args['id'])
        angle = int(request.args['angle'])

        if servo_id == 0:
            print(0,'to',angle)
            s0.repostion(angle)

        elif servo_id == 1:
            s1.repostion(angle)
            print(1,"to",angle)

        return "OK"
    else:
        return "Wrong Token"


def gen(cctv):
    while True:
        frame = cctv.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    if request.args['token'] == token:
        return Response(gen(cctv), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Wrong Token"


if __name__ == '__main__':
    app.run(host='0.0.0.0')

