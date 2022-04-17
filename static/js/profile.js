function saveAlter() {
   var newAlter = $("#newAlter").val()
   $.ajax({
       type: "POST",
       url: "/save-alter",
       data:JSON.stringify({"alterName": newAlter}),
       contentType:"application/json",
       datatype:"json",
       success: function(result) {
           alert(result.msg);
           $("#next-alter").append("<li>" + newAlter + "</li>");
           $("#rmAlter").append("\<option value=\"" + newAlter + "\" id=\"" + result.alter_id + "\"\>" + newAlter + "\<\/option\>");
       },
       error: function(_, error){
           console.error(error);
       }
   });
}

function removeAlter() {
    var rmAlter = $("#rmAlter").children("option:selected").attr("id");
    var rmAlterName = $("#rmAlter").children("option:selected").val();
    if(confirm("Are you sure you want to remove " + rmAlterName + " from your list? This will delete all of " + rmAlterName + "'s posts. This cannot be undone.")) {
        $.ajax({
            type: "POST",
            url: "/remove-alter",
            data:JSON.stringify({"alterId": rmAlter}),
            contentType:"application/json",
            datatype:"json",
            success: function(result) {
                alert(result.msg);
                $("#" + rmAlter + "x").remove();
                $("#" + rmAlter).remove();
            },
            error: function(_, error){
                console.error(error);
            }
        });
    }
 }