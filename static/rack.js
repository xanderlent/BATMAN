function $(id){ return document.getElementById(id); }
function qs(selector){ return document.querySelector(selector); }
function qsa(selector){ return document.querySelectorAll(selector); }
function checkStatus(response) {
	if (response.status >= 200 && response.status < 300) {
		return response.text();
	} else {
		console.log(response.status);
		return Promise.reject(new Error(response.status+': '+response.statusText)); 
	}
}

(function() {
	window.addEventListener("load", initRack);
})();

function initRack(){
	slots = qsa(".server")
	for (i in slots){
		slots[i].onclick = getDetails;
	}
}	
	
function getDetails(){
	// console.log(this);
	fetch('/rackdetail?rack='+this.getAttribute('data-rack')+
		'&server='+this.getAttribute('data-slot'))
		.then(checkStatus)
		.then(JSON.parse)
		.then(function(response){
			console.log(response)
			updateDetails(response);
		})
		.catch(function(){
			console.log("error getting server details");
		})
}

function updateDetails(data) {
	//TODO: make this pretty
	detailBlock = document.createElement('p');
	detailBlock.innerText = data.type+'\n'+data.size+'U\n';
	detailActions = document.createElement('div');
	detailActions.classList.add('detail-actions')
	functs = [];
	actionNames = [];
	for ( i in actionNames){
		action = document.createElement('div');
		action.classList.add('button');
		action.classList.add('detail-button');
		action.onclick = functs[i];
		detailActions.appendChild(action);
	}
	$('details').innerHTML = '';
	$('details').appendChild(detailBlock);
	$('details').appendChild(detailActions);
}