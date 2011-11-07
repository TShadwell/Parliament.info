
function keyPress(e) {
    if (e.keyCode == 13) {
        Answer()
        return false;
    }
}
function Answer()
{
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
	$('#suggest').fadeOut('slow');
	$('#response').fadeOut('slow');
	document.getElementById("response").innerHTML=xmlhttp.responseText;
	$('#response').fadeIn('slow');
	}
	else
	{
	$('#suggest').fadeOut('slow');
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
