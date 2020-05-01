function realtimeClock() {
    var rtClock = new Date();

    var hour = rtClock.getHours();
    var minute = rtClock.getMinutes();
    var seconde = rtClock.getSeconds();

    var amPm = (hour < 12) ? "AM" : "PM";
    // hour = (hour > 12) ? hour -12 : hour;

    hour = ("0" + hour).slice(-2);
    minute = ("0" + minute).slice(-2);
    seconde = ("0" + seconde).slice(-2);

    document.getElementById('clock').innerHTML=
        hour + " : " + minute + " : " + seconde + " " + amPm ;
    var t = setTimeout(realtimeClock, 500);
    if((hour === 23) || (minute === 48) ) {
        window.prompt("hallo World!!")
    }
}
