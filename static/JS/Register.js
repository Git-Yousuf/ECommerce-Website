const inputs = document.querySelectorAll(".input");


function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});

function validateForm(event) {
	var fname = document.getElementById("fname").value;
	if (fname == "") {
	  alert("First Name must be filled out");
	  event.preventDefault();
	  return false;
	}

	var lname = document.getElementById("lname").value;
	if (lname == "") {
	  alert("Last Name must be filled out");
	  event.preventDefault();
	  return false;
	}

	var email = document.getElementById("email").value;
	if (email == "") {
	  alert("Email must be filled out");
	  event.preventDefault();
	  return false;
	}

	var phone = document.getElementById("phone").value;
	if (phone == "") {
	  alert("Phone Number must be filled out");
	  event.preventDefault();
	  return false;
	}

	var username = document.getElementById("username").value;
	if (username.trim() === "") {
	  alert("Username must be filled out");
	  event.preventDefault();
	  return false;
	}

	var password = document.getElementById("password").value;
	if (password == "") {
	  alert("Password must be filled out");
	  event.preventDefault();
	  return false;
	}

	var confirm_password =
	  document.getElementById("confirm_password").value;
	if (confirm_password == "") {
	  alert("Confirm Password must be filled out");
	  event.preventDefault();
	  return false;
	}

	if (password != confirm_password) {
	  alert("Password and Confirm Password must be same");
	  event.preventDefault();
	  return false;
	}
  }