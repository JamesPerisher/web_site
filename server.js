const express = require('express')
const app = express()

app.use(express.static(__dirname + '/public'));
app.set('views', __dirname + '/public');
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');


app.use("/home", function(req, res) {
  res.render('home.html')
});
app.use("/about", function(req, res) {
  res.render('about.html')
});
app.use("/discord_bot", function(req, res) {
  res.render('discord_bot.html')
});
app.use("/res_pack", function(req, res) {
  res.render('res_pack.html')
});
app.use("/thank_you", function(req, res) {
  res.render('thank_you.html')
});
app.use("/helpme", function(req, res) {
  res.render('helpme.html')
});
app.use("/help_me", function(req, res) {
  res.redirect("helpme")
});


app.get('/', function(req, res) {
  res.render("home.html")
})

app.listen(3000, function() {
  console.log('Example app listening on port 3000!')
})