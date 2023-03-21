// get elements from DOM
const inputUrl = document.getElementById('url');
const convertButton = document.getElementById('convert');
const info = document.getElementById('info');
const result = document.getElementById('result');

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

const convertUrl = function() {
    // clear previous search results
    result.innerHTML = "";

    // get input value
    const source_url = inputUrl.value;
  
    // send API request to backend
    fetch(`/convert?url=${source_url}`)
      .then(response => response.json())
      .then(data => {
        // update output with converted link or error message
        console.log(data);
        console.log(data.service_url);
        const infoText = `${data.title} by ${data.artist}`
        info.innerText = infoText || "";
        const service_urls = data.service_url;
  
  
        // Map results data to result elements
        service_urls.map(service_url => {
          let result_section = document.createElement('section');
          result_section.classList.add('h-10', 'bg-blue-300', 'my-2', 'rounded-lg', 'text-slate-700', 'flex', 'flex-row');
  
          // Get the service name and result from the service_url object
          const serviceName = Object.keys(service_url)[0];
          const resultUrl = Object.values(service_url)[0];
  
          // Create a new element to contain logo and service name
          // and elements for logo and service name
          let logoWrapper = document.createElement('div');
          logoWrapper.classList.add('h-10', 'bg-gray-300', 'rounded', 'p-2', 'flex', 'items-center');
          
          let logoImg = document.createElement('img');
          logoImg.src = logos[serviceName];
          logoImg.alt = serviceName;
          logoImg.classList.add('py-0.5', 'h-10');
  
          let serviceNameElem = document.createElement('span');
          serviceNameElem.innerText = serviceName;
          serviceNameElem.classList.add('pl-px', 'text-gray-700');
  
          logoWrapper.appendChild(logoImg);
          logoWrapper.appendChild(serviceNameElem);
  
          // Create a new element for the track result
          let resultElem = document.createElement('span');
          resultElem.classList.add('pl-2')
          resultElem.innerText = resultUrl;
  
          // Append logo, service name, track result elements to the result_section
          result_section.appendChild(logoWrapper);
          result_section.appendChild(resultElem);
  
          result.appendChild(result_section);
        });
      })
      .catch(error => console.error(error));
};