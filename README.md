# BUS-Prototype

1. Brief Description of the system and it’s purpose (200 words)  

The system ‘UniSupport’ is a web application used to assist university students struggling with their mental wellbeing. As university wellbeing resources are often difficult to find, the purpose of this system is to ease the stress students experience by creating a convenient and easy-to-use application that enables students to find mental wellbeing resources provided by the university and make connections to other students. Ultimately, the goal of the system is to support students and encourage positivity. 

The system uses three fundamental features to achieve this: student profiles with rewards, event calendar and meeting booking system. These features are summarised in part 4 of the Read Me file.   

The system was implemented using model-view controller (MVC) software architecture. For example, the Hobbies model manages data concerning student hobbies, this data is viewed on the student profile, and the user can control this view by adding or removing hobbies to the model.  

The system allows users to register for a password-protected account using their personal details. Users must also choose a role for their account from ‘admin’, ‘staff’ or ‘student’. These roles determine which functionalities of the website the account can access.  

2. Step- by-step instructions on How to Run 

  - Install Conda packages used in the app into your environment 
  - Edit configurations to module = ‘flask’ and script parameters = ‘run’ 
  - Open the web application
  - Sign into the app using the login (tom@student.com / Mypassword123) to test student features and login (trq@staff.com / Mypassword123) to test staff features  

3. Programming languages, frameworks, or tools used 

  - Python 3.11.11
  - Flask
  - SQLAlchemy
  - Flask-WTF
  - Flask-Login
  - Jinja2 / HTML
  - Bootstrap

4. Summary of implemented functionalities 

Feature 1 – Student profiles with rewards  

After registering or logging in to ‘Uni Support’, student users can manage their profiles on the web application. This includes viewing and editing their profile information. Users can also manage their hobbies and interest lists which are displayed on their profile. Student profiles also use gamification to encourage user engagement with the web application. This is in the form of a point system allowing users to gain 10 points for fresh login daily, 5 points for adding hobbies or interests, and 5 points for booking meetings.  

Feature 2 – Event calendar  

Staff users of ‘Uni Support’ can add events to the system using a dedicated form which is linked on the navigation bar (only viewable to staff accounts). The details of new events include; title, description, start time, end time, mode (online/in-person), location or online link, and category (academics/well-being/other). Student users can view their personal event calendar with all upcoming events. Events in the calendar display dynamically by showing the location or clickable link depending on the mode.  

Feature 3 – Meeting booking system  

Student users can access a meeting booking system through a navigation bar link. These meetings will be held with a staff member registered with ‘Uni Support’. When booking a meeting, the student can pick a date, time and staff member to book a meeting with. If the meeting conflicts with a prior booked meeting, the student will be warned to pick an alternative time. When the meeting is successfully booked, a notification will be sent on the web application to the staff member the meeting is booked with to alert them of the meeting booking. Students can also view their upcoming meetings through a link in the navigation bar.  


5. Contribution table 

| Student name and ID  | Contribution (%) |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |
