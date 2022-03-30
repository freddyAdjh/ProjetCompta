$(document).ready(function(){
    $("#qte").keyup(function(){
        $.ajax({
            type:'POST',
            url:"{% url 'verify' %}",
            dataType:"json",
            data:$("#qte").val(),
            success:function(data){
                alert("ok")
            }
        })}
    })
})