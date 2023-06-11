<br/>
<p align="center">
  <a href="https://github.com/tirthyakamaldasgupta/pan-card-utility">
    <img src="https://raw.githubusercontent.com/tirthyakamaldasgupta/pan-card-utility/main/static/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">PAN Card utility</h3>

  <p align="center">
    Effortlessly extract and store PAN Card metadata
    <br/>
    <br/>
    <a href="https://github.com/tirthyakamaldasgupta/pan-card-utility"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/tirthyakamaldasgupta/pan-card-utility">View Demo</a>
    .
    <a href="https://github.com/tirthyakamaldasgupta/pan-card-utility/issues">Report Bug</a>
    .
    <a href="https://github.com/tirthyakamaldasgupta/pan-card-utility/issues">Request Feature</a>
  </p>
</p>

![Downloads](https://img.shields.io/github/downloads/tirthyakamaldasgupta/pan-card-utility/total) ![Contributors](https://img.shields.io/github/contributors/tirthyakamaldasgupta/pan-card-utility?color=dark-green) ![Forks](https://img.shields.io/github/forks/tirthyakamaldasgupta/pan-card-utility?style=social) ![Stargazers](https://img.shields.io/github/stars/tirthyakamaldasgupta/pan-card-utility?style=social) ![Issues](https://img.shields.io/github/issues/tirthyakamaldasgupta/pan-card-utility) ![License](https://img.shields.io/github/license/tirthyakamaldasgupta/pan-card-utility) 

## Table Of Contents

* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## About The Project

This project showcases a Python-based application that streamlines the process of handling PAN Card images and their associated metadata. When the application is executed, it diligently monitors a designated directory, actively searching for any new PAN Card images that may have been added. Upon detecting image(s), it seamlessly converts them to base64 representation, optimizing its compatibility for subsequent processing.

The application harnesses the immense capabilities of IDfy's PAN OCR API, a cutting-edge solution that leverages advanced optical character recognition technology specifically tailored for PAN Cards. By integrating this API into the workflow, the application retrieves comprehensive and accurate metadata from the PAN Card images, extracting key details such as name, date of birth, PAN number, and more.

With the extracted metadata in hand, the application proceeds to store this valuable information in a secure and efficient database. This enables streamlined access, retrieval, and management of PAN Card data, promoting enhanced organizational efficiency and minimizing manual data entry errors. Additionally, it archives the processed images into a separate designated folder.

## Built With

- Python: The application is developed using the Python programming language, leveraging its versatility and extensive libraries to ensure efficient and reliable functionality.
- PlanetScale: The metadata extracted from the PAN Card images is stored in a secure and scalable manner using the PlanetScale managed serverless MySQL platform. This robust database solution ensures data integrity and provides seamless access to stored information.
- Docker: The entire application is packaged and deployed using Docker, allowing for easy distribution and consistent execution across different environments. Docker ensures portability and simplifies the deployment process, enhancing the application's reliability and maintainability.

This well-organized combination of Python, PlanetScale, and Docker forms the backbone of the project, enabling a seamless and efficient workflow for processing PAN Card images, extracting metadata, and storing it in a reliable database system.

## Getting Started

Get the application up and running on your system.

### Prerequisites

1. Subscribe to the free version of the API which IDfy provides in partnership with RapidAPI - [India - Pan card OCR](https://rapidapi.com/idfy-idfy-default/api/india-pan-card-ocr/pricing).

2. Obtain the following details from the endpoint page:
   - The value for the **X-RapidAPI-Key** key
   - The value for the **X-RapidAPI-Host** key
   - The value for the **url** key of the API
   - The value for the **task_id** key of the API
   - The value for the **group_id** key of the API

3. Create a database named **pan_card_utility** in PlanetScale by referring to the documentation [here](https://planetscale.com/docs/onboarding/create-a-database). 
   Retrieve the following details required for the connection string by referring to the documentation [here](https://planetscale.com/docs/concepts/connection-strings):
   - **database**
   - **username**
   - **host**
   - **password**

4. Create a table named **pan_card_details** in PlanetScale by following the instructions provided in the documentation [here](https://planetscale.com/docs/onboarding/create-a-database). Here is the syntax to create the table:

   ```sql
   CREATE TABLE `pan_card_details` (
       `id` int NOT NULL AUTO_INCREMENT,
       `age` int NOT NULL,
       `date_of_birth` date NOT NULL,
       `date_of_issue` date,
       `fathers_name` varchar(255) NOT NULL,
       `id_number` varchar(10) NOT NULL,
       `is_scanned` tinyint(1) NOT NULL,
       `minor` tinyint(1) NOT NULL,
       `name_on_card` varchar(255) NOT NULL,
       `pan_type` varchar(255) NOT NULL,
       `verified` tinyint(1) NOT NULL,
       PRIMARY KEY (`id`)
   ) ENGINE InnoDB,
   CHARSET utf8mb4,
   COLLATE utf8mb4_0900_ai_ci;
   ```

5. Install Python 3.9 locally if you plan to use this application on your local machine.

6. Install Docker if you intend to utilize this application in the form of a Docker container.

### Installation

#### Building locally

1. Clone the repository- [https://github.com/tirthyakamaldasgupta/pan-card-utility](https://github.com/tirthyakamaldasgupta/pan-card-utility).

2. Create and activate a virtual environment by following the instructions in the documentation [here](https://dev.to/pizofreude/how-to-create-virtual-environments-in-python-for-windows-mac-and-linux-5ceo).

3. Install the required packages specified in the **requirements.txt** file:
   ```shell
   pip install -r requirements.txt
   ```

#### Pulling pre-built image from DockerHub

1. Pull the image from DockerHub:
   ```shell
   docker pull tirthyakamaldasgupta/pan-card-utility
   ```

#### Build Docker image from source:

1. Clone the repository: [https://github.com/tirthyakamaldasgupta/pan-card-utility](https://github.com/tirthyakamaldasgupta/pan-card-utility).

2. Build the Docker image by running the following command inside the root directory of the project:
   ```shell
   docker build --no-cache -t <your preferred image name> .
   ```

   **Example:**
   ```shell
   docker build --no-cache -t my-pan-card-utility .
   ```

## Usage

#### Running locally

1. Create the following directories at the root of the project directory:
   - **pan-card-new-images**
   - **pan-card-archived-images**

2. Copy the sample image from the **images** folder or place your own images inside the **pan-card-new-images** directory.

3. Create a **.env** file at the root of the project directory and populate it with the specified parameters (refer to [here](#environment-file-variables) for the parameters).

4. Populate the **.env** file with the necessary parameters and their corresponding values.

5. Run the **main.py** script:
   - *For Windows*:
     ```shell
     python main.py
     ```
   - *For Linux/Mac OS*:
     ```shell
     python3 main.py
     ```
#### Running in the form of a container from pre-built Docker image

1. Create a **.env** file anywhere and populate it with the specified parameters (refer to [here](#environment-file-variables) for the parameters).

2. Create the following directories anywhere:
   - **pan-card-new-images**
   - **pan-card-archived-images**

3. Put the PAN card images or download a sample image from [here](https://github.com/tirthyakamaldasgupta/pan-card-utility/blame/99c34cf237d4765c5d30ca60857f21086f99f08e/images/sample-pan-card-image-one.webp) and place it inside the **pan-card-new-images** folder.

4. Create a container and run it each time you want to execute the application by issuing the following command:
   ```shell
   docker run --env-file <**.env** file path> -it -v <**pan-card-new-images** directory path>:/usr/src/app/pan-card-new-images -v <**pan-card-archived-images** directory path>:/usr/src/app/pan-card-archived-images --rm --name pan-card-utility <your preferred container name>
   ```

   **Example**
   ```shell
   docker run --env-file .env -it -v /Users/tirthyakamaldasgupta/Downloads/Projects/Production/POCs/pan-card-utility/pan-card-new-images:/usr/src/app/pan-card-new-images -v /Users/tirthyakamaldasgupta/Downloads/Projects/Production/POCs/pan-card-utility/pan-card-archived-images:/usr/src/app/pan-card-archived-images --rm --name pan-card-utility pan-card-utility
   ```

#### Running in the form of a container from source-built Docker image

1. Follow the steps for creating and running the container [here](#running-in-the-form-of-a-docker-container).

   **Notes:**
   1. Skip step 1 of the section since you are building the image from scratch.
   2. Modify the command mentioned in step 5 before executing it, as follows:
       ```shell
       docker run --env-file <**.env** file path> -it -v <**pan-card-new-images** directory path>:/usr/src/app/pan-card-new-images -v <**pan-card-archived-images** directory path>:/usr/src/app/pan-card-archived-images --rm --name <your image name> <your preferred container name>
       ```

       **Example:**
       ```shell
       docker run --env-file .env -it -v /path/to/pan-card-new-images:/usr/src/app/pan-card-new-images -v /path/to/pan-card-archived-images:/usr/src/app/pan-card-archived-images --rm --name my-pan-card-utility my-pan-card-utility-container
       ```
#### Walkthrough

You can watch the complete walkthrough video [here](https://www.youtube.com/watch?v=u0L3-7YoL_s&t=2s).

In this walkthrough example, I will demonstrate the steps involved in using the pre-built Docker image of the application.

1. Creating the required directories: Inside the **Downloads** folder, I have already set up the **pan-card-new-images** directory with a sample PAN card image, and the **pan-card-archived-images** directory is empty.

   ![Creating the required directories](https://raw.githubusercontent.com/tirthyakamaldasgupta/pan-card-utility/main/examples/walkthrough/images/1.%20Folders%20created.png)

2. Setting up the environment variables: I have stored the required environment variables in a **.env** file located in my home directory.

   ![Setting up the environment variables](https://raw.githubusercontent.com/tirthyakamaldasgupta/pan-card-utility/main/examples/walkthrough/images/2.%20Environment%20variables.png)

3. Database table state: The **pan_card_details** table in the PlanetScale hosted database currently does not contain any rows.

   ![Empty database table](https://raw.githubusercontent.com/tirthyakamaldasgupta/pan-card-utility/main/examples/walkthrough/images/3.%20Current%20empty%20state%20of%20PlanetScale%20database%20table.png)

4. Docker image creation: I have already created the required Docker image on my system.

   ![Docker image created](https://raw.githubusercontent.com/tirthyakamaldasgupta/pan-card-utility/main/examples/walkthrough/images/4.%20Docker%20image.png)

5. Running the container: I will run the container from my Terminal. The container logs will display the extraction of data and the archiving of the image. Validation will be performed in the next steps.

    ![Running the container](https://raw.githubusercontent.com/tirthyakamaldasgupta/pan-card-utility/main/examples/walkthrough/images/5.%20Docker%20container%20running.png)

6. Data insertion: The data extracted from the PAN card image has been successfully inserted into the database table.

   ![Data inserted into the table](https://raw.githubusercontent.com/tirthyakamaldasgupta/pan-card-utility/main/examples/walkthrough/images/7.%20Data%20inserted.png)

7. Image archiving: The PAN card image has been moved from the **pan-card-new-images** directory to the **pan-card-archived-images** directory.

   ![Image archived](https://raw.githubusercontent.com/tirthyakamaldasgupta/pan-card-utility/main/examples/walkthrough/images/6.%20Image%20archived.png)

#### Environment file variables

| Name                                               | Value                                                                           |
|----------------------------------------------------|---------------------------------------------------------------------------------|
| **X_RAPIDAPI_KEY**                                 | Your RapidAPI key.                                                              |
| **X_RAPIDAPI_HOST**                                | Your RapidAPI host.                                                             |
| **PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_URI**      | The URL of the PAN Card OCR extraction API.                                     |
| **PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_TASK_ID**  | The task ID for the PAN Card OCR extraction API.                                |
| **PAN_CARD_OCR_EXTRACTION_SCHEDULER_API_GROUP_ID** | The group ID for the PAN Card OCR extraction API.                               |
| **DB_HOST**                                        | The host address of the database server.                                        |
| **DB_USERNAME**                                    | The username for accessing the database.                                        |
| **DB_PASSWORD**                                    | The password for accessing the database.                                        |
| **DB_NAME**                                        | The name of the database to store the metadata.                                 |

##### Environment variables reference

Refer to the [Prerequisites](#prerequisites) section for instructions on how to obtain the values for the environment variables.



## Roadmap

See the [open issues](https://github.com/tirthyakamaldasgupta/pan-card-utility/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/tirthyakamaldasgupta/pan-card-utility/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/tirthyakamaldasgupta/pan-card-utility/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](https://github.com/tirthyakamaldasgupta/pan-card-utility/blob/main/LICENSE.md) for more information.

## Authors

* **Tirthya Kamal Dasgupta** - *Senior Automation Engineer at BAAR Technologies (Formerly Allied Media Innotech Pvt. Ltd.)* - [Tirthya Kamal Dasgupta](https://github.com/tirthyakamaldasgupta) - *Designed, and implemented the entire solution.*

## Acknowledgements

* [Mehwish](https://www.flaticon.com/free-icon/id-card_4489837)
* [Graphix's Art](https://www.flaticon.com/free-icons/settings)
