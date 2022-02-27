$(document).ready(function () {
    listing();
});

function listing() {
    let email = $("#email").text();
    let mbti = $("#mbti").text();
    console.log(email, mbti);
    $.ajax({
        type: "POST",
        url: "/celeb",
        data: { mbti: mbti },
        success: function (response) {
            let list = response["msg"];
            for (let i = 0; i < list.length; i++) {
                let each = list[i];
                $("#append").append(each);
            }
        },
    });
}

function logout() {
    window.location.assign("http://localhost:5000/logout");
}
