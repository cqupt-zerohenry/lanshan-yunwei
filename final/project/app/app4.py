# 产生验证码图片

from io import BytesIO
import random
import string
from PIL import Image, ImageFont, ImageDraw, ImageFilter

import psutil
from flask import (
    Flask,
    render_template,
    request,
    json,
    redirect,
    url_for,
    jsonify,
    session,
    make_response,
    flash,
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)

app = Flask(__name__, template_folder="temp1", static_folder="static1")
app.secret_key = "T"
login_manager = LoginManager(app)


# 用户
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# 验证码
@app.route("/imgCode")
def imgCode():
    return imageCode().getImgCode()


class imageCode:
    """
    验证码处理
    """

    def rndColor(self):
        """随机颜色"""
        return (
            random.randint(32, 127),
            random.randint(32, 127),
            random.randint(32, 127),
        )

    def geneText(self):
        """生成4位验证码"""
        return "".join(
            random.sample(string.ascii_letters + string.digits, 4)
        )  # ascii_letters是生成所有字母 digits是生成所有数字0-9

    def drawLines(self, draw, num, width, height):
        """划线"""
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill="black", width=1)

    def getVerifyCode(self):
        """生成验证码图形"""
        code = self.geneText()
        # 图片大小120×50
        width, height = 120, 50
        # 新图片对象
        im = Image.new("RGB", (width, height), "white")
        # 字体
        font = ImageFont.truetype("static1/static/fonts/Arial.ttf", size=40)
        # draw对象
        draw = ImageDraw.Draw(im)
        # 绘制字符串
        for item in range(4):
            draw.text(
                (5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                text=code[item],
                fill=self.rndColor(),
                font=font,
            )
        # 划线
        self.drawLines(draw, 2, width, height)
        return im, code

    def getImgCode(self):
        image, code = self.getVerifyCode()
        # 图片以二进制形式写入
        buf = BytesIO()
        image.save(buf, "jpeg")
        buf_str = buf.getvalue()
        # 把buf_str作为response返回前端，并设置首部字段
        response = make_response(buf_str)
        response.headers["Content-Type"] = "image/gif"
        # 将验证码字符串储存在session中
        session["imageCode"] = code
        return response


# 进入登录页面
@app.route("/")
def login():
    return render_template("login.html")


# 登录页面验证后并跳转到index页面
@app.route("/vaildate", methods=["POST"])
def register():
    print(request.method)
    if request.method == "POST":
        import pymysql

        # 连接数据库
        # Don't use hard code password
        db = pymysql.connect(
            host="db",
            port=3306,
            user="root",
            password="root",
            db="mydb",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        # 获取游标
        cursor = db.cursor()
        # 进行查询命令
        select_sql = """select * from users where user=%s and pwd=%s"""

        # Don't store plaintext password
        username = request.form["userName"]
        password = request.form["password"]
        captcha = request.form.get("captcha").lower()
        print(username)
        print(password)
        cursor.execute(select_sql, (username, password))
        # 用fetchall的参数提取数据表中的值
        data = cursor.fetchall()
        if len(data) != 0 and captcha == session["imageCode"].lower():
            flag = True
        else:
            flag = False
        print(flag)
        if flag:
            for row in data:
                user_id = row["id"]  # 使用字段名获取 ID
                # 在这里可以使用 user_id 进行处理
                print("User ID:", user_id)
            user = User(user_id)
            login_user(user)
            return redirect(url_for("index"))
        else:
            if captcha == session["imageCode"].lower():
                # flash('账号或密码错误', "1")
                return render_template("login.html", error="账号或密码错误")
            else:
                # return jsonify({'code': -1, 'msg': '图片验证码错误'},render_template("login.html"))
                # flash('验证码错误',"2")
                return render_template("login.html", error="验证码错误")


def get_disk_io():
    # 获取磁盘 I/O 信息
    disk_io_stats = psutil.disk_io_counters()
    disk_io_info = {
        "读取次数": disk_io_stats.read_count,
        "写入次数": disk_io_stats.write_count,
        "读取字节数": disk_io_stats.read_bytes,
        "写入字节数": disk_io_stats.write_bytes,
        "读取时间": disk_io_stats.read_time,
        "写入时间": disk_io_stats.write_time,
    }

    return disk_io_info


def get_system_info():
    # 获取系统信息
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    cpu_cores = psutil.cpu_count(logical=False)
    memory = psutil.virtual_memory()
    network_stats = psutil.net_io_counters()
    disk_stats = psutil.disk_partitions(all=True)

    system_info = {
        "CPU使用率": f"{cpu_percent}%",
        "CPU频率": f"{cpu_freq.current:.2f} MHz" if cpu_freq is not None else "N/A",
        "CPU核心数": f"{cpu_cores} 核",
        "总内存": f"{memory.total / (1024 ** 3):.2f} GB",
        "已用内存": f"{memory.used / (1024 ** 3):.2f} GB",
        "内存使用百分比": f"{memory.percent}%",
        "发送字节数": f"{network_stats.bytes_sent / (1024 ** 2):.2f} MB",
        "接收字节数": f"{network_stats.bytes_recv / (1024 ** 2):.2f} MB",
        "磁盘使用": {
            partition.device: f"{psutil.disk_usage(partition.mountpoint).percent}%"
            for partition in disk_stats
        },
        "磁盘I/O信息": get_disk_io(),
    }

    return system_info


# 数据接口,统一返回
@app.route("/metrics", methods=["GET"])
@login_required
def get_metrics():
    return jsonify(get_system_info())


@app.route("/index")
@login_required
def index():
    return render_template("index.html")


@app.route("/login_out")
@login_required
def login_out():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
