$(function() {
    page = $('header').attr("id");
    $("#" + page).removeAttr("id");
    $.ajax({
        url: '/header',
        dataType: 'html',
        success: function(data) {
            $('header').html(data);
            $("#" + page).addClass("current");
        },
        error: function(_, error){
            console.error(error);
        }
    });
    $.ajax({
        url: '/footer',
        dataType: 'html',
        success: function(data) {
            $('footer').html(data);
            $("#" + page).addClass("current");
            $("#" + page).removeAttr("href");
        },
        error: function(_, error){
            console.error(error);
        }
    });
});