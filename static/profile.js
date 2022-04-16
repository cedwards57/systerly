function saveAlter() {
   var newAlter = $("#newalter").val()
   $.ajax({
       type: "POST",
       url: "/save-alter",
       data:JSON.stringify({"alterName": newAlter}),
       contentType:"application/json",
       datatype:"json",
       success: function(result) {
           alert(result.msg);
           $("#next-alter").append("<li>" + newAlter + "</li>");
       },
       error: function(_, error){
           console.error(error);
       }
   });
}