
function manage(txt){
    var input1 = document.getElementById("txt1").value;
    var input_regex1 = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([$regex]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}"(\s*){0,20}(.{1,50})(\s*){0,20}"(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}/g;
    var input2 = document.getElementById("txt2").value;
    var input_regex2 = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([$set]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)(\s*){0,20}|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}/g
    var result1 = input_regex1.test(input1);
    var result2 = input_regex2.test(input2);
    var bt1 = document.getElementById('btSubmit1');
    
    if (result1 || result2) {    
        
        bt1.disabled = false;
        console.log("match");
    } 
    else {
        bt1.disabled = true;

    }
    
    }
        
      