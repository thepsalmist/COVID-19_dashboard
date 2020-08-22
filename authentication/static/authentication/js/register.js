
//username field event listener
const usernameField = document.querySelector("#usernameField");
const feedbackArea = document.querySelector(".invalid-feedback");


//add keyup event listner
usernameField.addEventListener('keyup', (e) => {
    console.log('99898988');
    //declare usernameValue const, fetches value at keyup
    const usernameValue = e.target.value;

    console.log("usernameValue", usernameValue);
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = 'none';


    if (usernameValue.length > 0) {
        //make API call, returns promise
        fetch("/auth/validate_username/", {
            body: JSON.stringify({ username: usernameValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.username_error) {
                    usernameField.classList.add("is-invalid");
                    feedbackArea.style.display = 'block';
                    feedbackArea.innerHTML = `<p>${data.username_error}</p>`
                }
            });

    }

});