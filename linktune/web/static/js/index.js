// get elements from DOM
const inputUrl = document.getElementById('url');
const convertButton = document.getElementById('convert');
const info = document.getElementById('info');
const results = document.getElementById('results');

const logos = {
  'Spotify': '../static/img/icons/Spotify_icon.svg',
  'Tidal': '../static/img/icons/Tidal_logo.svg',
  'Deezer': '../static/img/icons/deezer-logo.svg',
  'YouTube Music': '../static/img/icons/Youtube_Music_icon.svg',
  'Apple Music': '../static/img/icons/Apple_Music_icon.svg'
};

// event listeners for button click and pressing enter in input
convertButton.addEventListener('click', (event) => {
  event.preventDefault(); 
  convertUrl();
});

inputUrl.addEventListener('keydown', (event) => {
  if (event.key === "Enter"){
  event.preventDefault();
  convertUrl();
  }
});

// add event listener to results for clicking copy button
results.addEventListener('click', event => {
  if(event.target.classList.contains('copy-button')) {
    if(navigator.clipboard) {
      navigator.clipboard.writeText(event.target.id)
    } else {
    console.log(event.target.id);
    };
  }
})


const convertUrl = function() {
    // clear previous search results
    results.innerHTML = "";

    // get input value
    const source_url = inputUrl.value;
  
    // send API request to backend
    fetch(`/convert?url=${source_url}`)
      .then(response => response.json())
      .then(data => {
        // update output with converted link or error message
        const infoText = `${data.title} by ${data.artist}`
        info.innerText = infoText || "";
        const service_urls = data.service_url;
  
        // Map results data to result elements
        service_urls.map(service_url => {  
          // Get the service name and result from the service_url object
          const serviceName = Object.keys(service_url)[0];
          const resultUrl = Object.values(service_url)[0];

          // the result div nested in the li
          let resultDiv = document.createElement('div');
          resultDiv.classList.add('flex', 'items-center', 'space-x-3');
  
          // The list item that must be appended to the ul
          let resultElem = document.createElement('li');
          resultElem.classList.add('p-5', 'pb-10', 'sm:pb-4', 'hover:bg-sky-700');
  
          // Create a new element to contain logo and service name
          // and elements for logo and service name
          let logoWrapper = document.createElement('div');
          logoWrapper.classList.add('flex-shrink-0', 'pl-6');
          // get logo img from the service : logos map
          let logoImg = document.createElement('img');
          logoImg.src = logos[serviceName];
          logoImg.alt = serviceName;
          logoImg.classList.add('h-14', 'w-14');
          // append logo img to the logo wrapper div
          logoWrapper.appendChild(logoImg);

          // create div wrapper for service name
          let serviceNameWrapper = document.createElement('div');
          serviceNameWrapper.classList.add('min-w-0', 'flex-1');

          let serviceNameElem = document.createElement('p');
          serviceNameElem.innerText = serviceName;
          serviceNameElem.classList.add('text-2xl', 'font-medium', 'text-sky-100');
          // append service name element to wrapper element
          serviceNameWrapper.appendChild(serviceNameElem);

          // create elements for GO and COPY buttons
          let goButton = document.createElement('div');
          goButton.classList.add('inline-flex', 'text-2xl', 'items-center', 'text-base', 'font-semibold', 'text-sky-100', 'hover:text-fuchsia-400');
          // create anchor element and append
          let goLink = document.createElement('a');
          goLink.innerText = "GO";
          goLink.href = resultUrl;
          goLink.target = "_blank";
          goButton.appendChild(goLink);

          let copyButton = document.createElement('button');
          copyButton.classList.add('copy-button', 'text-2xl', 'inline-flex', 'items-center', 'text-base', 'font-semibold', 'text-sky-100', 'hover:text-fuchsia-400', 'pr-8');
          copyButton.innerText = "COPY";
          copyButton.id = resultUrl;

          resultDiv.appendChild(logoWrapper);
          resultDiv.appendChild(serviceNameWrapper);
          resultDiv.appendChild(goButton);
          resultDiv.appendChild(copyButton);
          resultElem.appendChild(resultDiv);
          results.appendChild(resultElem);
        });
      })
      .catch(error => console.error(error));
};