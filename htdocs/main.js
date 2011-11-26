
function keyPress(e) {
    if (e.keyCode == 13) {
        Answer()
        return false;
    }
}
function Answer()
{
$('#subm').css("backgroundColor", "#D7D7D7");
document.getElementById("subm").value="";
$('#load').fadeIn('medium');
$('#suggest').fadeOut('slow');
$('#response').fadeOut('slow');
var xmlhttp;


if (window.XMLHttpRequest)
  {

  xmlhttp=new XMLHttpRequest();
  }
else
  {
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
	if (document.getElementById("response").style.display != "none")
	{
	$('#subm').css("backgroundColor", "#18D218");
	document.getElementById("subm").value="Ask";
	
	document.getElementById("response").innerHTML=xmlhttp.responseText;
	$('#load').fadeOut('fast');
	$('#response').fadeIn('slow');
	}
	else
	{
	$('#suggest').fadeOut('slow');
	$('#load').fadeOut('fast');
	$('#subm').css("backgroundColor", "#18D218");
	document.getElementById("subm").value="Ask";
	document.getElementById("response").innerHTML=xmlhttp.responseText;
	$('#response').fadeIn('slow');
	}
	$('#suggest').fadeOut('slow');
	
	document.getElementById("input").blur();
	//document.getElementById("suggest").style.display="none";
	}
  }
xmlhttp.open("GET","/cgi-bin/r.py?q=" + document.getElementById("input").value ,true);

xmlhttp.send();
}


//done
