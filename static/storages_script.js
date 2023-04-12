// const form_sklad = document.getElementById('form-sklad');

// form_sklad.addEventListener('submit', (e) => {

//     e.preventDefault();
//     console.log(JSON.stringify(new FormData(form_sklad)).toString())
//     fetch('https://webhook.site/b9ed395e-fe05-4f91-bc13-ec6c0a5d5491', {
//         method: 'POST',
//         body: JSON.stringify({"price_maker": JSON.stringify(new FormData(form_sklad))}),
//         dataType: 'json'
//     }).then((resp) => {
//         console.log(resp.text);
//     })
// });