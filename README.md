

# Article and Author Management API

## Project Description

This project is a RESTful API designed for managing articles and authors, providing a seamless and efficient way for users to create, update, delete, and search for articles and authors. The API facilitates essential functionalities, allowing users to manage authors, search for articles, and perform advanced queries using Elasticsearch.

## Target Audience

- **Authors**: Individuals who want to create and manage their articles, providing their details and associated information.
- **Readers**: Users interested in browsing and searching for articles based on various criteria such as tags, categories, and authors.
- **Administrators**: Users responsible for managing authors and articles, ensuring a smooth operation of the system.

This API is built using Django and Django Rest Framework, ensuring robust performance and scalability to accommodate growing user needs.

## API Reference

After running the project locally, you can access your APIs through the following links:

- **Swagger UI Documentation**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Redoc Documentation**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Roadmap

- As an **administrator**, you can add or delete authors, manage articles, and have full access to CRUD operations for both articles and authors.
- As a **user**, you can browse and search articles based on various filters like tags, categories, and author names.

### API Endpoints

#### Authors Endpoints

1. **Create Author**
   - **Method**: POST
   - **URL**: `/authors/create/`
   - **Request Body**:
     ```json
     {
       "name": "Author Name",
       "specialization": "Author Specialization",
       "biography": "Biography of the author"
     }
     ```

2. **List Authors**
   - **Method**: GET
   - **URL**: `/authors/list/`
   - **Description**: Retrieves a list of all authors. You can filter by name or specialization using query parameters.

3. **Find Author by Article ID**
   - **Method**: GET
   - **URL**: `/authors/byArticle/<article_id>/`
   - **Description**: Finds the author associated with the given article ID.

4. **Retrieve Author Details**
   - **Method**: GET
   - **URL**: `/authors/<str:pk>/`
   - **Description**: Retrieves detailed information about a specific author by their ID.

5. **Update Author**
   - **Method**: PUT
   - **URL**: `/authors/<str:pk>/`
   - **Description**: Updates the information of a specific author by their ID. Requires the same fields as create.

6. **Delete Author**
   - **Method**: DELETE
   - **URL**: `/authors/<str:pk>/`
   - **Description**: Deletes a specific author by their ID.

7. **Count Articles by Author**
   - **Method**: GET
   - **URL**: `/authors/count/`
   - **Description**: Retrieves the count of articles for each author, returning a summary of authors and their associated article counts.

#### Articles Endpoints

1. **Create Article**
   - **Method**: POST
   - **URL**: `/articles/create/`
   - **Request Body**:
     ```json
     {
       "title": "Article Title",
       "content": "Content of the article",
       "author": {
         "name": "Author Name",
         "email": "author@example.com"
       },
       "tags": ["tag1", "tag2"],
       "categories": ["category1", "category2"]
     }
     ```

2. **List Articles**
   - **Method**: GET
   - **URL**: `/articles/list/`
   - **Description**: Retrieves a list of all articles. You can filter by title, tags, and categories using query parameters.

3. **Search Articles**
   - **Method**: GET
   - **URL**: `/articles/search/?keyword=<keyword>&tags=<tags>&categories=<categories>&author=<author>&start_date=<start_date>&end_date=<end_date>`
   - **Description**: Performs an advanced search on articles based on the specified criteria. Returns a filtered list of articles.

4. **Retrieve Article Details**
   - **Method**: GET
   - **URL**: `/articles/<str:pk>/`
   - **Description**: Retrieves detailed information about a specific article by its ID.

5. **Update Article**
   - **Method**: PUT
   - **URL**: `/articles/<str:pk>/`
   - **Description**: Updates the information of a specific article by its ID. Requires the same fields as create.

6. **Delete Article**
   - **Method**: DELETE
   - **URL**: `/articles/<str:pk>/`
   - **Description**: Deletes a specific article by its ID.

7. **Calculate Common Tags**
   - **Method**: POST
   - **URL**: `/articles/<str:article_id>/calculate-common-tags/`
   - **Request Body**:
     ```json
     {
       "tags": ["tag1", "tag2"]
     }
     ```
   - **Description**: Calculates and updates common tags associated with the specified article ID. It will return the similar articles that share these tags.

## How to Use the API

- **Authentication**: You do not need authentication for creating authors or articles.
- You can view the list of authors and articles without authentication.
- To perform any write operations (like creating or updating), use the appropriate endpoints.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the server**:
   ```bash
   python manage.py runserver
   ```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Special thanks to the developers and maintainers of Django and Elasticsearch for their exceptional tools and support.

---

Feel free to modify any sections or add more details as necessary! If you have any additional URLs or specific functionalities you'd like to include, let me know!
