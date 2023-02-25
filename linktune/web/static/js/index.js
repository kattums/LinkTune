// get elements from DOM
const inputUrl = document.getElementById('url');
const inputTargetService = document.getElementById('service');
const convertButton = document.getElementById('convert');
const info = document.getElementById('info');
const result = document.getElementById('result');

const checkboxes = document.querySelector('ul')
let selected = [];
// event listener for checkbox update
checkboxes.addEventListener('change', (event) => {
  if (event.target.type === 'checkbox') {
    const checked = document.querySelectorAll('input[type="checkbox"]:checked')
    selected = Array.from(checked).map(x => x.value)
  }
  console.log(selected);
});

// TODO: implement ability to search multiple services at once using checkbox selection
// not sure if I should have it make multiple request from frontend or backend

// event listener for button
convertButton.addEventListener('click', (event) => {
  // prevent default form submission behavior
  event.preventDefault();

  // get input values
  const url = inputUrl.value;
  const targetService = inputTargetService.value;

  // send API request to backend
  fetch(`/convert?url=${url}&target_service=${targetService}`)
    .then(response => response.json())
    .then(data => {
      // update output with converted link or error message
      info.innerText = data.info || "";
      result.innerText = data.url || data;
    })
    .catch(error => console.error(error));
});