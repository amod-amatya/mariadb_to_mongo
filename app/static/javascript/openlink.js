function openLink(evt, linkName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("myLink");
    console.log("The value of x is " + x.length);
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" w3-blue", "");
    }
    document.getElementById(linkName).style.display = "block";
    evt.currentTarget.className += " w3-blue";
  }
  
  // Click on the first tablink on load
document.getElementsByClassName("tablink")[0].click();