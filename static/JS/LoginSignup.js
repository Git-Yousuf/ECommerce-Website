function validateForm() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username) {
        usernameError.textContent = 'UserName is Required.';
        return false;
    } else {
        usernameError.textContent = '';
    }

    if (!password) {
         passwordError.textContent = ('Password is required.');
        return false;
    } else {
        passwordError.textContent = '';
    }
    
    // if (username !== 'correctUsername' || password !== 'correctPassword') {
    // loginError.textContent = 'Invalid username or password.';
    // return false;
    // } else {
    //     loginError.textContent = '';
    // }

    /*

    To Check Username and Password Individually and print the Error Message.
    if (username !== 'correctUsername') {
        CorrectUserError.textContent = 'Invalid username.';
        return false;
    }

    if ( password !== 'correctPassword'){
        CorrectPasswordError.textContent = 'Invalid Password.';
        return false;
    }
    */

    return true;
}

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