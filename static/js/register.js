function register() {
    let name = $("#name").val();
    let email = $("#email").val();
    let password = $("#password").val();
    let password_confirm = $("#password_confirm").val();
    if (email.includes("@") == true && password == password_confirm) {
        $.ajax({
            type: "POST",
            url: "/register",
            data: { name: name, email: email, password: password },
            success: function (response) {
                alert(`${response["msg"]}`);
                window.location.assign(
<<<<<<< HEAD
                    "http://localhost:7000/registration/mbti"
=======
                    "http://localhost:5003/registration/mbti"
>>>>>>> 3e487abcec3c794aec99d2099c0a41916afb9882
                );
            },
        });
    }
    if (email.includes("@") == false) {
        $(".email_text_msg").show();
        $(".email_placeholder").hide();
        $("#email").addClass("wrong_email");
        $("#email").addClass("shake");
    } else if (email.includes("@") == true) {
        $(".email_text_msg").hide();
        $(".email_placeholder").show();
        $("#email").removeClass("wrong_email");
        $("#email").removeClass("shake");
    }
    if (password !== password_confirm) {
        $(".password_text_msg").show();
        $(".password_placeholder").hide();
        $("#password_confirm").addClass("wrong_password");
        $("#password_confirm").addClass("shake");
    } else if (password == password_confirm) {
        $(".password_text_msg").hide();
        $(".password_placeholder").show();
        $("#password_confirm").removeClass("wrong_password");
        $("#password_confirm").removeClass("shake");
    }
}

function return_home() {
<<<<<<< HEAD
    window.location.assign("http://localhost:7000/login");
=======
    window.location.assign("http://localhost:5003/login");
>>>>>>> 3e487abcec3c794aec99d2099c0a41916afb9882
}
