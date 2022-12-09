"use strict";

// listen for button click to:

//// BOOK A RESERVATION /// 
function bookReservation(evt) {
    const date = evt.currentTarget.getAttribute("value");
    const startTime = evt.currentTarget.getAttribute("id"); 

    console.log("This is the date grabbed from the button that was clicked on")
    console.log(date)
    console.log("This is the start time that was grabbed from the button click")
    console.log(startTime)

    const reservation = {
        date : date,
        starttime : startTime,

    };

    fetch('/book_reservation.json', {
        method: 'POST',
        body: JSON.stringify(reservation),
        headers: {
          'Content-Type': 'application/json',
        },
    })


    // TODO: COMPLETE .then response 


}

let bookRecordButtons = document.querySelectorAll('.book-start-time');
    for (const button of bookRecordButtons) {
        button.addEventListener('click', bookReservation);
    }






//// EDIT A RESERVATION ///


//// DELETE A RESERVATION ///