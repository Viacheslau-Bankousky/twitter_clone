![Alternate Text](twitter_clone_logo.jpg)
# Twitter Clone API

Our twitter clone project provides a collection of APIs to achieve similar functionality as Twitter.

## Setup and Running Application

Before running the application, first, you need to clone this repository to your local machine using `git clone <repository_url>`. Replace `<repository_url>` with the actual URL of this repository. 

Navigate to the root directory of the project via your command line interface and start the application with Docker using the command: `docker compose up --build`. 

## Endpoints

### POST Methods

- **/api/tweets** : Adds a new tweet.
- **/api/medias** : Adds a new media file to a tweet.
- **/api/tweets/{id}/likes** : Likes a specified tweet.
- **/api/users/{id}/follow** : Follows a specified user.
- **/api/users/new** : Adds a new user.

### DELETE Methods

- **/api/tweets/{id}** : Deletes a specified tweet.
- **/api/tweets/{id}/likes** : Deletes a like from a specified tweet.
- **/api/users/{id}/follow** : Unfollow a specified user.

### GET Methods

- **/api/tweets** : Returns tweets of people whom the current user follows, sorted by the tweet's popularity.
- **/api/users/me** : Returns information about the current user, including who they are following and who their followers are. 
- **/api/users/{id}** : Returns the same information as the previous method but for a specified user.

## Running the Application

To access any of these routes, use the localhost after starting the application. Complete API documentation can be accessed via the `/docs` endpoint. 

Additionally, you can also configure Nginx to map a domain name to your server. This provides an alternative way to access the application, other than using localhost.

**Important**: Before using this application, please add at least one user to the database via `/api/users/new` with API-key header as "test". This is essential for the proper integration of frontend and backend services, and facilitates retrieval of necessary user data at application startup. 

Subsequently, users can be added via the graphical interface using any API-key header. Authentication is processed through this mechanism. Happy tweeting!