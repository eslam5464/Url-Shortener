<a id="readme-top"></a>

[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Github][github-shield]][github-url]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project

* The project aims to build a URL shortener service that takes long URLs and generates shortened versions, making them
  easier to share
* Users can input long URLs, and the system will generate a unique short URL for each input

### Sample image

![Sample image](https://i.imgur.com/0pDChCQ.png)

### Technologies Used

[![Python][Python-shield]][Python-url]
[![FastApi][FastAPI-shield]][FastAPI-url]
[![PostgreSQL][PostgreSQL-shield]][PostgreSQL-url]
[![Redis][Redis-shield]][Redis-url]
[![Jinja][Jinja-shield]][Jinja-url]
[![HTML][HTML-shield]][HTML-url]
[![CSS][CSS-shield]][CSS-url]
[![JavaScript][JavaScript-shield]][JavaScript-url]

* Python: The primary programming language for backend development.
* FastAPI: To create the web service and handle HTTP requests/responses.
* PostgreSQL: As the primary database to store information about original URLs and their corresponding short URLs.
* Redis: To cache frequently accessed URLs for faster retrieval and better performance and use it for the api limiter to
  limit requests.
* Jinja2 Template Engine: To render HTML templates for the frontend interface.
* HTML/CSS/JavaScript: For the frontend interface.

*Note: each of the above icons redirects to its official documentation*

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

* [Docker](https://www.docker.com/get-started/)
* [Python](https://www.python.org/downloads/release/python-3123/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/eslam5464/Url-Shortener.git
   ```

##### Environment variables

```dotenv
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

CORS_ORIGIN=["*"]

ALLOWED_HOSTS=["*"]

POSTGRES_DB=main-database
POSTGRES_DB_SCHEMA=url-shortener
POSTGRES_HOST=localhost
POSTGRES_PASSWORD=change-this
POSTGRES_PORT=5432
POSTGRES_USER=postgres

REDIS_HOST=localhost
REDIS_USER=
REDIS_PASS=change-this
REDIS_PORT=6379
```

#### Local

1. Add the previous environment variables to your project
2. Create a new virtual
   environment [Official python website documentation](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
3. Activate the virtual environment
4. Change the directory to 'backend' folder e.g. `cd backend`, and then run the following commands

```shell
pip install poetry poetry-plugin-export
poetry config virtualenvs.create false
poetry export --without-hashes -f requirements.txt -o requirements.txt
pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

#### Docker

1. Add the environment variables from above in the shell
2. Change directory to project root directory and run dockerfile

```docker
docker-compose -f docker-compose-local.yml -p url-shortener up -d --build backend
```

3. You should see the web interface at http://localhost:8000 or
   the port and host that you specified in the environment variables.*

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->

## License

Distributed under the MIT License. See the file `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->

## Contact

Project Link: [GitHub](https://github.com/eslam5464/Url-Shortener)

Social: [LinkedIn][linkedin-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->

[HTML-shield]: https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=fff&style=flat

[HTML-url]: https://developer.mozilla.org/en-US/docs/Web/HTML

[CSS-shield]: https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=fff&style=flat

[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS

[JavaScript-shield]: https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=000&style=flat

[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript

[Jinja-shield]: https://img.shields.io/badge/Jinja-B41717?logo=jinja&logoColor=fff&style=flat

[Jinja-url]: https://jinja.palletsprojects.com

[Python-shield]: https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=flat

[Python-url]: https://www.python.org

[Redis-shield]: https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=fff&style=flat

[Redis-url]: https://redis.io

[PostgreSQL-shield]: https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=fff&style=flat

[PostgreSQL-url]: https://www.postgresql.org

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge

[license-url]: https://github.com/eslam5464/Url-Shortener/blob/main/LICENSE

[github-shield]: https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=fff&style=for-the-badge

[github-url]: https://github.com/eslam5464/Url-Shortener

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[linkedin-url]: https://linkedin.com/in/eslam5464

[FastAPI-shield]: https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=flat

[FastAPI-url]: https://fastapi.tiangolo.com