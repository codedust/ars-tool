// SPDX-FileCopyrightText: 2021 codedust
//
// SPDX-License-Identifier: EUPL-1.2

var arsMap = []; // list of ARS and area names
var layer; // shape layer
var map; // leaflet map
let offset = 0; // results offset
const PAGE_SIZE = 30;

const shapeStyle = {
	"color": "#2A8A15",
	"weight": 4,
	"opacity": 0.65
};

let elSearchInput = document.getElementById('search-input');
let elLoadMore = document.getElementById('a-load-more');
let elResultsSection = document.querySelector('.results');
let templateResult = document.getElementById('template-result').innerHTML;

// load ars list
fetch("ars_from_geojson.json").then(response => response.json()).then(function(responseJson) {
	// get query from location.hash
	if (location.hash) {
		elSearchInput.value = decodeURIComponent(location.hash.substr(1));
	}

	arsMap = responseJson;

	// show results
	showResults(elSearchInput.value, offset, true);

	// initialize leaflet map
	map = L.map('map').setView([51.5, 11], 6);

	// add the OpenStreetMap tiles and attribution
	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 19,
		attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a> | Gebietsumrisse: <a href="https://geoportal.de/Info/2E26078A-4D60-43E2-9728-DDC001DAABC3">GeoBasis-DE / BKG 2021 (Datendarstellung verändert)</a> | <a href="https://okfn.de/impressum/">Impressum</a>'
	}).addTo(map);

	// easteregg
	L.marker({lat: 49.8748, lon: 8.6539}).bindPopup('Grüße aus Darmstadt!').addTo(map);
});

// update results
function showResults(query, offset, autoExpand) {
	const queryLower = query.toLowerCase().trim();
	const queryIsNumeric = parseInt(queryLower).toString() == queryLower;
	let arsMapFiltered;

	if (queryLower.length == 0) {
		arsMapFiltered = [];
	} else {
		arsMapFiltered = Object.keys(arsMap)
		.filter(key => key.indexOf(queryLower) !== -1 || arsMap[key].toLowerCase().indexOf(queryLower) !== -1)
		.map(function(ars, i) { return {
			"ars": ars,
			"name": arsMap[ars],
			"shapeExists": ars.length == 12
		}});
	}

	if (arsMapFiltered.length >= 1 && arsMapFiltered[0]['shapeExists']) {
		fetch("geojson/" + arsMapFiltered[0]['ars'] + ".geojson.json").then(response => response.json()).then(function(geojson) {
			// remove existing shape layer from map
			if (layer) layer.remove();

			// add geojson shape layer
			layer = L.geoJSON(geojson['features'], {
				style: shapeStyle
			}).addTo(map);

			// zoom to shape
			map.fitBounds(layer.getBounds(), {
				"animate": true,
				"maxZoom": 13
			});
		});
	}

	// clear results section
	if (offset == 0) {
		elResultsSection.innerHTML = '';
	}

	// render results
	var rendered = Mustache.render(templateResult, arsMapFiltered.slice(offset, offset + PAGE_SIZE));
	elResultsSection.innerHTML += rendered;

	// update 'load more' link
	const items_remaining = arsMapFiltered.length - (offset + PAGE_SIZE);
	if (items_remaining > 0) {
		elLoadMore.classList.remove('is-hidden');
		elLoadMore.innerText = "Mehr laden (" + Math.min(PAGE_SIZE, items_remaining) + " von " + items_remaining + " weiteren)";
	} else {
		elLoadMore.classList.add('is-hidden');
	}
}

// search input event
elSearchInput.addEventListener('keyup', function() {
	offset = 0;
	showResults(elSearchInput.value, offset, false);
	location.hash = elSearchInput.value;
});

// result click event (show/hide table)
document.querySelector('.results').addEventListener('click', function(e) {
	let el = e.target;
	// traverse up the document tree
	while (el.parentElement) {
		// update location.href and search on ARS result click
		if (el.dataset.urn !== undefined) {
			location.hash = el.dataset.urn;
			elSearchInput.value = location.hash.substr(1);
			offset = 0;
			showResults(elSearchInput.value, offset, true);
			return;
		}
		el = el.parentElement;
	}
});

// load more event
elLoadMore.addEventListener('click', function(e) {
	e.preventDefault();
	offset += PAGE_SIZE;
	showResults(elSearchInput.value, offset, false);
});
