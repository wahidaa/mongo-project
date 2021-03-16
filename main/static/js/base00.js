$(function () {
    $('[data-toggle="tooltip"]').tooltip()
    })


$(".current").click(function()
{
    link=$(this).val()
    db = $(this).attr('name')
    action=$("#exampleModal2").find('form ').attr('action',link);
    h5 = $("#exampleModal2 ").find('#exampleModalLabel').text("Add collection to "+ db);
    });



$(".current2").click(function()
{
    link=$(this).val()
    action=$("#exampleModal4").find('form ').attr('action',link);
    });

$(".current0").click(function()
{
link=$(this).val()
action=$("#exampleModal6").find('form ').attr('action',link);
}); 

$(".current6").click(function()
{
link=$(this).val()
action=$("#exampleModal6").find('form ').attr('action',link);
});
//aggregation

//update text when choose option      
function updateText(select_name,input_name) { 
    document.getElementById(input_name).value = document.getElementById(select_name).value;
    }
    function deletes() {
      var select = document.getElementById('todolist_aggregate');
      select.removeChild(select.lastChild);
    }
    
    function manage(txt,input_name){
      var input = document.getElementById(input_name).value;
      var input_regex = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}\$([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}.{1,100}(\s*){0,20}\}(\s*){0,20}/g;
      var result = input_regex.test(input);
      var bt1 = document.getElementById('btsubmit_aggregate');
      
      if (result) {    
          bt1.disabled = false;
          console.log("match");
      } else {
          bt1.disabled = true;
          console.log("not match");
      }
      
      }  
    
    //add div when button clicked
    var button = document.getElementById('btn_aggregate');
    var todolist_aggregate = document.getElementById('todolist_aggregate');
    
    button.addEventListener('click', function() {
    var id = Math.random();
    
      const elements = `
      <div id = "${id}" >
        <select class="browser-default custom-select custom-select-lg mb-3"  id="conditions${id}" onchange="updateText('conditions${id}','agregate_stages${id}')">
          <option selected >choose stages</option>
          <option value='{ "$match": { <query> } }'>$match</option>
          <option value='{ "$count": <string> }'>$count</option>
          <option value='{"$group":{_id: <expression>, // Group By Expression <field1>: { <accumulator1> : <expression1> },...}}'>$group</option>    
          <option value='{"$sort":{<field1>:<sort order>,<field2>: <sort order>...}}'>$sort</option>
          <option value='{"$limit":<positive integer>}'>$limit</option>
          <option value='{"$skip":<positive integer>}'>$skip</option>
          <option value="">other</option>
      </select>
    <div class="input-group">
        <span class="input-group-addon"><span class="glyphicon glyphicon-lock"></span></span>
        <input input onkeyup="manage(this,'agregate_stages${id}')" type="text" class="form-control" id="agregate_stages${id}" name = "agregate_stages" pattern ='(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}\$([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}.{1,100}(\s*){0,20}\}(\s*){0,20}'  required>       
    </div>  
    </br>
    </div>
    
     `
      todolist_aggregate.insertAdjacentHTML('beforeend', elements);  
    });
    //get values from multiple inputs
    var k = ""; 
    function update() { 
        var input = document.getElementsByName('agregate_stages'); 
      console.log(input)
        for (var i = 0; i < input.length; i++) { 
            var a = input[i]; 
            k +=  a.value  + ', ' ; 
        } 
        ;
        document.getElementById("par_aggregate").value = '[' + k.slice (0, -2) + ']'; 
    }
    //delete many documents 

    function manage_delete_mn(txt_delete_mn){
      var input = document.getElementById("txt_delete_mn").value;
      var input_regex = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([$regex]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}"(\s*){0,20}(.{1,50})(\s*){0,20}"(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}/g;
      var result = input_regex.test(input);
      var bt1 = document.getElementById('bt_delete_mn');
      
      if (result) {    
          bt1.disabled = false;
          document.getElementById("txt_delete_mn").style.color = "green";
          console.log("match");
      } else {
          bt1.disabled = true;
          document.getElementById("txt_delete_mn").style.color = "red";
          console.log("not match");
      }
      
      } 

// filter by id
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

// filter with comparison 

function function_comparison() {
  document.getElementById("demo_comparison").innerHTML = `<label class="label control-label">skip</label>
<div class="input-group">
<span class="input-group-addon"></span>
<input type="number" class="form-control" name="skip" value = "" placeholder="skip number" pattern='(^$|([+-]?([0-9]*[.])?[0-9]+))'>
</div>
<label class="label control-label">limit</label>
<div class="input-group">
<span class="input-group-addon"></span>
<input type="number" class="form-control" name="limit" value = "" placeholder="limit number" pattern='(^$|([+-]?([0-9]*[.])?[0-9]+))'>
</div>
<label class="label control-label">sort</label>
<div class="input-group">
<span class="input-group-addon"></span>
<input type="text" class="form-control" name="field" value = "" placeholder='field' pattern='(^$|([a-zA-Z0-9._%+-]+))'>
<input type="text" class="form-control" name="order" value = "" placeholder='ASCENDING/DESCENDING' pattern='(^$|(([1]+)|([-1]+)))'>
</div>
`;
}
  function updatetext_comparison(type) {
  var selected = [];
  var id = type;
  for (var option of document.getElementById('condition_comparison').options) {
    if (option.selected) {
      selected.push(option.value);
    }
  }
  document.getElementById('txt_comparison').value = '{' + selected + '}';
}
$('select').selectpicker();

function manage_comparison(txt_comparison){
var input = document.getElementById("txt_comparison").value;
var input_regex = /(\s*){0,20}\{(\s*){0,20}((\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}\$([a-z]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(\[(\s*){0,20}((\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"),)*((\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})){1}\]|(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}))(\s*){0,20}\}(\s*){0,20},)*("(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}\$([a-z]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(\[((\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"),)*((\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})){1}\]|(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}))(\s*){0,20}\}){1}(\s*){0,20}\}(\s*){0,20}/g;
var result = input_regex.test(input);
var bt1 = document.getElementById('bt_comparison');

if (result) {    
bt1.disabled = false;
document.getElementById("txt_comparison").style.color = "green";
console.log("match");
} else {
bt1.disabled = true;
document.getElementById("txt_comparison").style.color = "red";
console.log("not match");
}
} 
// filter with logical
function myFunction_logical() {
  document.getElementById("demo_logical").innerHTML = `<label class="label control-label">skip</label>
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
function updateText_logical(type) { 
var id = type;
document.getElementById('txt_logical').value = document.getElementById(type).value;
}

function manage_logical(txt_logical){
var input = document.getElementById("txt_logical").value;
var input_regex = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}(([$and]+)|([$nor]+)|([$or]+))(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\[(\s*){0,20}(((\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}\$([a-z]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}((\s*){0,20}\[(\s*){0,20}(\s*){0,20}((\s*){0,20}(?:(?=([0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}")(\s*){0,20},(\s*){0,20})*((\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})){1}(\s*){0,20}\](\s*){0,20}|(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"))(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}|\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})(\s*){0,20}\}(\s*){0,20}),(\s*){0,20})*(((\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}\$([a-z]+)(\s*){0,20}"(\s*){0,20}:((\s*){0,20}\[(\s*){0,20}((\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}),(\s*){0,20})*((\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})){1}\]|(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}))(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}|(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})(\s*){0,20}\}(\s*){0,20})){1}(\s*){0,20}\](\s*){0,20}\}(\s*){0,20}/g;
var result = input_regex.test(input);
var bt1 = document.getElementById('bt_logical');

if (result) {    
bt1.disabled = false;
document.getElementById("txt_logical").style.color = "green";
console.log("match");
} else {
bt1.disabled = true;
document.getElementById("txt_logical").style.color = "red";
console.log("not match");
}
}
//filter regular

function function_regular() {
  document.getElementById("demo_regular").innerHTML = `<label class="label control-label">skip</label>
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
  
  function manage_regular(txt_regular){
    var input = document.getElementById("txt_regular").value;
    var input_regex = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([$regex]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}"(\s*){0,20}(.{1,50})(\s*){0,20}"(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}/g;
    var result = input_regex.test(input);
    var bt1 = document.getElementById('bt_regular');
    
    if (result) {    
        bt1.disabled = false;
        document.getElementById("txt_regular").style.color = "green";
        console.log("match");
    } else {
        bt1.disabled = true;
        document.getElementById("txt_regular").style.color = "red";
        console.log("not match");
    }
    
    } 
// filter with fields
function function_filter() {
  document.getElementById("demo_filter").innerHTML = `<label class="label control-label">skip</label>
  <div class="input-group">
  <span class="input-group-addon"></span>
  <input type="number" class="form-control" name="skip" value = "" placeholder="skip number" pattern='(^$|([0-9]+))'>
  </div>
  <label class="label control-label">limit</label>
  <div class="input-group">
  <span class="input-group-addon"></span>
  <input type="number" class="form-control" name="limit" value = "" placeholder="limit number" pattern='(^$|([0-9]+))'>
  </div>
  <label class="label control-label">sort</label>
  <div class="input-group">
  <span class="input-group-addon"></span>
  <input type="text" class="form-control" name="field" value = "" placeholder='field' pattern='(^$|([a-zA-Z0-9._%+-]+))'>
  <input type="text" class="form-control" name="order" value = "" placeholder='ASCENDING/DESCENDING' pattern='(^$|(([1]+)|([-1]+)))'>
  </div>
  `;
  }
  
  
  
  function manage_filter(txt_filter){
  var input = document.getElementById("txt_filter").value;
  var input_regex = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([0-9]+))([0-9]+)|"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})(\s*){0,20}\}(\s*){0,20}/g;
  var result = input_regex.test(input);
  var bt1 = document.getElementById('bt_filter');
  
  if (result) {    
      bt1.disabled = false;
      document.getElementById("txt_filter").style.color = "green";
      console.log("match");
  } else {
      bt1.disabled = true;
      document.getElementById("txt_filter").style.color = "red";
      console.log("not match");
  }
  }
//insert many

function manage_insert_mn(txt_insert_mn){
  var input = document.getElementById("txt_insert_mn").value;
  var input_regex = /(\s*){0,20}\[(\s*){0,20}((\s*){0,20}\{(\s*){0,20}(((\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}))(\s*){0,20},(\s*){0,20})*((\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}")){1}(\s*){0,20}\},)*(\{(\s*){0,20}(("(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}))(\s*){0,20},(\s*){0,20})*((\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})){1}(\s*){0,20}\}(\s*){0,20}){1}(\s*){0,20}\](\s*){0,20}/g;
  var result = input_regex.test(input);
  var bt1 = document.getElementById('bt_insert_mn');
  
  if (result) {    
      bt1.disabled = false;
      document.getElementById("txt_insert_mn").style.color = "green";
      console.log("match");
  } else {
      bt1.disabled = true;
      document.getElementById("txt_insert_mn").style.color = "red";
      console.log("not match");
  }
  
  } 
//insert one

function manage_insert(txt_insert){
  var input = document.getElementById("txt_insert").value;
  var input_regex = /(\s*){0,20}\{(\s*){0,20}(((\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}")),(\s*){0,20})*("(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})){1}(\s*){0,20}\}(\s*){0,20}/g;
  var result = input_regex.test(input);
  var bt1 = document.getElementById('bt_insert');
  
  if (result) {    
      bt1.disabled = false;
      document.getElementById("txt_insert").style.color = "green";
      console.log("match");
  } else {
      bt1.disabled = true;
      document.getElementById("txt_insert").style.color = "red";
      console.log("not match");
  }
  }
//update many
function manage_update_mn(txt){
  var input1 = document.getElementById("txt1").value;
  var input_regex1 = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([$regex]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}"(\s*){0,20}(.{1,50})(\s*){0,20}"(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}/g;
  var input2 = document.getElementById("txt2").value;
  var input_regex2 = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([$set]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)(\s*){0,20}|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}/g
  var result1 = input_regex1.test(input1);
  var result2 = input_regex2.test(input2);
  var bt1 = document.getElementById('bt_update_mn');
  
  if (result1 || result2) {    
    
      bt1.disabled = false;
      console.log("match");
  } 
  else {
    bt1.disabled = true;

  }
  
  }

  // update one 

  function manage_update(txt){

    var input2 = document.getElementById("txt_update").value;
    var input_regex2 = /(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([$set]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}\{(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20}:(\s*){0,20}(?:(?=([+-]?([0-9]*[.])?[0-9]+))([+-]?([0-9]*[.])?[0-9]+)(\s*){0,20}|(\s*){0,20}"(\s*){0,20}([a-zA-Z0-9._%+-]+)(\s*){0,20}"(\s*){0,20})(\s*){0,20}\}(\s*){0,20}\}(\s*){0,20}/g
    var result2 = input_regex2.test(input2);
    var bt1 = document.getElementById('bt_update');
    
    if (result2) {    
      
        bt1.disabled = false;
        console.log("match");
    } 
    else {
      bt1.disabled = true;
    }
    }
// modals 