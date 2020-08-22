
//username field event listener
const usernameField = document.querySelector("#usernameField");
const usernamefeedbackArea = document.querySelector(".usernamefeedBackArea");
const emailField = document.querySelector('#emailField');
const emailfeedbackArea = document.querySelector(".emailfeedBackArea");
const submitBtn = document.querySelector(".submit-btn");


//add keyup event listner
usernameField.addEventListener('keyup', (e) => {
    //declare usernameValue const, fetches value at keyup
    const usernameValue = e.target.value;

    //
    usernameField.classList.remove("is-invalid");
    usernamefeedbackArea.style.display = 'none';


    if (usernameValue.length > 0) {
        //make API call, returns promise
        fetch("/auth/validate_username/", {
            body: JSON.stringify({ username: usernameValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.username_error) {
                    submitBtn.disabled = true;
                    usernameField.classList.add("is-invalid");
                    usernamefeedbackArea.style.display = 'block';
                    usernamefeedbackArea.innerHTML = `<p>${data.username_error}</p>`
                }
                else {
                    submitBtn.removeAttribute("disabled");
                }
            });

    }

});

//add event listener to emailvalidator
emailField.addEventListener('keyup', (e) => {
    const emailValue = e.target.value;

    emailField.classList.remove("is-invalid");
    emailfeedbackArea.style.display = 'none';

    if (emailValue > 0) {
        //make API call
        fetch("/auth/validate_email/", {
            body: JSON.stringify({ email: emailValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.email_error) {
                    submitBtn.disabled = true;
                    emailField.classList.add("is-invalid");
                    emailfeedbackArea.style.display = 'block';
                    emailfeedbackArea.innerHTML = `<p>${data.email_error}</p>`

                }
                else {
                    submitBtn.removeAttribute("disabled");
                }
            });
    }
});

