import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# a constant for paginatePages function 
REQUEST_PER_PAGE = 10

# Constants for Error Handlers
BAD_RQUEST_ERR = 400
NOT_FOUND_ERR = 404
NOT_ALLOWED_ERR = 405
NOT_PROCESSED_ERR = 422
SERVER_ERR = 500
SERVER_UNAVAILABLE = 503


#######################################################
# Pagenation Function Based on Lesson 3
# {We are going to pagenate based on our Request}
# pagenateTarget will work as our refrence
# pagenateTarget = Q Then paginate question
# pagenateTarget = C then paginate categories
#######################################################
def paginatePages(request, Querydata, pagenateTarget):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * REQUEST_PER_PAGE
  end = start + REQUEST_PER_PAGE

  if pagenateTarget == "Q":
    questions = [question.format() for question in Querydata]
    CurrentRequest = questions[start:end]
  else:
    categories = [category.format() for category in Querydata]
    CurrentRequest = categories[start:end]

  return CurrentRequest

# Create our app
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  #Set the app Cors Allow '*' for origins. Based On Lesson 3 Flask CORS
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  #######################################################
  # handle GET requests for all available categories count.
  #######################################################
  @app.route('/api/categories')
  def collectCats():
    try:
      # lets get the categories from our database
      GetCats = Category.query.order_by(Category.id).all()

      # get total categories numbers
      catsnum = len(GetCats)

      # if we have nothing abort with Error 404
      if catsnum == 0:
        abort(NOT_FOUND_ERR)

      # we may need to  paginate our categories as well so we can
      # get 10 records per shelf
      # paginatedCats = paginatePages(request, GetCats, "C")
      #------------------------------------------------------
      # but we wont do it now maybe useful in future use
      # we will just send our whole Categories
      collectedCatarray = []
      collectedCatarray = [category.format() for category in GetCats]
        
      # return jsonify response
      return jsonify({
        "categories":collectedCatarray,
        "total_categories":catsnum,
        "success": True
        })
    except Exception as E:
      print(E)
      print("Exception in collectCats")
      abort(BAD_RQUEST_ERR)
  #end

  ####################################################################
  # Handle Post To Create New Category
  ####################################################################
  @app.route('/api/categories', methods=['POST'])
  def CreateNewCat():
    # lets Try to add new Category to our database
    try:
      Cdata = request.get_json()
      #lets get our cat data or set none if its not exist
      catname = Cdata.get("catname", None)

      cats = Category(type=catname)
      cats.insert()
      return jsonify({
        "Created":catname,
        "success": True
        })
    except Exception as E:
      print(E)
      print("Exception in CreateNewCat")
      abort(NOT_PROCESSED_ERR)
  #end

  #####################################################################
  # handle GET request for all available Quetions Count
  #####################################################################
  @app.route('/api/questions')
  def CollectQuestions():
    # lets get all Questions
    GetQuestions = Question.query.order_by(Question.id).all()
    Qnum = len(GetQuestions)
    # if we have nothing abort with Error 404
    if Qnum == 0:
      abort(NOT_FOUND_ERR)

    # get the paginated Records from our paginatepages Function for Questions
    paginatedQuestions = paginatePages(request, GetQuestions, "Q")
    # lets get our all available categories to send them as well
    GetCats = Category.query.all()
    Getcategories = []
    # lets loop through GetCats to append our Getcategories array
    # we dont care about pagination now we will just send all available categories
    # so in client side a user can see available categories in response
    for catitem in GetCats:
      Getcategories.append(catitem.format())
    # end loop
    
    print(Getcategories)
    # return jsonify Response
    return jsonify({
      "questions": paginatedQuestions,
      "total_questions": Qnum,
      "categories": Getcategories,
      "success": True
      })
  #end

  ##############################################################################
  # Handle Delete Question
  ##############################################################################
  @app.route('/api/questions/<int:questionid>', methods=['DELETE'])
  def deleteQuestion(questionid):
    try:
      Error_Delete = False
      # lets try to get our Question this will return None if there
      # if there is no question found with that questionid value
      Getquestion = Question.query.filter(Question.id == questionid).one_or_none()

      # if we did not find our question Set Error_Delete To True
      if not Getquestion:
        Error_Delete = True

      # if Error_Delete is true abort with 404 Error 
      if Error_Delete:
        abort(NOT_FOUND_ERR)
        
      # lets try to delete
      Getquestion.delete()
      # Return success Response
      return jsonify({
        "deleted": questionid,
        "success": True
        })
    except Exception as E:
      print(E)
      abort(NOT_PROCESSED_ERR)
      
  #end
      
  ######################################################################
  # Handle Post New Question
  ######################################################################
  @app.route('/api/questions', methods=['POST'])
  def CreateNewQuestion():
    # lets try to insert our question to our database
    try:
      Qdata = request.get_json()
      # lets get our question data or set none if its not exist
      # as in lesson 3 said.
      question = Qdata.get("question", None)
      answer = Qdata.get("answer", None)
      category = Qdata.get("category", None)
      difficulty = Qdata.get("difficulty", None)
      print(category)

      questions = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      questions.insert()
      return jsonify({
        "success": True,
        "Created": question
        })
    except Exception as E:
      print(E)
      print("Exception in CreateNewQuestion")
      abort(NOT_PROCESSED_ERR)
  #end

  #####################################################################
  # Handle Search Term
  #####################################################################
  @app.route('/api/questions/search', methods=['POST'])
  def searchquestions():
    # lets get our search data
    searchData = request.get_json()
    searchTerm = searchData.get('searchTerm', None)
    # set our count
    questionsFound = 0
    # lets try to start our search
    try:
      searchRes = Question.query.filter(Question.question.ilike('%'+ searchTerm +'%')).order_by(Question.id).all()
      # Count questions that matched the search
      if searchRes:
        questionsFound = len(searchRes)

      # if we dont have any result then abort with 404 error
      if questionsFound ==0:
        abort(NOT_FOUND_ERR)

      print(searchTerm)

      # paginate our result so we make sure we take 10 record per shelf
      paginatedQuestions = paginatePages(request, searchRes, "Q")

      return jsonify({
        "questions":paginatedQuestions,
        "total_questions":questionsFound,
        "success": True
        })
    except Exception as E:
      print(E)
      print("Exception in searchquestions")
      abort(NOT_PROCESSED_ERR)
  #end

  ###############################################################
  # Handle Get Questions From category
  ###############################################################
  @app.route('/api/categories/<int:catid>/questions')
  def GetQuestionsFromCategories(catid):
    #lets Try To get All categories
    Getcategory = Category.query.get(catid)
    # if no categories Found abort with 404 Error
    if not Getcategory:
      abort(NOT_FOUND_ERR)
      
    # lets try to fetch all questions from that Getcategory
    try:
      QuestionsFromCategory = Question.query.filter_by(category=Getcategory.id).order_by(Question.id).all()
      paginatedQuestions = paginatePages(request, QuestionsFromCategory, "Q")
      catQuestionNum = len(QuestionsFromCategory)
      return jsonify({
        "questions":paginatedQuestions,
        "total_questions": str(catQuestionNum),
        "current_category": str(catid),
        "categories":Getcategory.format(),
        "success": True
        })
    except Exception as E:
      print(E)
      print("Exception in GetQuestionsFromCategories")
      abort(NOT_PROCESSED_ERR)
  #end

  ###################################################################
  # Play random Qizzes
  ###################################################################
  @app.route('/api/quizzes', methods=['POST'])
  def playquizzes():
    try:
      #Get our quiz Data
      rdata = request.get_json()
      # set our variables from rdata to use them later
      # the data we excpet comming from QuizView.js
      quizcategory = rdata.get("quiz_category", None)
      previousQ = rdata.get("previous_questions", None)

      # set category id from quizcategory or return zero
      quizcategory_id = quizcategory.get("id", 0)
      print("quizid " + str(quizcategory_id))

      # get category
      GetCategory = Category.query.get(quizcategory_id)

      # if we did not find a category then lets fetch
      # our all categories
      if not GetCategory:
        print("Category not Found " + str(quizcategory_id))
        Getallcats = Category.query.all()
        # now after we have collected our all categories
        # lets set our GetCategory with a randomize choice
        GetCategory = random.choice(Getallcats)
        
      # now we are at least know that we have category
      # in our GetCategory
      # now lets try to get questions from our GetCategory
      # that was not in our previousQ array 
      GetQuizzQuestions = Question.query.filter(Question.id.notin_(previousQ)).filter_by(category=GetCategory.id).all()
      print(GetQuizzQuestions)
      # now we should excpect that we have some questions that is not equal to
      # our previous questions
      # it is good to paginate our records as well
      paginatedQuestions = paginatePages(request, GetQuizzQuestions, "Q")
      # now we excpect to have some paginated Questions
      # but lets check how many we have
      QuestionsCount = len(paginatedQuestions)
      print(str(QuestionsCount))
      QFound = True
      # if our count is zero then we should abort 
      # probably we dont have records of questions that matched
      # in the category provided in the GetQuizzQuestions query
      if QuestionsCount ==0:
        QFound = False

      # now we can randomize our output to send it to the client
      if not QFound:
        abort(NOT_FOUND_ERR)

      randomizeQuestion = random.choice(paginatedQuestions)
      
      return jsonify({
        "question": randomizeQuestion,
        "previousQuestions": previousQ,
        "success": True,
        })
        
    except Exception as E:
      print(E)
      abort(NOT_PROCESSED_ERR)
  #end

  #####################################
  # handle our Errors
  #####################################
  @app.errorhandler(BAD_RQUEST_ERR)
  def bandrequest(error):
    return jsonify({
      "error": BAD_RQUEST_ERR,
      "message": "Bad Request",
      "success": False
      })

  @app.errorhandler(NOT_FOUND_ERR)
  def notfound(error):
    return jsonify({
      "error": NOT_FOUND_ERR,
      "message": "Not Found",
      "success": False
      })

  @app.errorhandler(NOT_ALLOWED_ERR)
  def notallowed(error):
    return jsonify({
      "error": NOT_ALLOWED_ERR,
      "message": "Not Allowed",
      "success": False
      })

  @app.errorhandler(NOT_PROCESSED_ERR)
  def notprocessed(error):
    return jsonify({
      "error": NOT_PROCESSED_ERR,
      "message": "Not Processed",
      "success": False
      })

  @app.errorhandler(SERVER_ERR)
  def servererror(error):
    return jsonify({
      "error": SERVER_ERR,
      "message": "Server Error",
      "success": False
      })
  @app.errorhandler(SERVER_UNAVAILABLE)
  def servererror(error):
    return jsonify({
      "error": SERVER_UNAVAILABLE,
      "message": "Server Unavailable",
      "success": False
      })
  
  return app

#############################################
# Start our app
#############################################

if __name__ == '__main__':
  app = create_app()
  app.run(host="localhost", port=4000, debug=False)
    
