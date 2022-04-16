$(".archiveMessage").click(function() {
    var archiveId = $(this).parent().attr("id")
    $.ajax({
        type: "POST",
        url: "/archive-message",
        data:JSON.stringify({"archiveId": archiveId}),
        contentType:"application/json",
        datatype:"json",
        success: function(result) {
            alert(result.msg);
            $(this).parent().append("<br/>Archived");
        },
        error: function(_, error){
            console.error(error);
        }
    });
 });

 function postMessage() {
    var newMessage = $("#newMessage").val()
    var alter = $("#poster").val()
    let currentDate = new Date();
    var datetime = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds() + "  " + currentDate.getMonth() + "/" + currentDate.getDate() + "/" + currentDate.getFullYear();
    $.ajax({
        type: "POST",
        url: "/post-message",
        data:JSON.stringify({"newMessage": newMessage, "alter": alter}),
        contentType:"application/json",
        datatype:"json",
        success: function(result) {
            alert(result.msg);
            $("#messages").prepend(
                "From " + poster + " at " + datetime + ":\n" + newMessage + 
                "\n\<form id=\"{{message['message'].id}}\"\>\n\<input type='hidden' value=\"{{message['message'].id}}\" name=\"message\"\>\n\<input type=\"button\" value=\"Archive Message\" class=\"archiveMessage\"\>\n\<\/form\>"
            );
        },
        error: function(_, error){
            console.error(error);
        }
    });
 }