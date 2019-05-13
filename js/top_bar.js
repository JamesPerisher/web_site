console.log("script loaded");

var isMobile = {
  Android: function() {
    return navigator.userAgent.match(/Android/i);
  },
  BlackBerry: function() {
    return navigator.userAgent.match(/BlackBerry/i);
  },
  iOS: function() {
    return navigator.userAgent.match(/iPhone|iPad|iPod/i);
  },
  Opera: function() {
    return navigator.userAgent.match(/Opera Mini/i);
  },
  Windows: function() {
    return navigator.userAgent.match(/IEMobile/i);
  },
  any: function() {
    return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
  }
};

function topbar(current) { // default navagarion bar HTML
  var a = "<div class=\"id564\">\
      \<div class=\"mobile\"><div class=\"topnav\">\
      \<div id=\"myLinks\">\
      \<a class=\"cat home\" href=\"home.html\">Home</a>\
      \<a class=\"cat about\" href=\"about.html\">About</a>\
      \<a class=\"cat discord_bot\" href=\"discord_bot.html\">Discord Bot</a>\
      \<a class=\"cat res_pack\" href=\"res_pack.html\">Resource pack</a>\
      \</div>\
      \<a href=\"javascript:void(0);\" class=\"icon\" onclick=\"mobile_button()\">\
        \<i class=\"fa fa - bars \"></i>hello\
      \</a>\
      \ \
      \<a class=\"right\" href=\"https://discord.gg/2wj94TP\" target=\"_blank\">Join my discord</a>\
    \</div></div> </div>";




  doc = new DOMParser().parseFromString(a, "text/html");
  element = doc.firstChild.querySelector('a.cat.' + current);
  if (element == null) { // if page not in nav bar display it temporaraly
    console.warn("could not find navagarion element for: " + current);
    current = "bad_page";
    element = doc.firstChild.querySelector('a.cat').insertAdjacentHTML("beforeEnd", "<a class=\"cat " + current + "\" href=\"" + current + ".html\">hiddenPage</a>");
    element = doc.firstChild.querySelector('a.cat.' + current);
  }
  element.classList.add("active");
  element.removeAttribute("href");


  if (isMobile.any()) { // display  mobile version
    doc.getElementsByClassName("topnav")[0].classList.add("topnav-mobile");

    var d1 = document.getElementsByTagName("header")[0];
    d1.insertAdjacentHTML('beforeEnd', doc.firstChild.querySelector('body > div.id564').innerHTML);
  } else { // display pc version

    doc.getElementsByClassName("icon")[0].setAttribute("style", "display: none");

    doc.querySelector("#myLinks").setAttribute("id", "none");
    var d1 = document.getElementsByTagName("header")[0];
    d1.insertAdjacentHTML('beforeEnd', doc.firstChild.querySelector('body > div.id564').innerHTML);
  };
};

function mobile_button() {
  var x = document.getElementById("myLinks");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
}


topbar(document.URL.split("/").pop().split(".")[0]); // may break with webpages with no filename extensions