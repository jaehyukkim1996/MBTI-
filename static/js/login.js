function return_home() {
    window.location.reload();
}

function login() {
    let inputemail = $("#email").val();
    let inputpassword = $("#password").val();
    $.ajax({
        type: "POST",
        url: "/authentication",
        data: { email: inputemail },
        success: function (response) {
            let dbpassword = response["msg"];
            if (dbpassword !== "not") {
                if (inputpassword == dbpassword) {
                    alert("환영합니다!!");
                    $.ajax({
                        type: "POST",
                        url: "/loginsuccess",
                        data: { email: inputemail },
                        success: window.location.assign(
                            "http://localhost:5000/user"
                        ),
                    });
                } else {
                    alert("비밀번호가 틀립니다!");
                }
            } else {
                alert("이메일을 확인해 주세요!");
            }
        },
    });
}

function register() {
    window.location.assign("http://localhost:5000/registration");
}

function forgotpassword() {
    alert("죄송해요.. 이 서비스는 준비 중입니다..!");
}
