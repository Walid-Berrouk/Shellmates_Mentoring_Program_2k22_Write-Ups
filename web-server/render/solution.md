# render

## Write-Up

```
sqlmap -u "http://render.web-server.challs.ctf.shellmates.club/" --data="name=Walid" --method POST --dbs
```

```
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.6.10#stable}
|_ -| . [']     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[02:07:07] [INFO] testing connection to the target URL
[02:07:07] [INFO] testing if the target URL content is stable
[02:07:08] [INFO] target URL content is stable
[02:07:08] [INFO] testing if POST parameter 'name' is dynamic
[02:07:08] [WARNING] POST parameter 'name' does not appear to be dynamic
[02:07:08] [WARNING] heuristic (basic) test shows that POST parameter 'name' might not be injectable
[02:07:08] [INFO] testing for SQL injection on POST parameter 'name'
[02:07:08] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[02:07:09] [WARNING] reflective value(s) found and filtering out
[02:07:11] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[02:07:11] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[02:07:12] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[02:07:13] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[02:07:13] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[02:07:14] [INFO] testing 'Generic inline queries'
[02:07:14] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[02:07:14] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[02:07:14] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[02:07:15] [WARNING] turning off pre-connect mechanism because of connection reset(s)
[02:07:15] [WARNING] there is a possibility that the target (or WAF/IPS) is resetting 'suspicious' requests
[02:07:15] [CRITICAL] connection reset to the target URL. sqlmap is going to retry the request(s)
[02:07:15] [WARNING] most likely web server instance hasn't recovered yet from previous timed based payload. If the problem persists please wait for a few minutes and rerun without flag 'T' in option '--technique' (e.g. '--flush-session --technique=BEUS') or try to lower the value of option '--time-sec' (e.g. '--time-sec=2')
[02:07:15] [CRITICAL] connection reset to the target URL
[02:07:15] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
there seems to be a continuous problem with connection to the target. Are you sure that you want to continue? [y/N] y
[02:07:22] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[02:07:24] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[02:07:27] [INFO] testing 'Oracle AND time-based blind'
it is recommended to perform only basic UNION tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] Y
[02:07:35] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[02:07:38] [WARNING] POST parameter 'name' does not seem to be injectable
[02:07:38] [CRITICAL] all tested parameters do not appear to be injectable. Try to increase values for '--level'/'--risk' options if you wish to perform more tests. If you suspect that there is some kind of protection mechanism involved (e.g. WAF) maybe you could try to use option '--tamper' (e.g. '--tamper=space2comment') and/or switch '--random-agent'

[*] ending @ 02:07:38 /2022-12-26/


```

## Flag