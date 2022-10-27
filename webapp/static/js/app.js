// app.js

function init_schedule_page() {
    $(".js-move-up").on("click", (e) => {
        const index = $(e.currentTarget).data("index");
        $("#index").val(index);
        $("#act").val("move-up");
        document.getElementById("actform").submit();
    });

    $(".js-move-down").on("click", (e) => {
        const index = $(e.currentTarget).data("index");
        $("#index").val(index);
        $("#act").val("move-down");
        document.getElementById("actform").submit();
    });

    $(".js-delete").on("click", (e) => {
        const index = $(e.currentTarget).data("index");
        $("#index").val(index);
        $("#act").val("delete");
        document.getElementById("actform").submit();
    });

    $(".js-activate").on("click", (e) => {
        const index = $(e.currentTarget).data("index");
        $("#index").val(index);
        $("#act").val("activate");
        document.getElementById("actform").submit();
    });
}

function show_ss() {
    $(".js-loading-ss").hide();
    $(".js-ss-img").show();
}

function init_status_page(screenshoturl) {
    $(".js-show-ss-btn").on("click", () => {
        $(".js-show-ss-btn").hide();
        $(".js-loading-ss").show();
        $(".js-ss-img").attr("src", screenshoturl)
    });
}
