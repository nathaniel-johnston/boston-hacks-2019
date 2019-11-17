import '../styles/index.scss';

// let payload = JSON.parse(
//     `
//     {
//         "pills": [{
//             "pill_id": "d208c413-eea9-40ae-8b42-097bfe2b06f8",
//             "name": "MOVANTIK",
//             "quantity": 20,
//             "time": "15:00:00",
//             "dose": 1
//         },
//         {
//             "pill_id": "e319d524-ffb0-51bf-9c53-108cgf3c17g9",
//             "name": "FARXIGA",
//             "quantity": 12,
//             "time": "20:00:00",
//             "dose": 2
//         }]
//     }
//     `
// );

var oldId = null;

function eventFire(el, etype){
    if (el.fireEvent) {
      el.fireEvent('on' + etype);
    } else {
      var evObj = document.createEvent('Events');
      evObj.initEvent(etype, true, false);
      el.dispatchEvent(evObj);
    }
  }

function animate_card(e) {
    e.preventDefault();

		if ($(this).hasClass('tabs-controls__link--active')) {
			return false;
		}

		var currentId = parseInt($(this).data('id'), 10);
        $('.tabs-controls__link--active').removeClass('tabs-controls__link--active');
        $('.card--current').removeClass('card--current');
        $(this).addClass('tabs-controls__link--active');
        
        $(`.card:nth-child(${currentId})`).addClass('card--current');

		if (currentId < oldId) { // item is hidden
			var timing = $('.card.hidden').length * 100;
			$('.card').each(function(index) {
				if (index > (currentId - 1 ) || index == (currentId - 1)) {
					window.setTimeout(function() {
						$('.card').eq(index).removeClass('hidden');
					}, timing - (index * 100));
				}
			});
		} else {
			$('.card').each(function(index) {
				if (index < (currentId - 1)) {
					window.setTimeout(function() {
						$('.card').eq(index).addClass('hidden');
					}, index * 100);
				}
			});
		}

	oldId = currentId;
}

$(document).ready(function() {
    /*
    <div class="card" id="6">
        <h1>F. Labore et dolore magna aliqua</h1>
        <p>
        Labore et dolore magna aliqua. Ut enim ad minim veniam,
        quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
        consequat. Duis aute irure dolor in reprehenderit in volupest laborum.
        </p>
    </div>
    */
    /*
    <li class="tabs-controls__item">
        <a href="#" class="tabs-controls__link" data-id="6">
            Tab F
        </a>
    </li>
    */
   let payload;

    $.ajax({
        url : "http://104.196.204.181:8080/pills/1",
        type: "GET",
        success: function(data, textStatus, jqXHR)
        {
            console.log('GET pills Success!');
            payload = JSON.parse(data);

            payload["pills"].forEach((pill, ind) => {
                const name = pill.name;
                const quantity = pill.quantity;
                const time = pill.time;
                const dose = pill.dose;
                console.log(name);
                // const tabs = $(`.tabs-controls:nth-child(${ind})`);
                let tab = document.querySelector('.tabs-controls').children[ind];
                if (tab == null) {
                    tab = document.createElement('li');
                    tab.className = "tabs-controls__item";
                    let anchor = document.createElement('a');
                    anchor.setAttribute('href', '#');
                    anchor.className = "tabs-controls__link";
                    anchor.addEventListener('click', animate_card);
                    anchor.setAttribute('data-id', ind + 1);

                    tab.appendChild(anchor);
                    document.querySelector('.tabs-controls').appendChild(tab);
                }
                tab = tab.children[0];
                tab.innerHTML = name;


                let card = document.querySelector('.cards-container').children[ind];
                if (card == null) {
                    card = document.createElement('div');
                    card.className = "card";
                    card.id = ind + 1;
            
                    let card_header = document.createElement('h1');
                    card_header.innerHTML = "Pill Name";
                    card_header.setAttribute('id', 'name');
                    card_header.setAttribute('contenteditable', true);
                    // let card_text = document.createElement('p');
                    let card_quantity = document.createElement('p');
            
                    card.appendChild(card_header);
                    card.appendChild(card_quantity);

                    document.querySelector('.cards-container').appendChild(card);
                }

                card.querySelector('h1').innerHTML = name;
                card.querySelector('h1').setAttribute('id', 'name');
                card.querySelector('p').remove();
                let card_quantity = document.createElement('p');
                card_quantity.setAttribute('id', 'quantity');
                card_quantity.innerHTML = 
                `
                <b>Quantity</b>: <span contenteditable="true">${quantity}</span>
                `;
                let card_time = document.createElement('p');
                card_time.setAttribute('id', 'time');
                card_time.innerHTML = 
                `
                <b>Time</b>: <span contenteditable="true">${time}</span>
                `;
                let card_dose = document.createElement('p');
                card_dose.setAttribute('id', 'dose');
                card_dose.innerHTML = 
                `
                <b>Dose</b>: <span contenteditable="true">${dose}</span>
                `;
                /*
                        <a><i class="fas fa-arrow-circle-up"></i></a>
        
                */
                // let save = document.createElement('a');
                // let save_icon = document.createElement('i');
                // save_icon.className = "fas fa-arrow-circle-up fa-lg";
        
                // save.appendChild(save_icon);
                // let save_wrapper = document.createElement('ul').appendChild(
                //     document.createElement('li').appendChild(
                //         save
                //     )
                // )
        
                card.appendChild(card_quantity);
                card.appendChild(card_time);
                card.appendChild(card_dose);
                // card.appendChild(save_wrapper);
        
                /*
                .innerHTML = 
                    `
                    <b>Quantity</b>: ${quantity}<br>
                    <b>Time</b>: ${time}<br>
                    <b>Dose</b>: ${dose}<br>
                    `;
                */
            });
        },
        error: function (jqXHR, textStatus, errorThrown)
        {
            console.log('Failure!');
        }
    });

	$('.tabs-controls__link').click(event, animate_card);
    

    // nav menu

    function openMenu (thisButton) {
    if(!thisButton.hasClass('active'))
    thisButton.addClass('active');
    else
    $('.radialnav, .submenu').removeClass('active');
    }

    /* On click of the ellipsis */
    $('.ellipsis').click(function (event) {
    event.preventDefault();

    openMenu($('.radialnav'));
    });

    $('#add-pill').click(function (event) {
        /*
        <div class="card" id="6">
            <h1>F. Labore et dolore magna aliqua</h1>
            <p>
            Labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat. Duis aute irure dolor in reprehenderit in volupest laborum.
            </p>
        </div>
        */
        /*
            <li class="tabs-controls__item">
            <a href="#" class="tabs-controls__link" data-id="6">
                Tab F
            </a>
            </li>
        */
        const card_count = document.querySelectorAll('.cards-container .card').length;

        let card = document.createElement('div');
        card.className = "card";
        card.setAttribute('new', 'true');
        card.id = card_count+1;

        let card_header = document.createElement('h1');
        card_header.innerHTML = "Pill Name";
        card_header.setAttribute('id', 'name');
        card_header.setAttribute('contenteditable', true);
        // let card_text = document.createElement('p');
        let card_quantity = document.createElement('p');
        card_quantity.setAttribute('id', 'quantity');
        card_quantity.innerHTML = 
        `
        <b>Quantity</b>: <span contenteditable="true">00</span>
        `;
        let card_time = document.createElement('p');
        card_time.setAttribute('id', 'time');
        card_time.innerHTML = 
        `
        <b>Time</b>: <span contenteditable="true">00:00:00</span>
        `;
        let card_dose = document.createElement('p');
        card_dose.setAttribute('id', 'dose');
        card_dose.innerHTML = 
        `
        <b>Dose</b>: <span contenteditable="true">0</span>
        `;

        card.appendChild(card_header);
        card.appendChild(card_quantity);
        card.appendChild(card_time);
        card.appendChild(card_dose);

        let tab = document.createElement('li');
        tab.className = "tabs-controls__item";

        let tab_title = document.createElement('a');
        tab_title.href = "#";
        tab_title.className = "tabs-controls__link";
        tab_title.addEventListener('click', animate_card);
        tab_title.setAttribute('data-id', card_count+1);
        tab_title.innerHTML = '💊New Pill ';

        tab.appendChild(tab_title);

        console.log(card);
        console.log(tab);

        document.querySelector('.tabs-controls').appendChild(tab);
        document.querySelector('.cards-container').appendChild(card);
        tab_title.click();
        // $('.tabs-controls__link')
        // console.log('hello');
    });

    $('#upload-pill').click(function (event) {
        let active_card = document.querySelector('.card--current');

        let new_pill = false;

        let name = active_card.querySelector('#name').innerHTML;
        if (active_card.hasAttribute('new')) {
            new_pill = true;
        }
        let pill_id = payload["pills"].find(el => el.name == name);
        if (pill_id) {
            pill_id = pill_id.pill_id;
        }
        let quantity = active_card.querySelector('#quantity').querySelector('span').innerHTML;
        let time = active_card.querySelector('#time').querySelector('span').innerHTML;
        let dose = active_card.querySelector('#dose').querySelector('span').innerHTML;

        if (new_pill) {
            let formData = { 
                "patient_id": 1,
                "name": name,
                "quantity": quantity,
                "time": time,
                "dose": dose
            };

            $.ajax({
                url : "http://104.196.204.181:8080/new/pill",
                type: "POST",
                data : JSON.stringify(formData),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(data, textStatus, jqXHR)
                {
                    // and then update quantity
                    console.log('POST upload Success!');
                    location.reload();
                },
                error: function (jqXHR, textStatus, errorThrown)
                {
                    console.log('Failure!');
                }
            });
        } else {
            let formData = { 
                "patient_id": 1,
                "name": name,
                "quantity": quantity,
                "time": time,
                "dose": dose
            };

            $.ajax({
                url : `http://104.196.204.181:8080/pill/${pill_id}`,
                type: "PUT",
                data : JSON.stringify(formData),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(data, textStatus, jqXHR)
                {
                    // and then update quantity
                    console.log('POST upload Success!');
                    location.reload();
                },
                error: function (jqXHR, textStatus, errorThrown)
                {
                    console.log('Failure!');
                }
            });
        }
    });

    $('#dispense-pill').click(function (event) {
        let active_card = document.querySelector('.card--current');

        // let active_id = parseInt(active_card.getAttribute('id'), 10);

        let name = active_card.querySelector('#name').innerHTML;

        let pill_id = payload["pills"].find(el => el.name == name);
        if (pill_id) {
            pill_id = pill_id.pill_id;
        }

        let dose = active_card.querySelector('#dose').querySelector('span').innerHTML;

        let formData = {"id": pill_id};

        console.log(formData);

        $.ajax({
            url : "http://104.196.204.181:8080/dispense",
            type: "POST",
            data : JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data, textStatus, jqXHR)
            {
                // and then update quantity
                console.log('POST dispense Success!');
                // let quantity = active_card.querySelector('#quantity').querySelector('span').innerHTML;
                // active_card.querySelector('#quantity').querySelector('span').innerHTML = quantity - dose;
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                console.log('Failure!');
            }
        });
    });

    $('#remind-pill').click(function (event) {
        let active_card = document.querySelector('.card--current');

        // let active_id = parseInt(active_card.getAttribute('id'), 10);

        let name = active_card.querySelector('#name').innerHTML;

        let pill_id = payload["pills"].find(el => el.name == name);
        if (pill_id) {
            pill_id = pill_id.pill_id;
        }
        
        let dose = active_card.querySelector('#dose').querySelector('span').innerHTML;

        let formData = {"id": pill_id};

        console.log(formData);

        $.ajax({
            url : "http://104.196.204.181:8080/remind",
            type: "POST",
            data : JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data, textStatus, jqXHR)
            {
                // and then update quantity
                console.log('POST remind Success!');
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                console.log('Failure!');
            }
        });
    });
});