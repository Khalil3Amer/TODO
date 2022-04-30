$('.is_completed').click(function() {
    $.ajax({
        type: 'GET',
        url: 'update_status/' + this.id + '/' + this.checked,
        success: function(response) {
            if (response['valid']) {
                alert("Task Updated");
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
            }
        },
        error: function(response) {
            console.log(response)
        }
    });
});

function reload_screen() {

}
