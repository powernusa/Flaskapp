# Boiler Plate

/* Login Form in index.php */
<!--Login form-->    
<form method="post" id="loginform">
	<div class="modal" id="loginModal" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<button class="close" data-dismiss="modal">&times;</button>
					<h4 id="myModalLabel">Login: </h4>
				</div>
				
				<div class="modal-body">
		  
					<!--Login message from PHP file-->
					<div id="loginmessage"></div>
		  
					<div class="form-group">
						<label for="loginemail" class="sr-only">Email:</label>
						<input class="form-control" type="email" name="loginemail" id="loginemail" placeholder="Email" maxlength="50">
					</div>
					<div class="form-group">
						<label for="loginpassword" class="sr-only">Password</label>
						<input class="form-control" type="password" name="loginpassword" id="loginpassword" placeholder="Password" maxlength="30">
					</div>
					<div class="checkbox">
						<label>
							<input type="checkbox" name="rememberme" id="rememberme">Remember me
						</label>
						<a class="pull-right" style="cursor: pointer" data-dismiss="modal" data-target="#forgotpasswordModal" data-toggle="modal">
							Forgot Password?
						</a>
					</div>
				
				</div>
				
				<div class="modal-footer">
					<input class="btn green" name="login" type="submit" value="Login">
					<button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
					<button type="button" class="btn btn-default pull-left" data-dismiss="modal" data-target="signupModal" data-toggle="modal">
						Register
					</button>  
				</div>
			</div>
		</div>
	</div>
</form>

/* ------------------------------------------------------------------------------------------- */
/* Ajax call in javascript.js */
//Ajax Call for the login form
//Once the form is submitted
$("#loginform").submit(function(event){ 
    //hide message
    $("#loginmessage").hide();
    //show spinner
    $("#spinner").css("display", "block");
    //prevent default php processing
    event.preventDefault();
    //collect user inputs
    var datatopost = $(this).serializeArray();
	//console.log(datatopost);
    //send them to login.php using AJAX
    $.ajax({
        url: "login.php",
        type: "POST",
        data: datatopost,
        success: function(data){
            if(data == "success"){
                window.location = "mainpageloggedin.php";
            }else{
                $('#loginmessage').html(data);   
                //hide spinner
                $("#spinner").css("display", "none");
                //show message
                $("#loginmessage").slideDown();
            }
        },
        error: function(){
            $("#loginmessage").html("<div class='alert alert-danger'>There was an error with the Ajax Call. Please try again later.</div>");
            //hide spinner
            $("#spinner").css("display", "none");
            //show message
            $("#loginmessage").slideDown();
            
        }
    
    });

});

/* ---------------------------------------------------------------- */
/* login.php */ 
<?php
//Start session
session_start();
//Connect to the database
include("connection.php");
//Check user inputs
    //Define error messages
$missingEmail = '<p><stong>Please enter your email address!</strong></p>';
$missingPassword = '<p><stong>Please enter your password!</strong></p>'; 
    //Get email and password
    //Store errors in errors variable
if(empty($_POST["loginemail"])){
    $errors .= $missingEmail;   
}else{
    $email = filter_var($_POST["loginemail"], FILTER_SANITIZE_EMAIL);
}
if(empty($_POST["loginpassword"])){
    $errors .= $missingPassword;   
}else{
    $password = filter_var($_POST["loginpassword"], FILTER_SANITIZE_STRING);
}
    //If there are any errors
if($errors){
    //print error message
    $resultMessage = '<div class="alert alert-danger">' . $errors .'</div>';
    echo $resultMessage;   
}else{
    //else: No errors
    //Prepare variables for the query
    $email = mysqli_real_escape_string($link, $email);
$password = mysqli_real_escape_string($link, $password);
$password = hash('sha256', $password);
        //Run query: Check combinaton of email & password exists
$sql = "SELECT * FROM users WHERE email='$email' AND password='$password' AND activation='activated'";
$result = mysqli_query($link, $sql);
if(!$result){
    echo '<div class="alert alert-danger">Error running the query!</div>';
    exit;
}
        //If email & password don't match print error
$count = mysqli_num_rows($result);
if($count !== 1){
    echo '<div class="alert alert-danger">Wrong Username or Password</div>';
}
else {
    //log the user in: Set session variables
    $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
    $_SESSION['user_id']=$row['user_id'];
    $_SESSION['username']=$row['username'];
    $_SESSION['email']=$row['email'];
    
    if(empty($_POST['rememberme'])){
        //If remember me is not checked
        echo "success";
    }else{
        //Create two variables $authentificator1 and $authentificator2
        $authentificator1 = bin2hex(openssl_random_pseudo_bytes(10));
        //2*2*...*2
        $authentificator2 = openssl_random_pseudo_bytes(20);
        //Store them in a cookie
        function f1($a, $b){
            $c = $a . "," . bin2hex($b);
            return $c;
        }
        $cookieValue = f1($authentificator1, $authentificator2);
        setcookie(
            "rememberme",
            $cookieValue,
            time() + 1296000
        );
        
        //Run query to store them in rememberme table
        function f2($a){
            $b = hash('sha256', $a); 
            return $b;
        }
        $f2authentificator2 = f2($authentificator2);
        $user_id = $_SESSION['user_id'];
        $expiration = date('Y-m-d H:i:s', time() + 1296000);
        
        $sql = "INSERT INTO rememberme
        (`authentificator1`, `f2authentificator2`, `user_id`, `expires`)
        VALUES
        ('$authentificator1', '$f2authentificator2', '$user_id', '$expiration')";
        $result = mysqli_query($link, $sql);
        if(!$result){
            echo  '<div class="alert alert-danger">There was an error storing data to remember you next time.</div>';  
        }else{
            echo "success";   
        }
    }
}
    }
?>

/* =========================================================================================================== */
/* Signup Form in index.php */
<!--Sign up form--> 
<form method="post" id="signupform">
	<div class="modal" id="signupModal" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<button class="close" data-dismiss="modal">&times;</button>
					<h4 id="myModalLabel">Sign up today and Start using our Online Notes App! </h4>
				</div>
				
				<div class="modal-body">
			  
					<!--Sign up message from PHP file-->
					<div id="signupmessage"></div>
			  
					<div class="form-group">
						<label for="username" class="sr-only">Username:</label>
						<input class="form-control" type="text" name="username" id="username" placeholder="Username" maxlength="30">
					</div>
					<div class="form-group">
						<label for="firstname" class="sr-only">Firstname:</label>
						<input class="form-control" type="text" name="firstname" id="firstname" placeholder="Firstname" maxlength="30">
					</div>
					<div class="form-group">
						<label for="lastname" class="sr-only">Lastname:</label>
						<input class="form-control" type="text" name="lastname" id="lastname" placeholder="Lastname" maxlength="30">
					</div>
					<div class="form-group">
						<label for="email" class="sr-only">Email:</label>
						<input class="form-control" type="email" name="email" id="email" placeholder="Email Address" maxlength="50">
					</div>
					<div class="form-group">
						<label for="password" class="sr-only">Choose a password:</label>
						<input class="form-control" type="password" name="password" id="password" placeholder="Choose a password" maxlength="30">
					</div>
					<div class="form-group">
						<label for="password2" class="sr-only">Confirm password</label>
						<input class="form-control" type="password" name="password2" id="password2" placeholder="Confirm password" maxlength="30">
					</div>
					<div class="form-group">
						<label for="phonenumber" class="sr-only">Telephone:</label>
						<input class="form-control" type="text" name="phonenumber" id="phonenumber" placeholder="Telephone Number" maxlength="15">
					</div>
					<div class="form-group">
						<label><input type="radio" name="gender" id="male" value="male">Male</label>
						<label><input type="radio" name="gender" id="female" value="female">Female</label>
					</div>
					<div class="form-group">
						<label for="moreinformation">Comments: </label>
						<textarea name="moreinformation" class="form-control" rows="5" maxlength="300"></textarea>
					</div>
				</div>
				
				<div class="modal-footer">
					<input class="btn green" name="signup" type="submit" value="Sign up">
					<button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
				</div>
			</div>
		</div>
	</div>
</form>

// ------------------------------------------------------------------------------------------
// javascript.js
//Ajax Call for the sign up form 
//Once the form is submitted
$("#signupform").submit(function(event){
    //hide message
    $("#signupmessage").hide();
    //show spinner
    $("#spinner").css("display", "block");
    //prevent default php processing
    event.preventDefault();
    //collect user inputs
    var datatopost = $(this).serializeArray();
	//console.log(datatopost);
    //send them to signup.php using AJAX
    $.ajax({
        url: "signup.php",
        type: "POST",
        data: datatopost,
        success: function(data){
            if(data){
                $("#signupmessage").html(data);
                //hide spinner
                $("#spinner").css("display", "none");
                //show message
                $("#signupmessage").slideDown();
            }
        },
        error: function(){
            $("#signupmessage").html("<div class='alert alert-danger'>There was an error with the Ajax Call. Please try again later.</div>");
            //hide spinner
            $("#spinner").css("display", "none");
            //show message
            $("#signupmessage").slideDown();
            
        }
    
    });

});

// ---------------------------------------------------------------------------------------------
//signup.php
<?php
//<!--Start session-->
session_start();
include('connection.php'); 

//<!--Check user inputs-->
//    <!--Define error messages-->
$missingUsername = '<p><strong>Please enter a username!</strong></p>';
$missingEmail = '<p><strong>Please enter your email address!</strong></p>';
$invalidEmail = '<p><strong>Please enter a valid email address!</strong></p>';
$missingPassword = '<p><strong>Please enter a Password!</strong></p>';
$invalidPassword = '<p><strong>Your password should be at least 6 characters long and inlcude one capital letter and one number!</strong></p>';
$differentPassword = '<p><strong>Passwords don\'t match!</strong></p>';
$missingPassword2 = '<p><strong>Please confirm your password</strong></p>';
$missingfirstname = '<p><strong>Please enter your firstname!</strong></p>';
$missinglastname = '<p><strong>Please enter your lastname!</strong></p>';
$missingPhone = '<p><strong>Please enter your phone number!</strong></p>';
$invalidPhoneNumber = '<p><strong>Please enter a valid phone number (digits only and less than 15 long)!</strong></p>';
$invalidEmail = '<p><strong>Please enter a valid email address!</strong></p>';
$missinggender = '<p><strong>Please select your gender</strong></p>';
$missinginformaton = '<p><strong>Please share a few more words about yourself.</strong></p>';
//    <!--Get username, email, password, password2-->
//Get username
if(empty($_POST["username"])){
    $errors .= $missingUsername;
}else{
    $username = filter_var($_POST["username"], FILTER_SANITIZE_STRING);   
}
//Get firstname
if(empty($_POST["firstname"])){
    $errors .= $missingfirstname;
}else{
    $firstname = filter_var($_POST["firstname"], FILTER_SANITIZE_STRING);
}
//Get lastname
if(empty($_POST["lastname"])){
    $errors .= $missinglastname;
}else{
    $lastname = filter_var($_POST["lastname"], FILTER_SANITIZE_STRING);
}
//Get email
if(empty($_POST["email"])){
    $errors .= $missingEmail;   
}else{
    $email = filter_var($_POST["email"], FILTER_SANITIZE_EMAIL);
    if(!filter_var($email, FILTER_VALIDATE_EMAIL)){
        $errors .= $invalidEmail;   
    }
}
//Get passwords
if(empty($_POST["password"])){
    $errors .= $missingPassword; 
}elseif(!(strlen($_POST["password"])>6
         and preg_match('/[A-Z]/',$_POST["password"])
         and preg_match('/[0-9]/',$_POST["password"])
        )
       ){
    $errors .= $invalidPassword; 
}else{
    $password = filter_var($_POST["password"], FILTER_SANITIZE_STRING); 
    if(empty($_POST["password2"])){
        $errors .= $missingPassword2;
    }else{
        $password2 = filter_var($_POST["password2"], FILTER_SANITIZE_STRING);
        if($password !== $password2){
            $errors .= $differentPassword;
        }
    }
}
//Get phone number
if(empty($_POST["phonenumber"])){
    $errors .= $missingPhone;
}elseif(preg_match('/\D/',$_POST["phonenumber"])){
    $errors .= $invalidPhoneNumber;    
}else{
    $phonenumber = filter_var($_POST["phonenumber"], FILTER_SANITIZE_STRING);
}
//Get gender
if(empty($_POST["gender"])){
    $errors .= $missinggender;
}else{
    $gender = $_POST["gender"];
}
//Get moreinformation
if(empty($_POST["moreinformation"])){
    $errors .= $missinginformaton;
}else{
    $moreinformation = filter_var($_POST["moreinformation"], FILTER_SANITIZE_STRING);
}
//If there are any errors print error
if($errors){
    $resultMessage = '<div class="alert alert-danger">' . $errors .'</div>';
    echo $resultMessage;
    exit;
}

//no errors

//Prepare variables for the queries
$username = mysqli_real_escape_string($link, $username);
$email = mysqli_real_escape_string($link, $email);
$password = mysqli_real_escape_string($link, $password);
//$password = md5($password);
$password = hash('sha256', $password);
//128 bits -> 32 characters
//256 bits -> 64 characters
//If username exists in the users table print error
$sql = "SELECT * FROM users WHERE username = '$username'";
$result = mysqli_query($link, $sql);
if(!$result){
    echo '<div class="alert alert-danger">Error running the query!</div>';
    //echo '<div class="alert alert-danger">' . mysqli_error($link) . '</div>';
    exit;
}
$results = mysqli_num_rows($result);
if($results){
    echo '<div class="alert alert-danger">That username is already registered. Do you want to log in?</div>';  exit;
}
//If email exists in the users table print error
$sql = "SELECT * FROM users WHERE email = '$email'";
$result = mysqli_query($link, $sql);
if(!$result){
    echo '<div class="alert alert-danger">Error running the query!</div>'; exit;
}
$results = mysqli_num_rows($result);
if($results){
    echo '<div class="alert alert-danger">That email is already registered. Do you want to log in?</div>';  exit;
}
//Create a unique  activation code
$activationKey = bin2hex(openssl_random_pseudo_bytes(16));
    //byte: unit of data = 8 bits
    //bit: 0 or 1
    //16 bytes = 16*8 = 128 bits
    //(2*2*2*2)*2*2*2*2*...*2
    //16*16*...*16
    //32 characters

//Insert user details and activation code in the users table

$sql = "INSERT INTO users (`username`, `email`, `password`, `activation`, `first_name`, `last_name`, `phonenumber`, `gender`, `moreinformation`) VALUES ('$username', '$email', '$password', '$activationKey', '$firstname', '$lastname', '$phonenumber', '$gender', '$moreinformation')";
$result = mysqli_query($link, $sql);
if(!$result){
    echo '<div class="alert alert-danger">There was an error inserting the users details in the database!</div>'; 
    exit;
}

//Send the user an email with a link to activate.php with their email and activation code
$message = "Please click on this link to activate your account:\n\n";
$message .= "http://completewebsite.karyakitabersama.com/carsharing-app/activate.php?email=" . urlencode($email) . "&key=$activationKey";
if(mail($email, 'Confirm your Registration', $message, 'From:'.'fortune00088@gmail.com')){
       echo "<div class='alert alert-success'>Thank for your registring! A confirmation email has been sent to $email. Please click on the activation link to activate your account.</div>";
}
        
?>

// ----------------------------------------------------------------------------------------
// activate.php
<?php
//The user is re-directed to this file after clicking the activation link
//Signup link contains two GET parameters: email and activation key
session_start();
include('connection.php');
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Account Activation</title>
        <link href="css/bootstrap.min.css" rel="stylesheet">
        <style>
            h1{
                color:purple;   
            }
            .activationForm{
                border:1px solid #7c73f6;
                margin-top: 50px;
                border-radius: 15px;
            }
        </style> 

    </head>
    <body>
		<div class="container-fluid">
			<div class="row">
				<div class="col-sm-offset-1 col-sm-10 activationForm">
					<h1>Account Activation</h1>
<?php
//If email or activation key is missing show an error
if(!isset($_GET['email']) || !isset($_GET['key'])){
    echo '<div class="alert alert-danger">There was an error. Please click on the activation link you received by email.</div>'; 
	exit;
}
//else
    //Store them in two variables
$email = $_GET['email'];
$key = $_GET['key'];
    //Prepare variables for the query
$email = mysqli_real_escape_string($link, $email);
$key = mysqli_real_escape_string($link, $key);
    //Run query: set activation field to "activated" for the provided email
$sql = "UPDATE users SET activation='activated' WHERE (email='$email' AND activation='$key') LIMIT 1";
$result = mysqli_query($link, $sql);
    //If query is successful, show success message and invite user to login
if(mysqli_affected_rows($link) == 1){
    echo '<div class="alert alert-success">Your account has been activated.</div>';
    echo '<a href="index.php" type="button" class="btn-lg btn-success">Log in<a/>';
    
}else{
    //Show error message
    echo '<div class="alert alert-danger">Your account could not be activated. Please try again later.</div>';
    echo '<div class="alert alert-danger">' . mysqli_error($link) . '</div>';
    
}
?>
            
				</div>
			</div>
		</div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script src="js/bootstrap.min.js"></script>
    </body>
</html>

/* ========================================================================================= */
// Update profile picture in profile.php
<!--Update picture-->    
		<form method="post" enctype="multipart/form-data" id="updatepictureform">
			<div class="modal" id="updatepicturemodal" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
				<div class="modal-dialog">
					<div class="modal-content">
						<div class="modal-header">
							<button class="close" data-dismiss="modal">&times;</button>
							<h4 id="myModalLabel">Upload Picture:</h4>
						</div>
						<div class="modal-body">
                  
							<!--Update picture message from PHP file-->
							<div id="updatepicturemessage"></div>
							<?php
								if(empty($picture)){
									echo "<div class='image_preview'><img id='previewing' src='profilepicture/noimage.jpg' /></div>";
								}else{
									echo "<div class='image_preview'><img id='previewing' src='$picture' /></div>";
								}
							?>
							<!--div class="form-inline"-->
								<div class="form-group">
									<label for="picture">Select a picture:</label>
									<input type="file" name="picture" id="picture">
								</div>
							<!--/div-->
						</div>
						<div class="modal-footer">
							<input class="btn green" name="updatepicture" type="submit" value="Submit">
							<button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button> 
						</div>
					</div>
				</div>
			</div>
		</form>
		
// ---------------------------------------------------------------------------------------
// profile.js : to update profile picture and AJAX call
//Update picture
var file; var imageType; var imageSize;
// Function to preview image after validation
//$(function() {
	$("#picture").change(function() {
		$("#updatepicturemessage").empty();
		file = this.files[0];
		console.log(file);
		console.log("Hello from Andy");
		imageType = file.type;
		imageSize = file.size;
		var acceptableTypes= ["image/jpeg","image/png","image/jpg"];
		if($.inArray(imageType, acceptableTypes) == -1){
			$("#updatepicturemessage").html("<div class='alert alert-danger'>Wrong file format!</div>");
			return false;
		}
		
		if(imageSize > 3*1024*1024){
			$("#updatepicturemessage").html("<div class='alert alert-danger'>Please upload an image less than 3Mb!</div>");
			return false;
		}
		
		// FileReader object will be used to convert our image to a binary string ; so we can view the image just selected!
		var reader = new FileReader();  
		
		reader.onload = imageIsLoaded;  //callback function; andy addeded this
		
		//Start the read operation --> Convert content into a data URL which is passed to the callback function imageIsLoaded.
		reader.readAsDataURL(this.files[0]);
		
	});
//});

function imageIsLoaded(event) {    //callback function see above; andy added this
	console.log(event);
	
	//if comment this out, still able to submit picture to server. BUT can not preview the image just selected.
    $('#previewing').attr('src', event.target.result);
};



$("#updatepictureform").submit(function(event) {
    //hide message
    $("#updatepicturemessage").hide();
    //show spinner
    $("#spinner").css("display", "block");
    event.preventDefault();
    if(!file){
        $("#spinner").css("display", "none");
        $("#updatepicturemessage").html('<div class="alert alert-danger">Please upload a picture!</div>');
        $("#updatepicturemessage").slideDown();
        return false;
    }
    var imagefile = file.type;
    var match= ["image/jpeg","image/png","image/jpg"];
        if($.inArray(imagefile, match) == -1){
            $("#updatepicturemessage").html('<div class="alert alert-danger">Wrong File Format</div>');
            $("#updatepicturemessage").slideDown();
            $("#spinner").css("display", "none");
            return false;
        }else{
            $.ajax({
                url: "updatepicture.php", 
                type: "POST",             
                data: new FormData(this), 
                contentType: false,       // The content type used when sending data to the server.
                cache: false,             // To unable request pages to be cached
                processData:false,        // To send DOMDocument or non processed data file it is set to false
                success: function(data){
                    if(data){
                        $("#updatepicturemessage").html(data);
                        //hide spinner
                        $("#spinner").css("display", "none");
                        //show message
                        $("#updatepicturemessage").slideDown();
                        //update picture in the settings
                    }else{
                        location.reload();   //andy added this: update success!
                    }

                },
                error: function(){
                    $("#updatepicturemessage").html("<div class='alert alert-danger'>There was an error with the Ajax Call. Please try again later.</div>");
                    //hide spinner
                    $("#spinner").css("display", "none");
                    //show message
                    $("#signupmessage").slideDown();

                }
            });
        }

});

// --------------------------------------------------------------------------------
// updatepicture.php  -- processing upload picture
<?php
session_start();
include('connection.php');

$user_id = $_SESSION['user_id'];

function changeProfilePicture($id, $tmp_name, $ext, $con){
    $permanentdestination = 'profilepicture/' . md5(time()) . ".$ext";
    if(move_uploaded_file($tmp_name, $permanentdestination)){
        $sql = "UPDATE users SET profilepicture='$permanentdestination' WHERE user_id='$id'";
        $result = mysqli_query($con, $sql);
        if(!$result){
            $resultMessage = '<div class="alert alert-danger">Unable to update profile picture. Please try again later.</div>';
            echo $resultMessage;
			exit;  //andy added this
        }
	}else{
		$resultMessage = '<div class="alert alert-warning"Unable to upload file. Please try again later.></div>'; 
		echo $resultMessage;
		exit;   //andy added this
	} 
}

//error messages to display
$noFileToUpload = "<p><strong>Please upload a file!</strong></p>";
//$fileAlreadyExists = "<p><strong>This file already exists!</strong></p>";
$wrongFormat = "<p><strong>Sorry, you can only upload jpeg, png and jpg format!</strong></p>";
$fileTooLarge = "<p><strong>You can only upload files smaller than 3Mo!</strong></p>";



//file details
$name = $_FILES["picture"]["name"];
$extension = pathinfo($name, PATHINFO_EXTENSION);
$type = $_FILES["picture"]["type"];
$size = $_FILES["picture"]["size"];
$fileerror = $_FILES["picture"]["error"];
$tmp_name = $_FILES["picture"]["tmp_name"];

//allowed formats to upload
$allowedFormats = array("jpeg"=>"image/jpeg", "jpg"=>"image/jpg", "png"=>"image/png");


//check for errors
if($fileerror == 4){
    $errors .=$noFileToUpload;   
}else{
//    if(file_exists($permanentdestination)){
//        $errors .= $fileAlreadyExists;   
//    }
    if(!in_array($type, $allowedFormats)){
        $errors .= $wrongFormat;   
    }elseif($size > 3*1024*1024){
        $errors .= $fileTooLarge;   
    }  
}



if($errors){
    $resultMessage = '<div class="alert alert-danger">' . $errors .'</div>'; 
    echo $resultMessage;
}else{
    changeProfilePicture($user_id, $tmp_name, $extension, $link);
} 

//print_r($_FILES);
if($_FILES["picture"]["error"]>0){
    $errors = '<p>There was an error: '. $_FILES["picture"]["error"] .'</p>';
    $resultMessage = '<div class="alert alert-danger">' . $errors .'</div>'; 
    echo $resultMessage;
}else{
//    echo "<p>File: ".  $_FILES["picture"]["name"] ."</p>";   
//    echo "<p>File type: ".  $_FILES["picture"]["type"] ."</p>";   
//    echo "<p>Temporary location: ".  $_FILES["picture"]["tmp_name"] ."</p>";   
//    echo "<p>File size: ".  $_FILES["picture"]["size"] ."</p>";   
}


?>

// ===================================================================================================
// profile table and updating user data -- username, email and password in profile.php

<!--Table Container-->
		<div class="container-fluid" id="container">
			<div class="row">
				<div class="col-md-offset-3 col-md-6">

					<h2>General Account Settings:</h2>
					<div class="table-responsive">
						<table class="table table-hover table-condensed table-bordered">
							<tr data-target="#updateusernameModal" data-toggle="modal">
								<td>Username</td>
								<td><?php echo $username; ?></td>
							</tr>
							<tr data-target="#updateemailModal" data-toggle="modal">
								<td>Email</td>
								<td><?php echo $email ?></td>
							</tr>
							<tr data-target="#updatepasswordModal" data-toggle="modal">
								<td>Password</td>
								<td>hidden</td>
							</tr>
						</table>
                  
					</div>
              
				</div>
			</div>
		</div>

		<!--Update username-->    
		<form method="post" id="updateusernameform">
			<div class="modal" id="updateusernameModal" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
				<div class="modal-dialog">
					<div class="modal-content">
						<div class="modal-header">
							<button class="close" data-dismiss="modal">&times;</button>
							<h4 id="myModalLabel">Edit Username: </h4>
						</div>
						
						<div class="modal-body">
                  
							<!--update username message from PHP file-->
							<div id="updateusernamemessage"></div>
                  

							<div class="form-group">
								<label for="username" >Username:</label>
								<input class="form-control" type="text" name="username" id="username" maxlength="30" value="<?php echo $username; ?>">
							</div>
                  
						</div>
              
						<div class="modal-footer">
							<input class="btn green" name="updateusername" type="submit" value="Submit">
							<button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button> 
						</div>
					</div>
				</div>
			</div>
		</form>

		<!--Update email-->    
		<form method="post" id="updateemailform">
			<div class="modal" id="updateemailModal" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
				<div class="modal-dialog">
					<div class="modal-content">
						<div class="modal-header">
							<button class="close" data-dismiss="modal">&times;</button>
							<h4 id="myModalLabel">Enter new email: </h4>
						</div>
              
						<div class="modal-body">
                  
							<!--Update email message from PHP file-->
							<div id="updateemailmessage"></div>
                  

							<div class="form-group">
								<label for="email" >Email:</label>
								<input class="form-control" type="email" name="email" id="email" maxlength="50" value="<?php echo $email ?>">
							</div>
						</div>
						
						<div class="modal-footer">
							<input class="btn green" name="updateemail" type="submit" value="Submit">
							<button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button> 
						</div>
					</div>
				</div>
			</div>
		</form>
      
		<!--Update password-->    
		<form method="post" id="updatepasswordform">
			<div class="modal" id="updatepasswordModal" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
				<div class="modal-dialog">
					<div class="modal-content">
						<div class="modal-header">
							<button class="close" data-dismiss="modal">&times;</button>
							<h4 id="myModalLabel">Enter Current and New password:</h4>
						</div>
						
						<div class="modal-body">
						  
							<!--Update password message from PHP file-->
							<div id="updatepasswordmessage"></div>
						  

							<div class="form-group">
								<label for="currentpassword" class="sr-only" >Your Current Password:</label>
								<input class="form-control" type="password" name="currentpassword" id="currentpassword" maxlength="30" placeholder="Your Current Password">
							</div>
							<div class="form-group">
								<label for="password" class="sr-only" >Choose a password:</label>
								<input class="form-control" type="password" name="password" id="password" maxlength="30" placeholder="Choose a password">
							</div>
							<div class="form-group">
								<label for="password2" class="sr-only" >Confirm password:</label>
								<input class="form-control" type="password" name="password2" id="password2" maxlength="30" placeholder="Confirm password">
							</div>  
						</div>
						
						<div class="modal-footer">
							<input class="btn green" name="updatepassword" type="submit" value="Submit">
							<button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button> 
						</div>
					</div>
				</div>
			</div>
		</form>
// ----------------------------------------------------------------------------------------------------------------
// supporting profile.js
// Ajax call to updateusername.php
$("#updateusernameform").submit(function(event){ 
    //prevent default php processing
    event.preventDefault();
    //collect user inputs
    var datatopost = $(this).serializeArray();
	//console.log(datatopost);
    //send them to updateusername.php using AJAX
    $.ajax({
        url: "updateusername.php",
        type: "POST",
        data: datatopost,
        success: function(data){
            if(data){
                $("#updateusernamemessage").html(data);
            }else{
                location.reload();   
            }
        },
        error: function(){
            $("#updateusernamemessage").html("<div class='alert alert-danger'>There was an error with the Ajax Call. Please try again later.</div>");
            
        }
    
    });

});

// Ajax call to updatepassword.php
$("#updatepasswordform").submit(function(event){ 
    //prevent default php processing
    event.preventDefault();
    //collect user inputs
    var datatopost = $(this).serializeArray();
//    console.log(datatopost);
    //send them to updateusername.php using AJAX
    $.ajax({
        url: "updatepassword.php",
        type: "POST",
        data: datatopost,
        success: function(data){
            if(data){
                $("#updatepasswordmessage").html(data);
            }
        },
        error: function(){
            $("#updatepasswordmessage").html("<div class='alert alert-danger'>There was an error with the Ajax Call. Please try again later.</div>");
            
        }
    
    });

});



// Ajax call to updateemail.php
$("#updateemailform").submit(function(event){ 
    //prevent default php processing
    event.preventDefault();
    //collect user inputs
    var datatopost = $(this).serializeArray();
//    console.log(datatopost);
    //send them to updateusername.php using AJAX
    $.ajax({
        url: "updateemail.php",
        type: "POST",
        data: datatopost,
        success: function(data){
            if(data){
                $("#updateemailmessage").html(data);
            }
        },
        error: function(){
            $("#updateemailmessage").html("<div class='alert alert-danger'>There was an error with the Ajax Call. Please try again later.</div>");
            
        }
    
    });

});

//-----------------------------------------------------------------------------
//upadateusername.php
<?php

//start session and connect
session_start();
include ('connection.php');

//get user_id
$id = $_SESSION['user_id'];

//Get username sent through Ajax
$username = $_POST['username'];

//Run query and update username
$sql = "UPDATE users SET username='$username' WHERE user_id='$id'";
$result = mysqli_query($link, $sql);

if(!$result){
    echo '<div class="alert alert-danger">There was an error updating storing the new username in the database!</div>';
}else{
    //$_SESSION['user_id'] = $username;
	$_SESSION['username'] = $username;
}

?>

//---------------------------------------------------------------------------
//updateemail.php
<?php
//start session and connect
session_start();
include ('connection.php');

//get user_id and new email sent through Ajax
$user_id = $_SESSION['user_id'];
$newemail = $_POST['email'];

//check if new email exists
$sql = "SELECT * FROM users WHERE email='$newemail'";
$result = mysqli_query($link, $sql);
$count = $count = mysqli_num_rows($result);
if($count>0){
    echo "<div class='alert alert-danger'>There is already as user registered with that email! Please choose another one!</div>"; exit;
}


//get the current email
$sql = "SELECT * FROM users WHERE user_id='$user_id'";
$result = mysqli_query($link, $sql);

$count = mysqli_num_rows($result);

if($count == 1){
    $row = mysqli_fetch_array($result, MYSQL_ASSOC); 
    $email = $row['email']; 
}else{
    echo "<div class='alert alert-danger'>There was an error retrieving the email from the database</div>";exit;   
}

//create a unique activation code
$activationKey = bin2hex(openssl_random_pseudo_bytes(16));
//$activationKey = bin2hex(openssl_random_pseudo_bytes(16));

//insert new activation code in the users table
//$sql = "UPDATE users SET activation2='$activationKey' WHERE user_id = '$user_id'";
$sql = "UPDATE users SET activation='$activationKey' WHERE user_id = '$user_id'";
$result = mysqli_query($link, $sql);
if(!$result){
    echo "<div class='alert alert-danger'>There was an error inserting the user details in the database.</div>";exit;
}else{
    //send email with link to activatenewemail.php with current email, new email and activation code
    $message = "Please click on this link prove that you own this email:\n\n";
	$message .= "http://completewebsite.karyakitabersama.com/carsharing-app2/activatenewemail.php?email=" . urlencode($email) . "&newemail=" . urlencode($newemail) . "&key=$activationKey";
	if(mail($newemail, 'Email Update for your Car Sharing App 2', $message, 'From:'.'fortune00088@gmail.com')){
       echo "<div class='alert alert-success'>An email has been sent to $newemail. Please click on the link to prove you own that email address.</div>";
	   //echo "<div class='alert alert-success'>" . $sql . "</div";
	}
}


?>

//----------------------------------------------------------------------------------
// activatenewemail.php
<?php
//The user is re-directed to this file after clicking the link received by email and aiming at proving they own the new email address
//link contains three GET parameters: email, new email and activation key
session_start();
include('connection.php');
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>New Email activation</title>
        <link href="css/bootstrap.min.css" rel="stylesheet">
        <style>
            h1{
                color:purple;   
            }
            .contactForm{
                border:1px solid #7c73f6;
                margin-top: 50px;
                border-radius: 15px;
				padding-bottom:20px;
            }
        </style> 

    </head>
        <body>
<div class="container-fluid">
    <div class="row">
        <div class="col-sm-offset-1 col-sm-10 contactForm">
            <h1>Email Activation</h1>
<?php
//If email, new email or activation key is missing show an error
if(!isset($_GET['email']) || !isset($_GET['newemail']) || !isset($_GET['key'])){
    echo '<div class="alert alert-danger">There was an error. Please click on the link you received by email.</div>'; 
	exit;
}
//else
    //Store them in three variables
$email = $_GET['email'];
$newemail = $_GET['newemail'];
$key = $_GET['key'];
    //Prepare variables for the query
$email = mysqli_real_escape_string($link, $email);
$newemail = mysqli_real_escape_string($link, $newemail);
$key = mysqli_real_escape_string($link, $key);
    //Run query: update email
//$sql = "UPDATE users SET email='$newemail', activation2='0' WHERE (email='$email' AND activation2='$key') LIMIT 1";
$sql = "UPDATE users SET email='$newemail', activation='activated' WHERE (email='$email' AND activation='$key') LIMIT 1";
$result = mysqli_query($link, $sql);
    //If query is successful, show success message
if(mysqli_affected_rows($link) == 1){
    session_destroy();
    setcookie("rememeberme", "", time()-3600);
    echo '<div class="alert alert-success">Your email has been updated.</div>';
    echo '<button type="button" class="btn btn-lg btn-success"><a href="index.php" style="color:black;">Log in<a/></button>';
    
}else{
    //Show error message
    echo '<div class="alert alert-danger">Your email could not be updated. Please try again later.</div>';
    echo '<div class="alert alert-danger">' . mysqli_error($link) . '</div>';
    
}
?>
            
        </div>
    </div>
</div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script src="js/bootstrap.min.js"></script>
        </body>
</html>

//--------------------------------------------------------------------------
// updatepassword.php
<?php
//start session and connect
session_start();
include ('connection.php');

//define error messages
$missingCurrentPassword = '<p><strong>Please enter your Current Password!</strong></p>';
$incorrectCurrentPassword = '<p><strong>The password entered is incorrect!</strong></p>';
$missingPassword = '<p><strong>Please enter a new Password!</strong></p>';
$invalidPassword = '<p><strong>Your password should be at least 6 characters long and inlcude one capital letter and one number!</strong></p>';
$differentPassword = '<p><strong>Passwords don\'t match!</strong></p>';
$missingPassword2 = '<p><strong>Please confirm your password</strong></p>';

//check for errors
if(empty($_POST["currentpassword"])){
    $errors .= $missingCurrentPassword;
}else{
    $currentPassword = $_POST["currentpassword"];
    $currentPassword = filter_var($currentPassword, FILTER_SANITIZE_STRING);
    $currentPassword = mysqli_real_escape_string ($link, $currentPassword);
    $currentPassword = hash('sha256', $currentPassword);
    //check if given password is correct
    $user_id = $_SESSION["user_id"];
    $sql = "SELECT password FROM users WHERE user_id='$user_id'";
    $result = mysqli_query($link, $sql);
    $count = mysqli_num_rows($result);
    if($count !== 1){
        echo '<div class="alert alert-danger">There was a problem running the query</div>';
    }else{
        $row = mysqli_fetch_array($result, MYSQL_ASSOC);
        if($currentPassword != $row['password']){
            $errors .= $incorrectCurrentPassword;
        }
    }
    
}

if(empty($_POST["password"])){
    $errors .= $missingPassword; 
}elseif(!(strlen($_POST["password"])>6
         and preg_match('/[A-Z]/',$_POST["password"])
         and preg_match('/[0-9]/',$_POST["password"])
        )
       ){
    $errors .= $invalidPassword; 
}else{
    $password = filter_var($_POST["password"], FILTER_SANITIZE_STRING); 
    if(empty($_POST["password2"])){
        $errors .= $missingPassword2;
    }else{
        $password2 = filter_var($_POST["password2"], FILTER_SANITIZE_STRING);
        if($password !== $password2){
            $errors .= $differentPassword;
        }
    }
}

//if there is an error print error message
if($errors){
    $resultMessage = "<div class='alert alert-danger'>$errors</div>";
    echo $resultMessage;   
}else{
    $password = mysqli_real_escape_string($link, $password);
    $password = hash('sha256', $password);
    //else run query and update password
    $sql = "UPDATE users SET password='$password' WHERE user_id='$user_id'";
    $result = mysqli_query($link, $sql);
    if(!$result){
        echo "<div class='alert alert-danger'>The password could not be reset. Please try again later.</div>";
    }else{
        echo "<div class='alert alert-success'>Your password has been updated successfully.</div>";
    }
    
}


?>

//===============================================================================













