console.log("script loaded");


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


function add_button() {
  var a = "<div class=\"id562\">\
  \<link type=\"text/css\" rel=\"stylesheet\" href=\"css/donate.css\" />\
  \ \
  \<div id=\"myForm\">\
  \<div class=\"overlay\">\
    \<div class=\"donate\">\
      \<h1>Donate</h1>\
      \<table>\
        \<tr>\
          \<td class=\"dleft\">\
            \<form action=\"https://www.paypal.com/cgi-bin/webscr\" method=\"post\" target=\"_top\">\
              \<input type=\"hidden\" name=\"cmd\" value=\"_s-xclick\" />\
              \<input type=\"hidden\" name=\"hosted_button_id\" value=\"P8F897U3VR32U\" />\
              \<input type=\"image\" src=\"https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif\" border=\"0\" name=\"submit\" title=\"PayPal - The safer, easier way to pay online!\" alt=\"Donate with PayPal button\" />\
            \</form>\
            \ \
            \<img src=\"images/bitcoin.png\" alt=\"bitcoin request qr code\">\
          \</td>\
          \<td class=\"dright\">\
            \<h2>For as little as $1USD you can help support development of projects</h2>\
            \<p>important reason to use thisimportant reason to use thisimportant reason to use thisimportant reason to use thisimportant reason to use thisimportant reason to use thisimportant reason to use thisimportant reason to use this</p></td>\
        \</tr>\
      \</table>\
      \ \
      \<div class=\"dbottom\">\
        \<p style=\"padding: 14px 16px;\">bitcoin address: bc1qh3kmyz4tmet5j0h4gsalua9hr0lmxrpk6nmjv99rlw3279c20vkqsjwu6q</p>\
        \<span class=\"fake-link close\" onclick=\"closeForm()\" name=\"button\">Cancel</span>\
        \<p><br><br><br></p>\
      \</div>\
      \</div></div></div>"


  doc = new DOMParser().parseFromString(a, "text/html");


  document.getElementsByTagName("header")[0].insertAdjacentHTML('beforeEnd', doc.querySelector('div.id562').innerHTML);
}

add_button(document.URL.split("/").pop().split(".")[0]); // may break with webpages with no filename extensions