function validatePassword() {
    const password = document.getElementById("password").value;
    const repeat_password = document.getElementById("confirmation").value;

    let lengthCheck = password.length >= 8;
    let uppercaseCheck = /[A-Z]/.test(password);
    let lowercaseCheck = /[a-z]/.test(password);
    let numberCheck = /[0-9]/.test(password);
    let specialCheck = /[!@#$%^&*]/.test(password);
    let repeatCheck = password === repeat_password && password.length > 0;

    updateRequirementDisplay("length", lengthCheck);
    updateRequirementDisplay("uppercase", uppercaseCheck);
    updateRequirementDisplay("lowercase", lowercaseCheck);
    updateRequirementDisplay("number", numberCheck);
    updateRequirementDisplay("special", specialCheck);
    updateRequirementDisplay("repeat", repeatCheck);

    document.getElementById("submitBtn").disabled = !(lengthCheck && uppercaseCheck && lowercaseCheck && numberCheck && specialCheck && repeatCheck);
}

function updateRequirementDisplay(requirementId, isValid) {
    const requirement = document.getElementById(requirementId);
    if (isValid) {
        requirement.classList.add("valid");
    } else {
        requirement.classList.remove("valid");
    }
}
