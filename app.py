from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from datetime import timedelta

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

client = MongoClient('mongodb+srv://test:sparta@cluster0.citdv.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta

app = Flask(__name__)

# 세션을 사용하려면 시크릿 키가 필요하다 (기본세팅)
app.secret_key = "hello"
# 세션이 유저의 브라우저에 저장되는 시간, 이후 자동 로그아웃이 된다 
app.permanent_session_lifetime = timedelta(minutes=30)

# 현재 기본 페이지를 로그인 페이지로 설정함 
# 이후 따로 로그인전 앱을 소개하는 페이지로 대체하고자함 
@app.route("/")
def introduction():
    if "user" in session:
        username = session["user"]
        userdb = db.login.find_one({"email": username})
        usermbti = userdb["mbti"]
        return render_template("user.html", user=username, mbti=usermbti)
    if "register" in session and "register_mbti" in session:
        mbti = session["register_mbti"]
        username = session["register"]
        return render_template("user.html", user=username, mbti=mbti)
    return render_template("login.html")

# 로그인 페이지 
@app.route("/login")
def login():
    if "user" in session:
        username = session["user"]
        userdb = db.login.find_one({"email": username})
        usermbti = userdb["mbti"]
        return render_template("user.html", user=username, mbti=usermbti)
    if "register" in session and "register_mbti" in session:
        mbti = session["register_mbti"]
        username = session["register"]
        return render_template("user.html", user=username, mbti=mbti)
    return render_template("login.html")

# 로그인시 데이터베이스에서 확인하는 기능 
@app.route("/authentication", methods=["POST"])
def authentication():
    inputemail = request.form["email"]
    inputuser = db.login.find_one({"email": inputemail})
    if inputuser is not None:
        inputpassword = inputuser["password"]
        return jsonify({'msg': inputpassword})
    if inputuser is None:
        return jsonify({'msg': "not"})

# 로그인 성공시 세션을 만들고, 이 세션 키 (user)로 홈페이지 (/user) 로 접속가능하게 한다 
@app.route("/loginsuccess", methods=["POST"])
def loginsuccess():
    user = request.form["email"]
    session["user"] = user
    return redirect(url_for("user"))


# 회원가입 페이지 
@app.route("/registration")
def registration():
    if "user" in session:
        username = session["user"]
        userdb = db.login.find_one({"email": username})
        usermbti = userdb["mbti"]
        return render_template("user.html", user=username, mbti=usermbti)
    if "register" in session and "register_mbti" in session:
        mbti = session["register_mbti"]
        username = session["register"]
        return render_template("user.html", user=username, mbti=mbti)
    return render_template("register.html")

# 회원가입 기능 (1차)
@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    doc={
        "name": name,
        "email": email,
        "password": password,
        "mbti": ""
    }
    db.login.insert_one(doc)
    session["register"] = email
    return jsonify({'msg': "이제 MBTI를 선택해 주세요!"})

# 2차 회원가입 MBTI 선택할수 있는 페이지 
@app.route("/registration/mbti")
def mbti():
    if "register" in session and "register_mbti" not in session:
        return render_template("mbti.html")
    if "register" in session and "register_mbti" in session:
        mbti = session["register_mbti"]
        username = session["register"]
        return render_template("user.html", user=username, mbti=mbti)
    if "user" in session:
        username = session["user"]
        userdb = db.login.find_one({"email": username})
        usermbti = userdb["mbti"]
        return render_template("user.html", user=username, mbti=usermbti)
    else:
        return redirect(url_for("registration"))

# 2차 회원가입 페이지에서 MBTI를 정하면 데이터베이스에 저장되는 기능 
# 바로 홈페이지 (/user)로 이동하게 된다 (즉, 새로 로그인 안해도 된다) 
@app.route("/postmbti", methods=["POST"])
def postmbti():
    session["register_mbti"] = request.form["mbti"]
    register_mbti = session["register_mbti"]
    register_user = session["register"]
    mbti_list = register_mbti.lower()
    # print(mbti_list, register_mbti) mbti 대소문자 구분 (그래프용)
    db.login.update_one({"email": register_user},{'$set':{"mbti": register_mbti }})
    db.prac.insert_one({"mbti":mbti_list})
    return redirect(url_for("user"))



# 홈페이지: 로그인 또는 회원가입을 완료했을때만 접속이 가능하다 
@app.route("/user")
def user():
    if "register" in session and "register_mbti" in session:
        mbti = session["register_mbti"]
        username = session["register"]
        return render_template("user.html", user=username, mbti=mbti)
    if "user" in session:
        username = session["user"]
        userdb = db.login.find_one({"email": username})
        usermbti = userdb["mbti"]
        return render_template("user.html", user=username, mbti=usermbti)
    else:
        return redirect(url_for("login"))

# 로그아웃 기능: 모든 세션을 지운다 
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("register", None)
    session.pop("register_mbti", None)
    return redirect(url_for("login"))


# 여기서부터가 웹스크레핑 

@app.route("/celeb", methods=["POST"])
def celeb():
    mbti = request.form["mbti"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get("https://m.blog.naver.com/007bibo/221975539649", headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # ISTJ 타입 연예인
    if mbti == "ISTJ":
        celeb_istj = soup.select_one('#SE-48d2e943-7475-11ec-90a3-911d5c8ea861')
        celeb_istj_text = celeb_istj.text
        list_istj = celeb_istj_text.split(",")
        print(list_istj)
        return jsonify({'msg': list_istj})

    # ISFJ 타입 연예인
    if mbti == "ISFJ":
        celeb_isfj = soup.select_one('#SE-48d35e87-7475-11ec-90a3-83613d4eb033')
        celeb_isfj_text = celeb_isfj.text
        list_isfj = celeb_isfj_text.split(",")
        print(list_isfj)
        return jsonify({'msg': list_isfj})

    # ISTP 타입 연예인
    if mbti == "ISTP":
        celeb_istp = soup.select_one('#SE-48d3f9d9-7475-11ec-90a3-6b8cd4917d45')
        celeb_istp_text = celeb_istp.text
        list_istp = celeb_istp_text.split(",")
        print(list_istp)
        return jsonify({'msg': list_istp})

    # ISFP 타입 연예인
    if mbti == "ISFP":
        celeb_isfp = soup.select_one('#SE-48d46f1c-7475-11ec-90a3-5f31001f9280')
        celeb_isfp_text = celeb_isfp.text
        list_isfp = celeb_isfp_text.split(",")
        print(list_isfp)
        return jsonify({'msg': list_isfp})

    # INFJ 타입 연예인
    if mbti == "INFJ":
        celeb_infj = soup.select_one('#SE-48d580b5-7475-11ec-90a3-333dfc1a46df')
        celeb_infj_text = celeb_infj.text
        list_infj = celeb_infj_text.split(",")
        print(list_infj)
        return jsonify({'msg': list_infj})

    # INTJ 타입 연예인
    if mbti == "INTJ":
        celeb_intj = soup.select_one('#SE-48d580b5-7475-11ec-90a3-333dfc1a46df')
        celeb_intj_text = celeb_intj.text
        list_intj = celeb_intj_text.split(",")
        print(list_intj)
        return jsonify({'msg': list_intj})

    # INFP 타입 연예인
    if mbti == "INFP":
        celeb_infp = soup.select_one('#SE-48d5f5fa-7475-11ec-90a3-75a72af945fa')
        celeb_infp_text = celeb_infp.text
        list_infp = celeb_infp_text.split(",")
        print(list_infp)
        return jsonify({'msg': list_infp})

    # INTP 타입 연예인
    if mbti == "INTP":
        celeb_intp = soup.select_one('#SE-48d6924f-7475-11ec-90a3-1703a6b61c68')
        celeb_intp_text = celeb_intp.text
        list_intp = celeb_intp_text.split(",")
        print(list_intp)
        return jsonify({'msg': list_intp})

    # ESTP 타입 연예인
    if mbti == "ESTP":
        celeb_estp = soup.select_one('#SE-48d70791-7475-11ec-90a3-5ddbd88dcabc')
        celeb_estp_text = celeb_estp.text
        list_estp = celeb_estp_text.split(",")
        print(list_estp)
        return jsonify({'msg': list_estp})

    # ESFP 타입 연예인
    if mbti == "ESFP":
        celeb_esfp = soup.select_one('#SE-48d77cd7-7475-11ec-90a3-c70a41ca485f')
        celeb_esfp_text = celeb_esfp.text
        list_esfp = celeb_esfp_text.split(",")
        print(list_esfp)
        return jsonify({'msg': list_esfp})

    # ESTJ 타입 연예인
    if mbti == "ESTJ":
        celeb_estj = soup.select_one('#SE-48d8192e-7475-11ec-90a3-330182f6b817')
        celeb_estj_text = celeb_estj.text
        list_estj = celeb_estj_text.split(",")
        print(list_estj)
        return jsonify({'msg': list_estj})

    # ESFJ 타입 연예인
    if mbti == "ESFJ":
        celeb_esfj = soup.select_one('#SE-48d88e70-7475-11ec-90a3-dbd71604fecf')
        celeb_esfj_text = celeb_esfj.text
        list_esfj = celeb_esfj_text.split(",")
        print(list_esfj)
        return jsonify({'msg': list_esfj})

    # ENFP 타입 연예인
    if mbti == "ENFP":
        celeb_enfp = soup.select_one('#SE-48d903b2-7475-11ec-90a3-ed76b7427339')
        celeb_enfp_text = celeb_enfp.text
        list_enfp = celeb_enfp_text.split(",")
        print(list_enfp)
        return jsonify({'msg': list_enfp})

    # ENTP 타입 연예인
    if mbti == "ENTP":
        celeb_entp = soup.select_one('#SE-48d9a006-7475-11ec-90a3-4d11aeb72e2e')
        celeb_entp_text = celeb_entp.text
        list_entp = celeb_entp_text.split(",")
        print(list_entp)
        return jsonify({'msg': list_entp})

    # ENFJ 타입 연예인
    if mbti == "ENFJ":
        celeb_enfj = soup.select_one('#SE-48da1548-7475-11ec-90a3-93c529204ec0')
        celeb_enfj_text = celeb_enfj.text
        list_enfj = celeb_enfj_text.split(",")
        print(list_enfj)
        return jsonify({'msg': list_enfj})

    # ENTJ 타입 연예인
    if mbti == "ENTJ":
        celeb_entj = soup.select_one('#SE-48dab09f-7475-11ec-90a3-cbd7e4a38792')
        celeb_entj_text = celeb_entj.text
        list_entj = celeb_entj_text.split(",")
        print(list_entj)
        return jsonify({'msg': list_entj})

# 그래프 페이지

@app.route('/graph')
def graph():
    if "user" in session:
        return render_template("graph.html")
    if "register" in session and "register_mbti" in session:
        return render_template("graph.html")
    return render_template("login.html")

@app.route("/mbtiList", methods=["GET"])
def user_get():
    user_list = list(db.prac.find({}, {'_id': False}))
    print(user_list)
    # print(user_list)
    return jsonify({'user_list': user_list})

# add_page 페이지

@app.route('/add_page')
def comingsooon():
    return render_template('add_page.html')


# 포트는 5000으로 설정함
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

