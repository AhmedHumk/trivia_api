import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

const GETBASEURL = require('./globals');

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: []  // i am using array to fetch categories in python
    }
  }

  componentDidMount(){
    $.ajax({
      url: `${GETBASEURL.BASEURL}/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          // assign it anyways even if we do not have categories
          categories: result.categories ? result.categories : []
        })
        return;
      },

      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }

    })
  }


  submitQuestion = (event) => {
    event.preventDefault();
    var mycatid = document.getElementById("ALLCATS");
    var Catidnum = mycatid.options[mycatid.selectedIndex].value;
    $.ajax({
      url: `${GETBASEURL.BASEURL}/questions`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: Catidnum
      }),
      xhrFields: {
        withCredentials: false // i dont use credentials in my app CORS
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        document.getElementById("addRes").innerHTML = "Question " + result.Created + " successfully added.";
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
    const catcount = this.state.categories.length;
    // if we have categories then show add question form
    if (catcount > 0) {
      return (
        <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <p id="addRes"></p>
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
        <label>
        Question
        <input type="text" name="question" onChange={this.handleChange}/>
        </label>
        <label>
        Answer
        <input type="text" name="answer" onChange={this.handleChange}/>
        </label>
        <label>
        Difficulty
        <select name="difficulty" onChange={this.handleChange}>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
      </label>
      <label>
        Category
      <select id="ALLCATS" name="category" onChange={this.handleChange}>
      {this.state.categories.map((cat, ind) => (
        <option key={cat.id} value={cat.id}>{cat.type}</option>
      ))}
        </select>
      </label>
      <input type="submit" className="button" value="Submit" />
    </form>
  </div>
);
}
// if not the show add new categpries url
return(
  <center>
  <b>
  <p>There is no Categories yet To add questions
  <a href="catadd"> Create one !</a>
  </p>
  </b>
  </center>
);


  }
}

export default FormView;
