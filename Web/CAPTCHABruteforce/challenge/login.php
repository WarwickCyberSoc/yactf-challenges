<?php
    session_start();

    $error = "";
    
    if(isset($_POST["username"]) && isset($_POST["password"]) && isset($_POST["captcha"]))
    {
        if (!isset($_SESSION["captcha"]) || $_POST['captcha'] !== $_SESSION["captcha"]) {
            $error = "
            The captcha value was incorrect.
            ";
        }
        else
        {
            // Password is different on remote!
            if(!($_POST["username"] === "admin" && $_POST["password"] === "roxana")) {
                $error = "
                The username or password was incorrect.
                ";
            }
            else
            {
                // Log admin in
                $_SESSION["isAdmin"] = true;
                header("Location: /");
                die();
            }
        }
    }
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <link rel="stylesheet" href="/style.css">
</head>
<body>

<div class="container">
    <div class="row">
        <div class="col-lg-3 col-md-2"></div>
        <div class="col-lg-6 col-md-8 login-box">
            <div class="col-lg-12 login-title">
                ADMIN PANEL
            </div>

            <div class="col-lg-12 login-form">
                <div class="col-lg-12 login-form">
                    <form method="POST" action="/login.php">
                        <div class="form-group">
                            <label class="form-control-label">USERNAME</label>
                            <input type="text" name="username" class="form-control">
                        </div>
                        <div class="form-group">
                            <label class="form-control-label">PASSWORD</label>
                            <input type="password" name="password" class="form-control">
                        </div>
                        <div class="form-group">
                            <label class="form-control-label">CAPTCHA</label>
                            <input type="text" name="captcha" class="form-control">
                            <img id="captcha" src="/captcha.php?<?php echo rand(); ?>" alt="CAPTCHA Image" />

                        </div>

                        <div class="col-lg-12 loginbttm">
                            <div class="col-lg-6 login-btm login-text">
                                <?php echo $error ?? ""; ?>
                            </div>
                            <div class="col-lg-6 login-btm login-button">
                                <button type="submit" class="btn btn-outline-primary">LOGIN</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
