function archiveMessage(clicked) {
    var archiveId = $(clicked).parent().attr("id");
    console.log(archiveId)
    $.ajax({
        type: "POST",
        url: "/archive-message",
        data:JSON.stringify({"archiveId": archiveId}),
        contentType:"application/json",
        datatype:"json",
        success: function(result) {
            alert(result.msg);
            $("#" + archiveId).remove();
        },
        error: function(_, error){
            console.error(error);
        }
    })
 };

function postMessage() {
    var newMessage = $("#newMessage").val();
    console.log($("#newMessage"))
    console.log(newMessage);
    var alter = $("#poster").children("option:selected").val();
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
                "From " + alter + " at " + datetime + ":\<br\/\>" +
                newMessage + 
                "\n\<form id=\"{{message['message'].id}}\"\>\n\<input type='hidden' value=\"{{message['message'].id}}\" name=\"message\"\>\n\<input type=\"button\" value=\"Archive Message\" class=\"archiveMessage\"\>\n\<\/form\>"
            );
        },
        error: function(_, error){
            console.error(error);
        }
    });
 }