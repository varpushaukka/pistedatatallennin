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
%if 'loggedin' in session:
	<p>kirjautuneena: {{session['loggedin']}}
	<a id="kirj" href="/logout"> kirjaudu ulos </a>
%else:
<a id="kirj" href="/pages/kirjaudu.html"> kirjaudu </a>
%end

<h1>Paikkatietomuistikirja</h1>

<form method="post" action="/search">
	<p>
	<label for="haku"> Haku </label>
		<input type="text" name="haku"> 
	<input type=submit value="Hae">
</form>
<p> <a href="/place"> lisää paikka </a>


</div>

</body>
</html>
