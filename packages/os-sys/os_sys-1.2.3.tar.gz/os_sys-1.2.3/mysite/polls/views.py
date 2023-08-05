from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("""
<!DOCTYPE html>

<html lang="eng" lang="eng">
<head>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
   <meta name="description" content="beschrijving van de webpagina" />
   <meta name="keywords" content="trefwoorden, gescheiden, door, komma's" />
   <title>os_sys docs index</title>
   <style type='text/css'>
   a { color: rgb(0,0,255); }
   </style>
</head>
<body>
<h1>index</h1>
<p>welcome at the os_sys docs.</p>
<h2>index:</h2>
<a href="#first">first</a>
<hr>
<div id='first'>
<h2>first</h2>
<p>first there are somethings you need to know:<br>
1. this docs are under devlopment.<br>
2. if you want to add somethings to this docs go to os_sys github and post a what you want to add and i will ad it.<br>
3. have fun with this package.</p>
</div>
</body>
</html>""")
# Create your views here.
