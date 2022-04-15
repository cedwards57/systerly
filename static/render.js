$(function() {
    jQuery.ajax({
        url: '/static/header.html',
        dataType: 'html',
        success: function(data) {
            $('header').html(data);
        },
        error: function(_, error){
            console.error(error);
        }
    });
    jQuery.ajax({
        url: '/static/footer.html',
        dataType: 'html',
        success: function(data) {
            $('footer').html(data);
        },
        error: function(_, error){
            console.error(error);
        }
    });
});