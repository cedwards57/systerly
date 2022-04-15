$(function() {
    jQuery.ajax({
        url: 'header.html',
        dataType: 'html',
        success: function(data) {
            $('header').html(data);
        },
        error: function(_, error){
            alert('Error loading header');
            console.error(error);
        }
    });
    jQuery.ajax({
        url: 'footer.html',
        dataType: 'html',
        success: function(data) {
            $('footer').html(data);
        },
        error: function(_, error){
            alert('Error loading footer');
            console.error(error);
        }
    });
});