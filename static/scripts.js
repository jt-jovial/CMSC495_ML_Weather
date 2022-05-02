/**
 * @fileoverview Script file governing menus on webpage
 * @author John Prah
 * @version 04/30/2022
 * @see CMSC495 Team 6 - Fairbanks Machine Learning Project
 */

/**
 * Top level function resets the dynamic entry locations within the webpage
 *     and drive the form creation process.  All form elements are under "ak-form"
 * @param input The top level dropdown menu selection driving the rest of the form
 */
function select(input) {
    let value = input.value;
    //reset form
    let df = document.getElementById("dynamic-form");
    let dl = document.getElementById("daylight-form");
    let bt = document.getElementById("execute-button");
    df.innerHTML = "<p id=\"dynamic-form\"></p>"
    dl.innerHTML = "<p id=\"daylight-form\"></p>"
    bt.innerHTML = "<p id=\"execute-button\"></p>"

    form_maker(value);
}

/**
 * Drives the part of the menu related to daylight hour preference
 * @param in_bool selection of daylight preference, if true will provide input to user
 */
function day_input(in_bool) {
    let insertpoint = document.getElementById("daylight-form");
    let DAYLIGHT = document.createElement("input");

    if (in_bool === "true") {
        DAYLIGHT.setAttribute("type", "number");
        DAYLIGHT.setAttribute("name", "daylight");
        DAYLIGHT.setAttribute("id", "daylight");
        DAYLIGHT.setAttribute("form", "ak-form");
        DAYLIGHT.setAttribute("min", "3.5");
        DAYLIGHT.setAttribute("max", "22");
        DAYLIGHT.setAttribute("step", "0.5");
        DAYLIGHT.setAttribute("required", "");
        let DAYNUMTEXT = document.createTextNode("How many daylight hours would you prefer? (3.5-22): ");
        insertpoint.appendChild(DAYNUMTEXT);
        insertpoint.append(DAYLIGHT);
    }
    else {
        insertpoint.innerHTML = "<p id=\"daylight-form\"></p>"
    }
}

/**
 * Main form, calls sub functions based on top level selection through a switch box check
 * @param input Top level menu selection
 */
function form_maker(input) {
    /**
     * Temperature priority form
     */
    function temp_form() {
        // Create a form dynamically
        let form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "result");
        form.setAttribute("id", "ak-form");

        // Create an input element for temperature
        let TEMP = document.createElement("input");
        TEMP.setAttribute("type", "number");
        TEMP.setAttribute("name", "temp");
        TEMP.setAttribute("placeholder", "Degrees");
        TEMP.setAttribute("min", "-65");
        TEMP.setAttribute("max", "100");
        TEMP.setAttribute("required", "");

        // Create a selection element for daylight hours
        let DAY = document.createElement("select");
        DAY.setAttribute("name", "day-check");
        DAY.setAttribute("id", "day-check");
        DAY.setAttribute("form", "ak-form");
        DAY.add(new Option("No", "false", true));
        DAY.add(new Option("Yes", "true", false));

        // Create a submit button
        let s = document.createElement("input");
        s.setAttribute("type", "submit");
        s.setAttribute("value", "Submit");
        s.setAttribute("name", "temp_submit");
        s.setAttribute("id", "button");
        s.setAttribute("form", "ak-form");

        // Append the temp input to the form
        let TEMPTEXT = document.createTextNode("What is your preferred temperature? (Fahrenheit): ")
        form.appendChild(TEMPTEXT);
        form.append(TEMP);
        form.innerHTML += "<br><br>";

        // Append the daylight select to the form
        let DAYTEXT = document.createTextNode("Do you have a preference with regards to number of daylight hours?")
        form.appendChild(DAYTEXT);
        form.innerHTML += "<br>";
        form.append(DAY);

        // Append form to correct location in page
        document.getElementById("dynamic-form")
            .appendChild(form);
        document.getElementById("execute-button").append(s);

        // Create a listener for daylight preference selection
        document.getElementById("day-check").addEventListener(
            "change", function() {day_input(this.value);}, false);
    }

    /**
     * Daylight priority form
     * Skips most form elements in deference to daylight input
     */
    function day_form() {
        // Create a form dynamically
        let form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "result");
        form.setAttribute("id", "ak-form");

        // Call the day input method directly
        day_input("true")

        // Create a submit button
        let s = document.createElement("input");
        s.setAttribute("type", "submit");
        s.setAttribute("value", "Submit");
        s.setAttribute("name", "day_submit");
        s.setAttribute("id", "button");
        s.setAttribute("form", "ak-form");

        // Append form to correct location in page
        document.getElementById("dynamic-form")
            .appendChild(form);
        document.getElementById("execute-button").append(s);
    }

    /**
     * Snowfall priority form
     */
    function snow_form() {
        // Create a form dynamically
        let form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "result");
        form.setAttribute("id", "ak-form");

        // Create an input element for snowfall
        let SNOW = document.createElement("input");
        SNOW.setAttribute("type", "number");
        SNOW.setAttribute("name", "snow");
        SNOW.setAttribute("form", "ak-form");
        SNOW.setAttribute("placeholder", "Inches");
        SNOW.setAttribute("min", "0");
        SNOW.setAttribute("max", "24")
        SNOW.setAttribute("required", "");

        // Create a selection element for daylight hours
        let DAY = document.createElement("select");
        DAY.setAttribute("name", "day-check");
        DAY.setAttribute("id", "day-check");
        DAY.setAttribute("form", "ak-form");
        DAY.add(new Option("No", "false", true));
        DAY.add(new Option("Yes", "true", false));

        // Create a submit button
        let s = document.createElement("input");
        s.setAttribute("type", "submit");
        s.setAttribute("value", "Submit");
        s.setAttribute("name", "snow_submit");
        s.setAttribute("id", "button");
        s.setAttribute("form", "ak-form");

        // Append the temp input to the form
        let SNOWTEXT = document.createTextNode("How much accumulated snow would you like to see? (0-24in): ")
        form.appendChild(SNOWTEXT);
        form.append(SNOW);
        form.innerHTML += "<br><br>";

        // Append the daylight select to the form
        let DAYTEXT = document.createTextNode("Do you have a preference with regards to number of daylight hours?")
        form.appendChild(DAYTEXT);
        form.innerHTML += "<br>";
        form.append(DAY);

        // Append form to the correct location in page
        document.getElementById("dynamic-form")
            .appendChild(form);
        document.getElementById("execute-button").append(s);

        // Add a listener for daylight preference
        document.getElementById("day-check").addEventListener(
            "change", function() {day_input(this.value);}, false);
    }

    /**
     * Northern lights priority form
     */
    function light_form() {
        // Create a form dynamically
        let form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "result");
        form.setAttribute("id", "ak-form");

        // Create a selection element for daylight hours
        let DAY = document.createElement("select");
        DAY.setAttribute("name", "day-check");
        DAY.setAttribute("id", "day-check");
        DAY.setAttribute("form", "ak-form");
        DAY.add(new Option("No", "false", true));
        DAY.add(new Option("Yes", "true", false));

        // Create a submit button
        let s = document.createElement("input");
        s.setAttribute("type", "submit");
        s.setAttribute("value", "Submit");
        s.setAttribute("name", "light_submit");
        s.setAttribute("id", "button");
        s.setAttribute("form", "ak-form");

        // Append the temp input to the form
        let LIGHTTEXT = document.createTextNode("The best time to see the Northern Lights is between August and April.")
        form.appendChild(LIGHTTEXT);
        form.innerHTML += "<br><br>";

        // Append the daylight select to the form
        let DAYTEXT = document.createTextNode("Do you have a preference with regards to number of daylight hours?")
        form.appendChild(DAYTEXT);
        form.innerHTML += "<br>";
        form.append(DAY);

        // Append the form to correct page location
        document.getElementById("dynamic-form")
            .appendChild(form);
        document.getElementById("execute-button").append(s);

        // Add a listener for daylight preference
        document.getElementById("day-check").addEventListener(
            "change", function() {day_input(this.value);}, false);
    }

    /**
     * Governing switch box to select correct form method.
     * input is pulled from the first dropdown on the html page
     */
    switch (input) {
        case "temp":
            temp_form();
            break;
        case "daylight":
            day_form();
            break;
        case "snowfall":
            snow_form();
            break;
        case "northernlights":
            light_form();
            break;
        default:
            //return nothing
            let form = document.createElement("form");
            document.getElementById("dynamic-form")
                .appendChild(form);
    }
}