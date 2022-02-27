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