function showHide() {
    
    
    var x = document.getElementById("myDiv");
    console.log("The valueeeeeeeeee " + x);
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      console.log("The valueeeeeeeeee wwww");
      x.style.display = "none";
    }
    return false;
  }