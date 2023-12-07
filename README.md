# HeadHunter Data Integration Project

## Overview

The HeadHunter Data Integration project is designed to leverage the HeadHunter (hh.ru) API to gather comprehensive information about job vacancies. The primary objectives include translating salary data into Russian Rubles and storing the enriched dataset in a PostgreSQL database managed through PGAdmin 4.

## Main Features

1. **Data Retrieval from HeadHunter API:**
   - Utilizes the HeadHunter public API to fetch detailed data about job vacancies, including company information, job titles, and salaries.

2. **Currency Translation to Russian Rubles:**
   - Implements a robust currency conversion mechanism to translate salaries into Russian Rubles, ensuring uniformity and ease of analysis.

3. **Database Integration with PostgreSQL:**
   - Designs a well-structured PostgreSQL database using PGAdmin 4 to store the gathered data efficiently.

4. **DBManager Class for Data Management:**
   - Implements the `DBManager` class, streamlining interactions with the PostgreSQL database. This class provides a clean and organized way to manage and manipulate the data.

## Project Execution

Follow these steps to run the project:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/your-project.git
   
## Project Components
 - DBManager.py: Contains the DBManager class for efficient data management within the PostgreSQL database.
 - YourScript.py: The main script that orchestrates the project steps.

## Dependencies
 - requests: Powerful library for making HTTP requests to the HeadHunter API.
 - psycopg2: PostgreSQL adapter for Python, facilitating seamless interaction with PostgreSQL databases.

**Happy coding! 🚀**