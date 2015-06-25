<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
 <title>Paikkatietomuistikirja</title>
 <meta name="author" content="Henna Kalliokoski">
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
 <link rel="stylesheet" type="text/css" href="/pages/ptmuistikirjatyyli.css">
</head>
<body>
<div class="box">

% for place in m.list_coordinates((9583,8374), tag=tag):
<br> {{ str(place) }}
% end


<br>
<iframe
  width="450"
  height="250"
  frameborder="0" style="border:0"
  src="https://www.google.com/maps/embed/v1/view?key=AIzaSyCF7pHbZ2VY2Pyo0E1iCNtSHDTwZEkNXQU
  &center=60.1732816, 24.9523583" allowfullscreen>
</iframe>



</div>

</body>
</html>
