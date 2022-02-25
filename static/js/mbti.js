$(".first .flip-card:nth-child(1) .flip-card-back").click(function () {
    alert("INTJ를 고르셨군요");
    let mbti = "INTJ";
    post_mbti(mbti);
});

$(".first .flip-card:nth-child(2) .flip-card-back").click(function () {
    alert("INTP를 고르셨군요");
    let mbti = "INTP";
    post_mbti(mbti);
});

$(".first .flip-card:nth-child(3) .flip-card-back").click(function () {
    alert("ENTJ를 고르셨군요");
    let mbti = "ENTJ";
    post_mbti(mbti);
});

$(".first .flip-card:nth-child(4) .flip-card-back").click(function () {
    alert("ENTP를 고르셨군요");
    let mbti = "ENTP";
    post_mbti(mbti);
});

$(".second .flip-card:nth-child(1) .flip-card-back").click(function () {
    alert("INFJ를 고르셨군요");
    let mbti = "INFJ";
    post_mbti(mbti);
});

$(".second .flip-card:nth-child(2) .flip-card-back").click(function () {
    alert("INFP를 고르셨군요");
    let mbti = "INFP";
    post_mbti(mbti);
});

$(".second .flip-card:nth-child(3) .flip-card-back").click(function () {
    alert("ENFJ를 고르셨군요");
    let mbti = "ENFJ";
    post_mbti(mbti);
});

$(".second .flip-card:nth-child(4) .flip-card-back").click(function () {
    alert("ENFP를 고르셨군요");
    let mbti = "ENFP";
    post_mbti(mbti);
});

$(".third .flip-card:nth-child(1) .flip-card-back").click(function () {
    alert("ISTJ를 고르셨군요");
    let mbti = "ISTJ";
    post_mbti(mbti);
});

$(".third .flip-card:nth-child(2) .flip-card-back").click(function () {
    alert("ISFJ를 고르셨군요");
    let mbti = "ISFJ";
    post_mbti(mbti);
});

$(".third .flip-card:nth-child(3) .flip-card-back").click(function () {
    alert("ESTJ를 고르셨군요");
    let mbti = "ESTJ";
    post_mbti(mbti);
});

$(".third .flip-card:nth-child(4) .flip-card-back").click(function () {
    alert("ESFJ를 고르셨군요");
    let mbti = "ESFJ";
    post_mbti(mbti);
});

$(".fourth .flip-card:nth-child(1) .flip-card-back").click(function () {
    alert("ISTP를 고르셨군요");
    let mbti = "ISTP";
    post_mbti(mbti);
});

$(".fourth .flip-card:nth-child(2) .flip-card-back").click(function () {
    alert("ISFP를 고르셨군요");
    let mbti = "ISFP";
    post_mbti(mbti);
});

$(".fourth .flip-card:nth-child(3) .flip-card-back").click(function () {
    alert("ESTP를 고르셨군요");
    let mbti = "ESTP";
    post_mbti(mbti);
});

$(".fourth .flip-card:nth-child(4) .flip-card-back").click(function () {
    alert("ESFP를 고르셨군요");
    let mbti = "ESFP";
    post_mbti(mbti);
});

function post_mbti(mbti) {
    $.ajax({
        type: "POST",
        url: "/postmbti",
        data: { mbti: mbti },
        success: function (response) {
            alert(`환영합니다! 홈페이지로 이동합니다!`);
            window.location.assign("http://localhost:5000/user");
        },
    });
}
