<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/MyCallAngel0/bluevoyage">
    <img src="./Logo_blue_voyage.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Blue Voyage</h3>

  <p align="center">
    Travel blog website developed with Django.
    <br />
    <a href="https://github.com/MyCallAngel0/bluevoyage"><strong>Explore the repo »</strong></a>
    <br />
    <br />
    <a href="https://github.com/MyCallAngel0/bluevoyage">View Demo</a>
    ·
    <a href="https://github.com/MyCallAngel0/bluevoyage/issues/new">Report Bug</a>
    ·
    <a href="https://github.com/MyCallAngel0/bluevoyage/issues/new">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <!--
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    -->
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Blue Voyage is a web app designed to help travelers overcome the difficulties of finding trustworthy information and sharing their experiences. By offering a platform that combines the best of travel blogging and social media, Blue Voyage creates a welcoming space where users can connect, inspire one another, and share their journeys.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

**Backend:**
* [![Django][Django.js]][Django-url]
* [<a href="Django_rest-url"> <img src="https://storage.caktusgroup.com/media/blog-images/drf-logo2.png" width="75" height="75" alt="Django logo" /> </a> ](Django_rest-url)  

**Frontend:**
* [![Next.js][Next.js]][Next_js-url]
* [![React][React.io]][React-url]  

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- GETTING STARTED -->
## Getting Started

This guide will help you set up the project locally. Follow these steps to get a local copy of the project up and running.

### Prerequisites

Before you begin, ensure you have the following installed:
```
Python 3.10.12 (or higher)
Node.js
pnpm
TypeScript
Prettier & TailwindCSS
```

### Installation
### **Backend**
1. Clone the repo
```
git clone https://github.com/MyCallAngel0/bluevoyage
```
2. Change you *blueVoyage/settings.py* *DATABASES* attribute with the correct information.
3. Create a .env file in the *bluevoyage/blueVoyage* directory (same as settings.py):
```
SECRET_KEY=your_secret_key
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
EMAIL_HOST_USER=your_email_host_user
EMAIL_HOST_PASSWORD=your_email_host_password
```
4. In the same directory as the requirements.txt file, run:
```
pip install -r requirements.txt
```
5. In the same directory as *manage.py*, run the following commands to build the ORM database
```
python3 manage.py makemigrations
python3 manage.py migrate
```
6. Run the Django backend server from the same directory as *manage.py*: 
```
python3 manage.py runserver
```

### **Docker**
<br>Alternatively, you could run the database and backend on docker. 
1. In the *blueVoyage/settings.py*, change the *DATABASES* host to 'db'.
2. Edit the *docker-compose.yml* with the correct information (ex.POSTGRES_USER)
3. In the same directory as docker-compose.yml, execute
```
docker compose up
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!--

## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/github_username/repo_name/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=github_username/repo_name" alt="contrib.rocks image" />
</a>



## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>




## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/MyCallAngel0/bluevoyage/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: Logo_blue_voyage.png
[Django.js]: https://ucarecdn.com/19205348-9397-400e-89c5-053a6da9adeb/-/resize/75/75
[Django-url]: https://docs.djangoproject.com
[Django_rest.js]: <img src="https://storage.caktusgroup.com/media/blog-images/drf-logo2.png" width="75" height="75" alt="Django logo" />
[Django_rest-url]: https://www.django-rest-framework.org/
[Next.js]: https://miro.medium.com/v2/resize:fit:75/1*_bJ2z2NRfTncHAv5UjUxwA.jpeg
[Next_js-url]: https://nextjs.org/
[React.io]: https://miro.medium.com/v2/resize:fit:75/0*y6IcBe5J1AdALzXw.png
[React-url]: https://create-react-app.dev