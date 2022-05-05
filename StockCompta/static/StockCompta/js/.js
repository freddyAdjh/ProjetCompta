$(document).ready(function(){
    var qte;
    $("#qte").keyup(function(){
        qte = $("#qte").val()
        $.ajax({
            type:"POST",
            url:"{% url 'verify' %}",
            dataType:"json",
            data:qte,
            success:function(data){
                console.log(data.content)
            }
        })
    })
})