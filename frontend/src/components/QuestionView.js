import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';
const GETBASEURL = require('./globals');

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [], // i am using array to fetch Categories in python
      currentCategory: null,
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `${GETBASEURL.BASEURL}/questions?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          // fetch all questions and categories
          // we will assign them anyways whether if we have data or not
          // if we run it on empty database
          // why that ? because we already created functionalty to add categories
          // and implemented add questions to categories as well
          questions: result.questions ? result.questions : [],
          totalQuestions: result.total_questions ? result.total_questions : 0,
          categories: result.categories ? result.categories : [],
          currentCategory: result.current_category
        })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory= (id) => {
    $.ajax({
      url: `${GETBASEURL.BASEURL}/categories/${id}/questions`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `${GETBASEURL.BASEURL}/questions/search`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      xhrFields: {
        withCredentials: false //iam not using credentials in my app CORS
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          // fetch questions array that matched our search or if
          // its not assigned then assign it with empty result
          questions: result.questions ? result.questions : [],
          totalQuestions: result.total_questions ? result.total_questions : 0
         })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `${GETBASEURL.BASEURL}/questions/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }


  render() {
    const qCount = this.state.questions.length;
    // show the page if we have Questions
    if (qCount > 0) {

      return (
        <div className="question-view">
          <div className="categories-list">
            <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
            <ul>
              {this.state.categories.map((cat, ind) => (
                <li key={cat.id} onClick={() => {this.getByCategory(cat.id)}}>
                  <img className="category" src={`${cat.type}.svg`}/>
                  {cat.type}
                </li>
              ))}
            </ul>
            <Search submitSearch={this.submitSearch}/>
          </div>
          <div className="questions-list">
            <h2>Questions</h2>

            {this.state.questions.map((q, ind) => (
              <Question
                key={q.id}
                question={q.question}
                answer={q.answer}
                // get category name from question category id
                category={this.state.categories.filter(cat => { return cat.id === q.category })[0].type}
                difficulty={q.difficulty}
                questionAction={this.questionAction(q.id)}
              />
            ))}
            <div className="pagination-menu">
              {this.createPagination()}
            </div>
          </div>

        </div>
      );

    }

    return(
      <center>
      <b>
      <p>There is no Questions yet 
      <a href="add"> Create one !</a>
      </p>
      </b>
      </center>
    );


  }
}

export default QuestionView;
