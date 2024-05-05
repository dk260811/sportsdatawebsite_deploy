
/*
function applyFilters() {
    var season = document.getElementById('season').value;
    var league = document.getElementById('league').value;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/update-table/?season=' + season + '&league=' + league, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('team-table').innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}
*/


function applyFilters() {
    var season, league, homeAway;
    var isIndexPage = document.getElementById('isIndexPage').value;
    var isTablePage;
    try {
        var isTablePage = document.getElementById('isTablePage').value;
      } catch (error) {
        // Code to handle the exception
        var isTablePage = 'true'
      }
    console.log(isIndexPage);
    console.log(isTablePage);
  
    //season = document.getElementById('season').value;
    //league = document.getElementById('league').value;
  
    // Check if called from index page (no existing table data)
    // Check if the request originates from the index page
    if (isTablePage === 'true')  {
    // Get season and league from select elements on index page
    season = document.getElementById('season').value; // Use 'all' if no value selected
    league = document.getElementById('league').value; // Use 'all' if no value selected
  } else {
    // Get season and league from existing table
    season = document.getElementById('season').value;
    league = document.getElementById('league').value;
    homeAway = document.getElementById('homeaway').value;
    //homeAway = 'Homegame';
    console.log(homeAway);
  }
  
    // Update homeAway based on the clicked button
    if (homeAway === 'all') {
      homeAway = 'all';
    } else if (homeAway === 'Homegame') {
      homeAway = 'Homegame';
    } else if (homeAway === 'Awaygame'){
      homeAway = 'Awaygame';
    } else {
      homeAway = 'all';  
    }

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/update-table/?season=' + season + '&league=' + league + '&homeAway=' + homeAway, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('team-table').innerHTML = xhr.responseText;
        }
    };
    xhr.send();
  
    /*
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/update-table/?season=${season}&league=${league}&home_away=${homeAway}`, true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        document.getElementById('team-table').innerHTML = xhr.responseText;
      }
    };
    xhr.send();
    */
  }
  
  // Helper function to get parameter value by name from URL
  function getParameterByName(name) {
    var url = window.location.href;
    var name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '=([^&#]*)');
    var results = regex.exec(url);
    if (results != null) {
      return decodeURIComponent(results[1].replace(/\+/g, ' '));
    }
    return null;
  }
  


function sortTable(columnIndex) {
    var table, rows, switching, i, x, y, shouldSwitch, sortDirection, header;
    table = document.querySelector(".team-table");
    switching = true;
    sortDirection = "asc"; // Default sorting direction is ascending
    header = table.rows[0].getElementsByTagName("th")[columnIndex];
  
    // Toggle sorting direction indicators
    if (header.classList.contains("asc")) {
      header.classList.remove("asc");
      header.classList.add("desc");
      sortDirection = "desc";
    } else if (header.classList.contains("desc")) {
      header.classList.remove("desc");
      header.classList.add("asc");
      sortDirection = "asc";
    } else {
      header.classList.add("asc");
    }
  
    while (switching) {
      switching = false;
      rows = table.rows;
  
      // Loop from the second row (skipping the header)
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("td")[columnIndex];
        y = rows[i + 1].getElementsByTagName("td")[columnIndex];
  
        // Extract numeric values from cell content (handling empty cells)
        var xValue = parseFloat(x.innerHTML.trim().replace(",", "")) || 0;
        var yValue = parseFloat(y.innerHTML.trim().replace(",", "")) || 0;
  
        // Compare based on sort direction
        if ((sortDirection === "asc" && xValue > yValue) ||
            (sortDirection === "desc" && xValue < yValue)) {
          shouldSwitch = true;
          break;
        }
      }
  
      if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true; // Continue looping until no more switching is needed
      }
    }
  }


function toggleColumn(kpiName) {
    var table = document.querySelector(".team-table");
    var columnIndex = -1;

    // Find the index of the column with the given KPI name
    var headers = table.rows[0].getElementsByTagName("th");
    for (var i = 0; i < headers.length; i++) {
        if (headers[i].innerText === kpiName) {
            columnIndex = i;
            break;
        }
    }

    if (columnIndex === -1) {
        console.error("Column with name '" + kpiName + "' not found.");
        return;
    }

    // Toggle "hidden" class on all corresponding header and data cells
    var headerToToggle = table.rows[0].getElementsByTagName("th")[columnIndex];
    headerToToggle.classList.toggle("hidden");

    var cellsToToggle = document.querySelectorAll('.team-table tr td:nth-child(' + (columnIndex + 1) + ')');
    cellsToToggle.forEach(function(cell) {
        cell.classList.toggle("hidden");
    });

    // Toggle active class on clicked KPI
    var kpi = document.querySelector('.kpi[data-kpi="' + kpiName.trim() + '"]');
    kpi.classList.toggle("active");
}


var isTotals = true; // Initially, show totals

function toggleTotalsAverages() {
    var table = document.querySelector(".team-table");

    // Get all data cells in the table (excluding "Games Played" column)
    var dataCells = document.querySelectorAll('.team-table tr td:not(:nth-child(4))');

    // Toggle between showing totals and averages
    isTotals = !isTotals;

    // Update button text accordingly
    var button = document.getElementById("totalsAveragesButton");
    button.textContent = isTotals ? "Totals" : "Averages";

    // Calculate totals or averages based on the current state
    dataCells.forEach(function(cell) {
        var columnIndex = cell.cellIndex; // Get the index of the current cell's column
        var gamesPlayed = parseFloat(cell.parentElement.querySelector('td:nth-child(4)').textContent);
        var value = parseFloat(cell.textContent);

        // Check if the current cell belongs to the excluded columns
        if (columnIndex !== 0 && columnIndex !== 1 && columnIndex !== 2) {
            if (isTotals) {
                cell.textContent = Math.round(value * gamesPlayed); // Display totals as whole numbers
            } else {
                var average = value / gamesPlayed;
                cell.textContent = average.toFixed(2); // Display averages with 2 decimal places
            }
        }
    });
}


/*
function toggleTotalsAverages() {
    var table = document.querySelector(".team-table");

    // Get all data cells in the table (excluding "Games Played" column)
    var dataCells = document.querySelectorAll('.team-table tr td:not(:nth-child(4))');

    // Toggle between showing totals and averages
    isTotals = !isTotals;

    // Update button text accordingly
    var button = document.getElementById("totalsAveragesButton");
    button.textContent = isTotals ? "Totals" : "Averages";

    // Calculate totals or averages based on the current state
    dataCells.forEach(function(cell) {
        var columnIndex = cell.cellIndex; // Get the index of the current cell's column
        var gamesPlayed = parseFloat(cell.parentElement.querySelector('td:nth-child(4)').textContent);
        var value = parseFloat(cell.textContent);

        // Check if the current cell belongs to the excluded columns
        if (columnIndex !== 0 && columnIndex !== 1 && columnIndex !== 2) {
            if (isTotals) {
                cell.textContent = (value * gamesPlayed).toFixed(2); // Format totals with 2 decimal places
            } else {
                var average = value / gamesPlayed;
                cell.textContent = average.toFixed(2); // Format averages with 2 decimal places
            }
        }
    });
}





*/

