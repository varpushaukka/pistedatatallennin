document.write("joo kyl toimii");

window.onload = function() { 
 navigator.geolocation.getCurrentPosition(function (loc) {
  coordfield = document.getElementById("piste");
  coordfield.value = "" + loc.coords.latitude + "," + loc.coords.longitude;
})};
