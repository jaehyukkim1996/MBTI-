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
        data: {mbti: mbti},
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

let isAboutOpen = false;

$(document).click(function (event) {
    if (
        event.target.id !== "about-us" &&
        event.target.tagName !== "A" &&
        event.target.tagName !== "SPAN"
    ) {
        $("#about-us-article").hide();
        $("#about-us").text("About 18조");
        $("#about-us").css({
            "background-color": "rgba(0, 136, 169, 1)",
            border: "none",
        });
        isAboutOpen = false;
    }
});

function handleAboutClick() {
    if (isAboutOpen) {
        $("#about-us-article").hide();
        $("#about-us").text("About 18조");
        $("#about-us").css({
            "background-color": "rgba(0, 136, 169, 1)",
            border: "none",
        });
        isAboutOpen = false;
    } else {
        $("#about-us-article").show();
        $("#about-us").text("닫기");
        $("#about-us").css({
            "background-color": "rgba(0, 136, 169, 0.8)",
            border: "2px solid whitesmoke",
        });
        isAboutOpen = true;
    }
}