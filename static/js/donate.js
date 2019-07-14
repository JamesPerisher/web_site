document.onkeyup = function(e) {
  if (e.which == 27) {
    closeForm();
  }
}


function openForm() {
  document.getElementById("myForm").style.display = "block";
  document.getElementsByTagName("html")[0].style.position = "fixed";
  console.log(document.getElementsByClassName("page_content")[0]);
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
  document.getElementsByTagName("html")[0].style.position = "inherit";
}