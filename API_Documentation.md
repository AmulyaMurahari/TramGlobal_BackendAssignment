# General Information
* Framework: Flask
* Database: SQLite3
* Purpose: To provide services for shortening URLs and managing them.
# Database Setup
* Database Name: url_shortener.db
    * Tables:
        * urls: Stores the long URL, its corresponding short URL, and the user ID who created it.
        * Fields: id, long_url, short_url, user_id.
        * users: Stores user details.
        * Fields: user_id, tier.
# Functions
    * init_db()
    * Initializes the database by creating urls and users tables if they do not exist.
    * get_short_url(size=6, chars=string.ascii_letters + string.digits)
    * Generates a random short URL.
    * Parameters: size (default 6), chars (default alphanumeric).
    * validate_url(url)
    * Validates the given URL using a regular expression.
    * Supports HTTP, HTTPS, FTP, localhost, and IP-based URLs.
# API Endpoints
    * /shorten [POST]
    * Shortens a given URL.
    * Input: JSON with long_url and user_id.
        * Validations:
        * Checks for required parameters.
        * Validates the URL format.
        * Ensures user exists and checks their tier limit.
        * Responses:
        * Success: Returns shortened URL.
        * Failure: Returns error message with appropriate HTTP status code (400 for bad request, 404 for not found).
    * /history/<user_id> [GET]
    * Retrieves the history of URLs shortened by a specific user.
    * Parameter: user_id in the URL path.
    * Response: A list of long_url and short_url pairs.
    * /<short_url> [GET]
    * Redirects to the original (long) URL corresponding to the given short URL.
    * Parameter: short_url in the URL path.
        * Responses:
        * Success: Redirects to the original URL.
        * Failure: Returns error message with a 404 HTTP status code if the URL is not found.
# Running the Application
* The application is set to run in debug mode.
* To start the server, execute the script, and it will listen for incoming HTTP requests.
# Additional Notes
* The API does not include authentication or advanced error handling.
* Rate limiting is implemented based on user tiers, with different usage limits for each tier.
* Database connections are handled within each endpoint function, opening and closing connections as needed.
* The application does not provide an interface for managing users or their tiers. This needs to be managed externally or through additional endpoints.
