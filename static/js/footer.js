console.log("script loaded");

function footer(current) { // default navagarion bar HTML
  var a = "<div class=\"id565\">\
      \<div class=\"footer\">\
        \<p><a href=\"#terms\">Terms</a></p>\
        \<p><a class=\"fake-link\"onclick=\"openForm()\">Donate</a></p>\
        \<p>Conact:   <a href=\"#conact\">examplemail@email.com</a></p>\
        \<p>@PaulN07#2596</p>\
        \ \
        \<a href=\"https://github.com/JamesPerisher\"><img class=\"img\" src=\"static/images/github_icon.svg\"></a>\
      \</div>\
      \</div>";




  doc = new DOMParser().parseFromString(a, "text/html");

  var d1 = document.getElementsByTagName("body")[0];
  d1.insertAdjacentHTML('afterEnd', doc.firstChild.querySelector('body > div.id565').innerHTML);

};


footer(document.URL.split("/").pop().split(".")[0]); // may break with webpages with no filename extensions