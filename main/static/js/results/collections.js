
$(".current01").click(function()
{
    db = $(this).attr('name')
    h5 = $("#exampleModal2 ").find('#exampleModalLabel').text("Add collection to "+ db);
    console.log(db)
    });

$(".current1").click(function()
{
    link=$(this).val()
    action=$("#exampleModal4").find('form ').attr('action',link);
    });

