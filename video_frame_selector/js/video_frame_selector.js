var bigscreen = null;
var video = null;
var chop_time = 0;
var findex = 0;
var capture = null;
var duration = 0;
var index = new Array();
var canindex = new Array();
var m = null;
var i = 0;
var frt = 24;
var count = 0;
var play = 1;
var name = null;
var pt = null;
var v;
var frames = new Array();
var index = new Array();
var canindex = new Array();
var capturefrm = null;
var capctx = null;
var captureIdle = true;
var tempctx = null;
var first = true;
var temp = null;
var capture = null;
var vw = null;
var vh = null;
var _ids = [];
var ENDED = 0;
var STARTED = 0;
var touchEnd = 0;
var m = 0;
var capturing = 0;
var previewing = 0;
var FIRST = 1;
var videoStatus = 1;
var captureTimers = [];
var o = null;
var s = null;
var tp;
var src=null;

$(function()
{
    $( "#confirm-frame" ).dialog
    ({
        title: 'Confirm Segment Chop Point',
        autoOpen: false,
        height: 400,
        width: 1000,
        modal: true,
        resizable: false,
        buttons:
        {
          'Cancel': function(){
            $(this).dialog('close');
          }
        }
     
    }); //confirm-frame dialog
}

)


function backtoChopPoint()
{
   toggleVideoScreen(1);
   $(this).dialog('close');
}

function captureOnGo()
{
    while (captureTimers.length)
    {
      clearInterval(captureTimers.shift());
    }
    index = [];
    canindex = [];
    temp = [];
    i = 0;
    console.log('start');
    capture = setInterval(
    function()
    {
        var condition = (index.length>15);
        switch (condition)
            {
              case true:
                index.shift();
                i = canindex.shift();
                canindex.push(i);
                tempctx = $('#bufferCanvases canvas')[i].getContext('2d');
                if (ENDED)
                  {
                   tempctx.fillStyle = 'black';
                   tempctx.fillRect(0, 0, $('#bufferCanvases canvas')[i].width, $('#bufferCanvases canvas')[i].height);
                  }
                else
                  {
                    tempctx.drawImage(video[0], 0, 0, $('#bufferCanvases canvas')[i].width, $('#bufferCanvases canvas')[i].height);
                    tempctx.fillStyle = 'yellow';
                    tempctx.font = '20px arial';
                  }
                //var f = Math.round(video[0].currentTime*frt);
                var f = video[0].currentTime;
                //tempctx.fillText(f,0,30);
                temp.push(f);
                index.push(f);
                break;

              case false:
                canindex.push(i);
                tempctx = $('#bufferCanvases canvas')[i].getContext('2d');
                if (ENDED)
                {
                   tempctx.fillStyle = 'black'; 
                   tempctx.fillRect(0, 0, $('#bufferCanvases canvas')[i].width, $('#bufferCanvases canvas')[i].height);
                }
                else
                {
                  tempctx.drawImage(video[0], 0, 0, $('#bufferCanvases canvas')[i].width, $('#bufferCanvases canvas')[i].height);
                  tempctx.fillStyle = 'yellow';
                }
                //var f = Math.round(video[0].currentTime*frt);
                var f = video[0].currentTime;
                //tempctx.fillText(f,0,30);
                index.push(f);
                temp.push(f);
                i += 1;
                break;
            }

              if (video[0].paused && !ENDED) 
              {
                console.log('stopped because paused');
                clearInterval(capture);
                captureTimers.shift();
              }
        } ,1000/frt);
    captureTimers.push(capture);

} //captureOnGo

function greyoutButtons()
{
 $('.greycover').show();
 var ifCapturing = setInterval(function(){
  if (!capturing)
  {
    clearInterval(ifCapturing);
    $('.greycover').hide();
  }
 },100);

}

function greyoutButtons1()
{

  var pointerArray = $('.pointer');
  var onclickStack = [];
  var pointerStack =[];
  pointerArray.css('opacity', 0.3);
  pointerArray.css('background-color', '#000');
  for (var i=0; i<pointerArray.length; i++)
  {
    pointerStack.push(pointerArray.eq(i));
    onclickStack.push(pointerArray.eq(i).attr('onClick'));
    pointerArray.eq(i).removeAttr('onClick');
  }
  var current_element = null;
  var current_onclick = null;
  var ifCapturing = setInterval(function(){
  if (!capturing)
  {
    clearInterval(ifCapturing);
    for (var i=0; i<pointerArray.length; i++)
    {
      current_element = pointerStack.shift();
      current_onclick = onclickStack.shift();
      current_element.attr('onClick', current_onclick);  
    }
    pointerArray.css('opacity', '');
    pointerArray.css('background-color', '');
  }
 },100);
}


function updateScreen(callback)
{
     var putFrames0 = function(callback1)

      {
          console.log('putting frames');
          var j = 0;
          var k = 0;
          var l = 0;
          var width = 0;
          var height = 0;
          var pf = null;
          var pfpctx = null;
          var tempq = [].concat(canindex);
          for (j = 0; j<index.length; j++)
          {
            if (index[j] >= findex)
            {
                break;
                //postition in index
            }
          }
          
          for (k=0; k<j-3; k++)
          {
            tempq.push(tempq.shift());
            //pull the starting value of canindex to queue-head
          }

          for (k=0; k<9; k++)
          {
              //j: which position in sequence index is findex
              //l: from canindex
              l = tempq.shift();
              pf = $('#preview-frames canvas')[k];
              pfctx = pf.getContext('2d');
              width = pf.width;
              height = pf.height;
              pfctx.drawImage($('#bufferCanvases canvas')[l], 0, 0, width, height);
              pf.value = index[k+j-3];
          }
            if (ENDED)
            {
              clearInterval(capture);
              //ENDED = 0;
              capturing = 0;
            }
            else
            {
            video[0].pause();
            setTimeout(function(){
              video[0].currentTime = chop_time;  
            },100);
            
            capturing =0;
            }
            if (callback1)
            {
              callback1();
            }

      };//Function putFrames
      checkTimeRange();
      greyoutButtons1();
      //findex = Math.round(chop_time*frt);
      findex = chop_time;

      $("#ctime").val(chop_time.toFixed(4));
      $("#ctime_show").val(toFormat(chop_time.toFixed(4)));

      m =index.length;

      if (ENDED && index[m-1]<=findex && index[m-1]>index[m-2])
      {
            capturing =1;
            console.log('at end of buffer ended');
            setTimeout(function(){
            putFrames0(callback);
                },8000/frt);
            return;
      }

      else if (ENDED && index[3]<=findex && findex<=index[m-1]+4/frt )
      {
          capturing =1;
          console.log('within range ended');
          putFrames0(callback);
          return;
      }


      if (capturing)
      {
        console.log('capturing:'+capturing);
        return;
      }

      if ((index[m-1]<=findex && findex<=index[m-1]+1/frt && !video[0].paused))   //at the end of buffer
        {
          //video[0].play();
            capturing =1;
            console.log('at end of buffer');
            setTimeout(function(){
            putFrames0(callback);
                },8000/frt);
            return;          
        }

     if (index[2]<=findex && findex+5/frt<=index[m-1]) //within range
       {
        capturing =1;
        console.log('within range');
        putFrames0(callback);
        return;
       } 


      else //if not capturing
      {
      
            capturing =1;
            ENDED = 0;
            $("#demo")[0].currentTime=chop_time-8/frt;
            console.log('out of buffer');
            console.log(video[0].seeking);
            var timer = setInterval(function(){
              if (!video[0].seeking)
              {
                clearInterval(timer);
                if (video[0].paused)
                {
                  video[0].play();  
                }
                else
                {
                  clearInterval(capture);
                  captureOnGo();  
                } 

                setTimeout(function(){
                  putFrames0(callback);
                },17000/frt);
              }
            },100);
            return;
 
      } //if not capturing
} //function updateScreen()

function checkTimeRange()
{
  if (chop_time > duration)
  {
    chop_time = duration;
  }
  if (chop_time < duration - 5/frt)
  {
    ENDED = 0;
  }
}

function toFormat(seconds)
  {
    var min = Math.floor(seconds/60);
    min = '0'+String(min);
    ml=min.length;
    var sec = Math.round(seconds)%60;
    sec = '0'+String(sec);
    sl=sec.length;
    var str = min.slice(ml-2,ml)+":"+sec.slice(sl-2,sl);
    return str;
  }


function shiftdown(t)
    {
      ENDED = 0;
      chop_time = parseFloat($("#ctime")[0].value);
      chop_time = chop_time-t;
      updateScreen();
    }       


  function shiftup(t)
  {
     chop_time = parseFloat($("#ctime")[0].value);
      chop_time = chop_time - (-t);
      updateScreen();  
     } //click up   

  function jumpto(t)
  {
      chop_time = parseFloat(t);
      updateScreen();
  }



$(document).ready(function()
{   
  
    video=$("#demo");
    vw = parseFloat(video.attr('width'));
    vh = parseFloat(video.attr('height'));

    bigscreen = $("#bigscreen")[0].getContext('2d');
    var cover = $('#video-cover')[0].getContext('2d');
    cover.fillStyle = 'pink';
    cover.fillRect(0, 0, 600, 340);


      $("#demo").bind("play", function(){
        ENDED = 0;
        captureOnGo();
        });


    $('.ui-dialog-titlebar-close').remove();
    //$('#my_form').append($('.ui-dialog'));

    $("#chopButton").button();
    $('#doneButton').button();
    $('#setsrc').button();
    $('#doneButton').button('disable');
    $('#bigscreen').show();  


    $('#product_name_ad_input').on('blur', function(){
      if (tp)
        {
          tp = tp.toLowerCase();
          if ( $('input[value="tp"]').length ) $('input[value="tp"]:radio').attr('checked',true);
        }
    });

    $('#doneButton').click(function(){
      if (FIRST)
      {
        if (!video[0].paused)
          {
            video[0].pause();
          }
        contentNeverChanged();
      }
      else
      {
        $('#done').dialog('open');
      }
    });

 
    $("#chopButton").bind('click', function()
    {
        var chops_formatted = '00:00';
        var newCanvas = $('<canvas width="95" height = "65"/>').attr('class', 'leftStack');
        var newctx = newCanvas[0].getContext('2d');
        if (!STARTED)
        {
          video[0].play();
          $('#bigscreen').hide();
          $('#chopButton span span').html('chop');
          $('#doneButton').button('enable');
          STARTED = 1;
          $('#introText').hide();

          newctx.drawImage(video[0], 0, 0, newCanvas[0].width, newCanvas[0].height);
          newctx.font = '15px';
          newctx.fillStyle = 'yellow';
          newctx.fillText(chops_formatted,50,50);
          return;
        }
        if (ENDED)
        {
          $('#confirm-frame').dialog('open');
          return;
        }
        chop_time = video[0].currentTime-0.5;
        $("#ctime").val(chop_time.toFixed(4));
        $("#ctime_show").val(toFormat(chop_time.toFixed(4)));
        //toggleVideoScreen(0);
        var func = function()
        {
            $('#confirm-frame').dialog('open'); 
        }
        updateScreen(func);
    }); //click chopButton

    $("#ctime_show").mask("99:99");

    video.bind("loadedmetadata", function(){
      duration = video[0].duration;
      var newCanvas = $('<canvas/>').width(85).height(55);
      var newctx = newCanvas[0].getContext('2d');
      newctx.drawImage(video[0], 0,0, newCanvas[0].width, newCanvas[0].height);

    });

    $("#setsrc").bind('click', function(){
      src=$('#videosrc').val();
      $("#demo source").attr("src", src);
      video.load();
    });

}); //ready document


$(document).keypress(
    function(event){
     if (event.which == '13') {
        event.preventDefault();
      }
}); //prevent enter submit form 
