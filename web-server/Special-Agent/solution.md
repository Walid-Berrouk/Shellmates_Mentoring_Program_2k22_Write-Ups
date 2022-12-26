# Special Agent

## Write-Up

When accessing the home page, we get a button to get the flag. Unfortunatly, it doesn't work for us.

And when checking the provided `nginx` file, here is what we find :

```
events {
}

http {
  server {
    listen 1337;

    location = /flag.html {
      if ($http_user_agent = SuperSecretAgent) {
	rewrite ^ /flag.html break;
      }
      rewrite ^ /no_flag_for_you.html break;
    }

    location = /alive {
      return 200;
    }
  }
}
```

So, in order to get the flag, we need to send a request with a special agent named `SuperSecretAgent` :

```
curl 'http://secret-agent.web-server.challs.ctf.shellmates.club/flag.html' -H "User-Agent: SuperSecretAgent"
```

Here is what we get  :

```
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width-device-width, initial-scale=1.0" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet"/>
    <link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet"/>
    <title>Secret Agent</title>
  </head>
  <body class="bg-gray-50">
    <header>
      <div class="flex flex-row bg-gray-100 px-5 py-2">
 <a href="/" class="hover:underline hover:text-blue-500 text-black py-1 px-4 font-bold">
   <i class="ml-2 fas fa-user-secret"></i> Secret Agent
 </a>
      </div>
    </header>

    <main>
      <div class="my-5 flex justify-center items-center relative z-20">
 <h1 class="text-black text-5xl font-bold">shellmates{$uuUuUUP3r_S3CR37_aG3Nt}</h1>
      </div>
    </main>

  </body>
</html>

```

## Flag

shellmates{$uuUuUUP3r_S3CR37_aG3Nt}