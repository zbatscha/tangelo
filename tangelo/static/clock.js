setInterval(displayclock, 500)
function displayclock() {

    var now = new Date();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();
    var month = now.getMonth();

    if (hour > 12) {
        hour = hour - 12
    }

    if (hour == 0) {
        hour = 12
    }

    if (hour < 10) hour = '0' + hour;
    if (minute < 10) minute = '0' + minute;
    if (second < 10) second = '0' + second;

    document.getElementById('time').innerHTML = hour + "&nbsp&nbsp" + minute + "&nbsp&nbsp" + second
}
