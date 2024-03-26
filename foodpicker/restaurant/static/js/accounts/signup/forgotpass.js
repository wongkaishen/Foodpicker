function ShowForgotPasswordForm() {

	SetTitle("Forgot Password");

	ShowHideForm("RegistrationFrom", "Hide");
	ShowHideForm("LoginFrom", "Hide");
	ShowHideForm("ForgotPasswordForm", "Show");

	ActiveInactiveBtn("ShowLoginBtn", "Inactive");
	ActiveInactiveBtn("ShowRegistrationBtn", "Inactive");
	ShowHideFromSwitchBtn("Hide");
}

function SetTitle(Title) {
	var formTitle = document.getElementById('formTitle');
	formTitle.innerHTML = Title;
}

function ShowHideForm(FormID, ShowOrHide) {
	var Form = document.getElementById(FormID);

	if (ShowOrHide == "Show") {
		Form.style.display = 'block';
	} else {
		Form.style.display = 'none';
	}
}

function ActiveInactiveBtn(ButtonID, ActiveORInactive) {
	debugger;
	var Button = document.getElementById(ButtonID);

	if (ActiveORInactive == "Active") {
		Button.classList.add('active');
	} else {
		Button.classList.remove('active');
	}
}

function ShowHideFromSwitchBtn(ShowOrHide) {
	var formSwitchBtn = document.getElementById('formSwitchBtn');
	if (ShowOrHide == 'Show') {
		formSwitchBtn.style.display = '';
	} else {
		formSwitchBtn.style.display = 'none';
	}
}

document.addEventListener("DOMContentLoaded", function () {
	ShowForgotPasswordForm();
});
// end