# Reflect & Grow App
#### Video Demo: <https://youtu.be/zlD2GsM4kpY>
#### Description:

Reflect & Grow is an app that helps users track daily habits and write a personal journal. It's for personal growth and self-awareness, helping users stay on track with habits and think about their day.

#### Key Features:

- Habit Tracking: This feature lets users manage their daily habits. You can add, change, or remove habits and goals. You can also see your last 7 days' habits (3 days on mobile) and mark them as done or not done.
- Daily Journal:  A place for users to write about their day and thoughts. You can write a journal entry using markdown syntax. You can see a short preview of each entry and click to read the whole thing.
- Progress Visualization: This shows a graph of the top 5 habits, a table for tracking how often habits are done, and a calendar to see when you wrote in your journal. The table shows how many times you've done a habit, the rate of completion, and your current streak. The calendar shows when you added entries.
- User-Friendly Features: Includes showing your username near the logout button, changing your password, and a visual guide to create a strong password.
- Easy-to-Use Interface: The app is simple to use, making tracking habits and journaling easy. It works on both mobile and computer.

#### File Structure and Contents:

- app.py: The main app file for Flask, it handles how the app works and controls different parts. It manages user, habit, and journal features, and checks if a user is logged in.
- something-service.py: This manages the logic for habits, journal entries, and user information. It does all the calculations and talks to the database.
- database.py: Contains all the commands for managing data. It does basic operations and makes sure they are for the right user.
- templates/: Holds the HTML files for the app's pages. Some files for adding and updating content are similar and need some more work.

#### Technology & Design Choices:

- Python & Flask: Chosen for how easy they are to manage web pages and requests. I picked them based on what I learned before to get better at using them.
- JavaScript: Used for the front end. It was good to use basic JavaScript again without big libraries.
- SQLite: Used for its simplicity. It's good for handling data like user info, habits, and journal entries. I also use it in other small projects.
- Marked: Lets users make their journal entries look nice, not just plain text. I chose this over a complex text editor for simplicity and safety.
- Chart.js: Easier to use than D3. I used it to make simple bar charts. It has enough features for now, but I can add more if needed.
- FullCalendar: Added for showing dates visually. I had some trouble at first, but the documentation helped fix things.
- Bootstrap: Helps make the app look good and work well on all devices. It's especially helpful for me with CSS and making sure it looks right on phones..

#### Challenges and Solutions:

- User Authentication: Learned from the CS50 course. It was very important, especially if I make the app public.
- Data Visualization: It was hard to learn how to show data in graphs, but I managed with help from guides and others' examples.
- Features: I had many ideas but had to choose the most important ones to make sure everything works well without problems.
- Personal Challenge: I had an injury that made it hard to work. I used the time to read more about features and solutions.

#### Personal Journey and Development Insights:

I experienced a shoulder dislocation, which made it difficult for me to write in my paper journal. This challenge inspired me to find a simpler solution, leading to the creation of this app. Designed for ease of use, it's perfect for both mobile and computer users, accommodating those who may face similar physical challenges.
Initially, I had only planned a set of basic features for the app. However, as development progressed and I began using these features, new ideas emerged, leading to their integration into the app.
Behind the scenes, the development process was marked by a disciplined approach, even though I was working solo. Tools like Git for version control and Trello for task management were essential in maintaining organization and ensuring a structured development process.

#### Conclusion and Future Work:

Working on this project has been a great experience in developing a full-featured web app. In the future, I would like to add more features to the habit tracker, like setting different types of goals, reminders, and more ways to visualize progress. I'm also considering more ambitious enhancements, like integrating voice recognition to interpret user commands. I learned a lot of new things, and the most important lesson that programming is more than just coding:  it demands creativity, discipline, and attention to detail.