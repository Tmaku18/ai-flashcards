(AI Got An Idea)- Group 8
The Study Buddy AI
Software Engineering Project
Names: Carter Tierney, Krish Kalyani, Trinh Bui, Sarah Barkire,
Tanaka Makuvaza
Semester: Spring 2025
Group Number: 8
Coordinator: Carter Tierney
Name of the Guide: Dr. Tushara Sadasivuni

Date: (4/9/2025)
 TABLE OF CONTENTS
INTRODUCTION 3
Software Engineers’ information 3
Planning and Scheduling 4
Teamwork Basics 4
Problem Statement 5
System Requirements 5
1.5.1 Context Diagram 5
1.5.2 Activity Diagram 6
Section 5 Use Case: 7
Database Tables 33
Github 331.1 Software Engineers' information 4
1.2 Planning and Scheduling 4
1.3 Teamwork basics 4
1.4 Problem Statement 4
1.5 System Requirements 4
1.5.1 Context Diagram 4
1.5.2 Activity Diagram 4
2.0 REQUIREMENTS 4
2.1 Use Cases 4
2.2 Requirements 4
2.3 Use Case Diagrams 4
3.0 DATABASE TABLES 4
4.0 CLASS DIAGRAM 5
5.0 BEHAVIORAL MODELING 5
6.0 IMPLEMENTATION 5
7.0 TESTING 6
7.1 Test cases 5
7.2 Testing 6
8.0 ARCHITECTURAL MODELING 6
8.1 Architectural Views 4
8.2 Architectural Model 4
9.0 GITHUB 6
REFERENCES 6

INTRODUCTION
Software Engineers’ information
Carter Tierney- Languages- Python, Java, C, Dart, SQL/Flutter, Experienced with firebase/google connection and learning AWS services as well as MONGODB. New to HTML/CSS/Javascript
Trinh Bui- I have worked with HTML, CSS, and some JavaScript for front-end development. For back-end development, I have experience with Java. My experience with databases is minimal.
Sarah Barkire- Experienced in full-stack web development with strong skills in HTML,CSS, JAVASCRIPT, and React for frontend design.
Krish Kalyani- I have solid experience in web development, mainly working with Java, JavaScript, HTML, and CSS to build interactive websites. I have also worked with MySQL databases, giving me a decent background on backend development and data management.
Tanaka Makuvaza- I have experience with Python, Java, Javascript, HTML, and C, along with some experience with unity.

Planning and Scheduling

Teamwork Basics
We’ll divide tasks based on strengths and availability, with deadlines set as a group. One person will track progress, and if someone can’t meet a deadline, they need to communicate early. Work will be reviewed before submission, and feedback will be given if revisions are needed. To avoid last-minute rushes, we’ll set checkpoints along the way. If someone is not communicate their work and not meeting deadlines then they will be marked as so in
Communication will happen through discord, and meetings will be scheduled based on availability. If someone repeatedly misses meetings or doesn’t contribute, we’ll address it as a team. The facilitator role can and will change at least once/twice(on group discretion), ensuring we stay on track, contribute evenly, meet deadlines, and resolve any issues quickly. The facilitator and group goal is to keep everything organized and make sure everyone pulls their weight.

Problem Statement
Our product is an artificial intelligence (AI) powered flashcard and quiz app that is designed to help students, teachers, professors, etc. effectively obtain, remember, and memorize material/information on any subject of their choice. Our product uses artificial intelligence to create high quality flashcards, optimized study sessions, and record user progress for long term retention, while other traditional flashcard websites need a manual input. The website is perfect for teachers planning lessons, students preparing for a test, or even other users looking for a way to retain information long term.
Traditional flashcard based learning requires manual input, and they are not optimized by artifical intelligence. Our website offers real time progress tracking to gauge efficiency of the AI generated flashcards. Users also have access to their AI flashcard database system. The website incorporates AI using NLP models and is built with a database system and Java for the backend and TypeScript for the frontend. This website provides a quality and scalable solution that improves earning through AI, with a client login for storing study materials and admin login for content management and analytics.This scalable, AI-enhanced solution transforms learning, offering a secure client login for storing study materials and an admin portal for content management and analytics.

System Requirements

1.5.1 Context Diagram

This Next.JS application features a typescript frontend with google authentication. The frontend interacts with the backend using APIs via the Fetch API. The Node.js backend processes requests, handles authentication via Google Auth, and connects to SQL using supabase for data storage and retrieval. The backend can be deployed through Nxt.JS, Actions which automates deployments. The system enables seamless communication between the static website, backend API, and database, ensuring efficient data management and user authentication.

1.5.2 Activity Diagram

Section 5 Use Case:
Use Case:
Use case 1 - User Registration/Authorization
Use case 2 - Account Creation
Use case 3 - Access Homepage
Use case 4 - Create Flashcards/Study Set
Use case 5 - AI Generated Flashcards
Use case 6 - Manual Flashcard
Use case 7 - Set Flashcard Visibility
Use case 8 - Review Flashcards
Use case 9 - Add Private Set
Use case 10 - View Available Sets
Use case 11 - Select Study Set
Use case 12 - Study Mode with Real Time Progress Tracking
Use case 13 - Matching Game
Use case 14 - Quiz Mode with Analytics
Use case 15 - Upload/Edit Set & AI-Generated Flashcard Sharing

Section 5.1
Use Case no.: 1
Use Case Name: User Registration/Authorization
Actors:
User
system
Description:
This system will provide user registration and authentication.
The user must have access to the registration page.
If they are a new user, they must create an account to access the system.
A returning user will log in using an existing account.
The system will verify the provided credentials against stored data and the system will redirect the user to the homepage.
Alternate Path:
If the user forgets their password, they can choose the “Forgot Password” option to reset it.
Exception Path:
If the username or email is already taken during registration, the system prompts the user to enter a different one.
If the user provides incorrect login credentials, the system will display an error message.
Pre-condition:
The system must be online and accessible.
The user must have an internet connection.
Post-condition:
The user is logged in and will be redirected to the homepage.
If the user is not logged in, they will remain at the login page.
Section 5.2
Requirement number: 1
Use Case number: one
Introduction:
The system must allow users to create an account and log in securely using authentication methods.
Inputs:
Username
Email
Password
Requirements Description:
The system should provide a registration page where new users can sign up.
The system must store passwords securely.
Returning users must be able to log in using their credentials.
Users must be notified of incorrect credentials.
A “Forget Password” option must be available to reset login credentials.
Outputs:
Registration creates a new account and allows login.
Successful login redirects the user to the homepage.
Unsuccessful login prompts an error message.
Password reset sends an email with reset instructions.

Section 5.1
Use Case no.: 2
Use Case Name: two
Actors:
User
System
Description:
The system should provide a registration page where new users can sign up.
The system must store passwords safely and securely.
Returning users must be able to log in using their credentials.
Users must be notified of incorrect credentials or existing accounts.
A “Forgot Password” option will be available to reset login credentials.
Alternate Path:
If the user enters an email that is already registered, they are prompted to log in instead.
The user may choose to sign up using a third party authentication method like google or microsoft.
Exception Path:
If the password does not meet security requirements, an error message will display.
If the system fails to connect to the database, the user is informed of a temporary issue.
Pre-condition:
The system must be online and accessible.
The user must have a valid email address.
Post-condition:
If successful, the user account is created and stored in the database.
If unsuccessful, the user remains on the registration page and receives an error message.
Section 5.2
Requirement number: 2
Use Case number: two
Introduction: The system must provide a secure registration process to create new user accounts.
Inputs:
Username
Email
Password
Requirements Description:
The system must provide a registration form with fields for username, email, and password.
Usernames and emails must be checked for uniqueness before account creation.
Passwords must be stored securely.
If an email is already registered, the user will be prompted to log in instead.
A confirmation message will display once the account is successfully created.
Users will receive a verification email when registration is complete.
Outputs:
Successful registration will send a confirmation to the email.
The system stores the new user information in the database.
Unsuccessful registration prompts an error message with details.

Section 5.1
Use Case no.: 3
Use Case Name: Access Homepage
Actors:
User
System
Description:
The user successfully logs in or registers an account.
The system verifies the credentials and redirects the user to the homepage.
The homepage will display options such as creating a flashcard set, viewing existing study sets, and logging out.
The user can navigate to different sections from the homepage.
Alternate Path:
If the user is already logged in and revists the website, they are automatically directed to the homepage without needing to log in again.
If the user is inactive for a long period, the system may log them out.
Exception Path:
If the system fails to load the homepage due to server issues, an error message is displayed.
If the user session expires, they are redirected to the login page.
Pre-condition:
The user must be logged in successfully.
The system must be running and accessible.
Post-condition:
The user is on the homepage and can navigate to other features.
If unsuccessful, the user is redirected to the login page or an error message is displayed.
Section 5.2
Requirement number: 3
Use Case number: three
Introduction: The system must provide a homepage that serves as the main navigation hub after user authentication.
Inputs:
User authentication statue
User session data
Requirements Description:
The system must automatically redirect users to the homepage after a successful login or registration.
The homepage will display options including creating flashcards, viewing study sets, and logging out.
If the user is already logged in, they should be directed to the homepage when accessing the website.
The system must handle session expirations and redirect users to the login page if needed.
Outputs:
A successful homepage with navigation options.
If unsuccessful, the system will show an error message or redirect the user to the login page.

Section 5.1
Use Case no.: 4
Use Case Name: Create Flashcards/Study Set
Actors:
User
System
Description:
The user selects the “Create Flashcards/Study Set” option from the homepage.
The system prompts the user to choose how they want their flashcard generated.
Users have a choice to choose manual or AI generated flashcards.
The user will have access to set the visibility of the flashcard.
The system saves the flashcard set to the database.
The user is redirected to the homepage with a confirmation message.
Alternate Path:
The user may choose to copy and paste text instead of uploading a document or powerpoint.
The user may leave the flashcard set as a draft instead of finalizing it.
Exception Path:
If the document upload fails, an error message is displayed.
If the user does not enter a name or description, the system prevents submission and prompts them to complete the required fields.
Pre-condition:
The user must be logged in.
The system must be able to process AI generated content if AI is selected.
Post-condition:
The new flashcard set is successfully created and stored in the database.
If unsuccessful, the user is prompted to correct errors or retry the process.
Section 5.2
Requirement number: 4
Use Case number: four
Introduction: The system must allow users to create flashcards manually or through AI assistant.
Inputs:
Study set name and description
Flashcard content
Document upload
Visibility settings
Requirements Description:
The system must provide an interface for manually entering flashcards.
The system must allow document uploads for AI flashcards to generate.
AI must extract key points from the uploaded document and generate flashcards.
Users must be able to edit and review flashcards before saving or finalizing.
Users must set the visibility of the study set.
The system must store flashcard sets in the database for future access.
Outputs:
A successfully created flashcard set stored in the system.
If unsuccessful, an error message indicating missing fields, upload failure, or AI processing issues.

Section 5.1
Use Case no.: 5
Use Case Name: AI Generated Flashcards
Actors: Student/User, AI System
Description:

1. User selects the "Generate AI Flashcards" option
2. User inputs study material or topic description
3. AI System analyzes the input
4. AI System generates relevant flashcard pairs (question/answer)
5. User reviews generated flashcards
6. User can edit, delete, or save the generated flashcards
   Alternate Path:

- User can manually edit AI-generated flashcards if they're not satisfied
- User can regenerate flashcards with different parameters
- User can cancel generation process at any time
  Exception Path:
- AI system fails to generate appropriate flashcards
- Input text is too short or unclear
- System timeout during generation
- Network connectivity issues
  Pre-condition:
- User must be logged in
- AI system must be operational
- User must provide sufficient input material
  Post-condition:
- Set of AI-generated flashcards is created
- Flashcards are saved to user's account
  Section 5.2
  Requirement number: 5
  Use Case number: 5
  Introduction: The system must provide functionality for AI-assisted generation of flashcards based on user input.
  Inputs:
- Study material text
- Topic description
- Subject area
- Desired number of flashcards
- Optional parameters (difficulty level, format preferences)
  Requirements Description:

1. System must integrate with an AI model capable of natural language processing
2. AI must be able to identify key concepts and create appropriate question-answer pairs
3. Generated flashcards must be editable
4. System must maintain accuracy and relevance of generated content
5. Generation process should complete within reasonable time (< 30 seconds)
6. System must handle various subject matters and complexity levels
7. Generated content must be stored securely
   Outputs:

- Set of flashcards containing question-answer pairs
- Confirmation of successful generation
- Option to save or modify generated flashcards

Section 5.1
Use Case no.: 6
Use Case Name: Manual Flashcard
Actors: User
Description:

1. User selects "Create Manual Flashcard"
2. User uploads documents or slides
3. System processes uploaded files
4. User creates flashcards based on uploaded content
5. User saves flashcard set
   Alternate Path:

- User can directly input content without file upload
- User can combine multiple file sources
- User can save drafts and continue later
  Exception Path:
- File upload fails
- Unsupported file format
- File size exceeds limit
- Corrupted file
  Pre-condition:
- User must be logged in
- System must support required file formats
- Sufficient storage space available
  Post-condition:
- New flashcard set created
- Files successfully processed and linked to flashcards
  Section 5.2
  Requirement number: 6
  Use Case number: 6
  Introduction: Users must be able to create flashcards manually and upload supporting documents.
  Inputs:
- Document files (PDF, DOC, DOCX)
- Presentation slides (PPT, PPTX)
- Images
- Manual text entry
  Requirements Description:

1. System must support multiple file formats
2. File upload size limits must be implemented
3. Content extraction from uploaded files
4. Interface for manual flashcard creation
5. Support for rich text formatting
6. File storage and management system
7. Version control for uploaded content
   Outputs:

- Created flashcard set
- Processed and stored files
- Confirmation of successful creation

Section 5.1
Use Case no.: 7
Use Case Name: Set Flashcard Visibility
Actors: User
Description:

1. User selects flashcard set
2. User accesses visibility settings
3. User chooses between public/private
4. System updates visibility status
   Alternate Path:

- User can modify visibility settings later
- User can set default visibility preferences
  Exception Path:
- Permission errors
- System fails to update visibility
- Database update errors
  Pre-condition:
- User must own the flashcard set
- Flashcard set must exist
- User must be logged in
  Post-condition:
- Visibility status updated
- Access permissions adjusted accordingly
  Section 5.2
  Requirement number: 7
  Use Case number: 7
  Introduction: System must provide functionality to control flashcard set visibility.
  Inputs:
- Visibility selection (public/private)
- Flashcard set ID
- User authentication
  Requirements Description:

1. Clear visibility options (public/private)
2. Secure permission management
3. Immediate visibility updates
4. User ownership verification
5. Access control implementation
6. Visibility status indicators
7. Default visibility settings
   Outputs:

- Updated visibility status
- Confirmation message
- Updated access permissions

Section 5.1
Use Case no.: 8
Use Case Name: Review Flashcards
Actors: User
Description:

1. User selects flashcard set to review
2. System verifies access permissions
3. User reviews flashcards
4. System tracks progress
5. User completes review session
   Alternate Path:

- Random order review
- Spaced repetition review
- Focus on difficult cards
  Exception Path:
- Access denied for private sets
- System unavailable
- Progress tracking fails
  Pre-condition:
- User must have access to flashcard set
- Flashcard set must contain cards
- User must be logged in
  Post-condition:
- Review session completed
- Progress recorded
- Review statistics updated

Section 5.2
Requirement number: 8
Use Case number: 8
Introduction: System must enforce privacy controls for flashcard sets and manage access permissions.
Inputs:

- User credentials
- Flashcard set ID
- Access request

Requirements Description:

1. Strict access control for private sets
2. Creator-only access enforcement
3. Secure authentication system
4. Privacy status verification
5. Access request handling
6. Error messaging for unauthorized access
7. Access logging and monitoring
   Outputs:

- Access granted/denied response
- Error messages for unauthorized access
- Access audit logs

Section 5.1
Use Case No.: 9
Use Case Name: Add Private Set
Actors:
User
System
Description:
The user selects "Create Flashcard Set" from the homepage.
The system prompts the user to enter a name and description for the set.
The user manually enters flashcards or generates them using AI.
The system prompts the user to select a visibility setting.
The user selects "Private."
The system saves the flashcard set with restricted access.
Alternate Path:
The user may later edit the set and change its visibility to "Public."
Exception Path:
If no name is provided, the system prompts the user to enter one.
If no flashcards are entered, the system warns the user.
If an error occurs while saving, the system displays an error message.
Pre-condition:
The user must be logged in.
Post-condition:
A private flashcard set is successfully created and stored in the database.
Section 5.2
Requirement Number: 9Use Case Number: Nine
Introduction:The system must allow users to create flashcard sets that are private.
Inputs:
Flashcard set name, description, and entries
User selection of "Private" visibility
Requirement Description:
Users must be able to create flashcard sets.
Users must be able to set visibility to "Private."
The system must ensure that private sets are only accessible to the creator.
The system must store the private set securely in the database.
Outputs:
A successfully created private flashcard set.
If unsuccessful, an error message is displayed.

Section 5.1
Use Case No.: 10
Use Case Name: View Available Sets
Actors:
User
System
Description:
The user selects "View Flashcard Sets" from the homepage.
The system retrieves and displays public flashcard sets and the user's private sets.
The user browses available sets.
The user may search for a specific set using keywords.
The user selects a set to view details.
Alternate Path:
The user filters results based on subject or category.
Exception Path:
If no sets are available, the system displays a message.
If the system encounters an error retrieving sets, an error message is displayed.
Pre-condition:
The user must be logged in.
Post-condition:
The user successfully views available flashcard sets.

Section 5.2
Requirement Number: 10Use Case Number: Ten
Introduction: The system must allow users to view available flashcard sets, including public and private ones.
Inputs:
User request to view available flashcards
Optional search query or filter selection
Requirement Description:
The system must display public flashcard sets and the user’s private sets.
The system must allow keyword searches and filtering options.
Users must be able to select a set for more details.
Outputs:
A list of available flashcard sets.
If no sets are found, a message indicating no available sets.

Section 5.1
Use Case No.: 11
Use Case Name: Select Study Set
Actors:
User
System
Description:
The user navigates to "View Flashcard Sets."
The system displays available sets.
The user selects a specific set to study.
The system loads the selected flashcard set.
The system provides options for study modes.
Alternate Path:
The user may switch to a different flashcard set.
Exception Path:
If the selected set does not load, an error message is displayed.
Pre-condition:
The user must be logged in.
Post-condition:
The selected flashcard set is loaded for study.

Section 5.2
Requirement Number: 11Use Case Number: Eleven
Introduction: The system must allow users to select a study set from available flashcards.
Inputs:
User selection of a flashcard set
Requirement Description:
The system must display available flashcard sets.
Users must be able to select a specific set to study.
The system must load the selected set properly.
Outputs:
The flashcard set is successfully loaded for study.

Section 5.1
Use Case Name: Study Mode with Real-Time Progress Tracking
Actors:
User
System
Description:
The user selects a flashcard set to study.
The system presents the first flashcard.
The user flips the card to see the answer.
The user navigates through the flashcards.
The user may choose to shuffle cards or restart the study session.
The user may choose to shuffle cards, restart the session, or enable AI-suggested study paths
Alternate Path:
The user may exit study mode at any time.
The user may enable spaced repetition to prioritize difficult cards.
Exception Path:
If the flashcard set fails to load, an error message is displayed.
Pre-condition:
The user must be logged in.
A flashcard set must be selected.
Post-condition:
The user successfully reviews flashcards in study mode.
Section 5.2
Requirement Number: 12Use Case Number: Twelve
Introduction:The system must allow users to engage with flashcards in study mode.
Inputs:
User selection of study mode
User interactions (flipping, navigating, shuffling)
System tracking correct and incorrect responses
Requirement Description:
The system must display flashcards in study mode.
Users must be able to flip and navigate through flashcards.
The system must provide options for shuffling and restarting, and enabling AI-assisted study paths.
The system must track progress and recommend focus areas based on user performance.
Outputs:
The user successfully studies a flashcard set with tracked progress and performance insights.

Section 5.1
Use Case no.: 13Use Case Name: Matching GameActors:
User
System
Description: The student selects a flashcard set to play as a matching game. The system displays cards face down in a grid. The student clicks on two cards to reveal them, trying to find matching pairs. If the cards match, they remain face up. If not, they flip back face down. The student continues until all pairs are matched. The system tracks time and number of attempts.Alternate Path: Students may choose different difficulty levels which affect the number of cards displayed. Students may also enable hints that temporarily reveal unmatched cards after a set number of failed attempts.Exception Path: If the system encounters an error loading the flashcard set, it displays an error message and returns to the flashcard set selection screen.Pre-condition: Students must be logged in and have at least one flashcard set available.Post-condition: System records completion time and score. Students receive performance feedback and may choose to replay or select a different activity.
Section 5.2
Requirement number: 13Use Case number: 13Introduction: The system must provide a consistent way for users to return to the homepage at any time during any activity to enhance navigation and user experience. Inputs: User click/tap on home button or iconRequirements Description: A clearly visible home button or icon must be present in the navigation bar on all pages within the application. This element must be positioned consistently, preferably in the top left or right corner. When clicked, the system must immediately terminate the current activity (saving progress where appropriate) and return the user to the homepage. For activities where data loss might occur (such as creating/editing flashcards), the system must prompt for confirmation before navigating away.Outputs: User is returned to the homepage with appropriate saving of in-progress work when applicable.

Section 5.1
Use Case no.: 14Use Case Name: Quiz Mode with AnalyticsActors:
User
System
SystemDescription: The student selects a flashcard set to study in quiz mode. The system presents questions based on the flashcards one by one. For each question, the student inputs an answer. The system evaluates the answer, provides feedback on correctness, and reveals the correct answer if needed. The student proceeds through all cards in the set, with the system tracking performance.Alternate Path: Students may choose to skip difficult questions and return to them later. Students may also select quiz format (multiple choice, short answer, true/false) before starting.Exception Path: If a student's session times out during the quiz, the system saves progress and prompts for re-login. If there are technical issues, the system attempts to auto-save progress before displaying an error message.Pre-condition: Students must be logged in and have at least one flashcard set available.Post-condition: System records quiz results with accuracy percentages. Students receive detailed performance analysis showing strengths and areas for improvement.
Section 5.2
Requirement number: 14Use Case number: 14Introduction: The system should automatically log out inactive users after a specified period of inactivity to enhance security.Inputs: System detection of user inactivity beyond the threshold time periodRequirements Description: The system must track user activity through mouse movements, keyboard inputs, and screen interactions. If no activity is detected for 30 minutes (configurable by administrators), the system must display a warning notification 5 minutes before automatic logout. If the user does not respond to this warning, the system must securely end the user's session, saving any in-progress work to prevent data loss. For activities like quizzes or matching games, the system must save the current state to allow resumption upon re-login. The logout process must clear any sensitive data from the browser memory.Outputs: User is logged out with appropriate saving of in-progress work, and a message is displayed indicating the session has expired due to inactivity.

Section 5.1
Use Case no.: 15Use Case Name: Upload/Edit Set & AI-Generated SharingActors:
User
System
Description: The student accesses the flashcard management section and selects to create a new set or edit an existing one. For a new set, the student enters a title, description, and category. The student then adds flashcards by entering front text (question) and back text (answer) for each card. For editing, the student selects an existing set and modifies, adds, or removes cards. The system saves changes to the database.Alternate Path: Students may choose to upload flashcards in bulk using a CSV or spreadsheet file. Students may also import flashcard sets from other users if they are marked as shareable.Exception Path: If the upload format is invalid, the system provides specific error messages about formatting issues. If the database connection fails during saving, the system stores changes locally and attempts to sync when connection is restored.Pre-condition: Students must be logged in with permissions to create or edit flashcard sets.Post-condition: New or updated flashcard set is stored in the database and immediately available for study activities.
Section 5.2
Requirement number: 15Use Case number: 15Introduction: The system requires an efficient database system to store and retrieve flashcard sets quickly to ensure optimal performance for all flashcard-related activities.Inputs: Flashcard data (questions, answers, metadata), user account information, study history and statisticsRequirements Description: The database system must support CRUD operations (Create, Read, Update, Delete) for flashcard sets with response times under 500 ms for typical operations. It must implement efficient indexing strategies for rapid retrieval of flashcard sets by ID, title, category, and user. The system must support concurrent access by multiple users without degradation of performance. Data must be stored in a normalized format to minimize redundancy while maintaining data integrity. The database must implement a caching mechanism for frequently accessed flashcard sets to reduce load times. Backup procedures must run automatically at least once daily, with point-in-time recovery capabilities. The database must scale to support at least 100,000 flashcard sets and 10,000 concurrent users without significant performance degradation.Outputs: Reliable, fast storage and retrieval of flashcard data with appropriate data integrity, backup, and scalability features.

Section 5.3

Database Tables

M

Github

https://github.com/users/Tmaku18/projects/1

l./

Section 1:  
Planning and Scheduling table  
You will make a table like the one you have created for the previous week. The table should focus on the current assignment only!!
The group Coordinator must be changed for every sprint.  
Section 2:  
Our AI-powered flashcard and quiz app is designed to make studying smarter and more effective for students, teachers, and professors. Unlike traditional flashcard platforms that require manual input, our app leverages artificial intelligence to generate high-quality, personalized flashcards, optimize study sessions, and track user progress in real time for long-term retention. With features like AI-generated and user-created flashcard sharing, multiple study modes, and in-depth analytics, our platform is perfect for teachers planning lessons, students preparing for exams, or anyone looking to retain information more efficiently.

Section 3:  
Context Diagram

Section 4:  
Activity Diagram

Section 5:  
System Requirements (Use cases, Requirements and use case diagrams)
Based on the feedback provided and additional topics covered in class, you are to revise, refine, complete, and include your use cases, requirements, and use case diagram with sprint 3. Therefore, you will have an improved version of the system requirements you provided in Sprint 1 and 2.
Use Case Diagrams-

Section 6:  
Database Tables
Based on the feedback provided and additional topics covered in class, you are to revise, refine, complete and include your database tables with sprint 2. Therefore, you will have an improved version of the database tables you provided in Sprint 2.

Section 7:

Class Diagram (object Modeling, or structural modeling):
Create a system class diagram.
Identify objects.  
What are the associations between them?
What is their multiplicity?
What are the attributes of the objects?
What operations are defined on the objects?
The AI powered flashcard and quiz system consist of key objects; User, Student, Teacher,FlashcardSet, Flashcard, Quiz, and AI Engine. students and teachers inherit from user, teachers create Flashcardsets, while students review them and take quizzes.The relationships are 1 To Many (Teachers to Flashcardsets & AI engine to study materials) Many To Many (Students to FlashcardSets and Quizzes).

Section 8:
Behavioral Modeling
Create a UML sequence diagram for two major use cases, with one focusing on the core functionality of the system (do NOT make a sequence diagram for login, logout, or registration modules).
Show appropriate lifelines, activations, and message types. You may also use loop, alternative (alt), and optional fragments if needed. You may use your class diagram to identify the objects’ names and messages (methods) needed to develop your sequence diagram.
A sequence diagram visually represents how objects in a system interact. Keep in mind that the reasons to create a sequence diagram is to:
refine your use case diagram and uses cases (adding missed cases [functionalities]),
refine your class diagram (adding missed methods [messages]),
transition from the conceptual model and start thinking about the implementation, which is the most important.

Section 9:
Implementation
Implement the Database Design (Tables, Backend):
Select the tables associated with four of the major use cases in your system.
Implement the chosen tables using the selected database management system (MySQL, MS-SQL server, Oracle, etc.)
Creating tables using SQL scripts makes it easy to create the necessary tables on another computer to give demo: Development Environment, Test Environment, Production Environment; Deployment

Note: These are some free hosting database management systems:  
Amazon RDS (Relational Database Service) has a free usage tier for 12 months to run a Micro DB instance with 20GB of storage and 10 million I/Os  
Google Cloud Firestore / Datastore is a document-store with a permanent free tier of 1GB storage, 50k reads and 20k writes per day.  
MongoDB Atlas has a free tier with a 3-node replica set and 512MB storage.  
Redis Labs offers a 30MB Redis instance for free.  
Heroku Postgres has a free tier limited to 10k individual rows of data.

Implement the Class Diagram Design (Frontend and Logic): (develop/write code)

Get an overview of the software frameworks or platforms, programming languages, host, etc. Install the necessary Software  
Start creating the main parts (two of the major use cases) for your application (both Frontend, logic (CODE), and GUI).
Create a good structure for your code.
Test that you can communicate with the Database (data go from Frontend [GUI] to Backend [Tables]).
A description of how to compile and run your code
You should not instruct us to compile and execute your code in any IDE.
We recommend writing your own build script or generating one in an IDE (ant, mvn, etc.).
Or, if you chose to host your system in the cloud, make sure to provide the host link, username and password in the section of “description for how to compile your code”.

Section 1 :  
Planning and Scheduling table  
You will make a table like the one you have created for the previous week. The table should focus on the current sprint ONLY!!
Section 2:  
Our AI-powered flashcard and quiz app is designed to make studying smarter and more effective for students, teachers, and professors. Unlike traditional flashcard platforms that require manual input, our app leverages artificial intelligence to generate high-quality, personalized flashcards, optimize study sessions, and track user progress in real time for long-term retention. With features like AI-generated and user-created flashcard sharing, multiple study modes, and in-depth analytics, our platform is perfect for teachers planning lessons, students preparing for exams, or anyone looking to retain information more efficiently.  
Section 3 :

Section 4 :  
Activity Diagram

Section 5 :  
System Requirements (Use cases, Requirements and use case diagrams)

Test Case 6.1

Test Case 7.1

Test case 8.1

Test Case 9.1

Section 6 :  
Database Tables

Section 7 :
Class Diagram (object Modeling, or structural modeling):

The AI powered flashcard and quiz system consist of key objects; User, Student, Teacher,FlashcardSet, Flashcard, Quiz, and AI Engine. students and teachers inherit from user, teachers create Flashcardsets, while students review them and take quizzes.The relationships are 1 To Many (Teachers to Flashcardsets & AI engine to study materials) Many To Many (Students to FlashcardSets and Quizzes).

Section 8 :
Behavioral Modeling

Section 9 :
Implementation
Implement the Database Design (Tables, Backend)  
Implement the Class Diagram Design (Frontend and Logic)
Complete all the other modules of implementation, including the tables and front end associated with your project.

Section 10 :
Testing

Section 10.1
Test Cases

Test case 6.1:
Test Case ID: TC-AUTH-001
Description: Login with valid credentials
Test Inputs: Username UserA, Password: UserA@123
Expected Results: User is authenticated and redirected to homepage
Dependencies: User exists in the database and the authentication service is up and running.
Initialization: Navigate to login page
Test Steps:  
Enter username and Password
Login
Post-conditions: Homepage is shown and a new session is created

Test Case 7.1
Test Case ID: TC-Secure-001
Description: Registration process validates a unique email and stores data
Test inputs: Email (unique@email.com), Username:Student1, Password: UserA@123
Expected results: User data stored and confirmation email is sent
Dependencies: The email system must work
Initialization: New user registration is initiated
Test Steps:
Submit unique user details
check uniqueness of user details

Post conditions: Account is created and confirmation is received

Test Case 8.1
Test Case ID: TC-HOME-001
Description: Redirect to homepage after login
Test Inputs: Valid login credentials
Expected Results: Homepage is displayed with navigation options
Dependencies: The session must be valid
Initialization: Perform login
Test steps:
Login successfully
Observe redirect and content on homepage
Post condition: Navigation links available

Test Case 9.1
Test Case ID: TC-FC-001
Description: Create a flashcard set and save as a draft
Test inputs: Name “Chapter 1”, Content: “Draft Notes”
Expect results: Flashcard set saved in draft mode
Dependencies: Database must be working and online
Initialization: Login and create a flashcard section
Test Steps:
Fill in name and content
Select “save as draft”
Post condition: Draft appears in users saved sets.
Test Case 9.2
Test Case ID: TD-FC-002
Description: Flashcard Visibility
Test inputs: Flashcard “Example” Set to Private
Expected results: Visibility is updated in the system
Dependencies: database gives permission
Initialization: Login and access flashcard set
Test Steps:
Edit flashcard set
Change visibility to private
Save changes made
Post Condition: Flashcard set becomes invisible to the public

Section 11 :
Logical View:

Development View:

Process View:

Physical View:

Architectural Model: The client/server architecture is the best fit for our AI powered flashcard website application because it gives us room to improve and help centralize the process. The JavaScript based client handles the user interface, while the Java backend takes care of AI features, data storage, and user login. This setup lets heavier tasks like flashcard generation and study suggestions run on the server, keeping the client simple. It also supports multiple users, live progress tracking, and safe handling of user data. The design can scale with more users and works well with your database, making it a solid choice for our website application.

Github link: https://github.com/ctsc/Studdybuddy
