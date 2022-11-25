// app.js

let shutdown_url = "";
let reboot_url = ""

function init_schedule_page() {
    $(".js-move-up").on("click", (e) => {
        const index = $(e.currentTarget).data("index");
        post_action("/item_up", {"index": index});
    });

    $(".js-move-down").on("click", (e) => {
        const index = $(e.currentTarget).data("index");
        post_action("/item_down", {"index": index});
    });

    $(".js-delete").on("click", (e) => {
        const index = $(e.currentTarget).data("index");
        post_action("/item_delete", {"index": index});
    });

    $(".js-activate").on("click", (e) => {
        const index = $(e.currentTarget).data("index");
        post_simple("/item_activate", {"index": index});
    });
}

function show_ss() {
    $(".js-loading-ss").hide();
    $(".js-ss-img").show();
}

function init_status_page(screenshoturl, rebooturl, shutdownurl) {
    reboot_url = rebooturl;
    shutdown_url = shutdownurl;

    $(".js-show-ss-btn").on("click", () => {
        $(".js-show-ss-btn").hide();
        $(".js-loading-ss").show();
        $(".js-ss-img").attr("src", screenshoturl)
    });

    $(".js-reboot-btn").on("click", () => {
        $(".js-reboot-btn").hide();
        $(".js-shutdown-btn").hide();

        setTimeout(() => { $(".js-confirm-reboot-btn").show(); }, 1000);
        setTimeout(() => { $(".js-confirm-reboot-btn").hide(); }, 10000);
    });

    $(".js-shutdown-btn").on("click", () => {
        $(".js-reboot-btn").hide();
        $(".js-shutdown-btn").hide();

        setTimeout(() => { $(".js-confirm-shutdown-btn").show(); }, 1000);
        setTimeout(() => { $(".js-confirm-shutdown-btn").hide(); }, 10000);
    });

    $(".js-confirm-shutdown-btn").on("click", handleShutdown);
    $(".js-confirm-reboot-btn").on("click", handleReboot);
}

function handleReboot() {
    $(".js-confirm-reboot-btn").hide();

    post_simple(reboot_url, {});
}

function handleShutdown() {
    $(".js-confirm-shutdown-btn").hide();

    post_simple(shutdown_url, {});
}

function post_simple(url, data) {
	fetch(url, {
            method:"POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
	    }) 
        .then(result => {
            // Do nothing
        }).catch(err => {
	        // if any error occured, then catch it here
	        console.error(err);
	    });
}

function post_action(url, data) {
	fetch(url, {
            method:"POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
	    }) 
        .then(result => {
            return result.text();
        })
        .then(html => {
            let newbody = $(html);
            let newpartial = newbody.find(".js-partial-update");
            let partial = $(".js-partial-update");
            partial.empty();
            partial.append(newpartial);
            init_schedule_page();
	    }).catch(err => {
	        // if any error occured, then catch it here
	        console.error(err);
	    });
}