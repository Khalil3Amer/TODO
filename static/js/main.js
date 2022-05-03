$('.is_completed').click(function() {
    $.ajax({
        type: 'GET',
        url: 'update_status/' + this.id + '/' + this.checked,
        success: function(response) {
            if (response['valid']) {
                alert("Task Updated");
                location.reload();
            }
        },
        error: function(response) {
            console.log(response)
        }
    });
});
$('.delete_task').click(function() {
    $.ajax({
        type: 'GET',
        url: 'delete_task/' + this.id,
        success: function(response) {
            if (response['valid']) {
                alert("Task Deleted");
                location.reload();
            }
        },
        error: function(response) {
            console.log(response)
        }
    });
});
$(document).ready(function() {
    // Run code
    $('.time-left').each(function(i, obj) {
        $current_div = $(this);
        var endTime = new Date($current_div.data('deadline'));
        endTime = (Date.parse(endTime) / 1000);
        var now = new Date();
        now = (Date.parse(now) / 1000);

        var timeLeft = endTime - now;

        var days = Math.floor(timeLeft / 86400);
        var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
        var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600)) / 60);
        var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

        if (hours < "10") { hours = "0" + hours; }
        if (minutes < "10") { minutes = "0" + minutes; }
        if (seconds < "10") { seconds = "0" + seconds; }
        $current_div.children('.days').html(days + "<span>Days</span>");
        $current_div.children('.hours').html(hours + "<span>Hours</span>");
        $current_div.children('.minutes').html(minutes + "<span>Minutes</span>");
        $current_div.children('.seconds').html(seconds + "<span>Seconds</span>");
    });

    setInterval(function() {
        $('.time-left').each(function(i, obj) {
            $current_div = $(this);
            var endTime = new Date($current_div.data('deadline'));
            endTime = (Date.parse(endTime) / 1000);
            var now = new Date();
            now = (Date.parse(now) / 1000);

            var timeLeft = endTime - now;

            var days = Math.floor(timeLeft / 86400);
            var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
            var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600)) / 60);
            var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

            if (hours < "10") { hours = "0" + hours; }
            if (minutes < "10") { minutes = "0" + minutes; }
            if (seconds < "10") { seconds = "0" + seconds; }
            $current_div.children('.days').html(days + "<span>Days</span>");
            $current_div.children('.hours').html(hours + "<span>Hours</span>");
            $current_div.children('.minutes').html(minutes + "<span>Minutes</span>");
            $current_div.children('.seconds').html(seconds + "<span>Seconds</span>");
        });
    }, 1000);


});

function makeTimer(div) {

}
