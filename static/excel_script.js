const form_price = document.getElementById('form-price');
const news_checker = document.getElementById('upd_img');
const div_generation = document.querySelector('div[class="generate"]');
const generation_checkers = document.getElementsByName('excel_generation');

news_checker.addEventListener('click', () => {
    if (news_checker.checked) {
        document.getElementById('news_input').style.display = 'block';
    } else {
        document.getElementById('news_input').style.display = 'none';
    }
})

div_generation.addEventListener('click', () => {
    let checked = null;
    let rozn = document.querySelector('.rozn_input');
    let opt = document.querySelector('.opt_input');

    for (const radio of generation_checkers) {
        if (radio.checked) {
            checked = radio;
        }
    }

    switch (checked.value) {
        case 'rozn':
            rozn.style.display = 'block';
            opt.style.display = 'none';
            break;
        case 'opt':
            opt.style.display = 'block';
            rozn.style.display = 'none';
            break;
        case 'both':
            rozn.style.display = 'block';
            opt.style.display = 'block';
            break;
    }
})

// form_price.addEventListener('submit', (e) => {
//     e.preventDefault();
//     fetch('/excel-api/', {
//         method: 'POST',
//         body: new FormData(form_price)
//     }).then((resp) => {
//         console.log(resp.text)
//     })
// })