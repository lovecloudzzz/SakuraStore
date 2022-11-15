function checkRegForm(event) {
    let login = document.getElementById("login")
    let email = document.getElementById("email")
    let password = document.getElementById("password")
    let confirm_password = document.getElementById("confirm_password")
    if ((login.value.replaceAll(" ", "") === '') || (email.value.replaceAll(" ", "") === '') || (password.value.replaceAll(" ", "") === '') || (confirm_password.value.replaceAll(" ", "") === '') || (password.value.includes(" ")) || (email.value.includes(" ")) || (login.value.includes(" ")) || (confirm_password.value.includes(" ")))
    {
        window.alert('Пустые поля')
        event.preventDefault()
    } else if (password.value !== confirm_password.value)
    {
        window.alert('Пароль не подтвержден')
        event.preventDefault()
    }
}


function checkLogForm(event) {
    let email = document.getElementById("email")
    let password = document.getElementById("password")
    if ((email.value.replaceAll(" ", "") === '') || (password.value.replaceAll(" ", "") === '') || password.value.find(" ") || (password.value.includes(" ")) || (email.value.includes(" ")))
    {
        window.alert('Пустые поля')
        event.preventDefault()
    }
}


function checkProfForm(event) {
    let login = document.getElementById("login")
    let password = document.getElementById("password")
    if ((login.value.replaceAll(" ", "") === '') || (password.value.replaceAll(" ", "") === '') || (password.value.includes(" ")) || (login.value.includes(" ")))
    {
        window.alert('Пустые поля')
        event.preventDefault()
    }
}