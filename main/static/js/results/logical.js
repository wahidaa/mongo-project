function myFunction() {
    document.getElementById("demo").innerHTML = `<label class="label control-label">skip</label>
<div class="input-group">
<span class="input-group-addon"></span>
<input type="text" class="form-control" name="skip" value = "" placeholder="skip number" pattern='(^$|([0-9]+))'>
</div>
<label class="label control-label">limit</label>
<div class="input-group">
<span class="input-group-addon"></span>
<input type="text" class="form-control" name="limit" value = "" placeholder="limit number" pattern='(^$|([0-9]+))'>
</div>
<label class="label control-label">sort</label>
<div class="input-group">
<span class="input-group-addon"></span>
<input type="text" class="form-control" name="field" value = "" placeholder='field' pattern='(^$|([a-zA-Z0-9._%+-]+))'>
<input type="text" class="form-control" name="order" value = "" placeholder='ASCENDING/DESCENDING' pattern='(^$|(([1]+)|([-1]+)))'>
</div>
`;
  }
function updateText(type) { 
 var id = type;
 document.getElementById('txt').value = document.getElementById(type).value;
}

function manage(txt){
var input = document.getElementById("txt").value;
var input_regex = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}(([$and]+)|([$nor]+)|([$or]+))(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\[(\s*){0,20}(((\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}\$([a-z]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}((\s*){0,20}\[(\s*){0,20}(\s*){0,20}((\s*){0,20}(?:(?=([0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}")(\s*){0,20},(\s*){0,20})*((\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})){1}(\s*){0,20}\](\s*){0,20}|(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"))(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}|\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})(\s*){0,20}\}(\s*){0,20}),(\s*){0,20})*(((\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}\$([a-z]+)(\s*){0,20}"(\s*){0,20}:((\s*){0,20}\[(\s*){0,20}((\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}),(\s*){0,20})*((\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})){1}\]|(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}))(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}|(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})(\s*){0,20}\}(\s*){0,20})){1}(\s*){0,20}\](\s*){0,20}\}(\s*){0,20}/g;
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