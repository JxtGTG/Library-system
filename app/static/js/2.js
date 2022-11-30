

$(document).ready(function(){
    $("#All").show();

    $('[data-toggle="tooltip"]').tooltip(); 
    $(".check1").click(function(){
    $(".check1").toggleClass("fa-square-o");
     $(".check1").toggleClass("fa-check-square-o");  
});

$('.alert').fadeOut(5000);



$('[data-toggle="tooltip"]').tooltip();

// format of date
function formatDate(date) {

    return (
        date.getFullYear()+
            "/"+
        (date.getMonth() + 1) +
        "/" +
        date.getDate() +
            "-"+
        date.getHours()+
            ":"+
        date.getMinutes()

    );
}

//the formula of date
function Big(date){
    return (
        20000*parseInt(date.getFullYear())+

       9600*parseInt(date.getMonth() + 1) +

        3600*parseInt(date.getDate()) +

        60*parseInt(date.getHours())+

       parseInt( date.getMinutes())

    );
}

var currentDate = formatDate(new Date());
//date picker
$(".due-date-button").datetimepicker({
    format: "yyyy-mm-dd hh:ii",
     forceParse: 0,
    autoclose: true,
    todayHighlight: true,
    todaybtn:true,
    minView: 0,
    minuteStep:1,
    orientation: "bottom right",
    startDate:new Date()
});
$(".due-date-button11").datetimepicker({
    format: "yyyy-mm-dd hh:ii",
     forceParse: 0,
    autoclose: true,
    todayHighlight: true,
    todaybtn:true,
    minView: 0,
    minuteStep:1,
    orientation: "bottom right",
    startDate:new Date()

});

$("#searchc").datetimepicker({
    format: "yyyy-mm-dd hh:ii",
     forceParse: 0,
    autoclose: true,
    todayHighlight: true,
    todaybtn:true,
    minView: 0,
    minuteStep:1,
    orientation: "bottom right",
    startDate:new Date()

});



$(".due-date-button").on("click", function (event) {
    $(".due-date-button")
        .datetimepicker("show")
        .on("changeDate", function (dateChangeEvent) {
            $(".due-date-button").datetimepicker("hide");
            $(".due-date-label").text(formatDate(dateChangeEvent.date));
            var Date = formatDate(dateChangeEvent.date)
            document.getElementById('date11').value=Date;
            var big=Big(dateChangeEvent.date);
            document.getElementById('datebig').value=big;
        });
});

$("#searchc").on("click", function (event) {
    $("#searchc")
        .datetimepicker("show")
        .on("changeDate", function (dateChangeEvent) {
            $("#searchc").datetimepicker("hide");
            var Date = formatDate(dateChangeEvent.date)
            document.getElementById('search11').value=Date;
        });
});


$("#my_add").on("click",function(){
    document.getElementById('date22').value=currentDate;
    var create = Big(new Date())
     document.getElementById('datecreate').value=create;

})

$("#myselect").on('click', function () {
    var x =  document.getElementById('myselect').value;
    if (x=="Des"){
        $("#des1").show();
        $("#search1").hide();
        $("#pr1").hide();
          $("#All").hide();
    }
    else if(x=="Date"){
        $("#des1").hide();
        $("#search1").show();
        $("#pr1").hide();
          $("#All").hide();
    }
    else if(x=="Priority"){
        $("#des1").hide();
        $("#search1").hide();
        $("#pr1").show();
          $("#All").hide();

    }
    else{
         $("#des1").hide();
        $("#search1").hide();
        $("#pr1").hide();
         $("#All").show();

    }



});
$(".desc").on('click',function(){
    var itemId = this.id;
     $("#des1"+itemId).toggle(500);
});

// edit button of change
 $(".edit-btn").on('click', function () {
      var itemId = this.id;
      $("#line1"+itemId).show(500);
      $("#form" + itemId).show(500);
  $("#des1"+itemId).show(500);
      $("#form1"+itemId).removeAttr("readonly");
       $("#des1"+itemId).removeAttr("readonly")
      var date =  document.getElementById('label1'+itemId).innerText;
      var origin = document.getElementById('date33'+itemId).innerText;
      var big1 =  document.getElementById('date22222'+itemId).value;
      var create1 =  document.getElementById('date222222'+itemId).value;
      var Date2 =  document.getElementById('date2222'+itemId).value;
      var currentDate1 = document.getElementById('date222'+itemId).value;
      var y = $('#des1'+itemId).val();
      $(".cancel-btn").click(function() {
          $("#form1"+itemId).attr("readonly","readonly");
          $("#form" + itemId).hide(500);
          $("#des1"+itemId).hide(500);
             $("#des1"+itemId).attr("readonly","readonly");
          $("#line1"+itemId).hide(500);
          document.getElementById('label1'+itemId).innerText=date;
          document.getElementById('date33'+itemId).innerText=origin;
           document.getElementById('des1'+itemId).value=y;
            document.getElementById('date22222'+itemId).value=big1;
             document.getElementById('date222222'+itemId).value=create1;
             document.getElementById('date222'+itemId).value=currentDate1;
             document.getElementById('date2222'+itemId).value=Date2;
      });
      $("#due-date-button1"+itemId).on("click", function (event) {
    $("#due-date-button1"+itemId)
        .datetimepicker("show")
        .on("changeDate", function (dateChangeEvent) {
            $("#due-date-button1"+itemId).datetimepicker("hide");
             var Date1 = formatDate(dateChangeEvent.date);
             document.getElementById('date2222'+itemId).value=Date1;
              var h = document.getElementById('date33'+itemId);
             h.innerText=Date1;
             var x = document.getElementById('label1'+itemId);
             x.innerText=currentDate;
            var big = Big(dateChangeEvent.date);
              document.getElementById('date22222'+itemId).value=big;
            var create = Big(new Date());
             document.getElementById('date222222'+itemId).value=create;
             document.getElementById('date222'+itemId).value=currentDate;



        });
});
      $("#a1"+itemId).on("click", function (event) {
    var va=document.getElementById("form1"+itemId).value;
    document.getElementById('word'+itemId).value=va;
     var yy = $('#des1'+itemId).val();
    document.getElementById('des2'+itemId).value=yy;
    document.getElementById('form'+itemId).submit();

});


      });






});



