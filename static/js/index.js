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
    newMessage = newMessage.replaceAll("\n","\<br\/\>")
    var alter = $("#poster").children("option:selected").val();
    let currentDate = new Date();
    var datetime = ("\<span class=\"fas fa-calendar\" aria-label=\"posted on\"\>\<\/span\>&nbsp;" + (currentDate.getHours() + 24) % 12 || 12) + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds() + "&nbsp;&nbsp;\<span class=\"far fa-clock\" aria-label=\"posted at\"\>\<\/span\>&nbsp;" + (currentDate.getMonth()+1) + "/" + currentDate.getDate() + "/" + currentDate.getFullYear();
    if (alter != null) {
        $.ajax({
            type: "POST",
            url: "/post-message",
            data:JSON.stringify({"newMessage": newMessage, "alter": alter}),
            contentType:"application/json",
            datatype:"json",
            success: function(result) {
                alert(result.msg);
                $("#messages").prepend(
                    "\<div class=\"msg\"\>\<form id=\"" + result.msgId + "\"\>\<strong\>\<span class=\"" + result.alterId + "\" style=\"color:" + result.alterColor + "\"\>" + alter + "\<\/span\>\<\/strong\>\<br\/\>" + datetime + "\<br\/\>" +
                    newMessage + 
                    "\<br\/\>\<input type=\"button\" value=\"Archive Message\" onclick=\"archiveMessage(this)\" \>\n\<\/form\>\<\/div\>"
                );
            },
            error: function(_, error){
                console.error(error);
            }
        });
    } else {
        alert("You must have an alter selected to post a message. Head to the Profile page to add one!")
    }
 }

function setColor() {
    var alterId = $("#colorFor").children("option:selected").val();
    var newColor = $("#colorpicker").attr("data-current-color");
    $.ajax({
        type: "POST",
        url: "/set-color",
        data:JSON.stringify({"alterId": alterId, "newColor": newColor}),
        contentType:"application/json",
        datatype:"json",
        success: function(result) {
            alert(result.msg);
            $("." + alterId).css("color", newColor);
        },
        error: function(_, error){
            console.error(error);
        }
    })
 };