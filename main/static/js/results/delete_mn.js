function manage(txt){
    var input = document.getElementById("txt").value;
    var input_regex = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([$regex]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}"(\s*){0,20}(.{1,50})(\s*){0,20}"(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}/g;
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