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

class Action {
	constructor(node){
		this.node = node;
	}
}

let actions = {};

(function() {
	window.onload = function(){
		rerenderActions();
	};
})();

function rerenderActions(){
	let arr = qsa(".action");
	
	for (let i = 0; i < arr.length; i++){
		//console.log(arr[i].querySelector("h4").innerText);
		actions[arr[i].querySelector("h4").innerText] = new Action(arr[i]);
	}
	//console.log(actions);
	$("actions").innerHTML = "";
	for (let i in actions){
		//console.log(actions[i].node.querySelector("h4").innerText);
		let actionButton = document.createElement("div");
		actionButton.innerText = actions[i].node.querySelector("h4").innerText;
		actionButton.onclick = actionButtonHandler;
		actionButton.classList.add("button");
		actionButton.classList.add("action-button");
		$("actions").appendChild(actionButton);
	}
	//console.log(actions);
}

function actionButtonHandler(){
	//console.log(this.innerText);
	createDialogWindow(actions[this.innerText].node);
}

function createDialogWindow(contained){
	//make the close button
	let closeButton = document.createElement("span");
	closeButton.classList.add("w3-button");
	closeButton.classList.add("w3-display-topright");
	closeButton.innerText = String.fromCharCode(215);
	closeButton.onclick = closeDialogWindow;
	
	let dialogBox = document.createElement("div");
	dialogBox.classList.add("w3-container");
	dialogBox.appendChild(closeButton);
	dialogBox.appendChild(contained);
	
	let dialogContent = document.createElement("div");
	dialogContent.classList.add("w3-modal-content");
	dialogContent.appendChild(dialogBox);
	
	let dialogWindow = document.createElement("div");
	dialogWindow.id = "dialog-window";
	dialogWindow.classList.add("w3-modal");
	dialogWindow.appendChild(dialogContent);
	
	$("wrapper").appendChild(dialogWindow);
}

function closeDialogWindow(){
	$("wrapper").removeChild(qs("#dialog-window"));
}

function reloadData(){
	// fetch(window.location.hostname+'/tree')
		// .then(checkStatus)
		// .then(JSON.parse)
		// .then(function(response){
			// json = response;
			// st.loadJSON(response);
			// st.compute();
			// st.onClick(st.root);
		// }).catch(function(){});
}

