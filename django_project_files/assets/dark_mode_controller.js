function setCookie(value) {
    document.cookie = "dark_mode =" + value + "; " +"path=/";
}
function deleteCookie() {
    setCookie("dark_mode", null, null);
}
function getCookie(key){
    cookie_value = decodeURIComponent(document.cookie);
    return cookie_value;
}

function switchbox(){
    var switch_position = document.body.getAttribute('data-bs-theme')

    if (switch_position == "dark"){
        document.body.setAttribute('data-bs-theme', 'light');
        deleteCookie();
        setCookie("light");
    }else{
        document.body.setAttribute('data-bs-theme', 'dark');
        deleteCookie();
        setCookie("dark");
    }
}

function auto_switch(value){
    console.log(value)
    document.body.setAttribute('data-bs-theme', value);
}

function dark_mode_state(){
    value = getCookie("dark_mode");
    const cookie_arr = value.split("; ");
    let result = "dark";

    cookie_arr.forEach(element => {
        if(element.indexOf("dark_mode") == 0){
            mode = "dark_mode";
            result = element.substring(mode.length+1);
            console.log(result);
        }
    })

    if(result != null){
        auto_switch(result)
    }
}

dark_mode_state();
