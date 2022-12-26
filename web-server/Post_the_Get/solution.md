# Post the Get

## Write-Up

When accessing the page, we can find a simple form that we can fill and submit :

```html
<html>
    <head>
		<title>POST THE GET</title>
		<meta charset="UTF-8">
		<link rel="stylesheet" href="style.css">
		<link rel="preconnect" href="https://fonts.gstatic.com">
		<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&amp;display=swap" rel="stylesheet">
	</head>

	<body>
		<h1>HOW TO POST WHEN YOU GET</h1>

		<form action="/send" method="GET">
			<div class="inside">
			<label for="name" class="fname"> Full Name:</label><br>
			<input type="text" id="name" name="name"><br>
			<label for="address" class="addr">Address:</label><br>
			<input type="text" id="address" name="address"><br>
			<input type="submit" id="sub" name="sub">
		
	


		<script src="file.js"></script>

            </div>
        </form>
    </body>
</html>
```

But when we submit it with random value, here is what we get :

```
good try but you didn't post
```

When we see closly the code, we can find that the form actually sends a `GET` request instead of a `POST` :

```html
...
		<form action="/send" method="GET">
			<div class="inside">
...
```

So, let's change the method to `POST`, and try again (With random values) :

```html
<html>
    <head>
		<title>POST THE GET</title>
		<meta charset="UTF-8">
		<link rel="stylesheet" href="style.css">
		<link rel="preconnect" href="https://fonts.gstatic.com">
		<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&amp;display=swap" rel="stylesheet">
	</head>

	<body>
		<h1>HOW TO POST WHEN YOU GET</h1>

		<form action="/send" method="POST">
			<div class="inside">
			<label for="name" class="fname"> Full Name:</label><br>
			<input type="text" id="name" name="name"><br>
			<label for="address" class="addr">Address:</label><br>
			<input type="text" id="address" name="address"><br>
			<input type="submit" id="sub" name="sub">
		
	


		<script src="file.js"></script>

            </div>
        </form>
    </body>
</html>
```

We get the flag right away

## Flag

shellmates{7HE_w3B_is_w31RD}