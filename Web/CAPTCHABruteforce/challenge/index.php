<?php
    session_start();

    if($_SESSION["isAdmin"] !== true)
    {
        header("Location: /login.php");
        die();
    }

    if(isset($_GET["operation"]))
    {
        // Just in case we get hacked...
        $safetyRegex = "^.*[\^$(){}`&;*,|\-\"\'~\/ .].*$";
        if(preg_match($safetyRegex, $_GET["operation"]))
        {
            die("Invalid operation detected!");
        }

        $operationOutput = shell_exec($_GET["operation"]);
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome Admin!</title>


    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        <div class="col-8 offset-2" style="color: #ecf0f5; background-color: #1a2226; margin-top: 50px; padding: 20px;">
            <h1 class="text-center">Welcome admin!</h1>

            <strong>Available commands:</strong>
            <ul>
                <li><a href="/index.php?operation=ps">List Processes</a></li>
                <li><a href="/index.php?operation=ss">List Sockets</a></li>
                <li><a href="/index.php?operation=uptime">View Uptime</a></li>
            </ul>

            <div>
                <p style="white-space: pre-wrap;"><?php echo $operationOutput; ?></p>
            </div>
            <a href="/logout.php">Logout</a>
        </div>
    </div>
</body>
</html>
