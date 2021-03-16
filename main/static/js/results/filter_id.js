function manage(txt){
    var input = document.getElementById("txt").value;
    var input_regex = /.{0,20}/g;
    var result = input_regex.test(input);
    var bt1 = document.getElementById('btSubmit1');
    
    if (result) {    
        bt1.disabled = false;
        document.getElementById("txt").style.color = "green";
        console.log("match");
    } else {
        bt1.disabled = true;
        document.getElementById("txt").style.color = "red";
        console.log("not match");
    }
    
    }

    $(".current").click(function()
{
    link=$(this).val()
    action=$("#exampleModal3").find('form ').attr('action',link);
    console.log(db)
    });

$(".current7").click(function()
{
    link=$(this).val()
    action=$("#exampleModal7").find('form ').attr('action',link);
    console.log(db)
    });