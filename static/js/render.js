$(function() {
    $.ajax({
        url: '/static/html/header.html',
        dataType: 'html',
        success: function(data) {
            $('header').html(data);
        },
        error: function(_, error){
            console.error(error);
        }
    });
    $.ajax({
        url: '/static/html/footer.html',
        dataType: 'html',
        success: function(data) {
            $('footer').html(data);
        },
        error: function(_, error){
            console.error(error);
        }
    });
});