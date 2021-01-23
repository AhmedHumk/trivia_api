import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

const GETBASEURL = require('./globals');

class CATFORMVIEW extends Component {
  constructor(props){
    super();
    this.state = {
      catname: ""
    }
  }



  submitCategory = (event) => {
    event.preventDefault();
    $.ajax({
      url: `${GETBASEURL.BASEURL}/categories`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        catname: this.state.catname
      }),
      xhrFields: {
        withCredentials: false // i dont use credentials in my app CORS
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-cat-form").reset();
        document.getElementById("addRes").innerHTML = "Category " + result.Created + " successfully added.";
        return;
      },
      error: (error) => {
        alert('Unable to add Category. Please try your request again')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Trivia Category</h2>
        <h6>make sure that category name is placed as svg image in public folder</h6>
        <p id="addRes"></p>
        <form className="form-view" id="add-cat-form" onSubmit={this.submitCategory}>
          <label>
            Category Name
            <input type="text" name="catname" onChange={this.handleChange}/>
          </label>

          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default CATFORMVIEW;
