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
                    alert("login success");
                    $.ajax({
                        type: "POST",
                        url: "/loginsuccess",
                        data: { email: inputemail },
                        success: window.location.assign(
                            "http://localhost:5003/user"
                        ),
                    });
                } else {
                    alert("wrong password");
                }
            } else {
                alert("user does not exist");
            }
        },
    });
}

function register() {
<<<<<<< HEAD
    window.location.assign("http://localhost:7000/registration");
=======
    window.location.assign("http://localhost:5003/registration");
>>>>>>> 3e487abcec3c794aec99d2099c0a41916afb9882
}

function forgotpassword() {
    alert("죄송해요 현재는 이 서비스는 불가합니다");
}
